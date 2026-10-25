# Fotos del catálogo que deben mejorar

De los 249 productos, **98 ya tienen foto en alta resolución** (página oficial) y **151 siguen con la foto del PDF de Canva**, que se subió en baja resolución. Este archivo lo genera `scripts/photo-report.py`.

- **Tamaño:** la ficha muestra la foto a 320 px y en celulares necesita unos **640 px** (ideal: 800 px). Las fotos del PDF miden entre 160 y 600 px, a su resolución real (sin ampliar).
- **Nitidez:** se midió el detalle de cada foto; las borrosas o con "cuadritos" de compresión van primero.

| Prioridad | Qué significa | Fotos |
| --- | --- | ---: |
| **Alta** | Borrosa o con compresión visible: se nota aun en las tarjetas | 29 |
| **Media** | Pequeña (menos de 400 px): se ve suave en la ficha | 110 |
| **Baja** | Algo más grande o nítida, pero aún por debajo de 640 px | 12 |

## Qué se necesita

1. **Las fotos originales** (las que se subieron a Canva), nombradas con el ID del producto, o
2. **El enlace a la página oficial de cada producto** (se agrega en `PHOTO_PAGES` de `scripts/fetch-product-photos.py`).

## Resumen por marca

| Marca | Pendientes | Alta | Media | Baja | Tienda que ya se puede leer |
| --- | ---: | ---: | ---: | ---: | --- |
| Montoc | 4 | 2 | 1 | 1 | montoccosmetictools.com |
| Bloomshell | 12 | 4 | 8 | 0 | bloomshell.co |
| Girly | 1 | 1 | 0 | 0 | cocopinkstore.com (revendedor) |
| Maybelline | 3 | 0 | 2 | 1 | — |
| Majikal | 1 | 0 | 1 | 0 | majikalbeauty.com |
| Prosa | 12 | 2 | 9 | 1 | — |
| Samy | 2 | 0 | 2 | 0 | samycosmetics.com |
| Raquel | 1 | 0 | 1 | 0 | losestilistas.com.co (revendedor) |
| OG | 2 | 2 | 0 | 0 | ogmantra.co |
| Schwarzkopf | 2 | 0 | 2 | 0 | — |
| Tocobo | 2 | 1 | 1 | 0 | — |
| Skin 1004 | 2 | 1 | 1 | 0 | — |
| Bioaqua | 23 | 1 | 22 | 0 | — |
| Garnier | 4 | 0 | 4 | 0 | — |
| Milagros | 2 | 1 | 1 | 0 | milagrosbeauty.com |
| Anyeluz | 14 | 0 | 6 | 8 | — |
| Lehit | 4 | 0 | 4 | 0 | — |
| Leche pal pelo | 22 | 2 | 20 | 0 | — |
| Olé | 12 | 9 | 3 | 0 | — |
| Nude | 2 | 0 | 2 | 0 | — |
| Johnson's | 8 | 1 | 7 | 0 | — |
| Nivea | 9 | 2 | 7 | 0 | — |
| Chap Stick | 1 | 0 | 1 | 0 | — |
| Fantiluna | 6 | 0 | 5 | 1 | fantiluna.com |

## Lista de pendientes

"Enlace" indica si ya hay página oficial del producto (la de sus tonos).

### Montoc

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `montoc-003-2` | Polvos Translúcidos | 3 | 315 px | Alta | — |
| `montoc-009-1` | Set de Borlas | 9 | 339 px | Alta | — |
| `montoc-008-1` | Fijador de maquillaje Dixy Fix | 8 | 258 px | Media | — |
| `montoc-009-2` | Kit de brochas de maquillaje Fluffy x 10 | 9 | 429 px | Baja | sí |

### Bloomshell

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `bloomshell-011-1` | Base líquida 2 en 1 My foundation | 11 | 327 px | Alta | sí |
| `bloomshell-012-2` | Polvos sueltos 4 tonos | 12 | 267 px | Alta | — |
| `bloomshell-016-1` | Llavero Mimosa Tinta + Gloss | 16 | 217 px | Alta | — |
| `bloomshell-017-2` | Papel matificante Bloom Oil Stop | 17 | 312 px | Alta | — |
| `bloomshell-011-2` | Corrector My concealer | 11 | 318 px | Media | sí |
| `bloomshell-012-1` | Polvos sueltos | 12 | 294 px | Media | — |
| `bloomshell-014-2` | Iluminador Bloom Dazlee | 14 | 243 px | Media | — |
| `bloomshell-015-1` | Laminador de cejas | 15 | 330 px | Media | — |
| `bloomshell-015-2` | Paleta de sombras Bloom Vibes | 15 | 300 px | Media | — |
| `bloomshell-016-2` | Brillo labial - Bombón | 16 | 267 px | Media | — |
| `bloomshell-019-1` | Bloom Termo | 19 | 271 px | Media | — |
| `bloomshell-019-2` | Bloom porta cosméticos | 19 | 261 px | Media | — |

### Girly

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `girly-022-3` | Polvo suelto | 22 | 226 px | Alta | — |

### Maybelline

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `maybelline-023-1` | Pestañina Sky High Lavable | A prueba de agua | 23 | 287 px | Media | — |
| `maybelline-023-3` | Pestañina Surreal Lavable | A prueba de agua | 23 | 234 px | Media | — |
| `maybelline-023-2` | Pestañina Colossal Lavable | A prueba de agua | 23 | 582 px | Baja | — |

### Majikal

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `majikal-029-1` | Polvos sueltos - 4 tonos | 29 | 319 px | Media | — |

### Prosa

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `prosa-043-1` | Pestañina Profesional Silicon | 43 | 204 px | Alta | — |
| `prosa-044-2` | Pestañina Maxivolumen Silicon | 44 | 199 px | Alta | — |
| `prosa-043-2` | Pestañina Maxivolumen | 43 | 321 px | Media | — |
| `prosa-044-1` | Pestañina Microfibra | 44 | 297 px | Media | — |
| `prosa-045-1` | Pestañina Profesional Silicon - Café | 45 | 303 px | Media | — |
| `prosa-045-2` | Pestañina Sensual Love | 45 | 247 px | Media | — |
| `prosa-046-1` | Pestañina con aceite de mamey | 46 | 208 px | Media | — |
| `prosa-046-2` | Pestañina con aceite de aguacate | 46 | 252 px | Media | — |
| `prosa-047-1` | Pestañina red passion | 47 | 234 px | Media | — |
| `prosa-047-2` | Aceite para pestañas | 47 | 199 px | Media | — |
| `prosa-048-1` | Pestañina maxivolumen Borgoña | 48 | 312 px | Media | — |
| `prosa-048-2` | Tratamiento en máscara para pestañas y cejas | 48 | 596 px | Baja | — |

### Samy

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `samy-049-1` | Polvo suelto | 49 | 348 px | Media | sí |
| `samy-053-2` | Paleta de sombras x9 | 53 | 366 px | Media | sí |

### Raquel

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `raquel-062-1` | Polvo suelto traslúcido mate minerals con avena y trigo | 62 | 255 px | Media | sí |

### OG

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `og-065-1` | Gloss and lip Dreamy | 65 | 217 px | Alta | — |
| `og-065-2` | Brillo labial Yess Queen | 65 | 207 px | Alta | — |

### Schwarzkopf

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `schwarzkopf-066-1` | Gel fijador Glued Got2b amarillo | 66 | 192 px | Media | — |
| `schwarzkopf-066-2` | Gel para cejas Got2b amarillo | 66 | 247 px | Media | — |

### Tocobo

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `tocobo-067-1` | Bloqueador en barra Cotton Soft SPF50 | 67 | 222 px | Alta | — |
| `tocobo-067-2` | Dúo de limpieza | 67 | 192 px | Media | — |

### Skin 1004

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `skin-1004-068-2` | Centella Poremizing Deep Cleansing Foam Limpiador 125 ml | 68 | 220 px | Alta | — |
| `skin-1004-068-1` | Madagascar Centella Ampoule Foam Limpiador 125 ml | 68 | 234 px | Media | — |

### Bioaqua

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `bioaqua-073-2` | Espuma limpiadora de arroz | 73 | 288 px | Alta | — |
| `bioaqua-069-1` | Kit facial de rosas | 69 | 273 px | Media | — |
| `bioaqua-069-2` | Kit facial de arroz | 69 | 282 px | Media | — |
| `bioaqua-070-1` | Kit facial de centella asiática | 70 | 273 px | Media | — |
| `bioaqua-070-2` | Kit facial de ácido salicílico | 70 | 300 px | Media | — |
| `bioaqua-071-1` | Kit facial con retinol | 71 | 285 px | Media | — |
| `bioaqua-071-2` | Kit facial de ácido hialurónico | 71 | 273 px | Media | — |
| `bioaqua-072-1` | Mascarilla facial en velo | 72 | 360 px | Media | — |
| `bioaqua-073-1` | Jabón facial - ácido salicílico | 73 | 249 px | Media | — |
| `bioaqua-074-1` | Tónico de vitamina C | 74 | 297 px | Media | — |
| `bioaqua-074-2` | Tónico de centella asiática | 74 | 207 px | Media | — |
| `bioaqua-075-1` | Tónico de arroz | 75 | 267 px | Media | — |
| `bioaqua-075-2` | Tónico de ácido hialurónico | 75 | 258 px | Media | — |
| `bioaqua-076-1` | Serum de vitamina C | 76 | 246 px | Media | — |
| `bioaqua-076-2` | Serum de centella asiática | 76 | 199 px | Media | — |
| `bioaqua-077-1` | Esencia de arroz | 77 | 283 px | Media | — |
| `bioaqua-077-2` | Serum de ácido hialurónico | 77 | 243 px | Media | — |
| `bioaqua-078-1` | Serum de retinol | 78 | 258 px | Media | — |
| `bioaqua-078-2` | Serum pure skin | 78 | 183 px | Media | — |
| `bioaqua-079-1` | Crema hidratante con vitamina C | 79 | 246 px | Media | — |
| `bioaqua-079-2` | Crema hidratante con centella asiática | 79 | 234 px | Media | — |
| `bioaqua-080-1` | Crema hidratante de arroz | 80 | 273 px | Media | — |
| `bioaqua-080-2` | Crema hidratante con ácido hialurónico | 80 | 220 px | Media | — |

### Garnier

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `garnier-081-1` | Agua micelar todo en 1 Rosada x 400 ml | 81 | 256 px | Media | — |
| `garnier-081-2` | Agua micelar todo en 1 Rosada x 100 ml | 81 | 261 px | Media | — |
| `garnier-082-1` | Agua micelar pure active x 400 ml | 82 | 252 px | Media | — |
| `garnier-082-2` | Agua micelar con vitamina C x 400 ml | 82 | 312 px | Media | — |

### Milagros

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `milagros-092-1` | Perfume capilar y corporal | 92 | 273 px | Alta | sí |
| `milagros-088-2` | Doypack tratamiento capilar a base de frutas x100 ml | 88 | 276 px | Media | — |

### Anyeluz

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `anyeluz-096-1` | Shampoo con aloe vera x 500 ml | 96 | 381 px | Media | — |
| `anyeluz-096-2` | Acondicionador con argán y aloe vera x 500 ml | 96 | 396 px | Media | — |
| `anyeluz-097-1` | Shampoo liso en casa x 800 ml - línea profesional | 97 | 390 px | Media | — |
| `anyeluz-098-2` | Tratamiento reparación, restauración y brillo - línea profesional | 98 | 324 px | Media | — |
| `anyeluz-099-1` | Tratamiento capilar de crecimiento | 99 | 285 px | Media | — |
| `anyeluz-099-2` | Tratamiento con romero y bioelixir | 99 | 372 px | Media | — |
| `anyeluz-093-1` | Shampoo de cebolla x 500 ml | 93 | 452 px | Baja | — |
| `anyeluz-093-2` | Acondicionador de cebolla x 500 ml | 93 | 446 px | Baja | — |
| `anyeluz-094-1` | Shampoo con romero x 500 ml | 94 | 408 px | Baja | — |
| `anyeluz-094-2` | Acondicionador con romero x 500 ml | 94 | 423 px | Baja | — |
| `anyeluz-095-1` | Shampoo con ginseng x 500 ml | 95 | 429 px | Baja | — |
| `anyeluz-095-2` | Acondicionador con ginseng x 500 ml | 95 | 405 px | Baja | — |
| `anyeluz-097-2` | Acondicionador liso en casa x 800 ml - línea profesional | 97 | 440 px | Baja | — |
| `anyeluz-098-1` | Tratamiento liso en casa - línea profesional | 98 | 405 px | Baja | — |

### Lehit

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `lehit-100-1` | Tratamiento aceite de aguacate x30 gr | 100 | 273 px | Media | — |
| `lehit-100-2` | Tratamiento complejo biológico con queratina x30gr | 100 | 339 px | Media | — |
| `lehit-101-1` | Tratamiento cebolla y jengibre x30 gr | 101 | 276 px | Media | — |
| `lehit-101-2` | Tratamiento capullo de gusano de seda x30gr | 101 | 390 px | Media | — |

### Leche pal pelo

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `leche-pal-pelo-102-2` | Shampoo Protección Plus x 440 ml | 102 | 267 px | Alta | — |
| `leche-pal-pelo-106-2` | Mascarilla hidrosellante x 440 ml | 106 | 270 px | Alta | — |
| `leche-pal-pelo-102-1` | Shampoo tradicional x 440 ml | 102 | 276 px | Media | — |
| `leche-pal-pelo-103-1` | Shampoo especializado x 440 ml | 103 | 273 px | Media | — |
| `leche-pal-pelo-103-2` | Shampoo nutritivo para niños x 440 ml | 103 | 270 px | Media | — |
| `leche-pal-pelo-104-1` | Shampoo + Acondicionador para niños x 440 ml | 104 | 261 px | Media | — |
| `leche-pal-pelo-104-2` | Shampoo hidratante rizos para niños x 440 ml | 104 | 273 px | Media | — |
| `leche-pal-pelo-105-1` | Acondicionador para niños x 440 ml | 105 | 271 px | Media | — |
| `leche-pal-pelo-105-2` | Acondicionador Co-wash rizos y afro x 440 ml | 105 | 267 px | Media | — |
| `leche-pal-pelo-106-1` | Mascarilla nutritiva rizos y ondas x 440 ml | 106 | 276 px | Media | — |
| `leche-pal-pelo-107-1` | Mascarilla Regenerador Intenso 7 Oleos x 800 ml | 107 | 283 px | Media | — |
| `leche-pal-pelo-107-2` | Mascarilla WOW x 800 ml | 107 | 285 px | Media | — |
| `leche-pal-pelo-108-1` | Mascarilla Regenerador Intenso 7 Oleos x 40 ml | 108 | 288 px | Media | — |
| `leche-pal-pelo-108-2` | Mascarilla WOW x 40 ml | 108 | 360 px | Media | — |
| `leche-pal-pelo-109-1` | Termoprotector líquido X 250 ml | 109 | 309 px | Media | — |
| `leche-pal-pelo-109-2` | Termoprotector tradicional x 440 ml | 109 | 276 px | Media | — |
| `leche-pal-pelo-110-1` | Termoprotector protección plus x 440 ml | 110 | 285 px | Media | — |
| `leche-pal-pelo-110-2` | Termoprotector rizos y ondas x 440 ml | 110 | 282 px | Media | — |
| `leche-pal-pelo-111-1` | Gelatina slime definidora x 600 ml | 111 | 283 px | Media | — |
| `leche-pal-pelo-111-2` | Definidor de rizos y ondas x 440 ml | 111 | 291 px | Media | — |
| `leche-pal-pelo-112-1` | Tratamiento capilar reconstructor instantáneo x 30 ml | 112 | 261 px | Media | — |
| `leche-pal-pelo-112-2` | Termoprotector tradicional x 30 ml | 112 | 220 px | Media | — |

### Olé

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `ole-113-2` | Shampoo hidratación y nutrición x 500 ml | 113 | 237 px | Alta | — |
| `ole-114-1` | Shampoo control grasa x 500 ml | 114 | 240 px | Alta | — |
| `ole-115-1` | Shampoo + Acondicionador control frizz x 500 ml | 115 | 303 px | Alta | — |
| `ole-115-2` | Acondicionador hidratación y crecimiento x 500 ml | 115 | 273 px | Alta | — |
| `ole-116-1` | Acondicionador hidratación y suavidad x 500 ml | 116 | 306 px | Alta | — |
| `ole-116-2` | Acondicionador protección long lasting x 500 ml | 116 | 312 px | Alta | — |
| `ole-117-1` | Acondicionador purificante anti-grasa x 500 ml | 117 | 357 px | Alta | — |
| `ole-117-2` | Termoprotector desenredante | 117 | 276 px | Alta | — |
| `ole-118-1` | Óleo capilar de uchuva Hidratante de puntas | 118 | 249 px | Alta | — |
| `ole-113-1` | Shampoo protección y reparación x 500 ml | 113 | 249 px | Media | — |
| `ole-114-2` | Shampoo fortalecimiento y crecimiento x 500 ml | 114 | 300 px | Media | — |
| `ole-118-2` | Spray antihumedad - antifrizz | 118 | 273 px | Media | — |

### Nude

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `nude-119-1` | Protector solar Spf30 40 ml | 119 | 249 px | Media | — |
| `nude-119-2` | Autobronceador Doypack 200ml | 119 | 249 px | Media | — |

### Johnson's

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `johnsons-122-2` | Baño líquido - Antes de dormir | 122 | 273 px | Alta | — |
| `johnsons-120-1` | Shampoo baby - Cabello oscuro | 120 | 234 px | Media | — |
| `johnsons-120-2` | Shampoo baby - Cabello claro | 120 | 282 px | Media | — |
| `johnsons-121-1` | Shampoo - Fuerza y vitamina | 121 | 273 px | Media | — |
| `johnsons-121-2` | Shampoo baby - amarillo | 121 | 279 px | Media | — |
| `johnsons-122-1` | Baño líquido - Avena | 122 | 273 px | Media | — |
| `johnsons-123-1` | Crema líquida baby | 123 | 246 px | Media | — |
| `johnsons-123-2` | Crema líquida - Avena | 123 | 282 px | Media | — |

### Nivea

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `nivea-124-2` | Crema corporal Nivea reafirmante Q10 + vitamina C x 1000 Ml | 124 | 249 px | Alta | — |
| `nivea-125-1` | Crema Nivea Corporal Reafirmante Q10 Creatina x 400 ml | 125 | 283 px | Alta | — |
| `nivea-124-1` | Crema hidratante | 124 | 306 px | Media | — |
| `nivea-125-2` | Crema corporal Nivea milk nutritiva - Piel Seca x 400 ml | 125 | 264 px | Media | — |
| `nivea-126-1` | Desodorante aclarado natural Classic Touch x 50ml | 126 | 264 px | Media | — |
| `nivea-126-2` | Desodorante tono natural mujer satín spray x 150 ml | 126 | 306 px | Media | — |
| `nivea-127-1` | Desodorante men Invisible Black & White x 50ml | 127 | 271 px | Media | — |
| `nivea-127-2` | Desodorante dama Invisible Black & White x 50ml | 127 | 327 px | Media | — |
| `nivea-128-1` | Lip care - 24 horas de humectación | 128 | 345 px | Media | — |

### Chap Stick

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `chap-stick-129-1` | Protector labial | 129 | 333 px | Media | — |

### Fantiluna

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `fantiluna-130-1` | Mantequilla corporal x 220 ml | 130 | 345 px | Media | sí |
| `fantiluna-130-2` | Exfoliante corporal x 220ml | 130 | 267 px | Media | sí |
| `fantiluna-131-2` | Splash corporal x 105 ml | 131 | 375 px | Media | sí |
| `fantiluna-132-1` | Iluminador corporal x 160 ml | 132 | 300 px | Media | sí |
| `fantiluna-132-2` | Crema corporal | 132 | 276 px | Media | sí |
| `fantiluna-131-1` | Splash corporal x 250 ml | 131 | 443 px | Baja | sí |

