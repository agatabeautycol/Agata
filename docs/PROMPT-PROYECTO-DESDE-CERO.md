# Catálogo digital de Ágata Beauty — Guía y prompt para empezar desde cero

Esta guía permite crear **todo el proyecto desde cero con tus propias cuentas** (Claude, Canva y GitHub).
No necesitas saber programar: **Claude Code hace la parte técnica** y tú solo sigues los pasos, das permisos y revisas.

Al final tendrás:

- Un repositorio en tu GitHub con todo el código.
- Claude conectado a tu **Canva** (para leer el catálogo) y a tu **GitHub** (para guardar el trabajo).
- El catálogo publicado en internet, en una dirección como `https://TU-USUARIO.github.io/agata/`.

Tiempo aproximado: 30–45 minutos de configuración tuya + el tiempo que Claude trabaja (puede ser 1–2 horas).

> **Atajo opcional:** ya existe una versión terminada en https://github.com/agatabeautycol/Agata. Si prefieres partir de ella en vez de desde cero, en el Paso 3 usa **https://github.com/new/import**, pega `https://github.com/agatabeautycol/Agata` como origen y ponle de nombre `agata`. Luego sigue la guía igual (el prompt detecta que ya hay código y lo mejora en lugar de rehacerlo).

---

## PARTE 1 — Preparación paso a paso (lo haces tú)

### Paso 1. Cuenta de Claude

1. Entra a **https://claude.ai** e inicia sesión (o crea tu cuenta).
2. Claude Code en la web necesita un **plan de pago (Pro o Max)**. Si no lo tienes: tu foto/nombre abajo a la izquierda → **Settings → Billing** → elige el plan.

### Paso 2. Cuenta de GitHub

1. Entra a **https://github.com/signup** y crea tu cuenta gratis (correo, contraseña y un **nombre de usuario**; anótalo, aparecerá en la dirección del catálogo).
2. Confirma tu correo con el código que te llega.

### Paso 3. Crear el repositorio (la "carpeta" del proyecto en GitHub)

1. Entra a **https://github.com/new**.
2. **Repository name:** `agata` (en minúsculas, sin tildes ni espacios). **Este nombre aparecerá en la dirección del catálogo y no conviene cambiarlo después.**
3. Marca **Public** (la publicación gratuita en GitHub Pages necesita que sea público).
4. Marca **Add a README file** (para que el repositorio no quede vacío).
5. Toca **Create repository**.

> **Qué es git / GitHub, en simple:** GitHub guarda tu proyecto y cada cambio que se hace (quién, cuándo y por qué), como un historial de versiones de Word. Si algo sale mal, siempre se puede volver atrás. Claude se encarga de usarlo; tú solo das permisos y apruebas.

### Paso 4. Conectar GitHub con Claude

1. Entra a **https://claude.ai/connect-github** y toca **Connect** / **Conectar**.
2. GitHub te pedirá autorizar a Claude: toca **Authorize**.
3. Te pedirá **instalar la app de Claude**: elige tu cuenta, marca **Only select repositories**, elige **agata** y toca **Install**.

### Paso 5. Conectar Canva con Claude

1. Entra a **https://claude.ai/customize/connectors**.
2. Busca **Canva** y toca **Connect** / **Conectar**.
3. Inicia sesión en Canva con **la cuenta donde está el catálogo** y toca **Permitir / Allow**.
4. Comprueba que Canva aparece como **conectado**.

> Haz este paso **antes** de abrir la sesión de Claude Code: los conectores se cargan cuando la sesión empieza. Si conectas Canva después, abre una sesión nueva.

### Paso 6. Junta lo que Claude no puede sacar solo

Prepara esto en una carpeta de tu computador (no hace falta todo; con lo que tengas basta):

1. **El catálogo exportado de Canva** (por si el conector no puede exportarlo): en Canva → **Compartir → Descargar → PDF para impresión**. Si pesa mucho, descárgalo por partes con **Seleccionar páginas** (por ejemplo, de 30 en 30).
2. **Fotos originales de los productos en buena calidad** (mínimo 800 × 800 px), si las tienes. Las fotos que se subieron a Canva eran pequeñas y se ven borrosas en la web; las originales lo solucionan.
3. **Enlaces de las páginas oficiales de las marcas** (tiendas donde aparecen los productos), en una lista. Ejemplo: `https://montoccosmetictools.com/products/glow-filter`.

### Paso 7. Abrir Claude Code y darle acceso a internet

1. Entra a **https://claude.ai/code**.
2. Crea una sesión nueva y, en el selector de repositorio, elige **TU-USUARIO/agata**.
3. **Acceso a internet:** en la barra de arriba de la sesión abre el menú del **entorno** → **Edit** → **Network access**:
   - Lo más sencillo mientras dura el proyecto: elige el nivel de acceso **amplio / completo** (Full).
   - Si prefieres restringirlo: en **Allowed domains** agrega `canva.com`, `canva.link`, `cdn.shopify.com`, `fonts.googleapis.com`, `fonts.gstatic.com` y el dominio de cada página de marca de tu lista (la parte entre `https://` y la primera `/`). Deja marcada **Allow package managers**.
   - Guía oficial: https://code.claude.com/docs/en/cloud-environments#network-access
4. Si cambias el acceso a internet, **abre una sesión nueva** para que tome efecto.

### Paso 8. Pegar el prompt

1. Copia **todo** el bloque de la PARTE 2 (en GitHub: pasa el mouse sobre el bloque y toca el ícono de copiar ⧉ arriba a la derecha).
2. Pégalo en la sesión de Claude Code.
3. Si tienes el PDF o fotos, **adjúntalos en el mismo mensaje** (botón de adjuntar 📎 o arrastrándolos). Si el PDF pesa más de lo que deja adjuntar, envíalo por partes en mensajes seguidos.
4. Al final del mensaje, donde dice "DATOS QUE YO TENGO", completa lo que sepas (enlace de Canva, enlaces de marcas, tu usuario de GitHub).
5. Envía. Claude trabaja por fases y **te va a pedir aprobación** después de la auditoría (Fase 1): revisa lo que te muestra y responde "sí, continúa" o lo que quieras cambiar.
6. Cuando Claude pida permiso para ejecutar algo o para usar Canva/GitHub, acepta (**Allow**).

### Paso 9. Aprobar los cambios en GitHub (Pull Request)

Claude trabaja en una rama aparte y al final abre un **Pull Request** (una propuesta de cambios) para que tú la apruebes:

1. Abre el enlace que te dé Claude (o entra a `https://github.com/TU-USUARIO/agata/pulls`).
2. Revisa el resumen y toca **Merge pull request → Confirm merge**.
3. Esto pasa los cambios a la versión principal (`main`).

### Paso 10. Publicar el catálogo en internet (una sola vez)

1. Entra a `https://github.com/TU-USUARIO/agata/settings/pages`.
2. En **Build and deployment → Source** elige **Deploy from a branch**.
3. En **Branch** elige **main** y la carpeta **/ (root)**. Toca **Save**.
4. Espera 2 minutos y recarga: arriba aparecerá **"Your site is live at https://TU-USUARIO.github.io/agata/"**.
5. Esa es la dirección para compartir con tus clientes. Ábrela en el celular (la primera vez, mejor en una pestaña de incógnito).

### Para futuros cambios

Abre una sesión nueva en **https://claude.ai/code** con el repositorio **agata**, pide el cambio (por ejemplo, *"actualiza los precios con el nuevo catálogo de Canva"*) y repite los pasos 9 y 10 (el 10 ya queda activo; solo haz el merge).

### Lo que NO debes hacer

- No cambies el nombre del repositorio ni de la rama `main` después de publicar: la dirección del catálogo deja de funcionar.
- No subas el PDF de Canva directamente a GitHub (GitHub no acepta archivos de más de 100 MB).
- No borres archivos desde GitHub.

---

## PARTE 2 — Prompt para pegar en Claude Code

```text
Hola, Claude. Soy de Ágata Beauty y no tengo conocimientos técnicos: explícame en español y con palabras
sencillas lo que haces en cada fase, y pregúntame antes de tomar decisiones que cambien el contenido.

# Objetivo
Convertir el catálogo de productos que tengo en Canva en un CATÁLOGO DIGITAL INTERACTIVO (página web)
que conserve la identidad visual de Ágata Beauty y permita BUSCAR, FILTRAR y CONSULTAR productos sin pasar
página por página. Publicarlo gratis con GitHub Pages desde este repositorio.

# Herramientas y accesos
- Repositorio de GitHub de esta sesión (lo creé con un README). Si ya tiene código (p. ej. importado de
  https://github.com/agatabeautycol/Agata), no lo rehagas: revísalo, actualízalo con mi Canva y mejóralo.
- Conector de Canva: úsalo para buscar el diseño del catálogo (se llama algo como "Catálogo AGATA Beauty"),
  leer sus páginas y exportarlo en la MAYOR calidad posible (PDF para impresión y/o PNG). Si el conector no
  está disponible o no puede exportar, dímelo en una línea y usa el PDF que adjunte.
- Si una página web o una descarga está bloqueada por la red del entorno, dime EXACTAMENTE qué dominio debo
  agregar en Network access y sigue con lo que no dependa de eso.
- Archivos que adjunte en el chat (PDF del catálogo, fotos originales de productos).

# Reglas de oro (no negociables)
1. NO inventes nada: ni productos, ni precios, ni descripciones, ni categorías, ni datos de contacto.
   Si falta un dato, márcalo como [INFORMACIÓN PENDIENTE] y sigue.
2. NO uses imágenes generadas ni modificadas con IA. Las fotos de productos son reales. Solo se permite
   recortar, redimensionar, centrar, convertir a WebP y comprimir. No quites fondos con IA ni "mejores" la
   nitidez artificialmente.
3. Conserva los textos del catálogo tal cual. Si detectas erratas, muéstramelas en una lista y corrígelas
   SOLO si te lo autorizo (deja la lista de correcciones en el código para que se apliquen siempre).
4. Prioridad ante dudas de diseño: 1) identidad de Ágata Beauty, 2) legibilidad, 3) experiencia de usuario,
   4) celular, 5) rendimiento.
5. Archivos de más de 100 MB no van a GitHub (agrega el PDF al .gitignore).

# FASE 1 — Auditoría (NO programes todavía)
Analiza el catálogo completo y entrégame un diagnóstico:
- Número de páginas y qué hay en cada tipo de página (portada, proceso de compra, páginas de productos…).
- Marcas, secciones/categorías y cantidad de productos por cada una.
- Datos por producto (nombre, marca, sección, precio, precios por tamaño/tono, descripción, referencia).
- Datos de contacto y canal de compra REALES (WhatsApp, Instagram…), y el texto del proceso de compra.
- Paleta de colores (medida sobre el diseño, en hexadecimal), tipografías usadas y elementos gráficos que
  se repiten (marcos, círculos, divisores, adornos).
- Calidad real de las fotos: resolución en píxeles de cada foto dentro del diseño; avísame cuáles son
  menores de 800 px y propón de dónde obtenerlas en alta resolución.
- Problemas: fotos repetidas o que no corresponden al producto, erratas, productos sin sección, datos faltantes.
Cómo extraer los datos del PDF de forma confiable (lección aprendida): usa PyMuPDF (pip install pymupdf
pillow) y lee cada texto con su posición, tipografía y color: en Canva cada tipo de texto usa una fuente
distinta (título de marca, sección, nombre/precio, descripción). Agrupa textos y fotos por el marco de cada
tarjeta de producto. Verifica visualmente renderizando las páginas a PNG.
Datos verificados en una versión anterior (compruébalos contra MI Canva; si cambiaron, manda Canva):
- Marca: "ÁGATA beauty" (Ágata Beauty). Lema: "Belleza que nace del amor". "Makeup • Skincare • Selfcare".
- Instagram @agatabeauty_ · WhatsApp 3135496268 (Colombia, +57).
- Página 2: "Proceso de compra" en 5 pasos (Elige tus favoritos, Escríbenos, ¿No encuentras lo que buscas?,
  Confirmamos tu pedido, Realiza tu pago: transferencia o efectivo) + aviso IMPORTANTE de disponibilidad.
Al terminar la Fase 1, MUÉSTRAME EL DIAGNÓSTICO Y ESPERA MI APROBACIÓN antes de seguir.

# FASE 2 — Modelo de datos
- data/products.json como ÚNICA fuente de datos, separada del diseño:
  { brand: {nombre, lema, contacto, proceso de compra}, pages: [...], products: [...] }.
- Cada producto: id estable "marca-página-posición" (p. ej. montoc-003-1), name, brand, category,
  section (la original del catálogo), price (número, el menor), variants [{label, price}] si hay varios
  precios, presentation, description, details, image, imageWidth, imageHeight, imageAlt, gallery (fotos de
  tonos/variantes que aparezcan en la tarjeta), page. Los campos solo existen si el dato existe.
- CATEGORÍAS UNIFICADAS: el catálogo repite secciones con nombres distintos ("Ojos", "Cejas", "Cejas y ojos",
  "Ojos y cejas"…). Propónme una lista corta de categorías (referencia: Rostro, Ojos y cejas, Labios,
  Preparación y fijación, Brochas/accesorios/kits, Cuidado facial, Cuidado capilar, Cuidado corporal),
  asigna TODOS los productos (también los que no tienen sección, por su tipo) y muéstrame la tabla para
  aprobarla. Guarda la sección original en "section".
- Escribe un script reproducible (scripts/extract-catalog.py) que regenere data/products.json, las fotos y
  las páginas desde el PDF, con las correcciones aprobadas (erratas, categorías, fotos pendientes) en
  diccionarios al inicio del script, para que nada se pierda al actualizar el catálogo.
- Genera docs/PRODUCTOS.md con la tabla: ID | Producto | Marca | Categoría | Referencia | Precio | Imagen | Página.

# FASE 3 — Arquitectura
HTML5 + CSS3 + JavaScript moderno (módulos ES), sin frameworks ni compilación. Estructura:
index.html · 404.html · .nojekyll · css/styles.css · css/responsive.css · js/app.js · js/products.js ·
js/search.js · js/filters.js · js/state.js · js/ui.js · data/products.json · assets/images/productos/ ·
assets/images/decor/ · assets/catalog/ (páginas) · assets/icons/ · scripts/ · docs/ · catalogo-original/.
Explícame la arquitectura en pocas líneas y sigue.

# FASE 4 — Implementación (funciones obligatorias)
- Portada que replique la portada del catálogo (logo, lema, contacto con los íconos del catálogo) con un
  botón "Explorar catálogo".
- Buscador instantáneo que no distinga tildes ni mayúsculas y exija todas las palabras ("shampoo niños").
  Busca en nombre, marca, categoría, presentación, descripción y variantes.
- Filtro por CATEGORÍA (botones con contador) y por MARCA (fila de botones visible con contador).
  Cada contador tiene en cuenta los demás filtros.
- Productos AGRUPADOS POR MARCA por defecto (título de marca con el estilo del catálogo, como sus
  páginas), con opción "Agrupar por categoría" y "Sin agrupar".
- Orden: catálogo, nombre A-Z/Z-A, precio menor/mayor. Contador "Mostrando X de Y productos".
  Estado sin resultados con "Limpiar búsqueda".
- Tarjetas como las del catálogo: foto en círculo con anillo cobrizo, nombre, divisor con estrella,
  precio o lista de precios por tamaño/tono, botón "Ver producto".
- Detalle en ventana modal (pantalla completa en celular): foto grande, marca, categoría, nombre, precios,
  descripción, fotos de tonos, botón "Comprar / Solicitar producto" que abre WhatsApp con el nombre y la
  marca del producto en el mensaje, aviso de disponibilidad del proceso de compra, botón
  "← Volver al catálogo" y enlace "Ver en el catálogo original (página N)".
- "Vista catálogo": las páginas originales exportadas, con índice para saltar por marca y botones para
  abrir los productos de cada página.
- Secciones "Cómo comprar" (proceso de compra real) y "Contacto".
- Búsqueda, filtros, agrupación, orden, vista y producto abierto se guardan en la URL: el botón "atrás"
  del navegador no pierde los filtros y se pueden compartir enlaces a un producto.
- 404.html con la marca que redirija al catálogo. .nojekyll en la raíz.
- Ofertas: solo si existen en el catálogo.
Identidad visual:
- Fuentes del logo de Google Fonts si coinciden (en la versión anterior: Cormorant Garamond + Dancing
  Script). Las fuentes con licencia de Canva (The Seasons, Garet, Mont…) reemplázalas por equivalentes
  libres (p. ej. Poppins) y dímelo.
- Colores medidos sobre el diseño, definidos como variables CSS en un solo bloque.
- Anillo cobrizo del círculo dibujado en CSS (degradado medido alrededor del círculo), NO como imagen,
  para que se vea nítido. Adornos (labial, brocha, trazos, estrellas, íconos) extraídos del PDF.
Fotos (lección aprendida):
- El "PDF estándar" de Canva reduce las fotos a ~90 dpi y se ven borrosas. Usa la mayor resolución
  disponible: 1) fotos originales que adjunte, 2) fotos oficiales de las páginas de marcas que te dé
  (en tiendas Shopify puedes leer /products/<handle>.json), 3) exportación de Canva en máxima calidad.
- Cada foto debe ser EXACTAMENTE el mismo producto y presentación; compárala con la del catálogo y, si hay
  duda, pregúntame. Guarda el origen de cada foto en "imageSource".
- Recorta a la resolución nativa (sin ampliar y volver a reducir), WebP calidad ~90, lienzo cuadrado con
  el producto centrado y margen para el círculo. Si la foto del catálogo es de otro producto, muestra
  "Foto pendiente" en lugar de una foto equivocada.
- Imágenes con loading="lazy", width/height definidos e imagen de respaldo si alguna falla.

# FASE 5 — Validación visual
Compara el resultado con el catálogo (colores, tipografías, fotos, composición, textos, nombres) y
muéstrame capturas de portada, tarjetas y detalle en celular (390×844) y computador (1280×900).

# FASE 6 — Pruebas (UX)
Sirve el sitio localmente (python3 -m http.server) y prueba con Playwright/Chromium en celular y
computador: búsqueda (con y sin tildes), filtros, agrupación, orden, detalle, Esc y "Volver", botón atrás
del navegador, enlace directo a un producto, vista catálogo, estado sin resultados, que todas las imágenes
carguen (sin 404), sin errores de JavaScript y sin scroll horizontal en celular.

# FASE 7 — Optimización
Rendimiento (peso de imágenes y páginas), SEO (title, meta description, Open Graph con la portada,
favicon, H1/H2/H3), accesibilidad (HTML semántico, ALT descriptivos, contraste, teclado, foco visible,
ARIA donde haga falta, respeto de "reducir movimiento").

# Documentación
- README.md en español: cómo verlo localmente, estructura, cómo agregar/editar productos en
  data/products.json y cómo regenerar todo desde un PDF nuevo de Canva.
- docs/AUDITORIA.md: diagnóstico, decisiones, erratas corregidas, categorías, calidad de fotos y pendientes.
- docs/PRODUCTOS.md: tabla de productos.

# Git y publicación
- Trabaja en la rama de esta sesión, con commits pequeños y claros en español (por fase).
- Al terminar, abre un Pull Request hacia "main" con un resumen en español y dame el enlace.
- Luego dime, paso a paso, cómo hacer el merge y cómo activar GitHub Pages (Settings → Pages →
  Deploy from a branch → main → / (root)), y cuál será la dirección final del catálogo.
- Después de que yo haga el merge y active Pages, verifica en GitHub Actions que "pages build and
  deployment" termine en verde.
- No cambies nombres de repositorio ni de ramas existentes, no hagas force-push.

# Entrega final
1. Dirección pública del catálogo.
2. Resumen: número de productos, marcas y categorías; qué fotos se reemplazaron en alta resolución y cuáles
   faltan (por marca); erratas corregidas; datos pendientes.
3. Lista corta de lo que debo revisar o conseguir.

# DATOS QUE YO TENGO (completa o borra)
- Mi usuario de GitHub:
- Enlace o nombre del diseño en Canva:
- Enlaces de páginas oficiales de las marcas:
- Adjunto: (PDF del catálogo / fotos originales / nada)
```
