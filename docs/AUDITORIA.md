# Auditoría del catálogo — Ágata Beauty 2026

**Fuente:** diseño de Canva "1. Catálogo AGATA Beauty" (`DAHVCDkKSQY`, 133 páginas A4), exportado con el conector de Canva como PDF de máxima calidad ("pro", ~345 MB). Todo lo de este documento sale de ese PDF y del texto leído directamente en Canva.

> La versión anterior del proyecto (CaterineR/Agata) se hizo con un PDF de 121 páginas. Este documento la reemplaza.

## Fase 1 — Diagnóstico

### Estructura

| Páginas | Contenido |
| --- | --- |
| 1 | Portada: logo **ÁGATA beauty**, "Makeup • Skincare • Selfcare", "Catálogo 2026", Instagram **@agatabeauty_**, WhatsApp **3135496268**, lema "Belleza que nace del amor" |
| 2 | **Proceso de compra**: 5 pasos (Elige tus favoritos, Escríbenos, ¿No encuentras lo que buscas?, Confirmamos tu pedido, Realiza tu pago: transferencia o efectivo) y aviso **IMPORTANTE** de disponibilidad |
| 3 – 132 | Productos: una marca por página, con título de marca, sección y 1 a 3 tarjetas |
| 133 | Contraportada sin contenido |

### Productos: 249, de 27 marcas

| Marca | Productos | Páginas |
| --- | ---: | --- |
| Montoc | 15 | 3–10 |
| Bloomshell | 20 | 11–21 |
| Girly | 3 | 22 |
| Maybelline | 3 | 23 |
| Ani-k | 9 | 24–28 |
| Majikal | 3 | 29 |
| Atenea | 23 | 30–42 |
| Prosa | 12 | 43–48 |
| Samy | 12 | 49–54 |
| Lula | 12 | 55–61 |
| Raquel | 1 | 62 |
| OG | 6 | 63–65 |
| Schwarzkopf | 2 | 66 |
| Tocobo | 2 | 67 |
| Skin 1004 | 2 | 68 |
| Bioaqua | 23 | 69–80 |
| Garnier | 4 | 81–82 |
| Milagros | 19 | 83–92 |
| Anyeluz | 14 | 93–99 |
| Lehit | 4 | 100–101 |
| Leche pal pelo | 22 | 102–112 |
| Olé | 12 | 113–118 |
| Nude | 2 | 119 |
| Johnson's | 8 | 120–123 |
| Nivea | 9 | 124–128 |
| Chap Stick | 1 | 129 |
| Fantiluna | 6 | 130–132 |

### Cambios frente a la versión anterior (121 páginas, 225 productos)

| Cambio | Detalle |
| --- | --- |
| Marca nueva **Anyeluz** (pp. 93–99) | 14 productos de cuidado capilar |
| Marca nueva **Johnson's** (pp. 120–123) | 8 productos: 4 shampoos (Cuidado capilar) y 4 baños/cremas líquidas (Cuidado corporal), casi todos con precio por tamaño |
| Producto nuevo | Atenea — Paleta de sombras multiusos Moccalush, $140.500 (p. 34) |
| Producto nuevo | Prosa — Pestañina maxivolumen Borgoña, $21.500 (p. 48) |
| Precio cambiado | Prosa — Aceite para pestañas: $21.500 → **$22.000** (p. 47) |
| Precio cambiado | Prosa — Tratamiento en máscara para pestañas y cejas: $20.500 → **$21.000** (p. 48) |
| Foto corregida en Canva | Bloomshell — Contorno en barra Bloom define (p. 14) ya tiene su propia foto |
| Productos eliminados | Ninguno |

Desde la p. 34 los números de página se corrieron (+1) y desde la p. 92 (+8); los `id` de los productos siguen la página actual.

### Categorías unificadas

El catálogo organiza cada página por **marca** y, debajo, por **sección**, pero repite secciones con nombres distintos ("Ojos", "Cejas", "Cejas y ojos", "Ojos y cejas"…) y 28 productos no tienen sección. Se unificaron en **8 categorías** (aprobadas por Ágata Beauty). La sección original se conserva en el campo `section`; las reglas están en `CATEGORY_MAP`, `CATEGORY_BY_PRODUCT` y `CATEGORY_BY_BRAND` de `scripts/extract-catalog.py`.

| Categoría en la web | Productos | Secciones del catálogo que agrupa |
| --- | ---: | --- |
| Rostro | 40 | (sin sección), Rostro |
| Ojos y cejas | 36 | (sin sección), Cejas, Cejas y ojos, Gel fijador, Multiusos, Ojos, Ojos y cejas |
| Labios | 16 | (sin sección), Labios |
| Preparación y fijación | 5 | Fijación, Papel matificante, Primer |
| Brochas, accesorios y kits | 17 | Accesorios, Herramientas, Kit |
| Cuidado facial | 40 | (sin sección), Cuidado facial, Rostro |
| Cuidado capilar | 76 | Cuidado capilar, Gel fijador |
| Cuidado corporal | 19 | (sin sección), Cuidado corporal |

Asignaciones por producto (sin sección o con sección mixta), confirmadas por Ágata Beauty:

- **Majikal Magic Pen** → Labios · **Nude Protector solar** → Cuidado facial · **Bioaqua Mascarilla facial en velo** → Cuidado facial · **Atenea Paleta multiusos Moccalush** → Ojos y cejas.
- Girly: Gel hidratante → Cuidado facial, TINT → Labios, Polvo suelto → Rostro · Majikal Polvos sueltos → Rostro, Shiny Lip Oil → Labios.
- Schwarzkopf Got2b: Gel fijador Glued → Cuidado capilar, Gel para cejas → Ojos y cejas · Nude Autobronceador → Cuidado corporal.
- Maybelline y Ani-k (pestañinas, delineador) → Ojos y cejas · Nivea (cremas, desodorantes) y Fantiluna → Cuidado corporal.
- Anyeluz → Cuidado capilar · Johnson's según la sección de cada página (Cuidado capilar / Cuidado corporal).

### Datos disponibles por producto

| Dato | Disponible |
| --- | --- |
| Nombre, marca, precio | 249 / 249 |
| Sección en el catálogo | 221 / 249 (categoría en la web: 249 / 249) |
| Precios por tamaño, tono o versión | 27 productos |
| Descripción | 14 productos |
| Fotos de tonos / variantes | 58 productos |
| Referencia / código | **No existe** en el catálogo `[INFORMACIÓN PENDIENTE]` |
| Ofertas | **No existen** (el menú "Ofertas" queda oculto) |

### Identidad visual (medida sobre el PDF)

| Uso | Color |
| --- | --- |
| Fondo crema de las páginas | `#fdf3eb` / `#fcf3ec` |
| "ÁGATA" del logo | `#643011` |
| Textos de contacto / etiquetas | `#592510` |
| Sección ("Cuidado capilar", "Rostro"…) | `#764b36` |
| Títulos de marca | degradado marrón → cobre `#3c130d → #d08a72` |
| Anillo del círculo | degradado `#65312a → #bf6e58` |
| Disco detrás del producto | `#ddd7c9` |
| Estrellas y adornos de línea | `#db9d6a` / `#bf8a78` |
| Nombres y precios | negro |

| Uso | Fuente del catálogo | En la web |
| --- | --- | --- |
| "ÁGATA" | Cormorant Garamond Bold | la misma (Google Fonts) |
| "beauty" | Dancing Script Bold | la misma (Google Fonts) |
| Títulos de marca | The Seasons Bold | Cormorant Garamond (The Seasons tiene licencia de Canva) |
| Secciones | Mont Bold | Poppins |
| Nombres y precios | Garet Bold / Regular | Poppins |
| Proceso de compra | Poppins | la misma |
| Contacto de la portada | Codec Pro | Poppins |

Elementos que se repiten: tarjeta con borde fino redondeado, foto dentro de un círculo con anillo cobrizo sobre un disco beige, línea fina con estrella al centro, título de marca con degradado, adornos de línea (labial, brocha, trazos) y estrellas. En la web el anillo se dibuja en CSS y los adornos se extrajeron del PDF a `assets/images/decor/`.

### Calidad de las fotografías

Se exportó el diseño con la **máxima calidad** que ofrece Canva ("pro"). Los adornos salen a ~300 ppp, pero **las fotos de producto siguen en baja resolución porque ya eran pequeñas cuando se subieron a Canva**: la foto de cada producto, recortada dentro del círculo a su resolución real (sin ampliar), mide entre **260 y 596 px** (mediana 288 px). **Las 249 fotos están por debajo de 800 px** `[INFORMACIÓN PENDIENTE]`.

Para que se vean nítidas hay que conseguir las **fotos originales** (las que se subieron a Canva) o las **fotos oficiales** de cada marca del mismo producto y presentación. El proceso está en [`INSTRUCCIONES-FOTOS.md`](INSTRUCCIONES-FOTOS.md). Lista por marca (tamaño actual en píxeles):

<details><summary><strong>Montoc</strong> — 15 fotos</summary>

- `montoc-003-1` Base Glow Filter — 315 px
- `montoc-003-2` Polvos Translúcidos — 315 px
- `montoc-004-1` Paleta Light Set — 288 px
- `montoc-004-2` Rubor líquido radiante Glow Filter — 288 px
- `montoc-005-1` Bronzer Drops Light — 288 px
- `montoc-005-2` Bronzer luminoso en polvo + brocha Hello beach — 288 px
- `montoc-006-1` Paleta Harmony x6 — 297 px
- `montoc-006-2` Brow Wax Ultra Fijador de cejas — 291 px
- `montoc-007-1` Lápiz delineador de labios — 303 px
- `montoc-007-2` Hidratante de Labios Lippie Balm — 288 px
- `montoc-008-1` Fijador de maquillaje Dixy Fix — 288 px
- `montoc-009-1` Set de Borlas — 339 px
- `montoc-009-2` Kit de brochas de maquillaje Fluffy x 10 — 429 px
- `montoc-010-1` Esponja mini para difuminar maquillaje — 315 px
- `montoc-010-2` Brocha mini viajera — 330 px

</details>

<details><summary><strong>Bloomshell</strong> — 20 fotos</summary>

- `bloomshell-011-1` Base líquida 2 en 1 My foundation — 327 px
- `bloomshell-011-2` Corrector My concealer — 318 px
- `bloomshell-012-1` Polvos sueltos — 294 px
- `bloomshell-012-2` Polvos sueltos 4 tonos — 288 px
- `bloomshell-013-1` Rubor en barra Cherry Blossom — 288 px
- `bloomshell-013-2` Trío de Rubores — 288 px
- `bloomshell-014-1` Contorno en barra Bloom define — 288 px
- `bloomshell-014-2` Iluminador Bloom Dazlee — 288 px
- `bloomshell-015-1` Laminador de cejas — 330 px
- `bloomshell-015-2` Paleta de sombras Bloom Vibes — 300 px
- `bloomshell-016-1` Llavero Mimosa Tinta + Gloss — 288 px
- `bloomshell-016-2` Brillo labial - Bombón — 288 px
- `bloomshell-017-1` Papel matificante Bloom powder paper — 288 px
- `bloomshell-017-2` Papel matificante Bloom Oil Stop — 312 px
- `bloomshell-018-1` Fijador de maquillaje Bloom Fix — 300 px
- `bloomshell-019-1` Bloom Termo — 288 px
- `bloomshell-019-2` Bloom porta cosméticos — 288 px
- `bloomshell-020-1` Kit Kiss Love — 372 px
- `bloomshell-021-1` Beauty Blender Xl — 288 px
- `bloomshell-021-2` Bloom Blender Bliss — 318 px

</details>

<details><summary><strong>Girly</strong> — 3 fotos</summary>

- `girly-022-1` Gel hidratante con aloe vera — 261 px
- `girly-022-2` Girly TINT Labios y mejillas — 582 px
- `girly-022-3` Polvo suelto — 265 px

</details>

<details><summary><strong>Maybelline</strong> — 3 fotos</summary>

- `maybelline-023-1` Pestañina Sky High Lavable | A prueba de agua — 287 px
- `maybelline-023-2` Pestañina Colossal Lavable | A prueba de agua — 582 px
- `maybelline-023-3` Pestañina Surreal Lavable | A prueba de agua — 261 px

</details>

<details><summary><strong>Ani-k</strong> — 9 fotos</summary>

- `ani-k-024-1` 2 en 1: base y corrector — 288 px
- `ani-k-024-2` Loose powder Polvos sueltos — 288 px
- `ani-k-025-1` Serum Flyshy Blushy — 288 px
- `ani-k-025-2` Rubor líquido Bonita — 288 px
- `ani-k-026-1` Rubor en polvo Bonita — 288 px
- `ani-k-027-1` Lip Gloss — 360 px
- `ani-k-028-1` Delineador radiante Tono negro — 287 px
- `ani-k-028-2` Pestañina eternal lash — 582 px
- `ani-k-028-3` Pestañina Brown Paradise - A prueba de agua — 264 px

</details>

<details><summary><strong>Majikal</strong> — 3 fotos</summary>

- `majikal-029-1` Polvos sueltos - 4 tonos — 319 px
- `majikal-029-2` Magic Pen — 583 px
- `majikal-029-3` Shiny Lip Oil — 260 px

</details>

<details><summary><strong>Atenea</strong> — 23 fotos</summary>

- `atenea-030-1` Base de maquillaje 1ST Scene — 288 px
- `atenea-030-2` Serum Tinted 1ST Scene — 288 px
- `atenea-031-1` Polvo en gel matificante Matterpowder — 288 px
- `atenea-031-2` Polvo suelto- Banana 1ST Scene — 288 px
- `atenea-032-1` Rubor compacto 1ST Scene — 288 px
- `atenea-032-2` Rubor cremoso en barra — 303 px
- `atenea-033-1` Bronzer cremoso en barra — 288 px
- `atenea-033-2` Iluminador efecto húmedo Sublime — 345 px
- `atenea-034-1` Paleta de sombras multiusos Moccalush — 381 px
- `atenea-035-1` Paleta de sombras 18 tonos - Art Deco — 288 px
- `atenea-035-2` Paleta de sombras Majestic — 288 px
- `atenea-036-1` Paleta de sombras 12 tonos - 1ST SCENE — 318 px
- `atenea-036-2` Paleta de sombras 12 tonos - Rose sublime — 345 px
- `atenea-037-1` Pigmento Soft Touch — 288 px
- `atenea-037-2` Gel fijador de cejas — 291 px
- `atenea-038-1` Delineador de cejas — 321 px
- `atenea-039-1` Lápiz delineador Color pencil — 288 px
- `atenea-039-2` Lip Balm Mask — 288 px
- `atenea-040-1` Primer Gummy — 288 px
- `atenea-041-1` Brocha duo Base y productos en crema — 294 px
- `atenea-041-2` Beauty sponge — 288 px
- `atenea-042-1` Encrespador Focus — 288 px
- `atenea-042-2` Mini beauty sponge trio — 318 px

</details>

<details><summary><strong>Prosa</strong> — 12 fotos</summary>

- `prosa-043-1` Pestañina Profesional Silicon — 288 px
- `prosa-043-2` Pestañina Maxivolumen — 321 px
- `prosa-044-1` Pestañina Microfibra — 297 px
- `prosa-044-2` Pestañina Maxivolumen Silicon — 288 px
- `prosa-045-1` Pestañina Profesional Silicon - Café — 303 px
- `prosa-045-2` Pestañina Sensual Love — 288 px
- `prosa-046-1` Pestañina con aceite de mamey — 288 px
- `prosa-046-2` Pestañina con aceite de aguacate — 288 px
- `prosa-047-1` Pestañina red passion — 288 px
- `prosa-047-2` Aceite para pestañas — 288 px
- `prosa-048-1` Pestañina maxivolumen Borgoña — 312 px
- `prosa-048-2` Tratamiento en máscara para pestañas y cejas — 596 px

</details>

<details><summary><strong>Samy</strong> — 12 fotos</summary>

- `samy-049-1` Polvo suelto — 348 px
- `samy-049-2` Rubor en barra Velvet Glam — 288 px
- `samy-050-1` Rubor Compacto Velvet Glam Samy — 291 px
- `samy-050-2` Rubor 2 en 1 Sunset Glam Samy — 291 px
- `samy-051-1` Tinta en crema Lip Blush — 294 px
- `samy-051-2` Contorno en barra Velvet Glam — 288 px
- `samy-052-1` Betún de cejas — 297 px
- `samy-052-2` Kit para cejas — 330 px
- `samy-053-1` Paleta de sombras x3 — 327 px
- `samy-053-2` Paleta de sombras x9 — 366 px
- `samy-054-1` Esponja de maquillaje — 288 px
- `samy-054-2` Brocha retráctil — 288 px

</details>

<details><summary><strong>Lula</strong> — 12 fotos</summary>

- `lula-055-1` Lápiz delineador de ojos — 288 px
- `lula-056-1` Aceite para labios con charm — 288 px
- `lula-056-2` Bálsamo de labios — 288 px
- `lula-057-1` Bálsamo desmaquillante — 288 px
- `lula-057-2` Contorno de ojos Aloe Vera — 288 px
- `lula-058-1` Toallas húmedas desmaquillantes — 330 px
- `lula-058-2` Parches de puntos negros x 8 Unidades — 324 px
- `lula-059-1` Hidratante facial de noche con ceramidas — 288 px
- `lula-059-2` Hidratante facial de día con ceramidas — 288 px
- `lula-060-1` Tónico de Rosas — 288 px
- `lula-061-1` Kit de brochas Marshmallow X 13pcs — 396 px
- `lula-061-2` Kit de brochas Uva X 14pcs — 288 px

</details>

<details><summary><strong>Raquel</strong> — 1 fotos</summary>

- `raquel-062-1` Polvo suelto traslúcido mate minerals con avena y trigo — 288 px

</details>

<details><summary><strong>OG</strong> — 6 fotos</summary>

- `og-063-1` Base Aqua smooth — 288 px
- `og-063-2` Base Stay matte — 288 px
- `og-064-1` Rubor mineralizado Daily — 288 px
- `og-064-2` Rubor matte Daily — 288 px
- `og-065-1` Gloss and lip Dreamy — 288 px
- `og-065-2` Brillo labial Yess Queen — 288 px

</details>

<details><summary><strong>Schwarzkopf</strong> — 2 fotos</summary>

- `schwarzkopf-066-1` Gel fijador Glued Got2b amarillo — 288 px
- `schwarzkopf-066-2` Gel para cejas Got2b amarillo — 288 px

</details>

<details><summary><strong>Tocobo</strong> — 2 fotos</summary>

- `tocobo-067-1` Bloqueador en barra Cotton Soft SPF50 — 288 px
- `tocobo-067-2` Dúo de limpieza — 288 px

</details>

<details><summary><strong>Skin 1004</strong> — 2 fotos</summary>

- `skin-1004-068-1` Madagascar Centella Ampoule Foam Limpiador 125 ml — 288 px
- `skin-1004-068-2` Centella Poremizing Deep Cleansing Foam Limpiador 125 ml — 288 px

</details>

<details><summary><strong>Bioaqua</strong> — 23 fotos</summary>

- `bioaqua-069-1` Kit facial de rosas — 288 px
- `bioaqua-069-2` Kit facial de arroz — 288 px
- `bioaqua-070-1` Kit facial de centella asiática — 288 px
- `bioaqua-070-2` Kit facial de ácido salicílico — 300 px
- `bioaqua-071-1` Kit facial con retinol — 288 px
- `bioaqua-071-2` Kit facial de ácido hialurónico — 288 px
- `bioaqua-072-1` Mascarilla facial en velo — 360 px
- `bioaqua-073-1` Jabón facial - ácido salicílico — 288 px
- `bioaqua-073-2` Espuma limpiadora de arroz — 288 px
- `bioaqua-074-1` Tónico de vitamina C — 297 px
- `bioaqua-074-2` Tónico de centella asiática — 288 px
- `bioaqua-075-1` Tónico de arroz — 288 px
- `bioaqua-075-2` Tónico de ácido hialurónico — 288 px
- `bioaqua-076-1` Serum de vitamina C — 288 px
- `bioaqua-076-2` Serum de centella asiática — 288 px
- `bioaqua-077-1` Esencia de arroz — 288 px
- `bioaqua-077-2` Serum de ácido hialurónico — 288 px
- `bioaqua-078-1` Serum de retinol — 288 px
- `bioaqua-078-2` Serum pure skin — 288 px
- `bioaqua-079-1` Crema hidratante con vitamina C — 288 px
- `bioaqua-079-2` Crema hidratante con centella asiática — 288 px
- `bioaqua-080-1` Crema hidratante de arroz — 288 px
- `bioaqua-080-2` Crema hidratante con ácido hialurónico — 288 px

</details>

<details><summary><strong>Garnier</strong> — 4 fotos</summary>

- `garnier-081-1` Agua micelar todo en 1 Rosada x 400 ml — 288 px
- `garnier-081-2` Agua micelar todo en 1 Rosada x 100 ml — 288 px
- `garnier-082-1` Agua micelar pure active x 400 ml — 288 px
- `garnier-082-2` Agua micelar con vitamina C x 400 ml — 312 px

</details>

<details><summary><strong>Milagros</strong> — 19 fotos</summary>

- `milagros-083-1` Shampoo herbal x 500 ml (con romero y jengibre) — 288 px
- `milagros-083-2` Shampoo con cebolla x450 ml (con péptidos) — 288 px
- `milagros-084-1` Shampoo magia x 450 ml (ácido hialurónico) — 288 px
- `milagros-084-2` Shampoo anticaspa x 450 ml — 288 px
- `milagros-085-1` Acondicionador ultra nutritivo x 450 ml — 288 px
- `milagros-085-2` Acondicionador milagro herbal x 450 ml — 288 px
- `milagros-086-1` Acondicionador ultra nutritivo x100 ml — 312 px
- `milagros-086-2` Acondicionador milagro herbal x100 ml — 288 px
- `milagros-087-1` Tratamiento Emergencia Capilar x450 ml — 288 px
- `milagros-087-2` Tratamiento nutrición y crecimiento x 450 ml — 288 px
- `milagros-088-1` Tratamiento capilar a base de frutas x450 ml — 288 px
- `milagros-088-2` Doypack tratamiento capilar a base de frutas x100 ml — 288 px
- `milagros-089-1` Doypack bio - repolarizador capilar x100 gr — 288 px
- `milagros-089-2` Doypack tratamiento emergencia capilar x100 gr — 288 px
- `milagros-090-1` Tratamiento bio - repolarizador capilar x100 ml — 288 px
- `milagros-090-2` Tratamiento a base de frutas x100 ml — 288 px
- `milagros-091-1` Gotas Mágicas Capilares — 288 px
- `milagros-091-2` Tónico revitalizante capilar milagro herbal (tónico con romero) — 288 px
- `milagros-092-1` Perfume capilar y corporal — 288 px

</details>

<details><summary><strong>Anyeluz</strong> — 14 fotos</summary>

- `anyeluz-093-1` Shampoo de cebolla x 500 ml — 452 px
- `anyeluz-093-2` Acondicionador de cebolla x 500 ml — 446 px
- `anyeluz-094-1` Shampoo con romero x 500 ml — 408 px
- `anyeluz-094-2` Acondicionador con romero x 500 ml — 423 px
- `anyeluz-095-1` Shampoo con ginseng x 500 ml — 429 px
- `anyeluz-095-2` Acondicionador con ginseng x 500 ml — 405 px
- `anyeluz-096-1` Shampoo con aloe vera x 500 ml — 381 px
- `anyeluz-096-2` Acondicionador con argán y aloe vera x 500 ml — 396 px
- `anyeluz-097-1` Shampoo liso en casa x 800 ml - línea profesional — 390 px
- `anyeluz-097-2` Acondicionador liso en casa x 800 ml - línea profesional — 440 px
- `anyeluz-098-1` Tratamiento liso en casa - línea profesional — 405 px
- `anyeluz-098-2` Tratamiento reparación, restauración y brillo - línea profesional — 324 px
- `anyeluz-099-1` Tratamiento capilar de crecimiento — 288 px
- `anyeluz-099-2` Tratamiento con romero y bioelixir — 372 px

</details>

<details><summary><strong>Lehit</strong> — 4 fotos</summary>

- `lehit-100-1` Tratamiento aceite de aguacate x30 gr — 288 px
- `lehit-100-2` Tratamiento complejo biológico con queratina x30gr — 339 px
- `lehit-101-1` Tratamiento cebolla y jengibre x30 gr — 288 px
- `lehit-101-2` Tratamiento capullo de gusano de seda x30gr — 390 px

</details>

<details><summary><strong>Leche pal pelo</strong> — 22 fotos</summary>

- `leche-pal-pelo-102-1` Shampoo tradicional x 440 ml — 288 px
- `leche-pal-pelo-102-2` Shampoo Protección Plus x 440 ml — 288 px
- `leche-pal-pelo-103-1` Shampoo especializado x 440 ml — 288 px
- `leche-pal-pelo-103-2` Shampoo nutritivo para niños x 440 ml — 288 px
- `leche-pal-pelo-104-1` Shampoo + Acondicionador para niños x 440 ml — 288 px
- `leche-pal-pelo-104-2` Shampoo hidratante rizos para niños x 440 ml — 288 px
- `leche-pal-pelo-105-1` Acondicionador para niños x 440 ml — 288 px
- `leche-pal-pelo-105-2` Acondicionador Co-wash rizos y afro x 440 ml — 288 px
- `leche-pal-pelo-106-1` Mascarilla nutritiva rizos y ondas x 440 ml — 288 px
- `leche-pal-pelo-106-2` Mascarilla hidrosellante x 440 ml — 288 px
- `leche-pal-pelo-107-1` Mascarilla Regenerador Intenso 7 Oleos x 800 ml — 288 px
- `leche-pal-pelo-107-2` Mascarilla WOW x 800 ml — 288 px
- `leche-pal-pelo-108-1` Mascarilla Regenerador Intenso 7 Oleos x 40 ml — 288 px
- `leche-pal-pelo-108-2` Mascarilla WOW x 40 ml — 360 px
- `leche-pal-pelo-109-1` Termoprotector líquido X 250 ml — 309 px
- `leche-pal-pelo-109-2` Termoprotector tradicional x 440 ml — 288 px
- `leche-pal-pelo-110-1` Termoprotector protección plus x 440 ml — 288 px
- `leche-pal-pelo-110-2` Termoprotector rizos y ondas x 440 ml — 288 px
- `leche-pal-pelo-111-1` Gelatina slime definidora x 600 ml — 288 px
- `leche-pal-pelo-111-2` Definidor de rizos y ondas x 440 ml — 291 px
- `leche-pal-pelo-112-1` Tratamiento capilar reconstructor instantáneo x 30 ml — 288 px
- `leche-pal-pelo-112-2` Termoprotector tradicional x 30 ml — 288 px

</details>

<details><summary><strong>Olé</strong> — 12 fotos</summary>

- `ole-113-1` Shampoo protección y reparación x 500 ml — 288 px
- `ole-113-2` Shampoo hidratación y nutrición x 500 ml — 288 px
- `ole-114-1` Shampoo control grasa x 500 ml — 288 px
- `ole-114-2` Shampoo fortalecimiento y crecimiento x 500 ml — 300 px
- `ole-115-1` Shampoo + Acondicionador control frizz x 500 ml — 303 px
- `ole-115-2` Acondicionador hidratación y crecimiento x 500 ml — 288 px
- `ole-116-1` Acondicionador hidratación y suavidad x 500 ml — 306 px
- `ole-116-2` Acondicionador protección long lasting x 500 ml — 312 px
- `ole-117-1` Acondicionador purificante anti-grasa x 500 ml — 357 px
- `ole-117-2` Termoprotector desenredante — 288 px
- `ole-118-1` Óleo capilar de uchuva Hidratante de puntas — 288 px
- `ole-118-2` Spray antihumedad - antifrizz — 288 px

</details>

<details><summary><strong>Nude</strong> — 2 fotos</summary>

- `nude-119-1` Protector solar Spf30 40 ml — 288 px
- `nude-119-2` Autobronceador Doypack 200ml — 288 px

</details>

<details><summary><strong>Johnson's</strong> — 8 fotos</summary>

- `johnsons-120-1` Shampoo baby - Cabello oscuro — 288 px
- `johnsons-120-2` Shampoo baby - Cabello claro — 288 px
- `johnsons-121-1` Shampoo - Fuerza y vitamina — 288 px
- `johnsons-121-2` Shampoo baby - amarillo — 288 px
- `johnsons-122-1` Baño líquido - Avena — 288 px
- `johnsons-122-2` Baño líquido - Antes de dormir — 288 px
- `johnsons-123-1` Crema líquida baby — 288 px
- `johnsons-123-2` Crema líquida - Avena — 288 px

</details>

<details><summary><strong>Nivea</strong> — 9 fotos</summary>

- `nivea-124-1` Crema hidratante — 306 px
- `nivea-124-2` Crema corporal Nivea reafirmante Q10 + vitamina C x 1000 Ml — 288 px
- `nivea-125-1` Crema Nivea Corporal Reafirmante Q10 Creatina x 400 ml — 288 px
- `nivea-125-2` Crema corporal Nivea milk nutritiva - Piel Seca x 400 ml — 288 px
- `nivea-126-1` Desodorante aclarado natural Classic Touch x 50ml — 288 px
- `nivea-126-2` Desodorante tono natural mujer satín spray x 150 ml — 306 px
- `nivea-127-1` Desodorante men Invisible Black & White x 50ml — 288 px
- `nivea-127-2` Desodorante dama Invisible Black & White x 50ml — 327 px
- `nivea-128-1` Lip care - 24 horas de humectación — 345 px

</details>

<details><summary><strong>Chap Stick</strong> — 1 fotos</summary>

- `chap-stick-129-1` Protector labial — 333 px

</details>

<details><summary><strong>Fantiluna</strong> — 6 fotos</summary>

- `fantiluna-130-1` Mantequilla corporal x 220 ml — 345 px
- `fantiluna-130-2` Exfoliante corporal x 220ml — 288 px
- `fantiluna-131-1` Splash corporal x 250 ml — 443 px
- `fantiluna-131-2` Splash corporal x 105 ml — 375 px
- `fantiluna-132-1` Iluminador corporal x 160 ml — 300 px
- `fantiluna-132-2` Crema corporal — 288 px

</details>

### Problemas detectados en las fotos

- **OG, p. 64** — "Rubor mineralizado Daily" y "Rubor matte Daily" usan la misma foto principal (las fotos de tonos debajo sí son distintas). Se respeta tal cual.
- Bloomshell "Contorno en barra Bloom define" ya no usa la foto del rubor Cherry Blossom: no queda ninguna "Foto pendiente".

### Erratas corregidas a pedido de Ágata Beauty

Se corrigen **en la web** (`TEXT_FIXES` y `BRAND_FIXES` en `scripts/extract-catalog.py`, que se aplican cada vez que se regenera). Conviene corregirlas también en Canva con *Buscar y reemplazar* (el conector de Canva no permite editar diseños de 133 páginas).

| Página | En el catálogo | En la web |
| --- | --- | --- |
| 13 | **Trio** de Rubores | Trío |
| 16 | Brillo labial - **Bombon** | Bombón |
| 17 | Bloom **podwer** paper | powder |
| 19 | Bloom porta **cosmeticos** | cosméticos |
| 48 | Tratamiento en **mascara** para pestañas | máscara |
| 54 | Brocha **retractil** | retráctil |
| 70, 73 | ácido **salicilico** | salicílico |
| 70, 74, 76, 79 | centella **asiatica** | asiática |
| 70 | Necesidad: **Acne** | Acné |
| 100 | complejo **biologico** | biológico |
| 101 | cebolla y **gengibre** | jengibre |
| 111 | **Definir** de rizos y ondas | Definidor |
| 130 | **Mantaquilla corportal** | Mantequilla corporal |
| 122 | Baño **liquido** | líquido |
| 123 | Crema **liquida** | líquida |
| 120–123 | **JOHNSON’S** / **johnson´s** (título) | Johnson's |

## Fase 2 — Modelo de datos

`data/products.json` es la única fuente de datos: `{ brand, pages, products }`. Cada producto tiene `id` (`marca-página-posición`), `name`, `brand`, `category`, `section` (la original), `price` (el menor), `variants`, `presentation`, `description`, `details`, `image`, `imageWidth`, `imageHeight`, `imageAlt`, `imageSource`, `gallery` y `page`; cada campo existe solo si el dato existe. La tabla completa está en [`PRODUCTOS.md`](PRODUCTOS.md), generada por el script.

## Fases 3 a 7 — Arquitectura, implementación, validación y pruebas

- **Arquitectura:** HTML5 + CSS3 + JavaScript (módulos ES), sin frameworks ni compilación. Se conserva la del proyecto base (ver README → Estructura); todo el contenido sale de `data/products.json`.
- **Validación visual:** se compararon portada, tarjetas, detalle y vista catálogo con el PDF (colores, tipografías, círculo con anillo cobrizo, divisor con estrella, textos, nombres y precios; p. ej. Montoc p. 4 y Prosa pp. 47–48 verificadas contra la página renderizada).
- **Pruebas (`scripts/test-ux.cjs`):** 74/74 correctas en celular (390×844) y computador (1280×900): búsqueda con y sin tildes y con varias palabras, filtros con contadores cruzados, agrupación (27 marcas / 8 categorías / sin agrupar), orden, detalle (Esc, "Volver", atrás del navegador), WhatsApp con producto y marca, enlaces directos, vista catálogo (132 páginas), estado sin resultados, todas las imágenes cargan, sin errores de JavaScript, sin scroll horizontal y 404 con la marca.
- **Optimización:** fotos WebP a su resolución real (~5 MB los 249 productos, carga diferida), páginas del catálogo WebP de 900 px (~70 KB c/u, carga diferida), imagen JPG para compartir el enlace (`assets/og-portada.jpg`), Open Graph con la dirección definitiva, `canonical`, favicon, H1/H2/H3, foco visible y respeto de "reducir movimiento".

## Información pendiente `[INFORMACIÓN PENDIENTE]`

1. **Fotos en alta resolución** de los 249 productos (ver la lista por marca).
2. **Indicativo del WhatsApp.** El catálogo muestra 3135496268; el enlace usa **+57** (Colombia), deducido del número y de los precios en pesos.
3. **Referencias.** El proceso de compra dice "Guarda las referencias de los productos", pero el catálogo no tiene códigos. El mensaje de WhatsApp envía el nombre y la marca.
4. **Ofertas.** No hay en el catálogo 2026; el menú aparece solo cuando un producto tiene `offer`.
