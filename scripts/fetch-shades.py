#!/usr/bin/env python3
"""
Agrega los tonos de cada producto (nombre + foto de referencia) desde su página oficial.

    pip install pillow
    python3 scripts/fetch-shades.py            # todos los productos de SHADE_PAGES
    python3 scripts/fetch-shades.py Montoc     # solo una marca

Funciona con tiendas Shopify (lee /products/<handle>.json; una página de búsqueda usa el primer
resultado) y WooCommerce (lee las variaciones de la página): toma la opción de tono/color de cada
variante y su foto. Las fotos solo se recortan a un cuadrado centrado, se reducen y se guardan en
WebP (sin IA ni retoques) en assets/images/tonos/{id}/. Escribe en data/products.json los campos
"shades" y "shadesSource", que scripts/extract-catalog.py conserva al regenerar desde el PDF.

No inventa nada: si la página no tiene tonos (una sola variante), el producto queda igual y se avisa.
"""
import html, io, json, re, sys, unicodedata, urllib.request
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urljoin, urlsplit

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
    # Bloomshell: bloomshell.co es la tienda oficial; las otras son tiendas que revenden la marca.
    # En bloomshell.co cada tono es un producto aparte: "My foundation 2 en 1 (base líquida)(vainilla)".
    'Bloomshell|Base líquida 2 en 1 My foundation': {
        'store': 'https://bloomshell.co', 'title': r'^my foundation 2 en 1 \(base l[ií]quida\)\((?P<tono>[^)]+)\)$',
        'source': 'https://bloomshell.co/search?q=BASE+LIQUIDA+MY+FOUNDATION'},
    # Tonos del tamaño 10 ml (los 9 del "big" de 20 ml / Jumbo están incluidos).
    'Bloomshell|Corrector My concealer': {
        'store': 'https://bloomshell.co', 'title': r'^(?:corrector )?my concealer new 10 ml \((?P<tono>[^)]+)\)$',
        'source': 'https://bloomshell.co/search?q=Corrector+My+concealer'},
    'Bloomshell|Rubor en barra Cherry Blossom': 'https://www.girlymaquillaje.com/producto/rubor-cherry-blosson-bloomshell/',
    'Bloomshell|Trío de Rubores': 'https://mysticstore.com.co/producto/velvet-rubor-x3-bloomshell/',
    'Bloomshell|Contorno en barra Bloom define': 'https://kromaspace.com/producto/contorno-en-barra-bloom-define-bloomshell/',
    'Girly|Girly TINT Labios y mejillas': 'https://cocopinkstore.com/products/tinta-de-labios-girly',   # tienda que revende Girly
    'Ani-k|2 en 1: base y corrector': 'https://anikmakeup.com/products/base-bonita',
    'Ani-k|Loose powder Polvos sueltos': 'https://anikmakeup.com/products/polvo-suelto',
    'Ani-k|Serum Flyshy Blushy': 'https://anikmakeup.com/products/serum-blush-flushy-blushy',
    'Ani-k|Rubor líquido Bonita': 'https://anikmakeup.com/products/rubor-liquido-bonita',
    'Ani-k|Rubor en polvo Bonita': 'https://anikmakeup.com/products/rubor-bonita',
    'Ani-k|Lip Gloss': 'https://anikmakeup.com/products/gloss-bonita',
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
    # La tienda escribe "mÉdium"; se deja sin tilde, igual que "Medium beige".
    'Bloomshell|Base líquida 2 en 1 My foundation': {'Médium deep': 'Medium deep', 'Neutral médium': 'Neutral medium'},
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


def shopify_by_title(store, title, source):
    """Tienda Shopify que publica cada tono como un producto aparte: se recorren todos sus productos
    (/products.json) y se toma el tono del título con la expresión `title` (grupo "tono")."""
    rx = re.compile(title, re.I)
    items, page = [], 1
    while True:
        batch = json.loads(get(f'{store}/products.json?limit=250&page={page}'))['products']
        if not batch:
            break
        for p in batch:
            m = rx.match(p['title'].strip())
            if m:
                tone = m.group('tono').replace('-', ' ').strip()
                tone = tone.lower()                                  # "mÉdium deep" -> "médium deep"
                items.append((tone, p['images'][0]['src'].split('?')[0] if p['images'] else None))
        page += 1
    items.sort(key=lambda t: t[0])
    return ('Tono' if items else None), items, source


def shopify_options(url):
    """Tienda Shopify: (nombre de la opción, [(tono, url de foto)], url del producto)."""
    parts = urlsplit(url)
    if parts.path.rstrip('/').endswith('/search'):
        # Página de búsqueda: se usa el primer producto que devuelve el buscador de la tienda.
        q = parse_qs(parts.query).get('q', [''])[0]
        found = json.loads(get(f'{parts.scheme}://{parts.netloc}/search/suggest.json?'
                               + urlencode({'q': q, 'resources[type]': 'product', 'resources[limit]': 1})))
        hits = found['resources']['results']['products']
        if not hits:
            return None, [], url
        url = f"{parts.scheme}://{parts.netloc}{hits[0]['url'].split('?')[0]}"
    data = shopify_json(url)
    options = data.get('options', [])
    idx = next((i for i, o in enumerate(options) if SHADE_OPTIONS.search(o['name'])), None)
    if idx is None:
        if len(data.get('variants', [])) > 1 and options and options[0]['name'].lower() != 'title':
            idx = 0     # una sola opción con varios valores: se toma como tono y se informa
        else:
            return None, [o['name'] for o in options], url
    images = {img['id']: img for img in data.get('images', [])}
    by_variant = {vid: img for img in data.get('images', []) for vid in img.get('variant_ids', [])}
    items = []
    for v in data['variants']:
        img = v.get('featured_image') or by_variant.get(v['id']) or images.get(v.get('image_id'))
        items.append((v.get(f'option{idx + 1}'), img['src'].split('?')[0] if img else None))
    return options[idx]['name'], items, url


def woocommerce_options(url):
    """Tienda WooCommerce: lee las variaciones que la página trae en data-product_variations."""
    page = get(url).decode('utf-8', 'replace')
    m = re.search(r'data-product_variations="([^"]*)"', page)
    if not m or m.group(1) in ('', 'false'):
        return None, ['sin variaciones en la página'], url
    variations = json.loads(html.unescape(m.group(1)))
    # Nombre visible de cada valor: <select name="attribute_pa_color"><option value="rosa">Rosa</option>
    labels, names = {}, {}
    for sel in re.finditer(r'<select[^>]*name="(attribute_[^"]+)"[^>]*>(.*?)</select>', page, re.S):
        attr = sel.group(1)
        labels[attr] = {html.unescape(v): html.unescape(re.sub('<[^>]+>', '', t)).strip()
                        for v, t in re.findall(r'<option[^>]*value="([^"]+)"[^>]*>(.*?)</option>', sel.group(2), re.S)}
        lab = re.search(rf'<label[^>]*for="{re.escape(attr.replace("attribute_", ""))}"[^>]*>(.*?)</label>', page, re.S)
        names[attr] = html.unescape(re.sub('<[^>]+>', '', lab.group(1))).strip() if lab else attr.replace('attribute_pa_', '').replace('attribute_', '')
    attrs = list(labels) or list(variations[0]['attributes'])
    attr = next((a for a in attrs if SHADE_OPTIONS.search(names.get(a, a))), attrs[0])
    items = []
    for v in variations:
        value = v['attributes'].get(attr)
        img = (v.get('image') or {}).get('full_src') or (v.get('image') or {}).get('src')
        items.append((labels.get(attr, {}).get(value, value), img))
    return names.get(attr, attr), items, url


def shades_for(product, url):
    if isinstance(url, dict):
        option, items, url = shopify_by_title(url['store'], url['title'], url['source'])
    else:
        shopify = '/products/' in url or urlsplit(url).path.rstrip('/').endswith('/search')
        option, items, url = (shopify_options if shopify else woocommerce_options)(url)
    if option is None:
        return None, f'sin tonos en la página ({items})', url
    shades, seen = [], set()
    for raw_name, src in items:
        # Solo formato: espacios dobles, "tono " repetido al inicio, guion tras el número y mayúscula inicial.
        name = re.sub(r'^tono\s+', '', re.sub(r'\s+', ' ', raw_name or '').strip(), flags=re.I)
        name = re.sub(r'^(\d+(?:\.\d+)?)\s*-\s*', r'\1 ', name)          # "00-Anne" -> "00 Anne"

        name = re.sub(r'^([^A-Za-zÁÉÍÓÚÑáéíóúñ]*)([a-záéíóúñ])', lambda m: m.group(1) + m.group(2).upper(), name)
        if not name or name in seen:
            continue
        seen.add(name)
        shade = {'name': name}
        if src:
            src = urljoin(url, src)
            pic = square(Image.open(io.BytesIO(get(src))))
            pic = pic.resize((SWATCH, SWATCH), Image.LANCZOS) if pic.width > SWATCH else pic
            path = OUT / product['id'] / f'{slug(name)}.webp'
            path.parent.mkdir(parents=True, exist_ok=True)
            pic.save(path, 'WEBP', quality=90, method=6)
            shade.update(image=str(path.relative_to(ROOT)), imageWidth=pic.width, imageHeight=pic.height, imageSource=src)
        shades.append(shade)
    # Si todos los tonos llevan número ("Pink 01", "02 Tropical bronze"), se ordenan por ese número.
    nums = [re.search(r'\d+(?:\.\d+)?', s['name']) for s in shades]
    if shades and all(nums):
        shades = [s for _, s in sorted(zip((float(n.group()) for n in nums), shades), key=lambda t: t[0])]
    return shades, option, url


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
            shades, note, page_url = shades_for(product, url)
        except Exception as exc:   # red bloqueada, página movida…
            print(f'!! {key}: {exc}')
            continue
        if not shades:
            print(f'-- {key}: {note}')
            continue
        fixes = {k.lower(): v for k, v in SHADE_NAME_FIXES.get(key, {}).items()}
        product['shades'] = [{**s, 'name': fixes.get(s['name'].lower(), s['name'])} for s in shades]
        product['shadesLabel'] = option_label(note)
        used = {s.get('image') for s in product['shades']}
        for old in (OUT / product['id']).glob('*.webp'):     # fotos de tonos que ya no existen
            if str(old.relative_to(ROOT)) not in used:
                old.unlink()
        product['shadesSource'] = page_url
        sin_foto = sum(1 for s in shades if 'image' not in s)
        print(f'ok {key}: {len(shades)} × {product["shadesLabel"]} (opción «{note}» en la tienda)' + (f', {sin_foto} sin foto' if sin_foto else ''))
        for s in product['shades']:
            print(f"     · {s['name']}")
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
