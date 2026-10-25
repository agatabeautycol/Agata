#!/usr/bin/env python3
"""
Genera docs/FOTOS-A-MEJORAR.md: qué fotos principales siguen saliendo del PDF de Canva (baja
resolución), su tamaño, una medida de nitidez y si ya hay enlace oficial para reemplazarlas.

    python3 scripts/photo-report.py
"""
import collections, importlib.util, json
from pathlib import Path

from PIL import Image, ImageFilter, ImageStat

ROOT = Path(__file__).resolve().parent.parent
TARGET = 640          # px que necesita la foto de la ficha (320 px en pantalla × 2 en celulares)
SHARP_MIN = 18        # por debajo, la foto se ve borrosa o con compresión aun en las tarjetas

_spec = importlib.util.spec_from_file_location('fetch_shades', ROOT / 'scripts' / 'fetch-shades.py')
shades = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(shades)

STORES = {
    'Montoc': 'montoccosmetictools.com', 'Bloomshell': 'bloomshell.co', 'Ani-k': 'anikmakeup.com',
    'Atenea': 'ateneaprofesional.com', 'Majikal': 'majikalbeauty.com', 'Samy': 'samycosmetics.com',
    'Lula': 'lulabeauty.co', 'OG': 'ogmantra.co', 'Milagros': 'milagrosbeauty.com', 'Fantiluna': 'fantiluna.com',
    'Girly': 'cocopinkstore.com (revendedor)', 'Raquel': 'losestilistas.com.co (revendedor)',
}


def sharpness(path):
    """Desviación del Laplaciano en el centro de la foto, a un tamaño común (más alto = más detalle)."""
    im = Image.open(path).convert('RGBA')
    bg = Image.new('RGB', im.size, (221, 215, 201))
    bg.paste(im, mask=im.split()[3])
    gray = bg.convert('L').resize((256, 256)).crop((40, 40, 216, 216))
    edges = gray.filter(ImageFilter.Kernel((3, 3), [0, 1, 0, 1, -4, 1, 0, 1, 0], 1, 128))
    return ImageStat.Stat(edges).stddev[0]


def main():
    products = json.loads((ROOT / 'data' / 'products.json').read_text())['products']
    links = set(shades.SHADE_PAGES)
    by_brand = collections.OrderedDict()
    done = 0
    for p in products:
        if 'productos-hd' in p.get('image', ''):
            done += 1
            continue
        sharp = sharpness(ROOT / p['image'])
        level = 'Alta' if sharp < SHARP_MIN else 'Media' if p['imageWidth'] < 400 else 'Baja'
        by_brand.setdefault(p['brand'], []).append((p, level, f"{p['brand']}|{p['name']}" in links))
    pending = sum(len(v) for v in by_brand.values())
    counts = collections.Counter(level for v in by_brand.values() for _, level, _ in v)
    lines = [
        '# Fotos del catálogo que deben mejorar\n',
        f'De los {len(products)} productos, **{done} ya tienen foto en alta resolución** (página oficial) y '
        f'**{pending} siguen con la foto del PDF de Canva**, que se subió en baja resolución. '
        'Este archivo lo genera `scripts/photo-report.py`.\n',
        f'- **Tamaño:** la ficha muestra la foto a 320 px y en celulares necesita unos **{TARGET} px** (ideal: 800 px). '
        'Las fotos del PDF miden entre 160 y 600 px, a su resolución real (sin ampliar).',
        '- **Nitidez:** se midió el detalle de cada foto; las borrosas o con "cuadritos" de compresión van primero.\n',
        '| Prioridad | Qué significa | Fotos |', '| --- | --- | ---: |',
        f"| **Alta** | Borrosa o con compresión visible: se nota aun en las tarjetas | {counts['Alta']} |",
        f"| **Media** | Pequeña (menos de 400 px): se ve suave en la ficha | {counts['Media']} |",
        f"| **Baja** | Algo más grande o nítida, pero aún por debajo de {TARGET} px | {counts['Baja']} |\n",
        '## Qué se necesita', '',
        '1. **Las fotos originales** (las que se subieron a Canva), nombradas con el ID del producto, o',
        '2. **El enlace a la página oficial de cada producto** (se agrega en `PHOTO_PAGES` de `scripts/fetch-product-photos.py`).\n',
        '## Resumen por marca\n', '| Marca | Pendientes | Alta | Media | Baja | Tienda que ya se puede leer |',
        '| --- | ---: | ---: | ---: | ---: | --- |',
    ]
    for brand, items in by_brand.items():
        c = collections.Counter(level for _, level, _ in items)
        lines.append(f"| {brand} | {len(items)} | {c['Alta']} | {c['Media']} | {c['Baja']} | {STORES.get(brand, '—')} |")
    lines += ['\n## Lista de pendientes\n', '"Enlace" indica si ya hay página oficial del producto (la de sus tonos).\n']
    order = {'Alta': 0, 'Media': 1, 'Baja': 2}
    for brand, items in by_brand.items():
        lines += [f'### {brand}\n', '| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |', '| --- | --- | ---: | ---: | --- | --- |']
        for p, level, link in sorted(items, key=lambda t: (order[t[1]], t[0]['page'])):
            lines.append(f"| `{p['id']}` | {p['name']} | {p['page']} | {p['imageWidth']} px | {level} | {'sí' if link else '—'} |")
        lines.append('')
    (ROOT / 'docs' / 'FOTOS-A-MEJORAR.md').write_text('\n'.join(lines) + '\n')
    print(f'{done} en alta resolución, {pending} pendientes: {dict(counts)}')


if __name__ == '__main__':
    main()
