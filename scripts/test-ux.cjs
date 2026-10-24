// Pruebas de UX del catálogo con Playwright (celular 390×844 y computador 1280×900).
// Uso: python3 -m http.server 8765  y luego  node scripts/test-ux.cjs http://localhost:8765/ carpeta-capturas
const { chromium } = require('playwright');
const BASE = process.argv[2] || 'http://localhost:8765/';
const OUT = process.argv[3] || '.';
const results = [];
const check = (name, ok, extra = '') => { results.push({ name, ok, extra }); console.log(`${ok ? 'OK  ' : 'FALLA'} ${name} ${extra}`); };

async function run(viewport, label) {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport, deviceScaleFactor: label === 'celular' ? 2 : 1 });
  const page = await ctx.newPage();
  const errors = [], bad = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
  page.on('response', (r) => r.status() >= 400 && bad.push(`${r.status()} ${r.url()}`));
  const count = async () => page.locator('#catalogo .product-card').count();
  const resultText = async () => (await page.locator('[data-result-count]').textContent()).trim();

  await page.goto(BASE, { waitUntil: 'networkidle' });
  await page.screenshot({ path: `${OUT}/${label}-portada.png` });
  const total = await count();
  check(`[${label}] carga los 249 productos`, total === 249, `(${total})`);
  check(`[${label}] contador inicial`, /249 de 249/.test(await resultText()), await resultText());

  // Sin scroll horizontal
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  check(`[${label}] sin scroll horizontal`, overflow <= 0, `(${overflow}px)`);

  // Búsqueda con y sin tildes
  const search = page.locator('[data-search-input]');
  await search.fill('nino'); await page.waitForTimeout(300);
  const a = await count();
  await search.fill('niño'); await page.waitForTimeout(300);
  const b = await count();
  check(`[${label}] búsqueda sin tildes = con tildes ("nino"/"niño")`, a === b && a > 0, `(${a}/${b})`);
  await search.fill('SHAMPOO niños'); await page.waitForTimeout(300);
  const c = await count();
  const names = await page.locator('#catalogo .card-title').allTextContents();
  check(`[${label}] varias palabras ("SHAMPOO niños")`, c > 0 && names.every((n) => /shampoo/i.test(n)), `(${c}: ${names.join(' | ')})`);
  await search.fill('acne'); await page.waitForTimeout(300);
  check(`[${label}] busca en descripciones ("acne")`, (await count()) > 0, `(${await count()})`);
  await search.fill('750 ml'); await page.waitForTimeout(300);
  check(`[${label}] busca en variantes ("750 ml")`, (await count()) > 0, `(${await count()})`);

  // Estado sin resultados
  await search.fill('xyzinexistente'); await page.waitForTimeout(300);
  check(`[${label}] estado sin resultados visible`, await page.locator('[data-empty]').isVisible());
  await page.locator('[data-clear]').click();
  check(`[${label}] "Limpiar búsqueda" restaura todo`, (await count()) === 249 && (await search.inputValue()) === '');

  // Filtros con contadores cruzados
  await page.locator('[data-categories] [data-category="labios"]').click();
  const labios = await count();
  check(`[${label}] filtro categoría Labios`, labios === 16, `(${labios})`);
  const brandChip = await page.locator('[data-brands] [data-brand="bloomshell"] .chip-count').textContent();
  check(`[${label}] contador de marca respeta la categoría`, /\(2\)/.test(brandChip), brandChip.trim());
  await page.locator('[data-brands] [data-brand="bloomshell"]').click();
  check(`[${label}] filtro categoría + marca`, (await count()) === 2, `(${await count()})`);
  await page.screenshot({ path: `${OUT}/${label}-filtros.png` });

  // Botón atrás del navegador conserva filtros
  await page.goBack();
  await page.waitForTimeout(200);
  check(`[${label}] atrás: vuelve a solo categoría`, (await count()) === 16 && page.url().includes('cat=labios'), page.url());
  await page.goBack();
  await page.waitForTimeout(200);
  check(`[${label}] atrás: sin filtros`, (await count()) === 249);

  // Agrupación
  const groupTitles = async () => page.locator('#catalogo .group-title, #catalogo .product-group > h3, #catalogo .product-group h3.brand-title').allTextContents();
  check(`[${label}] agrupado por marca por defecto`, (await page.locator('#catalogo .product-group').count()) === 27, `(${await page.locator('#catalogo .product-group').count()} grupos)`);
  await page.selectOption('[data-group-select]', 'categoria');
  check(`[${label}] agrupar por categoría`, (await page.locator('#catalogo .product-group').count()) === 8, `(${await page.locator('#catalogo .product-group').count()})`);
  await page.selectOption('[data-group-select]', 'no');
  check(`[${label}] sin agrupar`, (await page.locator('#catalogo .product-group').count()) <= 1);

  // Orden por precio
  await page.selectOption('[data-sort-select]', 'price-asc');
  const firstCheap = (await page.locator('#catalogo .card-title').first().textContent()).trim();
  await page.selectOption('[data-sort-select]', 'price-desc');
  const firstExp = (await page.locator('#catalogo .card-title').first().textContent()).trim();
  check(`[${label}] orden por precio`, firstCheap !== firstExp, `(menor: ${firstCheap} · mayor: ${firstExp})`);
  await page.selectOption('[data-sort-select]', 'name-asc');
  const n1 = (await page.locator('#catalogo .card-title').first().textContent()).trim();
  const allN = await page.locator('#catalogo .card-title').allTextContents();
  const coll = new Intl.Collator('es', { sensitivity: 'base', numeric: true });
  check(`[${label}] orden A-Z`, allN.every((x, i) => i === 0 || coll.compare(allN[i - 1], x) <= 0), `(primero: ${n1})`);
  await page.goto(BASE, { waitUntil: 'networkidle' });

  // Tarjetas (captura)
  await page.locator('#catalogo .product-card').first().scrollIntoViewIfNeeded();
  await page.evaluate(() => window.scrollBy(0, -80));
  await page.waitForTimeout(400);
  await page.screenshot({ path: `${OUT}/${label}-tarjetas.png` });

  // Detalle, Esc y Volver
  await page.locator('#catalogo [data-open="montoc-003-2"]').click();
  const dialog = page.locator('dialog[open]');
  check(`[${label}] abre el detalle`, await dialog.isVisible());
  check(`[${label}] URL del producto`, page.url().includes('producto=montoc-003-2'));
  const wa = await dialog.locator('a[href*="wa.me"]').getAttribute('href');
  check(`[${label}] WhatsApp con producto y marca`, wa.startsWith('https://wa.me/573135496268') && decodeURIComponent(wa).includes('Polvos Translúcidos') && decodeURIComponent(wa).includes('Montoc'), decodeURIComponent(wa));
  check(`[${label}] enlace a página original`, (await dialog.textContent()).includes('página 3'));
  await page.waitForTimeout(300);
  await page.screenshot({ path: `${OUT}/${label}-detalle.png` });
  await page.keyboard.press('Escape');
  await page.waitForTimeout(200);
  check(`[${label}] Esc cierra el detalle`, (await page.locator('dialog[open]').count()) === 0 && !page.url().includes('producto='));
  await page.locator('#catalogo [data-open="johnsons-120-1"]').click();
  await page.locator('dialog[open] [data-close]').click();
  await page.waitForTimeout(200);
  check(`[${label}] "← Volver al catálogo" cierra`, (await page.locator('dialog[open]').count()) === 0);
  await page.locator('#catalogo [data-open="johnsons-120-1"]').click();
  await page.goBack();
  await page.waitForTimeout(200);
  check(`[${label}] atrás del navegador cierra el detalle`, (await page.locator('dialog[open]').count()) === 0);

  // Tonos: al elegir uno, su foto grande reemplaza la principal; al desmarcarlo vuelve la original
  await page.goto(`${BASE}?producto=montoc-007-2`, { waitUntil: 'networkidle' });
  const mainImg = page.locator('dialog[open] .detail-media img');
  const original = await mainImg.getAttribute('src');
  const shade = page.locator('dialog[open] .shade').nth(2);
  await shade.click();
  await page.waitForTimeout(300);
  const swapped = await mainImg.getAttribute('src');
  const loaded = await mainImg.evaluate((i) => i.complete && i.naturalWidth > 0);
  check(`[${label}] tono: su foto reemplaza la principal`, swapped !== original && swapped.includes('tonos/') && loaded, swapped);
  check(`[${label}] tono: nombre bajo la foto y en WhatsApp`, (await page.locator('dialog[open] .detail-media-caption').textContent()).includes('Sabor')
    && decodeURIComponent(await page.locator('dialog[open] .btn-whatsapp').getAttribute('href')).includes('sabor'));
  await shade.click();
  await page.waitForTimeout(200);
  check(`[${label}] tono: al desmarcar vuelve la foto del catálogo`, (await mainImg.getAttribute('src')) === original);
  await page.keyboard.press('Escape');

  // Enlace directo
  await page.goto(`${BASE}?producto=anyeluz-093-1`, { waitUntil: 'networkidle' });
  check(`[${label}] enlace directo a producto`, await page.locator('dialog[open]').isVisible());
  await page.goto(`${BASE}?q=shampoo&cat=cuidado-capilar&orden=price-asc`, { waitUntil: 'networkidle' });
  check(`[${label}] enlace con filtros restaura estado`, (await search.inputValue()) === 'shampoo' && (await count()) > 0, `(${await count()})`);

  // Vista catálogo
  await page.goto(`${BASE}?vista=catalogo`, { waitUntil: 'networkidle' });
  const pages = await page.locator('.catalog-page').count();
  check(`[${label}] vista catálogo con todas las páginas`, pages === 132, `(${pages})`);
  await page.locator('[data-page-index] [data-goto-page]').filter({ hasText: 'Anyeluz' }).click();
  await page.waitForTimeout(600);
  await page.screenshot({ path: `${OUT}/${label}-vista-catalogo.png` });
  const btn = page.locator('#pagina-93 [data-open]').first();
  await btn.click();
  check(`[${label}] botón de página abre producto`, await page.locator('dialog[open]').isVisible());
  await page.keyboard.press('Escape');

  // Cómo comprar y contacto
  await page.goto(BASE, { waitUntil: 'networkidle' });
  check(`[${label}] sección Cómo comprar (5 pasos)`, (await page.locator('[data-process-steps] > li').count()) === 5);
  check(`[${label}] sección Contacto visible`, await page.locator('#contacto').isVisible());
  await page.locator('#como-comprar').scrollIntoViewIfNeeded();
  await page.screenshot({ path: `${OUT}/${label}-como-comprar.png` });

  // Todas las imágenes cargan: recorrer la página para disparar lazy loading
  const height = await page.evaluate(() => document.body.scrollHeight);
  for (let y = 0; y < height; y += viewport.height) { await page.evaluate((v) => window.scrollTo(0, v), y); await page.waitForTimeout(40); }
  await page.waitForLoadState('networkidle');
  const broken = await page.evaluate(() => [...document.images].filter((i) => i.complete && i.naturalWidth === 0 || i.classList.contains('is-fallback')).map((i) => i.src));
  check(`[${label}] todas las imágenes cargan`, broken.length === 0, broken.slice(0, 5).join(' '));
  // Vista catálogo: imágenes de páginas
  await page.goto(`${BASE}?vista=catalogo`, { waitUntil: 'networkidle' });
  const h2 = await page.evaluate(() => document.body.scrollHeight);
  for (let y = 0; y < h2; y += viewport.height * 2) { await page.evaluate((v) => window.scrollTo(0, v), y); await page.waitForTimeout(20); }
  await page.waitForLoadState('networkidle');
  const broken2 = await page.evaluate(() => [...document.images].filter((i) => i.complete && i.naturalWidth === 0).map((i) => i.src));
  check(`[${label}] imágenes de la vista catálogo cargan`, broken2.length === 0, broken2.slice(0, 5).join(' '));

  // 404.html
  const r = await page.goto(`${BASE}404.html`, { waitUntil: 'networkidle' });
  check(`[${label}] página 404 con la marca`, (await page.content()).includes('ÁGATA'));

  check(`[${label}] sin errores de JavaScript`, errors.length === 0, errors.slice(0, 3).join(' | '));
  check(`[${label}] sin archivos 404 (excepto la prueba de 404)`, bad.filter((u) => !u.includes('no-existe')).length === 0, bad.filter((u) => !u.includes('no-existe')).slice(0, 5).join(' '));
  await browser.close();
}

(async () => {
  await run({ width: 390, height: 844 }, 'celular');
  await run({ width: 1280, height: 900 }, 'computador');
  const fails = results.filter((r) => !r.ok);
  console.log(`\n${results.length - fails.length}/${results.length} pruebas correctas`);
  process.exit(fails.length ? 1 : 0);
})();
