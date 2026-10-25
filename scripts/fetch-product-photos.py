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
# "#N" al final del enlace usa la foto N de la página (cuando la primera es de una modelo, no del producto).
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
    'Leche pal pelo|Shampoo tradicional x 440 ml': 'https://lechepalpelo.com/products/tratamiento-shampoo',
    'Leche pal pelo|Shampoo Protección Plus x 440 ml': 'https://lechepalpelo.com/products/shampoo-proteccion-plus',
    'Leche pal pelo|Shampoo especializado x 440 ml': 'https://lechepalpelo.com/products/shampoo-especializado-1',
    'Leche pal pelo|Shampoo nutritivo para niños x 440 ml': 'https://lechepalpelo.com/products/shampoo-nutritivo',
    'Leche pal pelo|Shampoo + Acondicionador para niños x 440 ml': 'https://lechepalpelo.com/products/shampoo-acondicionador',
    'Leche pal pelo|Shampoo hidratante rizos para niños x 440 ml': 'https://lechepalpelo.com/products/shampoo-hidratante',
    'Leche pal pelo|Acondicionador para niños x 440 ml': 'https://lechepalpelo.com/products/acondicionador-linea-kids',
    'Leche pal pelo|Acondicionador Co-wash rizos y afro x 440 ml': 'https://lechepalpelo.com/products/co-wash',
    'Leche pal pelo|Mascarilla nutritiva rizos y ondas x 440 ml': 'https://lechepalpelo.com/products/mascarilla-nutritiva-1',
    'Leche pal pelo|Mascarilla hidrosellante x 440 ml': 'https://lechepalpelo.com/products/mascarilla-hidrosellante-1',
    'Leche pal pelo|Mascarilla Regenerador Intenso 7 Oleos x 800 ml': 'https://lechepalpelo.com/products/mascarilla-7-oleos-regenerador-intenso',
    'Leche pal pelo|Mascarilla WOW x 800 ml': 'https://lechepalpelo.com/products/mascarilla-wow',
    'Leche pal pelo|Termoprotector líquido X 250 ml': 'https://lechepalpelo.com/products/termoprotector-liquido',
    'Leche pal pelo|Termoprotector tradicional x 440 ml': 'https://lechepalpelo.com/products/linea-tradicional-termoprotector',
    'Leche pal pelo|Termoprotector protección plus x 440 ml': 'https://lechepalpelo.com/products/linea-proteccion-plus-termoprotector',
    'Leche pal pelo|Termoprotector rizos y ondas x 440 ml': 'https://lechepalpelo.com/products/linea-rizos-ondas-termoprotector',
    'Leche pal pelo|Gelatina slime definidora x 600 ml': 'https://lechepalpelo.com/products/gelatina-slime-definidora',
    'Leche pal pelo|Definidor de rizos y ondas x 440 ml': 'https://lechepalpelo.com/products/definidor-rizos-ondas',
    'Anyeluz|Shampoo de cebolla x 500 ml': 'https://www.anyeluz.com/products/shampoo-de-cebolla',
    'Anyeluz|Acondicionador de cebolla x 500 ml': 'https://www.anyeluz.com/products/acondicionador-de-cebolla',
    'Anyeluz|Shampoo con romero x 500 ml': 'https://www.anyeluz.com/products/shampoo-de-romero',
    'Anyeluz|Acondicionador con romero x 500 ml': 'https://www.anyeluz.com/products/acondicionador-con-romero-anyeluz',
    'Anyeluz|Shampoo con ginseng x 500 ml': 'https://www.anyeluz.com/products/shampoo-ginseng',
    'Anyeluz|Acondicionador con ginseng x 500 ml': 'https://www.anyeluz.com/products/acondicionador-ginseng',
    'Anyeluz|Shampoo con aloe vera x 500 ml': 'https://www.anyeluz.com/products/shampoo-aloe-vera',
    'Anyeluz|Acondicionador con argán y aloe vera x 500 ml': 'https://www.anyeluz.com/products/acondicionador-ginseng-aloe',
    'Anyeluz|Shampoo liso en casa x 800 ml - línea profesional': 'https://www.anyeluz.com/products/shampoo-antifrizz-profesional',
    'Anyeluz|Acondicionador liso en casa x 800 ml - línea profesional': 'https://www.anyeluz.com/products/acondicionador-antifrizz-profesional',
    'Anyeluz|Tratamiento liso en casa - línea profesional': 'https://www.anyeluz.com/products/tratamiento-liso-casa-linea-profesional',
    'Anyeluz|Tratamiento reparación, restauración y brillo - línea profesional': 'https://www.anyeluz.com/products/tratamiento-reparacion-restauracion-y-brillo-linea-profesional',
    'Anyeluz|Tratamiento capilar de crecimiento': 'https://www.anyeluz.com/products/terapia-capilar-de-crecimiento-anyeluz',
    'Anyeluz|Tratamiento con romero y bioelixir': 'https://www.anyeluz.com/products/bioterapia-capilar-con-romero-y-bioelixir-anyeluz',
    'Olé|Shampoo protección y reparación x 500 ml': 'https://olecapilar.com/products/shampoo-antioxidante-mix-de-frutas',
    'Olé|Shampoo hidratación y nutrición x 500 ml': 'https://olecapilar.com/products/shampoo-hidratacion-coco-canela-miel',
    'Olé|Shampoo control grasa x 500 ml': 'https://olecapilar.com/products/shampoo-antigrasa-cebolla-jengibre',
    'Olé|Shampoo fortalecimiento y crecimiento x 500 ml': 'https://olecapilar.com/products/shampoo-crecimiento-revitalizante-de-arroz',
    'Olé|Shampoo + Acondicionador control frizz x 500 ml': 'https://olecapilar.com/products/shampoo-acondicionador-capilar-vinagre-de-manzana-control-frizz',
    'Olé|Acondicionador hidratación y crecimiento x 500 ml': 'https://olecapilar.com/products/acondicionador-capilar-proteina-de-arroz-hidratacion-y-crecimiento',
    'Olé|Acondicionador hidratación y suavidad x 500 ml': 'https://olecapilar.com/products/acondicionador-suavidad-algodon-coco',
    'Olé|Acondicionador protección long lasting x 500 ml': 'https://olecapilar.com/products/acondicionador-long-lasting-jarabe-de-mango',
    'Olé|Acondicionador purificante anti-grasa x 500 ml': 'https://olecapilar.com/products/acondicionador-capilar-extracto-natural-de-jengibre-purificante-anti-grasa',
    'Olé|Termoprotector desenredante': 'https://olecapilar.com/products/termoprotector-desenredante-aceite-de-acai',
    'Olé|Óleo capilar de uchuva Hidratante de puntas': 'https://olecapilar.com/products/oleo-capilar-de-uchuva-reparador-de-puntas',
    'Olé|Spray antihumedad - antifrizz': 'https://olecapilar.com/products/spray-anti-humedad-anti-frizz-con-restart-pro',
    'Skin 1004|Madagascar Centella Ampoule Foam Limpiador 125 ml': 'https://www.skin1004.com/products/skin1004-madagascar-centella-ampoule-foam#3',
    'Bioaqua|Kit facial de rosas': 'https://bioaqua.com.co/producto/20713/',
    'Bioaqua|Kit facial de arroz': 'https://bioaqua.com.co/producto/kit-arroz-blanco/',
    'Bioaqua|Kit facial de centella asiática': 'https://bioaqua.com.co/producto/kit-centella-asiatica-2/',
    'Bioaqua|Kit facial de ácido salicílico': 'https://bioaqua.com.co/producto/kit-acido-salicilico/',
    'Bioaqua|Kit facial con retinol': 'https://bioaqua.com.co/producto/kit-facial-retinol-bioaqua/',
    'Bioaqua|Kit facial de ácido hialurónico': 'https://bioaqua.com.co/producto/kit-hidratacion-intensiva/',
    'Bioaqua|Jabón facial - ácido salicílico': 'https://bioaqua.com.co/producto/jabon-facial-de-acido-salicilico/',
    'Bioaqua|Espuma limpiadora de arroz': 'https://bioaqua.com.co/producto/jabon-facial-de-arroz-blanco/',
    'Bioaqua|Serum de vitamina C': 'https://bioaqua.com.co/producto/suero-vc-bioaqua-30-ml/',
    'Bioaqua|Esencia de arroz': 'https://bioaqua.com.co/producto/esencia-de-arroz-y-ha/',
    'Bioaqua|Serum de ácido hialurónico': 'https://bioaqua.com.co/producto/suero-hidratacion-intensiva-ha-bioaqua/',
    'Bioaqua|Serum de retinol': 'https://bioaqua.com.co/producto/suero-retinol-bioaqua/',
    'Bioaqua|Serum pure skin': 'https://bioaqua.com.co/producto/suero-pure-skin/',
    'Bioaqua|Crema hidratante con vitamina C': 'https://bioaqua.com.co/producto/crema-vc-bioaqua/',
    'Bioaqua|Crema hidratante de arroz': 'https://bioaqua.com.co/producto/crema-de-arroz-blanco/',
    'Nude|Protector solar Spf30 40 ml': 'https://nude.com.co/producto/protector-spf30-nude-40ml/',
    'Nude|Autobronceador Doypack 200ml': 'https://nude.com.co/producto/autobronceador-doypack-nude-200ml/',
    'Prosa|Pestañina Profesional Silicon': 'https://www.prosacolombia.com.co/product-page/pesta%C3%B1ina-profesional-silic%C3%B3n',
    'Prosa|Pestañina Maxivolumen': 'https://www.prosacolombia.com.co/product-page/pesta%C3%B1ina-maxi-volumen',
    'Prosa|Pestañina Microfibra': 'https://www.prosacolombia.com.co/product-page/pesta%C3%B1ina-con-micro-fibras-prosa',
    'Prosa|Pestañina Maxivolumen Silicon': 'https://www.prosacolombia.com.co/product-page/pesta%C3%B1ina-maxi-volumen-silic%C3%B3n',
    'Prosa|Pestañina Profesional Silicon - Café': 'https://www.prosacolombia.com.co/product-page/pesta%C3%B1ina-profesional-silic%C3%B3n-caf%C3%A9',
    'Prosa|Pestañina Sensual Love': 'https://www.prosacolombia.com.co/product-page/pesta%C3%B1ina-sensual-love-prosa',
    'Prosa|Pestañina con aceite de mamey': 'https://www.prosacolombia.com.co/product-page/pesta%C3%B1ina-con-aceite-de-mamey-prosa',
    'Prosa|Pestañina con aceite de aguacate': 'https://www.prosacolombia.com.co/product-page/pesta%C3%B1ina-aguacate-prosa',
    'Prosa|Pestañina red passion': 'https://www.prosacolombia.com.co/product-page/pesta%C3%B1ina-red-passion',
    'Prosa|Pestañina maxivolumen Borgoña': 'https://www.prosacolombia.com.co/product-page/maxi-volumen-borgo%C3%B1a',
    'Prosa|Tratamiento en máscara para pestañas y cejas': 'https://www.prosacolombia.com.co/product-page/crystal-protein-gel-prosa',
    'Schwarzkopf|Gel fijador Glued Got2b amarillo': 'https://www.prosacolombia.com.co/product-page/got2b-glued-spiking-gel-water-resistant-35-g',
    'Tocobo|Bloqueador en barra Cotton Soft SPF50': 'https://kalonskinbar.com/products/cotton-soft-sun-stick',
    'Tocobo|Dúo de limpieza': 'https://kalonskinbar.com/products/mini-duo-doble-limpieza-tocobo',
    'Nivea|Crema corporal Nivea reafirmante Q10 + vitamina C x 1000 Ml': 'https://www.nivea.com.co/productos/crema-corporal-reafirmante-q10-(1000ml)-40059004910600057.html',
    'Nivea|Crema corporal Nivea milk nutritiva - Piel Seca x 400 ml': 'https://www.nivea.com.co/productos/crema-corporal-milk-nutritiva-(400ml)-40058083196950057.html',
    'Nivea|Desodorante men Invisible Black & White x 50ml': 'https://www.nivea.com.co/productos/black-and-white-invisible-roll-on-40059000367590057.html',
    'Maybelline|Pestañina Sky High Lavable | A prueba de agua': 'https://www.medipiel.com.co/pestanina-sky-high-negra-lavable-maybelline/p',
    'Maybelline|Pestañina Colossal Lavable | A prueba de agua': 'https://www.medipiel.com.co/pestanina-the-colossal-volum-express-lavable-maybelline/p',
    'Maybelline|Pestañina Surreal Lavable | A prueba de agua': 'https://www.medipiel.com.co/pestanina-falsies-surreal-very-black-lavable-maybelline/p',
    'Garnier|Agua micelar todo en 1 Rosada x 400 ml': 'https://www.cromantic.com/agua-micelar-garnier-1-skinactive-76409/p',
    'Garnier|Agua micelar pure active x 400 ml': 'https://www.exito.com/agua-micelar-pure-active-884326/p',
    "Johnson's|Shampoo - Fuerza y vitamina": 'https://www.exito.com/johnsons-baby-shampoo-fuerza-y-vitamina-x-750-ml-350597/p#2',
    "Johnson's|Baño líquido - Avena": 'https://www.exito.com/johnsons-baby-jab-n-l-quido-avena-x-400-ml-795218/p#2',
    "Johnson's|Baño líquido - Antes de dormir": 'https://www.exito.com/jabon-liquido-antes-de-dormir-865694/p#2',
    'Lehit|Tratamiento aceite de aguacate x30 gr': 'https://tiendalehit.com/products/tratamiento-aceite-de-aguacate',
    'Lehit|Tratamiento complejo biológico con queratina x30gr': 'https://tiendalehit.com/products/tratamiento-complejo-biologico',
    'Lehit|Tratamiento cebolla y jengibre x30 gr': 'https://tiendalehit.com/products/sobre-tratamiento-cebolla',
    'Lehit|Tratamiento capullo de gusano de seda x30gr': 'https://tiendalehit.com/products/tratamiento-gusano-de-seda',
    "Johnson's|Shampoo baby - Cabello oscuro": 'https://www.larebajavirtual.com/champu-bebe-johnson-s-cabello-oscuro-129840/p',
    "Johnson's|Shampoo baby - amarillo": 'https://www.larebajavirtual.com/champu-bebe-johnson-s-original-130677/p',
    'Garnier|Agua micelar todo en 1 Rosada x 100 ml': 'https://www.exito.com/agua-micelar-viajera-31008/p#2',
    "Johnson's|Shampoo baby - Cabello claro": 'https://www.exito.com/johnsons-baby-shampoo-manzanilla-x-200-ml-347355/p#2',
    "Johnson's|Crema líquida baby": 'https://www.exito.com/crema-hidratante-lquida-johnsons-baby-original-x-798-ml-268227/p#2',
    "Johnson's|Crema líquida - Avena": 'https://www.exito.com/johnsons-baby-crema-hidratante-avena-x-800-ml-190550/p#2',
}

# Productos cuyos tonos están publicados como productos separados: la foto de un tono no representa
# al producto completo, así que no se reemplaza automáticamente.
# Fotos oficiales que no sirven para recortar el fondo (se queda la foto del catálogo).
EXCLUDE = {
    # Revisadas por Ágata Beauty: el recorte borraba partes del producto.
    'Montoc|Base Glow Filter': 'el recorte borraba partes del producto',
    'Bloomshell|Trío de Rubores': 'el recorte borraba partes del producto',
    'Bloomshell|Papel matificante Bloom powder paper': 'el recorte borraba partes del producto',
    'Bloomshell|Kit Kiss Love': 'el recorte borraba partes del producto',
    'Majikal|Shiny Lip Oil': 'la foto de la tienda es de ambiente y el recorte borraba partes',
    'Atenea|Paleta de sombras multiusos Moccalush': 'Ágata Beauty prefiere la foto del catálogo',
    'Atenea|Polvo en gel matificante Matterpowder': 'el recorte borraba partes del producto',
    "Johnson's|Crema líquida - Avena": 'la tienda muestra otra versión de la etiqueta',
    'Garnier|Agua micelar con vitamina C x 400 ml': 'las fotos de la tienda traen letreros o una mano; ninguna sirve para quitar el fondo',
    'Lehit|Tratamiento aceite de aguacate x30 gr': 'la foto trae hojas decorativas que quedan sueltas al quitar el fondo',
    'Lehit|Tratamiento cebolla y jengibre x30 gr': 'la foto trae una cebolla decorativa que queda pegada al quitar el fondo',
    "Johnson's|Shampoo baby - Cabello oscuro": 'en la tienda es frasco con tapa; en el catálogo es con dosificador',
    "Johnson's|Shampoo baby - amarillo": 'en la tienda es frasco con tapa; en el catálogo es con dosificador',
    "Johnson's|Baño líquido - Avena": 'la tienda muestra otra versión de la etiqueta',
    "Johnson's|Baño líquido - Antes de dormir": 'la tienda muestra otra versión de la etiqueta',
    'Garnier|Agua micelar pure active x 400 ml': 'todas las fotos de la tienda traen letreros o son de uso (no hay foto limpia del producto)',
    'Prosa|Tratamiento en máscara para pestañas y cejas': 'en el catálogo el tubo es transparente; en la tienda tiene otra etiqueta',
    'Prosa|Pestañina Profesional Silicon - Café': 'en la tienda el tubo es dorado; en el catálogo es café oscuro',
    'Schwarzkopf|Gel fijador Glued Got2b amarillo': 'la tienda muestra otra versión del empaque (letras distintas)',
    'Bioaqua|Kit facial de rosas': 'la foto de la tienda trae el aviso "Envío Gratis" y un producto de regalo',
    'Bioaqua|Kit facial de arroz': 'la foto de la tienda trae el aviso "Envío Gratis" y un producto de regalo',
    'Bioaqua|Kit facial de centella asiática': 'la foto de la tienda trae el aviso "Envío Gratis" y un producto de regalo',
    'Bioaqua|Kit facial de ácido salicílico': 'la foto de la tienda trae el aviso "Envío Gratis" y un producto de regalo',
    'Bioaqua|Kit facial de ácido hialurónico': 'la foto de la tienda trae el aviso "Envío Gratis" y un producto de regalo',
    'Bioaqua|Kit facial con retinol': 'la foto de la tienda trae el aviso "Envío Gratis" y un producto de regalo',
    'Bioaqua|Espuma limpiadora de arroz': 'en la tienda es un tubo; en el catálogo es un frasco con cepillo',
    'Anyeluz|Tratamiento reparación, restauración y brillo - línea profesional': 'frasco blanco sobre fondo blanco: el recorte se come partes del frasco',
    'Olé|Shampoo hidratación y nutrición x 500 ml': 'el color del frasco en la tienda no coincide con el del catálogo',
    'Olé|Spray antihumedad - antifrizz': 'la etiqueta de la tienda es distinta a la del catálogo',
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
    url, _, n = url.partition('#')
    n = int(n or 1) - 1
    parts = urlsplit(url)
    if '/products/' in parts.path:                                  # Shopify
        images = shades.shopify_json(url).get('images', [])
        return images[n]['src'].split('?')[0] if len(images) > n else None
    if parts.netloc.endswith('samycosmetics.com') or parts.path.endswith('/p'):   # VTEX
        try:
            found = json.loads(shades.get(f"{parts.scheme}://{parts.netloc}/api/catalog_system/pub/products/search{parts.path.rstrip('/')}"))
        except Exception:
            found = None                                            # algunas tiendas cierran la API: se usa og:image
        items = found[0].get('items', []) if found else []
        if items and len(items[0].get('images') or []) > n:
            return items[0]['images'][n]['imageUrl']
    page = shades.get(url).decode('utf-8', 'replace')               # WooCommerce y otras
    if n:                                                           # foto N de la página (og:image en orden)
        found = re.findall(r'<meta property="og:image" content="([^"]+)"', page)
        return found[n] if len(found) > n else None
    m = (re.search(r'data-large_image="([^"]+)"', page)
         or re.search(r'"image":\["([^"]+)"', page)                  # datos estructurados (Nivea)
         or re.search(r'<meta property="og:image" content="([^"]+)"', page))
    if not m:
        return None
    return re.sub(r'(wixstatic\.com/media/[^/]+)/v1/.*', r'\1', m.group(1))   # Wix: foto original, sin reducir


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
