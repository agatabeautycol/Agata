# Guía para mejorar las fotos del catálogo web de Ágata Beauty

Esta guía es para la persona que tiene acceso al Canva del catálogo y a las fotos de los productos.
No necesitas saber programar: **Claude Code hace la parte técnica**. Tú solo consigues las fotos, se las das y revisas el resultado.

- Catálogo web (lo que ven los clientes): **https://agatabeautycol.github.io/Agata/**
- Repositorio en GitHub (donde vive el catálogo): **https://github.com/agatabeautycol/Agata**
- Rama de trabajo (no la cambies): **`main`**
- Lista de los 249 productos con su código: **[docs/PRODUCTOS.md](PRODUCTOS.md)**

### ¿Por qué hay que cambiar las fotos?

Las fotos del catálogo se ven borrosas porque **ya estaban en baja resolución cuando se subieron a Canva** (unos 200–300 píxeles). Exportar de nuevo no lo arregla: hacen falta **las fotos originales en buena calidad** (mínimo 800 × 800 píxeles), por ejemplo las fotos oficiales de cada marca o las que tú tomaste.

---

## PARTE 1 — Paso a paso para ti

### Paso 1. Pide acceso al repositorio (una sola vez)

1. Si no tienes cuenta de GitHub, créala gratis en **https://github.com/signup**.
2. Envíale tu **nombre de usuario de GitHub** a la dueña del catálogo (agatabeautycol).
3. Ella debe entrar a **https://github.com/agatabeautycol/Agata/settings/access**, tocar **Add people**, escribir tu usuario y tocar **Add**.
4. Te llega un **correo de invitación de GitHub**: ábrelo y toca **Accept invitation**.

### Paso 2. Junta las fotos

Las fotos se pueden conseguir de dos formas (puedes usar las dos):

**Opción A — Descargarlas tú (la más segura):**

1. Abre **[docs/PRODUCTOS.md](PRODUCTOS.md)**. Ahí está cada producto con su **código** (columna ID), por ejemplo `montoc-003-1` = Base Glow Filter de Montoc.
2. Busca la foto de ese producto en la página oficial de la marca o en tus archivos. Debe ser **exactamente el mismo producto** (mismo envase, tamaño y presentación que el catálogo).
3. Guárdala con el **código como nombre**: `montoc-003-1.jpg` (sirve `.jpg`, `.png` o `.webp`).
4. Si un producto tiene varias fotos buenas, guarda solo la principal.
5. Si no encuentras la foto de un producto, no pasa nada: se queda la actual.

**Opción B — Que Claude Code las busque en las páginas de las marcas:**
anota en una lista la dirección (enlace) de la página de cada marca o producto, por ejemplo
`https://montoccosmetictools.com/products/glow-filter`. Claude solo puede abrir las páginas que habilites en el Paso 4.

> Las fotos oficiales de una marca suelen poder usarse para vender sus productos, pero si tienes dudas, confírmalo con la marca o el distribuidor.

### Paso 3. Sube las fotos a GitHub (si usaste la Opción A)

1. En tu computador, pon todas las fotos dentro de una carpeta llamada **`fotos`**.
2. Entra a **https://github.com/agatabeautycol/Agata/tree/main/catalogo-original**
   (arriba a la izquierda debe decir la rama `main`).
3. Toca **Add file → Upload files**.
4. Arrastra **la carpeta `fotos` completa** (no las fotos sueltas) al recuadro: así GitHub crea `catalogo-original/fotos/`.
   Hasta 100 archivos por vez; cada foto debe pesar menos de 25 MB. Si tienes más de 100, haz varias carpetas `fotos` por marca y súbelas una por una (se juntan en la misma carpeta).
5. Abajo, en el mensaje, escribe por ejemplo: `Fotos originales Montoc`.
6. Deja marcado **Commit directly to the `main` branch** y toca **Commit changes**.
7. Repite por grupos (por ejemplo, una subida por marca) hasta terminar.

> Esto es "git": cada subida queda guardada como un cambio con fecha y mensaje, y siempre se puede volver atrás. No tienes que hacer nada más con git; Claude Code se encarga del resto.

### Paso 4. Abre Claude Code y prepara el entorno

1. Entra a **https://claude.ai/code** e inicia sesión.
2. Si te lo pide, conecta tu cuenta de GitHub (**Connect GitHub**) y permite el acceso al repositorio **agatabeautycol/Agata**.
3. Crea una sesión nueva y elige el repositorio **agatabeautycol/Agata**.
4. **Acceso a internet (solo si usarás la Opción B):** en la barra de arriba de la sesión, abre el menú del **entorno** → **Edit** → **Network access**, y en **Allowed domains** agrega los dominios de las páginas de las marcas (la parte entre `https://` y la primera `/`, por ejemplo `montoccosmetictools.com`) y también:
   - `cdn.shopify.com` (muchas tiendas guardan ahí sus fotos)
   - `canva.com` y `canva.link` (si vas a compartir el enlace del catálogo de Canva)

   Deja marcada la casilla **Allow package managers** y guarda. Guía oficial: https://code.claude.com/docs/en/cloud-environments#network-access

### Paso 5. Pega el prompt

1. Copia **todo** el bloque de la PARTE 2 (en GitHub, pasa el mouse por el bloque y toca el ícono de copiar ⧉ arriba a la derecha).
2. Pégalo en la sesión de Claude Code.
3. Si usaste la Opción B, al final del mensaje pega tu lista de enlaces.
4. Envíalo y espera. Claude te irá contando qué hace y te hará preguntas si algo no está claro: respóndelas.

### Paso 6. Revisa el resultado

1. Cuando Claude termine, te mostrará una tabla con las fotos cambiadas y las que no.
2. Espera 2 minutos y abre **https://agatabeautycol.github.io/Agata/** (en el celular, mejor en una pestaña de incógnito).
3. Si alguna foto no corresponde al producto, díselo a Claude con el código del producto, por ejemplo:
   *"La foto de `samy-051-2` no es el kit correcto, vuelve a la anterior"*.

### Lo que NO debes hacer

- No cambies el nombre del repositorio (`Agata`) ni de la rama: rompe la dirección del catálogo.
- No borres archivos desde GitHub.
- No subas el PDF de Canva a GitHub (pesa demasiado); si quieres dárselo a Claude, adjúntalo en el chat de Claude Code.

---

## PARTE 2 — Prompt para pegar en Claude Code

```text
Hola. Vas a trabajar en el catálogo web de Ágata Beauty, en el repositorio agatabeautycol/Agata.
Soy una persona no técnica: explícame en español y en palabras sencillas lo que haces, y pregúntame
si algo no está claro antes de decidir por tu cuenta.

## Contexto del proyecto
- Sitio estático (HTML + CSS + JavaScript, sin compilación) publicado con GitHub Pages en
  https://agatabeautycol.github.io/Agata/ desde la rama `main`, carpeta raíz.
- Trabaja y sube cambios SOLO a esa rama. No crees otras ramas, no cambies su nombre ni el del repositorio,
  no reescribas el historial (nada de force-push) y no abras pull requests.
- Lee primero: README.md, docs/AUDITORIA.md, docs/PRODUCTOS.md, data/products.json y scripts/extract-catalog.py.
- data/products.json es la única fuente de datos (249 productos, 27 marcas). Cada producto tiene un `id`
  (p. ej. `montoc-003-1` = marca, página y posición) que NO debes cambiar a mano.
- Las fotos actuales están en assets/images/productos/{id}.webp: son recortes circulares del PDF de Canva,
  de baja resolución (~200–400 px). El anillo cobrizo alrededor de la foto lo dibuja el CSS
  (.card-media / .detail-media), no la imagen.
- scripts/extract-catalog.py regenera productos, fotos y páginas desde el PDF; las correcciones manuales
  viven en TEXT_FIXES, BRAND_FIXES, CATEGORY_MAP, CATEGORY_BY_PRODUCT, CATEGORY_BY_BRAND y PHOTO_PENDING.

## Objetivo
Reemplazar las fotos de producto por versiones originales de buena calidad (mínimo 800 px de lado),
SIN alterar el producto.

## Reglas obligatorias
1. Nunca uses imágenes generadas o modificadas por IA, ni "mejores" la nitidez artificialmente.
   Solo se permite: recortar, redimensionar, centrar en un lienzo cuadrado, convertir a WebP y comprimir.
   Excepción autorizada por Ágata Beauty: quitar SOLO el fondo con el recortador automático de
   scripts/fetch-product-photos.py (los píxeles del producto no se modifican), para que todas las fotos
   queden sobre el mismo disco beige del catálogo.
2. Cada foto nueva debe ser EXACTAMENTE el mismo producto del catálogo: misma marca, mismo envase,
   mismo tamaño/presentación (p. ej. "x 450 ml" vs "x 100 ml"), mismo tono o versión.
   Compárala visualmente con la foto actual (assets/images/productos/{id}.webp) y con el nombre en
   data/products.json. Si tienes dudas, NO la cambies: anótala como "por confirmar" y pregúntame.
3. No inventes productos, precios, nombres ni descripciones. No cambies textos ni precios.
4. No modifiques el bloque `brand` de data/products.json (contacto, proceso de compra).

## Fuentes de las fotos (en este orden)
A. Archivos en catalogo-original/fotos/ nombrados con el id del producto (p. ej. montoc-003-1.jpg).
   Si el nombre no coincide con ningún id, pregúntame a qué producto corresponde.
B. Fotos que yo adjunte en este chat (te diré a qué producto corresponde cada una).
C. Enlaces de páginas de marcas/tiendas que pegue al final de este mensaje. Si una página está bloqueada
   por la red del entorno, dime exactamente qué dominio debo agregar en Network access y sigue con lo demás.
   En tiendas Shopify puedes leer /products/<handle>.json para obtener las fotos en alta resolución.
   Guarda la URL de origen de cada foto.

## Cómo procesar cada foto
1. Guarda el original sin tocar en catalogo-original/fotos/{id}.png (o .jpg/.webp), con el ID del producto.
   Para fotos de páginas oficiales, agrega el enlace en PHOTO_PAGES de scripts/fetch-product-photos.py.
2. Ejecuta `python3 scripts/fetch-product-photos.py` (requiere `pip install "rembg[cpu]" pillow`). Genera
   assets/images/productos-hd/{id}.webp: quita solo el fondo (si la foto ya es PNG transparente no la toca),
   centra el producto en un lienzo cuadrado transparente para que el círculo no lo corte y lo reduce a
   800 px si es más grande (nunca amplía). El origen queda en assets/images/productos-hd/fuentes.json.
3. Revisa cada foto contra la del catálogo (mismo producto y presentación, bordes bien recortados).
4. Regenera con `python3 scripts/extract-catalog.py catalogo-original/catalogo.pdf`: usa
   assets/images/productos-hd/{id}.webp en vez del recorte del PDF, y luego `python3 scripts/photo-report.py`.

## Verificación antes de subir
1. Sirve el sitio localmente (python3 -m http.server 8080) y revísalo con Playwright/Chromium en
   390×844 (celular) y 1280×900 (computador): que todas las fotos carguen (sin errores 404), que se vean
   dentro del círculo sin cortar el producto, que no haya scroll horizontal y que la búsqueda, los filtros
   de categoría y marca, la agrupación y el detalle sigan funcionando.
2. Muéstrame capturas de antes y después de al menos 6 productos de marcas distintas.
3. Comprueba que data/products.json sigue siendo JSON válido y que los 249 productos siguen ahí.

## Subir los cambios (git)
1. Haz commits pequeños y claros en español (por ejemplo, uno por marca), solo en la rama
   main, y súbelos con git push a esa misma rama.
2. Después del push, revisa en GitHub Actions que el despliegue "pages build and deployment"
   termine en verde.
3. Regenera docs/PRODUCTOS.md (columna Imagen) y agrega en docs/AUDITORIA.md una sección
   "Fotos en alta resolución" con: cuántas fotos se reemplazaron, de dónde salió cada una y cuáles faltan.

## Al terminar, entrégame
- Una tabla: id | producto | marca | ¿foto nueva? (sí/no) | origen | observaciones.
- La lista de productos que siguen con foto de baja resolución, agrupada por marca, para saber qué
  fotos faltan conseguir.
- Recuérdame abrir https://agatabeautycol.github.io/Agata/ en 2 minutos para ver el resultado.

## Pendientes que puedes preguntarme al final (no bloquean el trabajo)
- Confirmar que el WhatsApp 3135496268 es de Colombia (+57).

Enlaces de páginas de las marcas (si los tengo; si no, ignora esta parte):
```
