// Renderizado de la interfaz. Todo el contenido proveniente de datos se inserta
// con textContent / atributos (nunca innerHTML) para evitar inyección de HTML.

import { normalizeText } from './search.js';

const FALLBACK_IMAGE = 'assets/images/placeholder.svg';
const DEFAULT_IMAGE_SIZE = { width: 600, height: 600 };

export const $ = (selector, root = document) => root.querySelector(selector);
export const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (value === undefined || value === null || value === false) continue;
    if (key === 'class') node.className = value;
    else if (key === 'text') node.textContent = value;
    else if (key === 'dataset') Object.assign(node.dataset, value);
    else node.setAttribute(key, value === true ? '' : value);
  }
  for (const child of [].concat(children)) {
    if (child) node.append(child);
  }
  return node;
}

// "Tono" / "Tonos", "Sabor" / "Sabores"… según cómo llama la marca a las opciones.
const PLURALS = { Tono: 'Tonos', Color: 'Colores', Sabor: 'Sabores', Estilo: 'Estilos', Aroma: 'Aromas', 'Versión': 'Versiones' };
function shadeWord(product, count = 1) {
  const word = product.shadesLabel ?? 'Tono';
  return count === 1 ? word : PLURALS[word] ?? `${word}s`;
}

const divider = () => el('span', { class: 'divider', 'aria-hidden': 'true' });

/** "$57.000", igual que en el catálogo. */
export function money(value, brand) {
  return `${brand.currencySymbol ?? '$'}${value.toLocaleString('es-CO', { maximumFractionDigits: 2 })}`;
}

export function formatPrice(product, brand) {
  if (product.priceText) return product.priceText;
  if (typeof product.price !== 'number') return null;
  return product.variants.length > 1 ? `Desde ${money(product.price, brand)}` : money(product.price, brand);
}

function variantList(product, brand, className) {
  if (!product.variants.length) return null;
  return el('ul', { class: className }, product.variants.map((v) =>
    el('li', {}, [v.label ? `${v.label}: ` : '', el('strong', { text: money(v.price, brand) })])));
}

/** Muestra la presentación solo si no está ya escrita en el nombre ("… x 450 ml"). */
function presentationIfNew(product) {
  if (!product.presentation) return null;
  const compact = (t) => normalizeText(t).replace(/\s+/g, '');
  return compact(product.name).includes(compact(product.presentation)) ? null : product.presentation;
}

/** Imagen con lazy loading, dimensiones fijas, srcset y fallback si no carga. */
function productImage(product, { large = false } = {}) {
  // Foto equivocada en el catálogo original: se muestra un aviso en vez de una foto que no corresponde.
  if (product.imagePending) {
    return el('div', { class: 'photo-pending', role: 'img', 'aria-label': `${product.name}: foto pendiente` }, [
      el('span', { text: 'Foto pendiente' }),
    ]);
  }
  const width = product.imageWidth ?? DEFAULT_IMAGE_SIZE.width;
  const height = product.imageHeight ?? DEFAULT_IMAGE_SIZE.height;
  const src = (large ? product.image : product.imageSmall ?? product.image) || FALLBACK_IMAGE;
  const img = el('img', {
    src,
    alt: product.imageAlt ?? product.name,
    width,
    height,
    loading: large ? 'eager' : 'lazy',
    decoding: 'async',
    srcset: !large && product.imageSmall && product.image ? `${product.imageSmall} 320w, ${product.image} 640w` : null,
    sizes: !large && product.imageSmall ? '(min-width: 1100px) 240px, (min-width: 640px) 30vw, 45vw' : null,
  });
  img.addEventListener('error', () => {
    if (img.src.endsWith(FALLBACK_IMAGE)) return;
    img.removeAttribute('srcset');
    img.src = FALLBACK_IMAGE;
    img.classList.add('is-fallback');
  }, { once: true });
  return img;
}

/* ---------- Tarjetas ---------- */

function productCard(product, brand) {
  const single = product.variants.length === 0 ? formatPrice(product, brand) : null;
  return el('li', { class: 'product-card' }, [
    product.brand ? el('p', { class: 'card-brand brand-title', text: product.brand }) : null,
    product.category ? el('p', { class: 'card-category', text: product.category }) : null,
    el('div', { class: 'card-media' }, [
      productImage(product),
      product.offer ? el('span', { class: 'badge', text: typeof product.offer === 'string' ? product.offer : 'Oferta' }) : null,
    ]),
    el('div', { class: 'card-body' }, [
      el('h3', { class: 'card-title', text: product.name }),
      divider(),
      presentationIfNew(product) ? el('p', { class: 'card-meta', text: presentationIfNew(product) }) : null,
      product.reference ? el('p', { class: 'card-meta', text: `Ref. ${product.reference}` }) : null,
      product.shades.length ? el('p', { class: 'card-shades', text: `${product.shades.length} ${shadeWord(product, product.shades.length).toLowerCase()}` }) : null,
      single ? el('p', { class: 'card-price', text: single }) : variantList(product, brand, 'card-variants'),
      el('button', {
        type: 'button',
        class: 'btn btn-primary btn-block',
        dataset: { open: product.id },
        'aria-label': `Ver producto: ${product.name}${product.brand ? `, ${product.brand}` : ''}`,
        text: 'Ver producto',
      }),
    ]),
  ]);
}

function productList(products, brand) {
  return el('ul', { class: 'product-grid' }, products.map((p) => productCard(p, brand)));
}

/**
 * Pinta los productos, agrupados por marca o por categoría (con título y cantidad, como las páginas
 * del catálogo) o en una sola lista. Los grupos respetan el orden de aparición en el catálogo.
 */
export function renderGrid(container, products, brand, groupBy) {
  const key = { marca: 'brand', categoria: 'category' }[groupBy];
  container.dataset.group = key ? groupBy : 'no';
  if (!key) {
    container.replaceChildren(productList(products, brand));
    return;
  }
  const groups = new Map();
  for (const product of products) {
    const name = product[key] || 'Otros';
    if (!groups.has(name)) groups.set(name, []);
    groups.get(name).push(product);
  }
  container.replaceChildren(...[...groups].map(([name, items]) =>
    el('section', { class: 'product-group', 'aria-label': `${name}, ${items.length} producto${items.length === 1 ? '' : 's'}` }, [
      el('div', { class: 'group-head' }, [
        el('h3', { class: 'group-title brand-title', text: name }),
        el('span', { class: 'group-count', text: `${items.length} producto${items.length === 1 ? '' : 's'}` }),
      ]),
      el('span', { class: 'divider', 'aria-hidden': 'true' }),
      productList(items, brand),
    ])));
}

/* ---------- Filtros ---------- */

export function renderCategories(container, categories, counts, total, active) {
  const chip = (slug, label, count) =>
    el('button', {
      type: 'button',
      class: 'chip',
      dataset: { category: slug },
      'aria-pressed': String(active === slug),
      disabled: Boolean(slug) && !count && active !== slug,
    }, [label, el('span', { class: 'chip-count', text: ` (${count})` })]);

  container.replaceChildren(
    chip('', 'Todas', total),
    ...categories.map((c) => chip(c.slug, c.name, counts.get(c.slug) ?? 0)),
  );
}

export function renderBrands(container, brands, counts, total, active) {
  const chip = (slug, label, count) =>
    el('button', {
      type: 'button',
      class: 'chip',
      dataset: { brand: slug },
      'aria-pressed': String(active === slug),
      disabled: Boolean(slug) && !count && active !== slug,
    }, [label, el('span', { class: 'chip-count', text: ` (${count})` })]);

  container.replaceChildren(
    chip('', 'Todas', total),
    ...brands.map((b) => chip(b.slug, b.name, counts.get(b.slug) ?? 0)),
  );
}

/* ---------- Detalle ---------- */

function detailRow(label, value) {
  if (!value) return null;
  return el('div', { class: 'detail-row' }, [el('dt', { text: label }), el('dd', { text: value })]);
}

export function whatsappUrl(contact, text) {
  if (!contact.whatsapp) return null;
  const phone = `${contact.whatsappCountryCode ?? ''}${contact.whatsapp}`.replace(/\D/g, '');
  return `https://wa.me/${phone}${text ? `?text=${encodeURIComponent(text)}` : ''}`;
}

export function buildOrderLink(product, contact, shade) {
  const label = [product.name, product.brand].filter(Boolean).join(' – ')
    + (shade ? `, ${shadeWord(product).toLowerCase()} ${shade}` : '');
  const ref = product.reference ? ` (Ref. ${product.reference})` : '';
  const wa = whatsappUrl(contact, `Hola, quiero confirmar la disponibilidad de: ${label}${ref}`);
  if (wa) return { href: wa, channel: 'WhatsApp' };
  if (contact.instagram) {
    return { href: `https://www.instagram.com/${String(contact.instagram).replace(/^@/, '')}/`, channel: 'Instagram' };
  }
  if (contact.email) {
    return { href: `mailto:${contact.email}?subject=${encodeURIComponent(`Solicitud: ${label}`)}`, channel: 'correo' };
  }
  return null;
}

/**
 * Selector de tonos: un círculo con la muestra de cada tono y su nombre debajo. Al elegir uno,
 * el botón de compra agrega el tono al mensaje de WhatsApp.
 */
function shadePicker(product, onChange) {
  if (!product.shades.length) return null;
  const word = shadeWord(product).toLowerCase();
  const hint = `Elige un ${word} para incluirlo en tu pedido.`;
  const chosen = el('p', { class: 'shade-chosen', 'aria-live': 'polite', text: hint });
  const buttons = product.shades.map((shade) => {
    const color = /^#[0-9a-f]{3,8}$/i.test(shade.color ?? '') ? shade.color : null;
    // Sin foto ni color (o con la misma foto para todos los tonos): solo el nombre, en un botón.
    const swatch = shade.image
      ? el('img', { src: shade.image, alt: '', width: shade.imageWidth ?? 96, height: shade.imageHeight ?? 96, loading: 'lazy', decoding: 'async' })
      : color ? el('span', { class: 'shade-color', style: `background:${color}` }) : null;
    const button = el('button', { type: 'button', class: swatch ? 'shade' : 'shade shade-text', role: 'radio', 'aria-checked': 'false' }, [
      swatch ? el('span', { class: 'shade-swatch' }, [swatch]) : null,
      el('span', { class: 'shade-name', text: shade.name }),
    ]);
    button.addEventListener('click', () => {
      const wasChecked = button.getAttribute('aria-checked') === 'true';
      buttons.forEach((b) => b.setAttribute('aria-checked', 'false'));
      button.setAttribute('aria-checked', String(!wasChecked));
      chosen.textContent = wasChecked ? hint : `${shadeWord(product)} elegido: ${shade.name}`;
      onChange(wasChecked ? null : shade);
    });
    return button;
  });
  return el('section', { class: 'detail-shades', 'aria-labelledby': 'shades-title' }, [
    el('h3', { id: 'shades-title', class: 'shades-title', text: `${shadeWord(product, product.shades.length)} (${product.shades.length})` }),
    el('div', {
      class: buttons.every((b) => b.classList.contains('shade-text')) ? 'shade-list shade-list-text' : 'shade-list',
      role: 'radiogroup',
      'aria-labelledby': 'shades-title',
    }, buttons),
    chosen,
    product.shadesSource ? el('p', { class: 'shade-source' }, [`${shadeWord(product, 2)} según la `, el('a', { href: product.shadesSource, target: '_blank', rel: 'noopener', text: 'página oficial de la marca' }), '.']) : null,
  ]);
}

/**
 * Al elegir un tono con foto, esa foto (en grande) ocupa el círculo de la foto principal; al desmarcarlo,
 * o con un tono sin foto, vuelve la foto del catálogo.
 */
function showShadePhoto(container, product, shade) {
  const img = $('.detail-media img', container);
  const caption = $('.detail-media-caption', container);
  if (!img) return;
  img.dataset.originalSrc ??= img.getAttribute('src');
  img.dataset.originalAlt ??= img.getAttribute('alt');
  const src = shade?.imageLarge ?? shade?.image;
  if (src) {
    img.src = src;
    img.alt = `${product.name}, ${shadeWord(product).toLowerCase()} ${shade.name} (foto de la página oficial)`;
    caption.textContent = `${shadeWord(product)}: ${shade.name}`;
    // En el celular la foto queda arriba, fuera de la pantalla: se sube hasta ella para que se vea el cambio.
    const figure = img.closest('.detail-figure');
    const { top, bottom } = figure.getBoundingClientRect();
    if (top < 0 || bottom > window.innerHeight) {
      const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      figure.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    }
  } else {
    img.src = img.dataset.originalSrc;
    img.alt = img.dataset.originalAlt;
    caption.textContent = '';
  }
}

export function renderDetail(container, product, brand) {
  const order = buildOrderLink(product, brand.contact ?? {});
  const notice = brand.purchaseProcess?.notice;
  const extra = product.details && typeof product.details === 'object' ? Object.entries(product.details) : [];

  container.replaceChildren(
    el('figure', { class: 'detail-figure' }, [
      el('div', { class: 'detail-media' }, [productImage(product, { large: true })]),
      product.shades.length ? el('figcaption', { class: 'detail-media-caption', 'aria-live': 'polite' }) : null,
    ]),
    el('div', { class: 'detail-info' }, [
      product.brand ? el('p', { class: 'detail-brand brand-title', text: product.brand }) : null,
      product.category ? el('p', { class: 'card-category', text: product.category }) : null,
      el('h2', { id: 'detail-name', class: 'detail-title', text: product.name }),
      divider(),
      product.variants.length
        ? variantList(product, brand, 'detail-variants')
        : (formatPrice(product, brand) ? el('p', { class: 'detail-price', text: formatPrice(product, brand) }) : null),
      product.offer && typeof product.offer === 'string' ? el('p', { class: 'badge badge-inline', text: product.offer }) : null,
      product.description ? el('p', { class: 'detail-desc', text: product.description }) : null,
      el('dl', { class: 'detail-list' }, [
        detailRow('Marca', product.brand),
        detailRow('Categoría', product.category),
        detailRow('Presentación', product.presentation),
        detailRow('Referencia', product.reference),
        ...extra.map(([k, v]) => detailRow(k, String(v))),
      ]),
      shadePicker(product, (shade) => {
        const link = $('.btn-whatsapp', container);
        const next = buildOrderLink(product, brand.contact ?? {}, shade?.name);
        if (link && next) link.href = next.href;
        showShadePhoto(container, product, shade);
      }),
      ...product.gallery.map((g) => el('figure', { class: 'detail-gallery' }, [
        el('img', { src: g.src, alt: g.alt ?? '', width: g.width, height: g.height, loading: 'lazy', decoding: 'async' }),
        el('figcaption', { text: 'Tonos y presentaciones, como aparecen en el catálogo' }),
      ])),
      order
        ? el('a', {
            class: 'btn btn-primary btn-block btn-whatsapp',
            href: order.href,
            target: '_blank',
            rel: 'noopener',
            'aria-label': `Comprar o solicitar ${product.name} por ${order.channel} (se abre en una pestaña nueva)`,
          }, [order.channel === 'WhatsApp' ? el('img', { src: 'assets/icons/whatsapp.png', alt: '', width: 22, height: 20 }) : null, 'Comprar / Solicitar producto'])
        : null,
      notice ? el('p', { class: 'detail-notice' }, [el('strong', { text: 'Importante: ' }), notice]) : null,
      product.page
        ? el('button', { type: 'button', class: 'btn btn-link page-link', dataset: { gotoPage: product.page }, text: `Ver en el catálogo original (página ${product.page})` })
        : null,
    ]),
  );
}

/* ---------- Vista catálogo (páginas originales) ---------- */

export function renderCatalogPages(container, pages, productsById) {
  const fragment = document.createDocumentFragment();
  for (const page of pages) {
    const linked = (page.products ?? []).map((id) => productsById.get(id)).filter(Boolean);
    fragment.append(
      el('li', { class: 'catalog-page', id: `pagina-${page.number}` }, [
        el('img', {
          src: page.image,
          alt: page.alt ?? `Página ${page.number} del catálogo`,
          width: page.width ?? 900,
          height: page.height ?? 1273,
          loading: page.number <= 1 ? 'eager' : 'lazy',
          decoding: 'async',
        }),
        linked.length
          ? el('div', { class: 'page-products' }, [
              el('p', { class: 'page-products-label', text: `Página ${page.number} · ver detalle:` }),
              el('div', { class: 'chip-row' }, linked.map((p) =>
                el('button', { type: 'button', class: 'chip', dataset: { open: p.id }, text: p.name }))),
            ])
          : null,
      ]),
    );
  }
  container.replaceChildren(fragment);
}

/** Índice de marcas para saltar dentro de la vista catálogo. */
export function renderPageIndex(container, pages) {
  const firstPage = new Map();
  for (const page of pages) {
    if (page.brand && !firstPage.has(page.brand)) firstPage.set(page.brand, page.number);
  }
  container.replaceChildren(...[...firstPage].map(([name, number]) =>
    el('button', { type: 'button', class: 'chip', dataset: { gotoPage: number }, text: name })));
}

/* ---------- Proceso de compra ---------- */

export function renderProcess(section, process) {
  if (!process?.steps?.length) return false;
  $('[data-process-title]', section).textContent = process.title ?? 'Proceso de compra';
  $('[data-process-steps]', section).replaceChildren(...process.steps.map((step, i) =>
    el('li', { class: 'step' }, [
      el('span', { class: 'step-number', 'aria-hidden': 'true', text: String(i + 1) }),
      el('div', {}, [
        el('h3', { class: 'step-title', text: step.title }),
        step.text ? el('p', { class: 'step-text', text: step.text }) : null,
        step.payments ? el('ul', { class: 'payments' }, step.payments.map((p) =>
          el('li', {}, [el('span', { 'aria-hidden': 'true', text: `${p.icon} ` }), el('strong', { text: p.name }), el('br'), p.text]))) : null,
      ]),
    ])));
  const notice = $('[data-process-notice]', section);
  notice.replaceChildren(...(process.notice ? [el('strong', { text: 'IMPORTANTE: ' }), process.notice] : []));
  return true;
}

/* ---------- Contacto ---------- */

function contactItems(contact = {}) {
  const items = [];
  if (contact.instagram) {
    const user = String(contact.instagram).replace(/^@/, '');
    items.push({ icon: 'assets/icons/instagram.png', label: 'Instagram', text: `@${user}`, href: `https://www.instagram.com/${user}/` });
  }
  if (contact.whatsapp) {
    items.push({ icon: 'assets/icons/whatsapp.png', label: 'WhatsApp', text: contact.whatsapp, href: whatsappUrl(contact) });
  }
  if (contact.phone) items.push({ label: 'Teléfono', text: contact.phone, href: `tel:${String(contact.phone).replace(/[^\d+]/g, '')}` });
  if (contact.email) items.push({ label: 'Correo', text: contact.email, href: `mailto:${contact.email}` });
  if (contact.website) items.push({ label: 'Sitio web', text: contact.website, href: contact.website });
  return items;
}

/** Devuelve true si hay al menos un canal de contacto real. */
export function renderContact(lists, contact) {
  const items = contactItems(contact);
  for (const list of lists) {
    list.replaceChildren(...items.map((item) =>
      el('li', {}, [
        el('a', {
          href: item.href,
          target: item.href.startsWith('http') ? '_blank' : null,
          rel: 'noopener',
          'aria-label': `${item.label}: ${item.text}`,
        }, [
          item.icon ? el('img', { src: item.icon, alt: '', width: 28, height: 26 }) : el('span', { class: 'contact-label', text: `${item.label}: ` }),
          el('span', { text: item.text }),
        ]),
      ])));
  }
  return items.length > 0;
}
