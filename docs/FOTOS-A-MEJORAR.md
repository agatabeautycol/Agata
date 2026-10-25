# Fotos del catálogo que deben mejorar

De los 249 productos, **171 ya tienen foto en alta resolución** (página oficial) y **78 siguen con la foto del PDF de Canva**, que se subió en baja resolución. Este archivo lo genera `scripts/photo-report.py`.

- **Tamaño:** la ficha muestra la foto a 320 px y en celulares necesita unos **640 px** (ideal: 800 px). Las fotos del PDF miden entre 160 y 600 px, a su resolución real (sin ampliar).
- **Nitidez:** se midió el detalle de cada foto; las borrosas o con "cuadritos" de compresión van primero.

| Prioridad | Qué significa | Fotos |
| --- | --- | ---: |
| **Alta** | Borrosa o con compresión visible: se nota aun en las tarjetas | 15 |
| **Media** | Pequeña (menos de 400 px): se ve suave en la ficha | 60 |
| **Baja** | Algo más grande o nítida, pero aún por debajo de 640 px | 3 |

## Qué se necesita

1. **Las fotos originales** (las que se subieron a Canva), nombradas con el ID del producto, o
2. **El enlace a la página oficial de cada producto** (se agrega en `PHOTO_PAGES` de `scripts/fetch-product-photos.py`).

## Resumen por marca

| Marca | Pendientes | Alta | Media | Baja | Tienda que ya se puede leer |
| --- | ---: | ---: | ---: | ---: | --- |
| Montoc | 4 | 2 | 1 | 1 | montoccosmetictools.com |
| Bloomshell | 12 | 4 | 8 | 0 | bloomshell.co |
| Girly | 1 | 1 | 0 | 0 | cocopinkstore.com (revendedor) |
| Majikal | 1 | 0 | 1 | 0 | majikalbeauty.com |
| Prosa | 3 | 0 | 2 | 1 | — |
| Samy | 2 | 0 | 2 | 0 | samycosmetics.com |
| Raquel | 1 | 0 | 1 | 0 | losestilistas.com.co (revendedor) |
| OG | 2 | 2 | 0 | 0 | ogmantra.co |
| Schwarzkopf | 2 | 0 | 2 | 0 | — |
| Skin 1004 | 1 | 1 | 0 | 0 | — |
| Bioaqua | 15 | 1 | 14 | 0 | — |
| Garnier | 3 | 0 | 3 | 0 | — |
| Milagros | 2 | 1 | 1 | 0 | milagrosbeauty.com |
| Anyeluz | 1 | 0 | 1 | 0 | — |
| Lehit | 2 | 0 | 2 | 0 | — |
| Leche pal pelo | 4 | 0 | 4 | 0 | — |
| Olé | 2 | 1 | 1 | 0 | — |
| Johnson's | 7 | 1 | 6 | 0 | — |
| Nivea | 6 | 1 | 5 | 0 | — |
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

### Majikal

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `majikal-029-1` | Polvos sueltos - 4 tonos | 29 | 319 px | Media | — |

### Prosa

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `prosa-045-1` | Pestañina Profesional Silicon - Café | 45 | 303 px | Media | — |
| `prosa-047-2` | Aceite para pestañas | 47 | 199 px | Media | — |
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

### Skin 1004

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `skin-1004-068-2` | Centella Poremizing Deep Cleansing Foam Limpiador 125 ml | 68 | 220 px | Alta | — |

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
| `bioaqua-074-1` | Tónico de vitamina C | 74 | 297 px | Media | — |
| `bioaqua-074-2` | Tónico de centella asiática | 74 | 207 px | Media | — |
| `bioaqua-075-1` | Tónico de arroz | 75 | 267 px | Media | — |
| `bioaqua-075-2` | Tónico de ácido hialurónico | 75 | 258 px | Media | — |
| `bioaqua-076-2` | Serum de centella asiática | 76 | 199 px | Media | — |
| `bioaqua-079-2` | Crema hidratante con centella asiática | 79 | 234 px | Media | — |
| `bioaqua-080-2` | Crema hidratante con ácido hialurónico | 80 | 220 px | Media | — |

### Garnier

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
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
| `anyeluz-098-2` | Tratamiento reparación, restauración y brillo - línea profesional | 98 | 324 px | Media | — |

### Lehit

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `lehit-100-1` | Tratamiento aceite de aguacate x30 gr | 100 | 273 px | Media | — |
| `lehit-101-1` | Tratamiento cebolla y jengibre x30 gr | 101 | 276 px | Media | — |

### Leche pal pelo

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `leche-pal-pelo-108-1` | Mascarilla Regenerador Intenso 7 Oleos x 40 ml | 108 | 288 px | Media | — |
| `leche-pal-pelo-108-2` | Mascarilla WOW x 40 ml | 108 | 360 px | Media | — |
| `leche-pal-pelo-112-1` | Tratamiento capilar reconstructor instantáneo x 30 ml | 112 | 261 px | Media | — |
| `leche-pal-pelo-112-2` | Termoprotector tradicional x 30 ml | 112 | 220 px | Media | — |

### Olé

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `ole-113-2` | Shampoo hidratación y nutrición x 500 ml | 113 | 237 px | Alta | — |
| `ole-118-2` | Spray antihumedad - antifrizz | 118 | 273 px | Media | — |

### Johnson's

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `johnsons-122-2` | Baño líquido - Antes de dormir | 122 | 273 px | Alta | — |
| `johnsons-120-1` | Shampoo baby - Cabello oscuro | 120 | 234 px | Media | — |
| `johnsons-120-2` | Shampoo baby - Cabello claro | 120 | 282 px | Media | — |
| `johnsons-121-2` | Shampoo baby - amarillo | 121 | 279 px | Media | — |
| `johnsons-122-1` | Baño líquido - Avena | 122 | 273 px | Media | — |
| `johnsons-123-1` | Crema líquida baby | 123 | 246 px | Media | — |
| `johnsons-123-2` | Crema líquida - Avena | 123 | 282 px | Media | — |

### Nivea

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `nivea-125-1` | Crema Nivea Corporal Reafirmante Q10 Creatina x 400 ml | 125 | 283 px | Alta | — |
| `nivea-124-1` | Crema hidratante | 124 | 306 px | Media | — |
| `nivea-126-1` | Desodorante aclarado natural Classic Touch x 50ml | 126 | 264 px | Media | — |
| `nivea-126-2` | Desodorante tono natural mujer satín spray x 150 ml | 126 | 306 px | Media | — |
| `nivea-127-2` | Desodorante dama Invisible Black & White x 50ml | 127 | 327 px | Media | — |
| `nivea-128-1` | Lip care - 24 horas de humectación | 128 | 345 px | Media | — |

### Chap Stick

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `chap-stick-129-1` | Protector labial | 129 | 333 px | Media | sí |

### Fantiluna

| ID | Producto | Pág. | Tamaño | Prioridad | Enlace |
| --- | --- | ---: | ---: | --- | --- |
| `fantiluna-130-1` | Mantequilla corporal x 220 ml | 130 | 345 px | Media | sí |
| `fantiluna-130-2` | Exfoliante corporal x 220ml | 130 | 267 px | Media | sí |
| `fantiluna-131-2` | Splash corporal x 105 ml | 131 | 375 px | Media | sí |
| `fantiluna-132-1` | Iluminador corporal x 160 ml | 132 | 300 px | Media | sí |
| `fantiluna-132-2` | Crema corporal | 132 | 276 px | Media | sí |
| `fantiluna-131-1` | Splash corporal x 250 ml | 131 | 443 px | Baja | sí |

