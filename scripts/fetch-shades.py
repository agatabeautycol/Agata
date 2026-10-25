#!/usr/bin/env python3
"""
Agrega los tonos de cada producto (nombre + foto de referencia) desde su página oficial.

    pip install pillow
    python3 scripts/fetch-shades.py            # todos los productos de SHADE_PAGES
    python3 scripts/fetch-shades.py Montoc     # solo una marca

Funciona con tiendas Shopify (lee /products/<handle>.json; una página de búsqueda usa el primer
resultado), VTEX (Samy) y WooCommerce (lee las variaciones de la página): toma la opción de tono/color de cada
variante y su foto. Las fotos solo se recortan a un cuadrado centrado, se reducen y se guardan en
WebP (sin IA ni retoques) en assets/images/tonos/{id}/. Escribe en data/products.json los campos
"shades" y "shadesSource", que scripts/extract-catalog.py conserva al regenerar desde el PDF.

No inventa nada: si la página no tiene tonos (una sola variante), el producto queda igual y se avisa.
"""
import html, io, json, re, sys, unicodedata, urllib.request
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlencode, urljoin, urlsplit

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data' / 'products.json'
OUT = ROOT / 'assets' / 'images' / 'tonos'
SWATCH = 240          # px del lado de la foto de cada tono (se muestra a 60 px; 240 cubre pantallas 4x)
LARGE = 800           # foto grande que reemplaza a la principal al elegir el tono (nunca se amplía)

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
    'Majikal|Magic Pen': 'https://www.majikalbeauty.com/products/magic-pen',
    'Majikal|Shiny Lip Oil': 'https://www.majikalbeauty.com/products/lip-oil',
    'Atenea|Base de maquillaje 1ST Scene': 'https://ateneaprofesional.com/products/mini-base-liquida-1st-scene',
    'Atenea|Rubor compacto 1ST Scene': 'https://ateneaprofesional.com/products/rubores-individuales-1st-scene',
    'Atenea|Bronzer cremoso en barra': 'https://ateneaprofesional.com/products/bronzer-cremoso',
    # Sublime: las dos muestras de textura de la foto de la tienda ("TONO 01" arriba, "TONO 02" abajo), recortadas.
    'Atenea|Iluminador efecto húmedo Sublime': {
        'items': [('SH001', 'https://cdn.shopify.com/s/files/1/0741/6132/4314/files/ILUMINADOR_EFECTO_HUMEDO-03.webp#crop=0,0,0.5,0.5'), ('SH002', 'https://cdn.shopify.com/s/files/1/0741/6132/4314/files/ILUMINADOR_EFECTO_HUMEDO-03.webp#crop=0,0.5,0.5,1')],
        'label': 'Color', 'source': 'https://ateneaprofesional.com/products/iluminador-efecto-humedo-sublime'},
    'Atenea|Serum Tinted 1ST Scene': 'https://ateneaprofesional.com/products/serum-tinted-foundation',
    'Atenea|Rubor cremoso en barra': 'https://ateneaprofesional.com/products/rubor-en-barra-cremoso-atenea-collection',
    'Atenea|Pigmento Soft Touch': 'https://ateneaprofesional.com/products/sombra-cremosa-individual',
    'Atenea|Delineador de cejas': 'https://ateneaprofesional.com/products/delineador-de-cejas-1st-scene',
    'Atenea|Lápiz delineador Color pencil': 'https://ateneaprofesional.com/products/lapiz-delineador',
    'Atenea|Lip Balm Mask': 'https://ateneaprofesional.com/products/lip-balm-mask',
    # Línea de polvos sueltos de 8 g (la del catálogo: Translúcido, Durazno/Peachy, Banana, Miel/Honey,
    # Rosado/Blossom, Matificante/Blotting y Glowy); cada uno es un producto aparte en la tienda.
    'Samy|Polvo suelto': {
        'vtex': 'https://www.samycosmetics.com', 'ft': 'polvo suelto',
        'title': r'^polvo suelto (?P<tono>.+?)\s+samy\s+8\s*g', 'source': 'https://www.samycosmetics.com/polvo%20suelto'},
    'Samy|Rubor en barra Velvet Glam': 'https://www.samycosmetics.com/rubor-en-barra-velvet-glam-s421/p',
    'Samy|Rubor Compacto Velvet Glam Samy': 'https://www.samycosmetics.com/rubor-compacto-velvet-glam-s422/p',
    'Samy|Rubor 2 en 1 Sunset Glam Samy': 'https://www.samycosmetics.com/rubor-2-en-1-sunset-glam-samy-s388-1/p',
    'Samy|Tinta en crema Lip Blush': 'https://www.samycosmetics.com/tinta-en-crema-samy-s383/p',
    'Samy|Contorno en barra Velvet Glam': 'https://www.samycosmetics.com/contorno-en-barra-velvet-glam-s420/p',
    'Samy|Betún de cejas': 'https://www.samycosmetics.com/maquillaje-cremoso-de-cejas-perfect-brow-samy-s039/p',
    'Samy|Kit para cejas': 'https://www.samycosmetics.com/kit-para-cejas-perfect-brows-samy-s026/p',
    'Samy|Paleta de sombras x3': 'https://www.samycosmetics.com/-paleta-de-sombras-x-3-samy-s436/p',
    # Cada tono de la paleta x9 es un producto aparte ("Paleta X 9 Sombras De Ojos Samy # 20. Moon").
    'Samy|Paleta de sombras x9': {
        'vtex': 'https://www.samycosmetics.com', 'ft': 'paleta x 9',
        'title': r'^paleta x 9 sombras de ojos samy # (?P<tono>.+)$',
        'source': 'https://www.samycosmetics.com/paleta-x-9-sombra-de-ojos-samy-20-moon-s439/p'},
    'Lula|Lápiz delineador de ojos': 'https://lulabeauty.co/products/lapiz-delineador-para-ojos',
    'Lula|Aceite para labios con charm': 'https://lulabeauty.co/products/aceite-para-labios-con-charm',
    'Lula|Bálsamo de labios': 'https://lulabeauty.co/products/balsamo-de-labios',
    'Lula|Toallas húmedas desmaquillantes': 'https://lulabeauty.co/products/toallas-humedas-desmaquillante-pepino-lula',
    # Raquel en Los Estilistas (tienda que revende la marca): una página por tono. La tienda tiene las fotos
    # cruzadas (la del "#3 Almendras" es "N2-Miel"), así que se toman solo los nombres.
    'Raquel|Polvo suelto traslúcido mate minerals con avena y trigo': {
        'pages': [f'https://losestilistas.com.co/raquel-polvo-suelto-{h}' for h in
                  ('3-traslucidos', '1a-banana-traslucido', '2-traslucidos', '3-almendras', '4-beige')],
        'title': r'#\s*(?P<tono>.+)$', 'photos': False,
        'source': 'https://losestilistas.com.co/search?q=polvo+raquel'},
    'OG|Base Aqua smooth': 'https://ogmantra.co/products/base-cobertura-media-og',
    'OG|Base Stay matte': 'https://ogmantra.co/products/base-stay-matte-og',
    'OG|Rubor mineralizado Daily': 'https://ogmantra.co/products/rubor-mineralizado-daily',
    'OG|Rubor matte Daily': 'https://ogmantra.co/products/rubor-matte-daily',
    # Milagros: cada aroma es un producto ("Perfume Capilar y Corporal Bali (Notas Dulces y Relajantes)").
    'Milagros|Perfume capilar y corporal': {
        'store': 'https://milagrosbeauty.com', 'title': r'^perfume capilar y corporal (?P<tono>\S+) \(', 'label': 'Aroma',
        'source': 'https://milagrosbeauty.com/collections/perfumes-capilares'},
    # Chap Stick: cada sabor es un producto ("Chapstick Cherry"); los 4 sabores del catálogo.
    'Chap Stick|Protector labial': {
        'store': 'https://chapstick.com.co', 'title': r'^chapstick (?P<tono>strawberry|cherry|mint|med)$', 'label': 'Sabor',
        'source': 'https://chapstick.com.co/'},
    # Maybelline: cada versión (lavable / a prueba de agua) en la tienda que indicó Ágata Beauty.
    'Maybelline|Pestañina Sky High Lavable | A prueba de agua': {
        'items': [('Lavable', 'https://www.medipiel.com.co/pestanina-sky-high-negra-lavable-maybelline/p'), ('A prueba de agua', 'https://www.cromantic.com/pestanina-maybelline-lash-sensational-sky-high/p#2')],
        'label': 'Versión', 'sourceLabel': 'tiendas Medipiel (lavable) y Cromantic (a prueba de agua)', 'source': 'https://www.medipiel.com.co/pestanina-sky-high-negra-lavable-maybelline/p'},
    'Maybelline|Pestañina Colossal Lavable | A prueba de agua': {
        'items': [('Lavable', 'https://www.medipiel.com.co/pestanina-the-colossal-volum-express-lavable-maybelline/p'), ('A prueba de agua', 'https://www.cromantic.com/pestanina-maybelline-colossal-50938/p')],
        'label': 'Versión', 'sourceLabel': 'tiendas Medipiel (lavable) y Cromantic (a prueba de agua)', 'source': 'https://www.medipiel.com.co/pestanina-the-colossal-volum-express-lavable-maybelline/p'},
    'Maybelline|Pestañina Surreal Lavable | A prueba de agua': {
        'items': [('Lavable', 'https://www.medipiel.com.co/pestanina-falsies-surreal-very-black-lavable-maybelline/p'), ('A prueba de agua', 'https://www.cromantic.com/pestanina-maybelline-falsies-surreal-black/p#2')],
        'label': 'Versión', 'sourceLabel': 'tiendas Medipiel (lavable) y Cromantic (a prueba de agua)', 'source': 'https://www.medipiel.com.co/pestanina-falsies-surreal-very-black-lavable-maybelline/p'},
    # Nivea Lip care: los dos del catálogo (página 128), con el nombre del empaque.
    'Nivea|Lip care - 24 horas de humectación': {
        'items': [('Strawberry Shine', 'https://www.nivea.com.co/productos/protector-labial-strawberry-shine-40058088508390057.html'),
                  ('Blackberry Shine', 'https://www.nivea.com.co/productos/protector-labial-blackberry-shine-40059007645460057.html')],
        'label': 'Tono', 'source': 'https://www.nivea.com.co/productos/protector-labial-strawberry-shine-40058088508390057.html'},
    # Fantiluna (WooCommerce): cada aroma es un producto de la categoría.
    'Fantiluna|Mantequilla corporal x 220 ml': {
        'woo': 'https://fantiluna.com', 'category': 340, 'title': r'^mantequilla corporal (?P<tono>.+?)(?: 220 ?ml)?$',
        'source': 'https://fantiluna.com/categoria-producto/mantequillas-corporales/'},
    'Fantiluna|Exfoliante corporal x 220ml': {
        'woo': 'https://fantiluna.com', 'category': 322, 'title': r'^exfoliante corporal (?:de )?(?P<tono>.+)$',
        'source': 'https://fantiluna.com/categoria-producto/exfoliantes/'},
    'Fantiluna|Splash corporal x 250 ml': {
        'woo': 'https://fantiluna.com', 'category': 329, 'title': r'^splash (?:corporal )?(?P<tono>.+?)(?: 250 ?ml)?$',
        'source': 'https://fantiluna.com/categoria-producto/splash/'},
    'Fantiluna|Splash corporal x 105 ml': {
        'woo': 'https://fantiluna.com', 'category': 331,
        'title': r'^(?:splash mini|mini splash)(?: corporal)? (?P<tono>.+?)(?: 105 ?ml)?$',
        'source': 'https://fantiluna.com/categoria-producto/splash-mini/'},
    'Fantiluna|Iluminador corporal x 160 ml': {
        'woo': 'https://fantiluna.com', 'category': 346, 'title': r'^iluminador corporal (?P<tono>.+)$', 'label': 'Color',
        'source': 'https://fantiluna.com/categoria-producto/iluminadores-corporales/'},
    # Crema corporal: aromas de la presentación de 120 ml (cada uno con su foto).
    'Fantiluna|Crema corporal': {
        'woo': 'https://fantiluna.com', 'category': 354, 'title': r'^mini crema corporal (?P<tono>.+?)(?: 120 ?ml)?$',
        'source': 'https://fantiluna.com/cremas-corporales/'},
}

# Nombres de la página oficial ajustados con autorización de Ágata Beauty, por producto.
SHADE_NAME_FIXES = {
    # Sabores con los nombres del catálogo ("Fresa, cereza, menta y medicado").
    'Chap Stick|Protector labial': {'Strawberry': 'Fresa', 'Cherry': 'Cereza', 'Mint': 'Menta', 'Med': 'Medicado'},
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
    # Atenea escribe los tonos como códigos en mayúsculas y con las palabras pegadas.
    'Atenea|Rubor compacto 1ST Scene': {'dustyrose': 'Dusty Rose', 'peachmelba': 'Peach Melba', 'pinkpearl': 'Pink Pearl'},
    'Atenea|Pigmento Soft Touch': {'tropicalb': 'Tropical B', 'nakedmind': 'Naked Mind'},
    'Atenea|Lápiz delineador Color pencil': {   # así los escribe la tienda en la descripción del producto
        'palepink': 'Pale Pink', 'coolwood': 'Cool Wood', 'nudedark': 'Nude Dark', 'gojiberry': 'Goji Berry',
        'clearwine': 'Clear Wine', 'darksand': 'Dark Sand'},
    'Atenea|Delineador de cejas': {'aublight': 'Light'},   # la foto de la tienda dice "Light – café claro"
    'Atenea|Base de maquillaje 1ST Scene': {'eboky': 'Ebony'},
    'Atenea|Serum Tinted 1ST Scene': {'eboky': 'Ebony'},
    # Nombres como en el catálogo (página 32).
    'Atenea|Rubor cremoso en barra': {'pinkchai': 'Pink Chai', 'sugarplum': 'Sugar Plum', 'cherrypie': 'Cherry Pie', 'scarletfever': 'Scarlet Fever'},
    'Atenea|Bronzer cremoso en barra': {'tostedcoconut': 'Toasted Coconut'},
    'Majikal|Magic Pen': {'cafeina': 'Cafeína', 'cherrs': 'Cherry'},
    'Samy|Rubor 2 en 1 Sunset Glam Samy': {'04 coffe toffee': '04 Coffee Toffee'},
    'Lula|Lápiz delineador de ojos': {'magico': 'Mágico'},
    'Lula|Aceite para labios con charm': {'careza': 'Cereza'},
    'Lula|Toallas húmedas desmaquillantes': {'colageno': 'Colágeno'},
    'Raquel|Polvo suelto traslúcido mate minerals con avena y trigo': {'1 traslucidos': '1 Traslúcidos'},
    'OG|Rubor matte Daily': {'02 coray': '02 Coral'},
    'Milagros|Perfume capilar y corporal': {'bali': 'Balí'},   # como lo escribe el catálogo
    'Fantiluna|Exfoliante corporal x 220ml': {'exploción tropical': 'Explosión Tropical'},
    'Fantiluna|Crema corporal': {'seduccion': 'Seducción'},
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
    url = url.replace(' ', '%20')            # algunas tiendas (VTEX) dejan espacios en los nombres de archivo
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (catalogo Agata Beauty)'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def shopify_json(url):
    parts = urlsplit(url)
    path = re.sub(r'/$', '', parts.path)
    return json.loads(get(f'{parts.scheme}://{parts.netloc}{path}.json'))['product']


# Productos cuyas fotos de tonos no se recortan (primeros planos de textura u ojos, o carteles con letras:
# el recorte automático queda mal); conservan el fondo original de la tienda.
KEEP_BACKGROUND = {
    'Atenea|Delineador de cejas', 'Fantiluna|Iluminador corporal x 160 ml',
    # El recorte borraba partes del producto (revisado por Ágata Beauty): se deja la foto de la tienda.
    'Montoc|Base Glow Filter', 'Montoc|Kit de brochas de maquillaje Fluffy x 10', 'Bloomshell|Base líquida 2 en 1 My foundation',
    'Bloomshell|Trío de Rubores', 'Samy|Paleta de sombras x9',
    # Las fotos de cada tono traen una tarjeta blanca con íconos que el recorte no separa.
    'Atenea|Rubor cremoso en barra',
    # Muestras de textura recortadas y empaque de Nivea, que el recorte cortaba.
    'Atenea|Iluminador efecto húmedo Sublime',
}
# Fotos con fondo que deben verse completas dentro del círculo (empaques que llegan al borde de la foto).
FIT_IN_CIRCLE = set()
# Fondo blanco liso: se vuelve transparente solo el blanco conectado con los bordes de la foto (sin
# recortador automático, que aquí borraba partes del empaque). El producto no se toca.
WHITE_BACKGROUND = {'Nivea|Lip care - 24 horas de humectación'}


def white_to_alpha(img, tolerance=12):
    """Transparente el blanco liso que toca los bordes (relleno desde los bordes, no dentro del producto)."""
    work = img.convert('RGB')
    w, h = work.size
    marker = (1, 254, 3)                                  # color que no aparece en la foto
    edges = [(x, y) for x in range(0, w, max(1, w // 40)) for y in (0, h - 1)] \
        + [(x, y) for y in range(0, h, max(1, h // 40)) for x in (0, w - 1)]
    for xy in edges:
        if all(c >= 255 - tolerance for c in work.getpixel(xy)):
            ImageDraw.floodfill(work, xy, marker, thresh=tolerance)
    background = np.all(np.array(work) == marker, axis=2)
    out = np.array(img.convert('RGBA'))
    out[background, 3] = 0
    return Image.fromarray(out)

# Tonos cuyas fotos de la tienda no muestran el producto (primer plano de textura, ambiente): solo nombres.
NAMES_ONLY = set()

_SESSION = None
MARGIN = 0.10         # aire mínimo alrededor del producto
DISC = 0.88           # el producto (incluidas sus esquinas) cabe en este % del círculo


def cutout(img):
    """Quita solo el fondo (autorizado por Ágata Beauty): el recortador automático (rembg,
    isnet-general-use) calcula una máscara que se aplica como transparencia sobre los píxeles
    originales; el color del producto no se toca."""
    global _SESSION
    from rembg import new_session, remove
    if _SESSION is None:
        _SESSION = new_session('isnet-general-use')
    rgb = img.convert('RGB')
    mask = remove(rgb, session=_SESSION, only_mask=True, post_process_mask=True)
    out = rgb.convert('RGBA')
    out.putalpha(mask.convert('L'))
    return out


def has_transparency(img):
    return (img.mode in ('RGBA', 'LA', 'PA') or (img.mode == 'P' and 'transparency' in img.info)) \
        and img.convert('RGBA').getchannel('A').getextrema()[0] < 250


def frame_product(img, size):
    """Producto sin fondo (si la foto ya es PNG transparente no se recorta), centrado en un lienzo
    cuadrado transparente donde su diagonal cabe en el círculo, y reducido a `size` (nunca ampliado).
    En la web la transparencia deja ver el disco beige del catálogo (#d9d3c3)."""
    img = img.convert('RGBA') if has_transparency(img) else cutout(img)
    box = img.getchannel('A').point(lambda a: 255 if a > 8 else 0).getbbox() or (0, 0, *img.size)
    img = img.crop(box)
    w, h = img.size
    side = round(max(max(w, h) * (1 + 2 * MARGIN), (w * w + h * h) ** 0.5 / DISC))
    canvas = Image.new('RGBA', (side, side), (0, 0, 0, 0))
    canvas.paste(img, ((side - w) // 2, (side - h) // 2), img)
    return canvas.resize((size, size), Image.LANCZOS) if side > size else canvas


def square(img, fit=False):
    """Lienzo cuadrado con la foto centrada y completa (relleno con el color de la esquina).
    Con fit=True el lienzo crece hasta que las esquinas de la foto caben en el círculo de la web."""
    img = img.convert('RGBA')
    side = max(img.size)
    if fit:
        side = round(max(side, (img.width ** 2 + img.height ** 2) ** 0.5 / DISC))
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


def vtex_options(url):
    """Tienda VTEX (dirección terminada en /p, o una búsqueda): cada SKU del producto es un tono."""
    parts = urlsplit(url)
    base = f'{parts.scheme}://{parts.netloc}'
    path = parts.path.rstrip('/')
    if path.endswith('/p'):
        api = f"{base}/api/catalog_system/pub/products/search{path}"
    else:   # búsqueda ("/polvo%20suelto"): primer producto que devuelve la tienda
        api = f"{base}/api/catalog_system/pub/products/search?ft={quote(unquote(path.strip('/')))}&_from=0&_to=49"
    found = json.loads(get(api))
    if not found:
        return None, ['producto no encontrado'], url
    product = found[0]
    url = f"{base}/{product['linkText']}/p"
    items = product.get('items', [])
    variation = next((v for v in (items[0].get('variations') or []) if SHADE_OPTIONS.search(v)), None) if items else None
    if len(items) < 2 and not variation:
        return None, [f"una sola presentación ({product['productName']})"], url
    out = []
    for item in items:
        name = (item.get(variation) or [None])[0] if variation else item.get('name')
        img = (item.get('images') or [{}])[0].get('imageUrl')
        out.append((name, img))
    return variation or 'Tono', out, url


def vtex_by_title(base, ft, title, source):
    """Tienda VTEX que publica cada tono como un producto aparte: busca `ft` y toma el tono del nombre."""
    rx, items = re.compile(title, re.I), []
    found = json.loads(get(f"{base}/api/catalog_system/pub/products/search?ft={quote(ft)}&_from=0&_to=49"))   # VTEX no acepta "+"

    for product in found:
        m = rx.match(re.sub(r'\s+', ' ', product['productName']).strip())
        if m and product.get('items'):
            img = (product['items'][0].get('images') or [{}])[0].get('imageUrl')
            items.append((m.group('tono'), img))
    return ('Tono' if items else None), items, source


def woo_category(base, category, title, source):
    """Tienda WooCommerce que publica cada tono como un producto de una categoría (API pública de la tienda)."""
    rx, items = re.compile(title, re.I), []
    found = json.loads(get(f'{base}/wp-json/wc/store/v1/products?category={category}&per_page=100'))
    for product in found:
        m = rx.match(html.unescape(product['name']).strip())
        if m and product.get('type') == 'simple':      # los "al por mayor" son productos variables
            items.append((m.group('tono'), product['images'][0]['src'] if product.get('images') else None))
    return ('Aroma' if items else None), items, source


def pages_ld_json(pages, title, source, photos=True):
    """Una página por tono: toma el nombre (y la foto) de los datos de producto de cada página."""
    rx, items = re.compile(title, re.I), []
    for page in pages:
        text = get(page).decode('utf-8', 'replace')
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
            try:
                data = json.loads(block)
            except ValueError:
                continue
            if data.get('@type') == 'Product':
                m = rx.search(data['name'].strip())
                if m:
                    items.append((m.group('tono'), data.get('image') if photos else None))
                break
    return ('Tono' if items else None), items, source


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


def fixed_items(items, source):
    """Opciones con nombre fijo, cada una con su página de producto (VTEX con /p, datos estructurados) o su foto."""
    found = []
    for name, page in items:
        if re.search(r'\.(jpe?g|png|webp)(#crop=[\d.,]+)?$', page, re.I):   # foto directa, con su "#crop=" si lo trae
            found.append((name, page))
            continue
        page, _, n = page.partition('#')                      # "#N": foto N de la página (sin letreros)
        n = int(n or 1) - 1
        parts = urlsplit(page)
        if parts.path.endswith('/p'):                         # VTEX
            data = json.loads(get(f"{parts.scheme}://{parts.netloc}/api/catalog_system/pub/products/search{parts.path.rstrip('/')}"))
            images = data[0]['items'][0].get('images') if data and data[0].get('items') else None
            found.append((name, images[n]['imageUrl'] if images and len(images) > n else None))
        else:                                                 # datos estructurados de la página (Nivea)
            m = re.search(r'"image":\["([^"]+)"', get(page).decode('utf-8', 'replace'))
            found.append((name, m.group(1) if m else None))
    return 'Opción', found, source


def shades_for(product, url, keep_background=False, fit=False, white_bg=False):
    if isinstance(url, dict) and 'items' in url:
        option, items, url = fixed_items(url['items'], url['source'])
    elif isinstance(url, dict) and 'woo' in url:
        option, items, url = woo_category(url['woo'], url['category'], url['title'], url['source'])
    elif isinstance(url, dict) and 'pages' in url:
        option, items, url = pages_ld_json(url['pages'], url['title'], url['source'], url.get('photos', True))
    elif isinstance(url, dict) and 'vtex' in url:
        option, items, url = vtex_by_title(url['vtex'], url['ft'], url['title'], url['source'])
    elif isinstance(url, dict):
        option, items, url = shopify_by_title(url['store'], url['title'], url['source'])
    elif '/products/' in url or urlsplit(url).path.rstrip('/').endswith('/search'):
        option, items, url = shopify_options(url)
    elif urlsplit(url).netloc.endswith('samycosmetics.com'):
        option, items, url = vtex_options(url)
    else:
        option, items, url = woocommerce_options(url)
    if option is None:
        return None, f'sin tonos en la página ({items})', url
    shades, seen, seen_src = [], set(), {}
    for raw_name, src in items:
        # Solo formato: espacios dobles, "tono " repetido al inicio, guion tras el número y mayúscula inicial.
        name = re.sub(r'^tono\s+', '', re.sub(r'\s+', ' ', raw_name or '').strip(), flags=re.I)
        name = re.sub(r'^(\d+(?:\.\d+)?)\s*-\s*', r'\1 ', name)          # "00-Anne" -> "00 Anne"
        name = re.sub(r'^(\d+)\.\s*(?=\D)', r'\1 ', name)                  # "01. AUTHENTIC" -> "01 AUTHENTIC"
        name = name.split(':')[0].strip()                                 # "Latte: café medio cálido" -> "Latte"
        if name.isupper() and not re.fullmatch(r'[A-Z]+\d+', name):       # "ICONIC GIRL" -> "Iconic Girl" (no "SH001")
            name = name.title()

        name = re.sub(r'^([^A-Za-zÁÉÍÓÚÑáéíóúñ]*)([a-záéíóúñ])', lambda m: m.group(1) + m.group(2).upper(), name)
        if not name or name in seen:
            continue
        seen.add(name)
        shade = {'name': name}
        if src:
            src = urljoin(url, src)
            src, _, crop = src.partition('#crop=')               # "#crop=x0,y0,x1,y1": recorte (fracciones de la foto)
            original = Image.open(io.BytesIO(get(src)))
            if white_bg and not has_transparency(original):
                original = white_to_alpha(original)
            if crop:
                x0, y0, x1, y1 = (float(v) for v in crop.split(','))
                w, h = original.size
                original = original.crop((round(x0 * w), round(y0 * h), round(x1 * w), round(y1 * h)))
                src = f'{src}#crop={crop}'
            path = OUT / product['id'] / f'{slug(name)}.webp'
            path.parent.mkdir(parents=True, exist_ok=True)
            if src in seen_src:                       # misma foto para otro tono: no se recorta dos veces
                big = seen_src[src]
            else:
                if keep_background:
                    big = square(original, fit=fit)
                    big = big.resize((LARGE, LARGE), Image.LANCZOS) if big.width > LARGE else big
                else:
                    big = frame_product(original, LARGE)   # sin fondo, sobre el beige de la web
                seen_src[src] = big
            pic = big.resize((SWATCH, SWATCH), Image.LANCZOS) if big.width > SWATCH else big
            pic.save(path, 'WEBP', quality=90, alpha_quality=100, method=6)
            big_path = path.with_name(f'{slug(name)}-grande.webp')
            big.save(big_path, 'WEBP', quality=88, alpha_quality=100, method=6)
            shade.update(image=str(path.relative_to(ROOT)), imageWidth=pic.width, imageHeight=pic.height,
                         imageLarge=str(big_path.relative_to(ROOT)), imageLargeWidth=big.width, imageLargeHeight=big.height,
                         imageSource=src)
        shades.append(shade)
    # Una misma foto para todos los tonos no ayuda a elegir: se muestran solo los nombres.
    sources = [s.get('imageSource') for s in shades]
    if len(shades) > 1 and len(set(sources)) == 1 and sources[0]:
        for s in shades:
            for k in ('image', 'imageWidth', 'imageHeight', 'imageLarge', 'imageLargeWidth', 'imageLargeHeight', 'imageSource'):
                s.pop(k, None)
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
            shades, note, page_url = shades_for(product, url, key in KEEP_BACKGROUND, key in FIT_IN_CIRCLE, key in WHITE_BACKGROUND)
        except Exception as exc:   # red bloqueada, página movida…
            print(f'!! {key}: {exc}')
            continue
        if not shades:
            print(f'-- {key}: {note}')
            continue
        if key in NAMES_ONLY:
            shades = [{'name': s['name']} for s in shades]
        fixes = {k.lower(): v for k, v in SHADE_NAME_FIXES.get(key, {}).items()}
        product['shades'] = [{**s, 'name': fixes.get(s['name'].lower(), s['name'])} for s in shades]
        product['shadesLabel'] = url.get('label') if isinstance(url, dict) and url.get('label') else option_label(note)
        used = {s.get(k) for s in product['shades'] for k in ('image', 'imageLarge')}
        for old in (OUT / product['id']).glob('*.webp'):     # fotos de tonos que ya no existen
            if str(old.relative_to(ROOT)) not in used:
                old.unlink()
        product['shadesSource'] = page_url
        if isinstance(url, dict) and url.get('sourceLabel'):
            product['shadesSourceLabel'] = url['sourceLabel']
        sin_foto = sum(1 for s in shades if 'image' not in s)
        print(f'ok {key}: {len(shades)} × {product["shadesLabel"]} (opción «{note}» en la tienda)' + (f', {sin_foto} sin foto' if sin_foto else ''))
        for s in product['shades']:
            print(f"     · {s['name']}")
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
