#!/usr/bin/env python3
"""
Trae la foto principal en alta resolución de cada producto desde su página oficial.

    python3 scripts/fetch-product-photos.py            # todos los productos con enlace
    python3 scripts/fetch-product-photos.py Montoc     # solo una marca

Fuentes, en orden de prioridad: las fotos originales de catalogo-original/fotos/{id}.png|jpg|webp y los
enlaces de scripts/fetch-shades.py (SHADE_PAGES) más los de PHOTO_PAGES. Deja cada
foto en assets/images/productos-hd/{id}.webp con su origen en fuentes.json.

Proceso (autorizado por Ágata Beauty): se quita SOLO el fondo con un recortador automático (rembg,
modelo isnet-general-use), que únicamente decide qué píxeles son transparentes: los píxeles del producto
quedan intactos (sin cambiar colores, letras ni forma, sin "mejorar" la nitidez). Luego la foto se centra
en un lienzo cuadrado transparente con margen para el círculo y se reduce a 800 px si es más grande
(nunca se amplía). En la web la transparencia deja ver el disco beige del catálogo.

    pip install "rembg[cpu]" pillow

Después hay que regenerar el catálogo (scripts/extract-catalog.py), que usa estas fotos en vez del
recorte del PDF. Antes de publicar, revisar que cada foto sea el mismo producto y presentación.
"""
import importlib.util, io, json, re, sys
from pathlib import Path
from urllib.parse import urlsplit

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
LOCAL = ROOT / 'catalogo-original' / 'fotos'   # fotos originales entregadas por Ágata Beauty: {id}.png/.jpg/.webp
DATA = ROOT / 'data' / 'products.json'
OUT = ROOT / 'assets' / 'images' / 'productos-hd'
SIZE = 800            # lado máximo de la foto (la ficha la muestra a 320 px; 800 cubre pantallas 2,5x)
MARGIN = 0.10         # aire mínimo alrededor del producto
DISC = 0.88           # el producto (incluidas sus esquinas) cabe en este % del círculo

_spec = importlib.util.spec_from_file_location('fetch_shades', ROOT / 'scripts' / 'fetch-shades.py')
shades = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(shades)

# Productos sin tonos (o cuyo enlace de tonos no sirve para la foto principal): "Marca|Nombre": url.
# Coincidencias buscadas en la tienda de cada marca y revisadas contra la foto del catálogo.
PHOTO_PAGES = {
    'Montoc|Polvos Translúcidos': 'https://montoccosmetictools.com/products/polvo-suelto-soft-powder',
    'Montoc|Brow Wax Ultra Fijador de cejas': 'https://montoccosmetictools.com/products/brow-wax-ultra',
    'Montoc|Fijador de maquillaje Dixy Fix': 'https://montoccosmetictools.com/products/fijador-de-maquillaje-dixy-fix',
    'Montoc|Set de Borlas': 'https://montoccosmetictools.com/products/set-de-borlas-triangulares-para-maquillaje',
    'Montoc|Esponja mini para difuminar maquillaje': 'https://montoccosmetictools.com/products/esponja-mini-para-difuminar-maquillaje',
    'Bloomshell|Laminador de cejas': 'https://bloomshell.co/products/bloom-lamination-de-cejas',
    'Bloomshell|Llavero Mimosa Tinta + Gloss': 'https://bloomshell.co/products/mimosa-brillo-labial-lip-gloss',
    'Bloomshell|Papel matificante Bloom powder paper': 'https://bloomshell.co/products/bloom-powder-paper-white-papel-absorbente',
    'Bloomshell|Papel matificante Bloom Oil Stop': 'https://bloomshell.co/products/bloom-oil-stop-papel-de-absorbente',
    'Bloomshell|Fijador de maquillaje Bloom Fix': 'https://bloomshell.co/products/bloom-fix-fijador',
    'Bloomshell|Kit Kiss Love': 'https://bloomshell.co/products/kit-kiss-love-x-4',
    'Bloomshell|Beauty Blender Xl': 'https://bloomshell.co/products/bloom-swirl-xl-beauty-blender',
    'Bloomshell|Bloom Blender Bliss': 'https://bloomshell.co/products/bloom-blender-bliss-pink-x-4',
    'Girly|Gel hidratante con aloe vera': 'https://cocopinkstore.com/products/gel-hidratante-con-aloe-vera-girly',
    'Girly|Polvo suelto': 'https://cocopinkstore.com/products/polvo-suelto-mini-girly',
    'Ani-k|Delineador radiante Tono negro': 'https://anikmakeup.com/products/delineador-ani-k',
    'Ani-k|Pestañina eternal lash': 'https://anikmakeup.com/products/eternal-lash',
    'Ani-k|Pestañina Brown Paradise - A prueba de agua': 'https://anikmakeup.com/products/pestanina-cafe-brown-paradise-a-prueba-de-agua',
    'Majikal|Polvos sueltos - 4 tonos': 'https://www.majikalbeauty.com/products/polvo-suelto-translucido-pequeno-copia',
    'Atenea|Serum Tinted 1ST Scene': 'https://ateneaprofesional.com/products/serum-tinted-foundation',
    'Atenea|Polvo en gel matificante Matterpowder': 'https://ateneaprofesional.com/products/polvo-en-gel-matificante',
    'Atenea|Polvo suelto- Banana 1ST Scene': 'https://ateneaprofesional.com/products/polvo-suelto-1st-scene',
    'Atenea|Rubor cremoso en barra': 'https://ateneaprofesional.com/products/rubor-en-barra-cremoso-atenea-collection',
    'Atenea|Paleta de sombras multiusos Moccalush': 'https://ateneaprofesional.com/products/paleta-de-sombras-multiusos-moccalush',
    'Atenea|Paleta de sombras 18 tonos - Art Deco': 'https://ateneaprofesional.com/products/paleta-de-sombras-18-tonos-art-deco',
    'Atenea|Paleta de sombras Majestic': 'https://ateneaprofesional.com/products/paleta-de-sombras-35-tonos-birds-1',
    'Atenea|Paleta de sombras 12 tonos - 1ST SCENE': 'https://ateneaprofesional.com/products/paleta-de-sombras-first-12-tonos-1st-scene',
    'Atenea|Paleta de sombras 12 tonos - Rose sublime': 'https://ateneaprofesional.com/products/paleta-de-sombras-12-tonos-sublime',
    'Atenea|Gel fijador de cejas': 'https://ateneaprofesional.com/products/gel-fijador-de-cejas',
    'Atenea|Primer Gummy': 'https://ateneaprofesional.com/products/gummy-primer-con-4-de-niacinamida',
    'Atenea|Brocha duo Base y productos en crema': 'https://ateneaprofesional.com/products/brocha-duo-para-base',
    'Atenea|Beauty sponge': 'https://ateneaprofesional.com/products/beauty-sponge-marmol',
    'Atenea|Encrespador Focus': 'https://ateneaprofesional.com/products/encrespador-atenea',
    'Atenea|Mini beauty sponge trio': 'https://ateneaprofesional.com/products/mini-sponge',
    'Lula|Bálsamo desmaquillante': 'https://lulabeauty.co/products/balsamo-desmaquillante',
    'Lula|Contorno de ojos Aloe Vera': 'https://lulabeauty.co/products/contorno-de-ojos-con-aloe-vera',
    'Lula|Parches de puntos negros x 8 Unidades': 'https://lulabeauty.co/products/parches-de-puntos-negros',
    'Lula|Hidratante facial de noche con ceramidas': 'https://lulabeauty.co/products/hidratante-facial-de-noche-con-ceramidas',
    'Lula|Hidratante facial de día con ceramidas': 'https://lulabeauty.co/products/hidratante-facial-de-dia-con-ceramidas',
    'Lula|Tónico de Rosas': 'https://lulabeauty.co/products/tonico-de-rosas',
    'Lula|Kit de brochas Marshmallow X 13pcs': 'https://lulabeauty.co/products/kit-de-brochas-x-13-lula',
    'Lula|Kit de brochas Uva X 14pcs': 'https://lulabeauty.co/products/set-de-brochas-uva',
    'Milagros|Shampoo herbal x 500 ml (con romero y jengibre)': 'https://milagrosbeauty.com/products/shampoo-milagro-herbal',
    'Milagros|Shampoo con cebolla x450 ml (con péptidos)': 'https://milagrosbeauty.com/products/shampoo-de-cebolla',
    'Milagros|Shampoo magia x 450 ml (ácido hialurónico)': 'https://milagrosbeauty.com/products/shampoo-magia-capilar',
    'Milagros|Shampoo anticaspa x 450 ml': 'https://milagrosbeauty.com/products/shampoo-anticaspa-pro-crecimiento',
    'Milagros|Acondicionador ultra nutritivo x 450 ml': 'https://milagrosbeauty.com/products/acondicionador-ultranutritivo-premium',
    'Milagros|Acondicionador milagro herbal x 450 ml': 'https://milagrosbeauty.com/products/acondicionador-milagro-herbal',
    'Milagros|Acondicionador ultra nutritivo x100 ml': 'https://milagrosbeauty.com/products/acondicionador-ultra-nutritivo-premium-mini',
    'Milagros|Acondicionador milagro herbal x100 ml': 'https://milagrosbeauty.com/products/acondicionador-herbal-mini',
    'Milagros|Tratamiento Emergencia Capilar x450 ml': 'https://milagrosbeauty.com/products/tratamiento-emergencia-capilar',
    'Milagros|Tratamiento nutrición y crecimiento x 450 ml': 'https://milagrosbeauty.com/products/tratamiento-rizos-crespos',
    'Milagros|Tratamiento capilar a base de frutas x450 ml': 'https://milagrosbeauty.com/products/tratamiento-frutas',
    'Milagros|Doypack tratamiento capilar a base de frutas x100 ml': 'https://milagrosbeauty.com/products/doypack-tratamiento-frutas',
    'Milagros|Doypack bio - repolarizador capilar x100 gr': 'https://milagrosbeauty.com/products/doypack-biorepolarizador',
    'Milagros|Doypack tratamiento emergencia capilar x100 gr': 'https://milagrosbeauty.com/products/doypack-tratamiento-emergencia',
    'Milagros|Tratamiento bio - repolarizador capilar x100 ml': 'https://milagrosbeauty.com/products/tratamiento-bio-repolarizador-capilar-mini',
    'Milagros|Tratamiento a base de frutas x100 ml': 'https://milagrosbeauty.com/products/tratamiento-frutas-mini',
    'Milagros|Gotas Mágicas Capilares': 'https://milagrosbeauty.com/products/gotas-magicas',
    'Milagros|Tónico revitalizante capilar milagro herbal (tónico con romero)': 'https://milagrosbeauty.com/products/tonico-revitalizante',
    'Samy|Esponja de maquillaje': 'https://www.samycosmetics.com/esponja-de-maquillaje-x1-und-s235/p',
    'Samy|Brocha retráctil': 'https://www.samycosmetics.com/brocha-retractil-para-rostro-f7-samy-s442/p',
}

# Productos cuyos tonos están publicados como productos separados: la foto de un tono no representa
# al producto completo, así que no se reemplaza automáticamente.
# Fotos oficiales que no sirven para recortar el fondo (se queda la foto del catálogo).
EXCLUDE = {
    'Montoc|Kit de brochas de maquillaje Fluffy x 10': 'la foto oficial es la caja con letras: el recorte deja letras sueltas',
    'Montoc|Polvos Translúcidos': 'la foto de la tienda muestra otro empaque (caja dorada)',
    'Montoc|Fijador de maquillaje Dixy Fix': 'el envase de la tienda se ve distinto al del catálogo',
    'Montoc|Set de Borlas': 'la tienda solo muestra la caja cerrada',
    'Bloomshell|Laminador de cejas': 'la tienda muestra el exhibidor con muchas unidades',
    'Bloomshell|Llavero Mimosa Tinta + Gloss': 'la tienda muestra el exhibidor con muchas unidades',
    'Bloomshell|Papel matificante Bloom Oil Stop': 'el recorte automático queda mal',
    'Girly|Polvo suelto': 'la tienda solo muestra la caja',
    'Majikal|Polvos sueltos - 4 tonos': 'la tienda solo muestra las cajas',
    'Milagros|Doypack tratamiento capilar a base de frutas x100 ml': 'el diseño del empaque es distinto al del catálogo',
}

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
    """Producto sin fondo, centrado en un lienzo cuadrado transparente, reducido a SIZE (nunca ampliado)."""
    return shades.frame_product(img, SIZE)


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    products = {f"{p['brand']}|{p['name']}": p for p in json.loads(DATA.read_text())['products']}
    pages = {k: v for k, v in shades.SHADE_PAGES.items() if isinstance(v, str)} | PHOTO_PAGES
    by_id = {p['id']: key for key, p in products.items()}
    sources_file = OUT / 'fuentes.json'
    sources = json.loads(sources_file.read_text()) if sources_file.exists() else {}
    OUT.mkdir(parents=True, exist_ok=True)
    for key in sorted(set(pages) | (SKIP & set(shades.SHADE_PAGES))):
        if only and not key.startswith(f'{only}|'):
            continue
        if key in EXCLUDE:
            print(f'-- {key}: {EXCLUDE[key]}')
            (OUT / f"{products[key]['id']}.webp").unlink(missing_ok=True)
            sources.pop(products[key]['id'], None)
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
        pic.save(OUT / f"{product['id']}.webp", 'WEBP', quality=90, alpha_quality=100, method=6)
        sources[product['id']] = src
        print(f"ok {key}: {original.width}×{original.height} -> {pic.width} px")
    # Fotos originales entregadas (tienen prioridad sobre las de la página oficial).
    for file in sorted(LOCAL.glob('*')) if LOCAL.exists() else []:
        key = by_id.get(file.stem)
        if file.suffix.lower() not in ('.png', '.jpg', '.jpeg', '.webp') or (only and not (key or '').startswith(f'{only}|')):
            continue
        if not key:
            print(f'!! {file.name}: el nombre no coincide con ningún ID de data/products.json')
            continue
        original = Image.open(file)
        pic = framed(original)
        pic.save(OUT / f'{file.stem}.webp', 'WEBP', quality=90, alpha_quality=100, method=6)
        sources[file.stem] = f'Foto original de Ágata Beauty: catalogo-original/fotos/{file.name}'
        print(f'ok {key}: foto original {original.width}×{original.height} -> {pic.width} px')
    sources_file.write_text(json.dumps(dict(sorted(sources.items())), ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
