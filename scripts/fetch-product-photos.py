#!/usr/bin/env python3
"""
Trae la foto principal en alta resolución de cada producto desde su página oficial.

    python3 scripts/fetch-product-photos.py            # todos los productos con enlace
    python3 scripts/fetch-product-photos.py Montoc     # solo una marca

Usa los mismos enlaces que scripts/fetch-shades.py (SHADE_PAGES) más los de PHOTO_PAGES, y deja cada
foto en assets/images/productos-hd/{id}.webp con su origen en fuentes.json. La foto solo se recorta a un
lienzo cuadrado con el producto centrado y un margen para que el círculo no lo corte, se reduce a 800 px
si es más grande (nunca se amplía) y se guarda en WebP. Sin IA ni retoques.

Después hay que regenerar el catálogo (scripts/extract-catalog.py), que usa estas fotos en vez del
recorte del PDF. Antes de publicar, revisar que cada foto sea el mismo producto y presentación.
"""
import importlib.util, io, json, re, sys
from pathlib import Path
from urllib.parse import urlsplit

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data' / 'products.json'
OUT = ROOT / 'assets' / 'images' / 'productos-hd'
SIZE = 800            # lado máximo de la foto (la ficha la muestra a 320 px; 800 cubre pantallas 2,5x)
MARGIN = 0.12         # aire alrededor del producto para que el círculo no lo corte

_spec = importlib.util.spec_from_file_location('fetch_shades', ROOT / 'scripts' / 'fetch-shades.py')
shades = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(shades)

# Productos sin tonos (o cuyo enlace de tonos no sirve para la foto principal): "Marca|Nombre": url.
PHOTO_PAGES = {}

# Productos cuyos tonos están publicados como productos separados: la foto de un tono no representa
# al producto completo, así que no se reemplaza automáticamente.
SKIP = {
    'Bloomshell|Base líquida 2 en 1 My foundation', 'Bloomshell|Corrector My concealer',
    'Samy|Polvo suelto', 'Samy|Paleta de sombras x9',
    'Raquel|Polvo suelto traslúcido mate minerals con avena y trigo', 'Milagros|Perfume capilar y corporal',
    'Fantiluna|Mantequilla corporal x 220 ml', 'Fantiluna|Exfoliante corporal x 220ml',
    'Fantiluna|Splash corporal x 250 ml', 'Fantiluna|Splash corporal x 105 ml',
    'Fantiluna|Iluminador corporal x 160 ml', 'Fantiluna|Crema corporal',
}


def main_photo(url):
    """URL de la foto principal del producto en la página oficial."""
    parts = urlsplit(url)
    if '/products/' in parts.path:                                  # Shopify
        images = shades.shopify_json(url).get('images', [])
        return images[0]['src'].split('?')[0] if images else None
    if parts.netloc.endswith('samycosmetics.com'):                  # VTEX
        found = json.loads(shades.get(f"{parts.scheme}://{parts.netloc}/api/catalog_system/pub/products/search{parts.path.rstrip('/')}"))
        items = found[0].get('items', []) if found else []
        return (items[0].get('images') or [{}])[0].get('imageUrl') if items else None
    page = shades.get(url).decode('utf-8', 'replace')               # WooCommerce y otras
    m = (re.search(r'data-large_image="([^"]+)"', page)
         or re.search(r'<meta property="og:image" content="([^"]+)"', page))
    return m.group(1) if m else None


def framed(img):
    """Lienzo cuadrado con el producto centrado y un margen, relleno con el color de la esquina."""
    img = img.convert('RGBA')
    side = round(max(img.size) * (1 + 2 * MARGIN))
    corner = img.getpixel((0, 0))
    bg = corner if corner[3] > 0 else (217, 211, 195, 255)   # beige del disco si es transparente
    canvas = Image.new('RGBA', (side, side), bg)
    canvas.paste(img, ((side - img.width) // 2, (side - img.height) // 2), img)
    canvas = canvas.convert('RGB')
    return canvas.resize((SIZE, SIZE), Image.LANCZOS) if side > SIZE else canvas


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    products = {f"{p['brand']}|{p['name']}": p for p in json.loads(DATA.read_text())['products']}
    pages = {k: v for k, v in shades.SHADE_PAGES.items() if isinstance(v, str)} | PHOTO_PAGES
    sources_file = OUT / 'fuentes.json'
    sources = json.loads(sources_file.read_text()) if sources_file.exists() else {}
    OUT.mkdir(parents=True, exist_ok=True)
    for key in sorted(set(pages) | (SKIP & set(shades.SHADE_PAGES))):
        if only and not key.startswith(f'{only}|'):
            continue
        if key in SKIP:
            print(f'-- {key}: cada tono es un producto aparte; foto principal pendiente')
            continue
        product = products.get(key)
        if not product:
            print(f'!! {key}: no está en data/products.json')
            continue
        try:
            src = main_photo(pages[key])
            if not src:
                print(f'!! {key}: la página no tiene foto')
                continue
            src = src if src.startswith('http') else 'https:' + src if src.startswith('//') else src
            original = Image.open(io.BytesIO(shades.get(src)))
        except Exception as exc:
            print(f'!! {key}: {exc}')
            continue
        pic = framed(original)
        pic.save(OUT / f"{product['id']}.webp", 'WEBP', quality=90, method=6)
        sources[product['id']] = src
        print(f"ok {key}: {original.width}×{original.height} -> {pic.width} px")
    sources_file.write_text(json.dumps(dict(sorted(sources.items())), ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
