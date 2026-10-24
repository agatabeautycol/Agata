#!/usr/bin/env python3
"""
Agrega los tonos de cada producto (nombre + foto de referencia) desde su página oficial.

    pip install pillow
    python3 scripts/fetch-shades.py            # todos los productos de SHADE_PAGES
    python3 scripts/fetch-shades.py Montoc     # solo una marca

Funciona con tiendas Shopify: lee /products/<handle>.json, toma la opción de tono/color de cada
variante y su foto. Las fotos solo se recortan a un cuadrado centrado, se reducen y se guardan en
WebP (sin IA ni retoques) en assets/images/tonos/{id}/. Escribe en data/products.json los campos
"shades" y "shadesSource", que scripts/extract-catalog.py conserva al regenerar desde el PDF.

No inventa nada: si la página no tiene tonos (una sola variante), el producto queda igual y se avisa.
"""
import io, json, re, sys, unicodedata, urllib.request
from pathlib import Path
from urllib.parse import urlsplit

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data' / 'products.json'
OUT = ROOT / 'assets' / 'images' / 'tonos'
SWATCH = 240          # px del lado de la foto de cada tono (se muestra a 60 px; 240 cubre pantallas 4x)

# Página oficial de cada producto, por "Marca|Nombre" (como en data/products.json).
# Enlaces entregados por Ágata Beauty.
SHADE_PAGES = {
    'Montoc|Base Glow Filter': 'https://montoccosmetictools.com/products/glow-filter',
    'Montoc|Paleta Light Set': 'https://montoccosmetictools.com/products/paleta-light-set-montoc',
    'Montoc|Rubor líquido radiante Glow Filter': 'https://montoccosmetictools.com/products/rubor-liquido-radiante-glow-filter-con-particulas-de-brillorubor-liquido-radiante-glow-filter-con-particulas-de-brillo',
    'Montoc|Bronzer Drops Light': 'https://montoccosmetictools.com/products/bronzer-drops-light-set-bronceador-liquido-profesional',
    'Montoc|Bronzer luminoso en polvo + brocha Hello beach': 'https://montoccosmetictools.com/products/bronzer-luminoso-en-polvo-polvo-bronceador-para-todos-los-tonos-de-piel',
    'Montoc|Paleta Harmony x6': 'https://montoccosmetictools.com/products/paleta-de-sombras-harmony-eyeshadow-palette',
    'Montoc|Lápiz delineador de labios': 'https://montoccosmetictools.com/products/lapiz-de-labios-montoc',
    'Montoc|Hidratante de Labios Lippie Balm': 'https://montoccosmetictools.com/products/hidratante-de-labios-lippie-balm-natural',
    'Montoc|Kit de brochas de maquillaje Fluffy x 10': 'https://montoccosmetictools.com/products/kit-profesional-de-brochas-flofi-x-10-piezas',
    'Montoc|Brocha mini viajera': 'https://montoccosmetictools.com/products/brochas-minimi',
}

# Nombres de la página oficial ajustados con autorización de Ágata Beauty, por producto.
SHADE_NAME_FIXES = {
    # "Glow Filter" ya está en el nombre del producto (y la tienda escribe "Gow Filter" en 7 de 8).
    'Montoc|Base Glow Filter': {
        '1.0 Light Glow Filter': '1.0 Light', '1.5 Light neutral Gow Filter': '1.5 Light neutral',
        '2.0 Light sand Gow Filter': '2.0 Light sand', '2.5 Light medium Gow Filter': '2.5 Light medium',
        '3.0 Medium neutral Gow Filter': '3.0 Medium neutral', '3.5 Medium olive Gow Filter': '3.5 Medium olive',
        '4.0 Medium moyen Gow Filter': '4.0 Medium moyen', '4.5 Sun tan Gow Filter': '4.5 Sun tan',
    },
    # La tienda usa códigos; se nombran por el color del círculo que marca cada kit en su foto.
    'Montoc|Kit de brochas de maquillaje Fluffy x 10': {
        'lp670': 'Vino', 'lp671': 'Rosa claro', 'lp667': 'Fucsia', 'lp669': 'Lila', 'lp668': 'Rojo',
    },
    'Montoc|Brocha mini viajera': {'Sulpting': 'Sculpting'},
}

# Nombres de opción que indican un tono o color (Shopify llama "Title" a la opción única).
SHADE_OPTIONS = re.compile(r'tono|color|colou?r|shade|tonalidad|matiz|referencia|modelo|aroma', re.I)


# Cómo se llama la opción en la web ("Tonos", "Sabores"…), según el nombre que le da la tienda.
LABELS = [(r'sabor', 'Sabor'), (r'estilo|modelo', 'Estilo'), (r'aroma', 'Aroma'), (r'^colou?r$', 'Color')]


def option_label(option_name):
    return next((label for rx, label in LABELS if re.search(rx, option_name, re.I)), 'Tono')


def slug(text):
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (catalogo Agata Beauty)'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def shopify_json(url):
    parts = urlsplit(url)
    path = re.sub(r'/$', '', parts.path)
    return json.loads(get(f'{parts.scheme}://{parts.netloc}{path}.json'))['product']


def square(img):
    """Lienzo cuadrado con la foto centrada y completa (relleno con el color de la esquina)."""
    img = img.convert('RGBA')
    side = max(img.size)
    corner = img.getpixel((0, 0))
    bg = corner if corner[3] > 0 else (217, 211, 195, 255)   # beige del disco si es transparente
    canvas = Image.new('RGBA', (side, side), bg)
    canvas.paste(img, ((side - img.width) // 2, (side - img.height) // 2), img)
    return canvas.convert('RGB')


def shades_for(product, url):
    data = shopify_json(url)
    options = data.get('options', [])
    idx = next((i for i, o in enumerate(options) if SHADE_OPTIONS.search(o['name'])), None)
    if idx is None:
        if len(data.get('variants', [])) > 1 and options and options[0]['name'].lower() != 'title':
            idx = 0     # una sola opción con varios valores: se toma como tono y se informa
        else:
            return None, f"sin tonos en la página (opciones: {[o['name'] for o in options]})"
    images = {img['id']: img for img in data.get('images', [])}
    by_variant = {vid: img for img in data.get('images', []) for vid in img.get('variant_ids', [])}
    shades, seen = [], set()
    for v in data['variants']:
        name = re.sub(r'\s+', ' ', v.get(f'option{idx + 1}') or '').strip()   # solo espacios dobles
        if not name or name in seen:
            continue
        seen.add(name)
        img = v.get('featured_image') or by_variant.get(v['id']) or images.get(v.get('image_id'))
        shade = {'name': name}
        if img:
            src = img['src'].split('?')[0]
            pic = square(Image.open(io.BytesIO(get(src))))
            pic = pic.resize((SWATCH, SWATCH), Image.LANCZOS) if pic.width > SWATCH else pic
            path = OUT / product['id'] / f'{slug(name)}.webp'
            path.parent.mkdir(parents=True, exist_ok=True)
            pic.save(path, 'WEBP', quality=90, method=6)
            shade.update(image=str(path.relative_to(ROOT)), imageWidth=pic.width, imageHeight=pic.height, imageSource=src)
        shades.append(shade)
    return shades, options[idx]['name']


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    data = json.loads(DATA.read_text())
    by_key = {f"{p['brand']}|{p['name']}": p for p in data['products']}
    for key, url in SHADE_PAGES.items():
        if only and not key.startswith(f'{only}|'):
            continue
        product = by_key.get(key)
        if not product:
            print(f'!! {key}: no está en data/products.json')
            continue
        try:
            shades, note = shades_for(product, url)
        except Exception as exc:   # red bloqueada, página movida…
            print(f'!! {key}: {exc}')
            continue
        if not shades:
            print(f'-- {key}: {note}')
            continue
        fixes = SHADE_NAME_FIXES.get(key, {})
        product['shades'] = [{**s, 'name': fixes.get(s['name'], s['name'])} for s in shades]
        product['shadesLabel'] = option_label(note)
        product['shadesSource'] = url
        sin_foto = sum(1 for s in shades if 'image' not in s)
        print(f'ok {key}: {len(shades)} × {product["shadesLabel"]} (opción «{note}» en la tienda)' + (f', {sin_foto} sin foto' if sin_foto else ''))
        for s in product['shades']:
            print(f"     · {s['name']}")
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
