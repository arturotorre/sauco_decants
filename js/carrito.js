// Carrito de compras: estado (localStorage), selector de tamaño flotante,
// panel del carrito, aviso al agregar y checkout por WhatsApp.
// Depende de PERFUMES y PERFUMES_COMPLETOS (js/data.js).

const CARRITO_STORAGE_KEY = 'sauco_carrito';
const CARRITO_WHATSAPP_NUMERO = '525612567245';
const CARRITO_CANTIDAD_MAX = 99;

function perfumeId(p) {
  // p.concentracion solo existe en PERFUMES_COMPLETOS (los decants ya llevan
  // la concentración incluida en el nombre, ej. "Scandal Intense EDP"). Sin
  // esto, dos productos completos que comparten casa+nombre pero difieren
  // en concentración (ej. Scandal EDP vs Scandal EDT) colisionarían en el
  // mismo perfumeId y se mezclarían en el carrito.
  return (p.casa + ' ' + p.nombre + ' ' + (p.concentracion || ''))
    .toLowerCase()
    .normalize('NFD').replace(/\p{Diacritic}/gu, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '');
}

function formatoPrecio(valor) {
  return '$' + valor.toLocaleString('es-MX');
}

function precioANumero(precioStr) {
  if (!precioStr) return null;
  const n = Number(String(precioStr).replace(/[^0-9.]/g, ''));
  return Number.isFinite(n) && n > 0 ? n : null;
}

// El carrito se guarda en el navegador del cliente, así que todo lo que se
// pinta desde ahí se escapa antes de entrar al HTML.
function escaparHTML(texto) {
  return String(texto ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function textoTamano(tamano) {
  // "5ml" → "5 ml"; las concentraciones (EDP, EDT…) se dejan igual.
  return String(tamano).replace(/^(\d+)\s*ml$/i, '$1 ml');
}

let carrito = [];

function itemValido(item) {
  return item && typeof item === 'object'
    && typeof item.perfumeId === 'string'
    && typeof item.nombre === 'string'
    && Number.isInteger(item.cantidad) && item.cantidad >= 1;
}

function cargarCarrito() {
  try {
    const guardado = JSON.parse(localStorage.getItem(CARRITO_STORAGE_KEY));
    carrito = Array.isArray(guardado)
      ? guardado.filter(itemValido).map(item => ({ ...item, cantidad: Math.min(item.cantidad, CARRITO_CANTIDAD_MAX) }))
      : [];
  } catch (e) {
    carrito = [];
  }
}

function guardarCarrito() {
  // En modo privado o con el almacenamiento lleno, setItem puede fallar; el
  // carrito sigue funcionando en la página aunque no se recuerde después.
  try {
    localStorage.setItem(CARRITO_STORAGE_KEY, JSON.stringify(carrito));
  } catch (e) { /* sin persistencia */ }
}

function carritoCambio() {
  guardarCarrito();
  actualizarBadge();
  renderCarrito();
}

function agregarItem(datos) {
  const existente = carrito.find(item => item.tipo === datos.tipo && item.perfumeId === datos.perfumeId && item.tamano === datos.tamano);
  if (existente) {
    existente.cantidad = Math.min(existente.cantidad + 1, CARRITO_CANTIDAD_MAX);
  } else {
    carrito.push({ ...datos, cantidad: 1 });
  }
  carritoCambio();
  mostrarAviso(`${datos.alt || datos.nombre} · ${textoTamano(datos.tamano)}`);
}

function agregarAlCarrito(perfume, tamano) {
  agregarItem({
    perfumeId: perfumeId(perfume),
    casa: perfume.casa,
    nombre: perfume.nombre,
    imagen: perfume.imagen,
    alt: perfume.alt,
    tipo: 'decant',
    tamano,
    precio: precioANumero(perfume.precios[tamano])
  });
}

function agregarCompletoAlCarrito(perfume) {
  agregarItem({
    perfumeId: perfumeId(perfume),
    casa: perfume.casa,
    nombre: perfume.nombre,
    imagen: perfume.imagen,
    alt: perfume.alt,
    tipo: 'completo',
    tamano: perfume.concentracion,
    precio: precioANumero(perfume.precio)
  });
}

function quitarDelCarrito(indice) {
  if (!carrito[indice]) return;
  carrito.splice(indice, 1);
  carritoCambio();
  // Tras quitar, el foco no debe perderse al desaparecer el botón.
  const siguiente = document.querySelector(`.carrito-item[data-indice="${Math.min(indice, carrito.length - 1)}"] .carrito-item-quitar`);
  (siguiente || document.querySelector('.carrito-cerrar'))?.focus();
}

function cambiarCantidad(indice, delta) {
  const item = carrito[indice];
  if (!item) return;
  item.cantidad = Math.max(1, Math.min(item.cantidad + delta, CARRITO_CANTIDAD_MAX));
  carritoCambio();
  document.querySelector(`.carrito-item[data-indice="${indice}"] [data-cantidad="${delta > 0 ? 'mas' : 'menos'}"]`)?.focus();
}

function calcularTotal() {
  return carrito.reduce((suma, item) => item.precio != null ? suma + item.precio * item.cantidad : suma, 0);
}

function totalArticulos() {
  return carrito.reduce((suma, item) => suma + item.cantidad, 0);
}

function actualizarBadge() {
  const badge = document.getElementById('carrito-contador');
  const boton = document.getElementById('carrito-boton');
  if (!badge) return;
  const n = totalArticulos();
  badge.textContent = n > 99 ? '99+' : String(n);
  badge.hidden = n === 0;
  boton?.setAttribute('aria-label', n ? `Ver carrito (${n} ${n === 1 ? 'artículo' : 'artículos'})` : 'Ver carrito');
}

function carritoItemHTML(item, indice) {
  const nombre = escaparHTML(item.nombre);
  const precioUnitario = item.precio != null ? formatoPrecio(item.precio) : 'Precio a confirmar';
  const subtotal = item.precio != null ? formatoPrecio(item.precio * item.cantidad) : '';
  return `
  <div class="carrito-item" data-indice="${indice}">
    <div class="carrito-item-foto"><img src="${escaparHTML(item.imagen)}" alt="" onerror="this.style.visibility='hidden'"></div>
    <div class="carrito-item-info">
      <div class="carrito-item-casa">${escaparHTML(item.casa)}</div>
      <div class="carrito-item-nombre">${nombre}</div>
      <div class="carrito-item-detalle">${escaparHTML(textoTamano(item.tamano))} · ${precioUnitario}</div>
      <div class="carrito-item-acciones">
        <div class="carrito-cantidad" role="group" aria-label="Cantidad de ${nombre}">
          <button type="button" class="carrito-cantidad-btn" data-cantidad="menos" data-indice="${indice}" aria-label="Quitar uno" ${item.cantidad <= 1 ? 'disabled' : ''}><span aria-hidden="true" class="icono-menos"></span></button>
          <span class="carrito-cantidad-valor" aria-live="polite">${item.cantidad}</span>
          <button type="button" class="carrito-cantidad-btn" data-cantidad="mas" data-indice="${indice}" aria-label="Agregar uno" ${item.cantidad >= CARRITO_CANTIDAD_MAX ? 'disabled' : ''}><span aria-hidden="true" class="icono-mas"></span></button>
        </div>
        ${subtotal ? `<span class="carrito-item-subtotal">${subtotal}</span>` : ''}
      </div>
      ${item.cantidad >= CARRITO_CANTIDAD_MAX ? `<p class="carrito-item-tope">Máximo ${CARRITO_CANTIDAD_MAX} por producto; si necesitas más, escríbenos.</p>` : ''}
    </div>
    <button type="button" class="carrito-item-quitar" data-indice="${indice}">Quitar<span class="sr-only"> ${nombre} del carrito</span></button>
  </div>`;
}

// ----- Envío y pago (datos reales del negocio) -----
// Local (Monterrey y área metropolitana): $100, $150 en zonas extendidas,
// gratis desde $1,000; entrega en 1 día hábil. Nacional: se cotiza por CP,
// aprox. $160–$200, gratis desde $1,500; entrega en 1 a 3 días hábiles.
// Pago: transferencia o tarjeta. Estos costos aplican a decants; el envío de
// perfumes completos (sobre pedido, 7 a 10 días) se confirma por WhatsApp.
const ENVIO = {
  local: { etiqueta: 'Entrega local en Monterrey', costo: 100, costoExtendida: 150, gratisDesde: 1000, tiempo: '1 día hábil' },
  nacional: { etiqueta: 'Envío nacional', costoMin: 160, costoMax: 200, gratisDesde: 1500, tiempo: '1 a 3 días hábiles' }
};
const FORMAS_PAGO = ['Transferencia', 'Tarjeta'];
const ENVIO_STORAGE_KEY = 'sauco_envio';
const CAMPOS_ENVIO = [
  { id: 'nombre', etiqueta: 'Nombre de quien recibe', tipo: 'text', auto: 'name', requerido: true },
  { id: 'telefono', etiqueta: 'Teléfono (10 dígitos)', tipo: 'tel', auto: 'tel-national', requerido: true, modo: 'numeric' },
  { id: 'calle', etiqueta: 'Calle y número', tipo: 'text', auto: 'address-line1', requerido: true },
  { id: 'colonia', etiqueta: 'Colonia', tipo: 'text', auto: 'address-line2', requerido: true },
  { id: 'ciudad', etiqueta: 'Ciudad o municipio', tipo: 'text', auto: 'address-level2', requerido: true },
  { id: 'estado', etiqueta: 'Estado', tipo: 'text', auto: 'address-level1', requerido: true },
  { id: 'cp', etiqueta: 'Código postal', tipo: 'text', auto: 'postal-code', requerido: true, modo: 'numeric' },
  { id: 'referencias', etiqueta: 'Referencias (opcional)', tipo: 'textarea', requerido: false, ayuda: 'Entre qué calles, color de la casa, etc.' }
];

let carritoPaso = 'carrito'; // 'carrito' | 'envio' | 'enviado'
let envio = { entrega: '', pago: '', nombre: '', telefono: '', calle: '', colonia: '', ciudad: '', estado: '', cp: '', referencias: '' };
let envioErrores = {};
let ultimoPedido = null; // { numero, mensaje }

function cargarEnvio() {
  try {
    const g = JSON.parse(localStorage.getItem(ENVIO_STORAGE_KEY));
    if (g && typeof g === 'object') Object.keys(envio).forEach(k => { if (typeof g[k] === 'string') envio[k] = g[k]; });
  } catch (e) { /* sin datos guardados */ }
}

function guardarEnvio() {
  try { localStorage.setItem(ENVIO_STORAGE_KEY, JSON.stringify(envio)); } catch (e) { /* sin persistencia */ }
}

function hayCompletos() {
  return carrito.some(item => item.tipo === 'completo');
}

function envioEstimado(entrega, subtotal) {
  // Devuelve { texto, monto } para el resumen y el mensaje; monto null si se cotiza.
  if (entrega === 'local') {
    const e = ENVIO.local;
    return subtotal >= e.gratisDesde
      ? { texto: 'Gratis', monto: 0 }
      : { texto: `${formatoPrecio(e.costo)} (${formatoPrecio(e.costoExtendida)} en zonas extendidas)`, monto: e.costo };
  }
  if (entrega === 'nacional') {
    const e = ENVIO.nacional;
    return subtotal >= e.gratisDesde
      ? { texto: 'Gratis', monto: 0 }
      : { texto: `Se cotiza por código postal (aprox. ${formatoPrecio(e.costoMin)}–${formatoPrecio(e.costoMax)})`, monto: null };
  }
  return { texto: 'Según el tipo de entrega', monto: null };
}

function resumenEnvioHTML() {
  const l = ENVIO.local, n = ENVIO.nacional;
  return `<div class="carrito-info">
    <p><strong>100% original:</strong> preparamos tus decants al momento de tu pedido, de nuestras botellas originales y en frasco nuevo.</p>
    <p><strong>Envío en Monterrey:</strong> ${formatoPrecio(l.costo)} (${formatoPrecio(l.costoExtendida)} en zonas extendidas), gratis desde ${formatoPrecio(l.gratisDesde)}. Llega en ${l.tiempo}.</p>
    <p><strong>Envío nacional:</strong> aprox. ${formatoPrecio(n.costoMin)}–${formatoPrecio(n.costoMax)} según tu código postal, gratis desde ${formatoPrecio(n.gratisDesde)}. Llega en ${n.tiempo}.</p>
    <p><strong>Pago:</strong> transferencia o tarjeta; te mandamos los datos por WhatsApp.</p>
    ${hayCompletos() ? '<p>Los perfumes completos se piden sobre pedido (7 a 10 días hábiles); su envío se confirma por WhatsApp.</p>' : ''}
  </div>`;
}

function encabezadoCarrito(titulo, conAtras) {
  const h = document.getElementById('carrito-titulo');
  const atras = document.getElementById('carrito-atras');
  if (h) h.textContent = titulo;
  if (atras) atras.hidden = !conAtras;
}

function pasoCarritoHTML() {
  if (!carrito.length) {
    return `<div class="carrito-vacio">
      <p>Tu carrito está vacío.</p>
      <a class="enlace-secundario" href="/#catalogo/todos">Explorar decants</a>
    </div>`;
  }
  return carrito.map(carritoItemHTML).join('') + resumenEnvioHTML();
}

function campoHTML(c) {
  const err = envioErrores[c.id];
  const idCampo = `envio-${c.id}`;
  const desc = [c.ayuda ? `${idCampo}-ayuda` : '', err ? `${idCampo}-error` : ''].filter(Boolean).join(' ');
  const comunes = `id="${idCampo}" name="${c.id}" ${c.auto ? `autocomplete="${c.auto}"` : ''} ${c.modo ? `inputmode="${c.modo}"` : ''} ${c.requerido ? 'required aria-required="true"' : ''} ${err ? 'aria-invalid="true"' : ''} ${desc ? `aria-describedby="${desc}"` : ''}`;
  const control = c.tipo === 'textarea'
    ? `<textarea ${comunes} rows="2">${escaparHTML(envio[c.id])}</textarea>`
    : `<input type="${c.tipo}" ${comunes} value="${escaparHTML(envio[c.id])}">`;
  return `<div class="envio-campo${err ? ' con-error' : ''}">
    <label for="${idCampo}">${c.etiqueta}</label>
    ${control}
    ${c.ayuda ? `<p class="envio-ayuda" id="${idCampo}-ayuda">${c.ayuda}</p>` : ''}
    ${err ? `<p class="envio-error" id="${idCampo}-error">${err}</p>` : ''}
  </div>`;
}

function opcionesHTML(nombre, opciones, actual, leyenda) {
  const err = envioErrores[nombre];
  return `<fieldset class="envio-opciones${err ? ' con-error' : ''}" ${err ? `aria-describedby="envio-${nombre}-error"` : ''}>
    <legend>${leyenda}</legend>
    ${opciones.map(o => `<label class="envio-opcion">
      <input type="radio" name="${nombre}" value="${o.valor}" ${actual === o.valor ? 'checked' : ''} required>
      <span class="envio-opcion-texto"><strong>${o.titulo}</strong>${o.detalle ? `<span>${o.detalle}</span>` : ''}</span>
    </label>`).join('')}
    ${err ? `<p class="envio-error" id="envio-${nombre}-error">${err}</p>` : ''}
  </fieldset>`;
}

function pasoEnvioHTML() {
  const sub = calcularTotal();
  const local = envioEstimado('local', sub), nac = envioEstimado('nacional', sub);
  return `<form id="form-envio" class="envio-form" novalidate>
    ${opcionesHTML('entrega', [
      { valor: 'local', titulo: 'Entrega en Monterrey', detalle: `${local.texto} · ${ENVIO.local.tiempo}` },
      { valor: 'nacional', titulo: 'Envío nacional', detalle: `${nac.texto} · ${ENVIO.nacional.tiempo}` }
    ], envio.entrega, '¿Dónde lo recibes?')}
    ${opcionesHTML('pago', FORMAS_PAGO.map(f => ({ valor: f, titulo: f })), envio.pago, '¿Cómo prefieres pagar?')}
    <fieldset class="envio-datos"><legend>Datos de envío</legend>${CAMPOS_ENVIO.map(campoHTML).join('')}</fieldset>
  </form>`;
}

function pasoEnviadoHTML() {
  const p = ultimoPedido;
  return `<div class="pedido-enviado">
    <p class="pedido-numero">Pedido <strong>#${p.numero}</strong></p>
    <p>Abrimos WhatsApp con tu pedido ya escrito. Envíalo desde ahí para que lo recibamos.</p>
    <button type="button" class="btn-secundario" data-accion="reenviar">Abrir WhatsApp de nuevo</button>
    <h3 class="pedido-subtitulo">Lo que sigue</h3>
    <ol class="pedido-pasos">
      <li>Te respondemos por WhatsApp para confirmar tu pedido y el pago por ${p.pago.toLowerCase()}.</li>
      <li>Al confirmarse el pago, preparamos tu envío.</li>
      <li>${p.entrega === 'local' ? `Entrega en Monterrey: ${ENVIO.local.tiempo}.` : `Envío nacional: ${ENVIO.nacional.tiempo}.`}${p.conCompletos ? ' Los perfumes completos tardan de 7 a 10 días hábiles.' : ''}</li>
    </ol>
  </div>`;
}

function renderCarrito() {
  const cont = document.getElementById('carrito-items');
  const pie = document.getElementById('carrito-pie');
  if (!cont || !pie) return;
  if (carritoPaso !== 'carrito' && !carrito.length && carritoPaso !== 'enviado') carritoPaso = 'carrito';

  const sub = calcularTotal();
  const n = totalArticulos();
  const hayPendientes = carrito.some(item => item.precio == null);

  if (carritoPaso === 'envio') {
    encabezadoCarrito('Datos de envío', true);
    cont.innerHTML = pasoEnvioHTML();
    const est = envioEstimado(envio.entrega, sub);
    const totalTexto = est.monto != null ? formatoPrecio(sub + est.monto) : `${formatoPrecio(sub)} + envío`;
    pie.innerHTML = `
      <div class="carrito-total-fila"><span>Subtotal</span><span>${formatoPrecio(sub)}</span></div>
      <div class="carrito-total-fila"><span>Envío</span><span class="carrito-envio-texto">${envio.entrega ? est.texto : 'Elige dónde lo recibes'}</span></div>
      <div class="carrito-total-fila carrito-total-final"><span>Total estimado</span><span class="carrito-total-monto">${totalTexto}</span></div>
      <button type="submit" form="form-envio" class="carrito-principal">Enviar pedido por WhatsApp</button>
      <p class="carrito-nota-whatsapp">Se abrirá WhatsApp con tu pedido y tus datos ya escritos.</p>`;
  } else if (carritoPaso === 'enviado' && ultimoPedido) {
    encabezadoCarrito('Pedido listo', false);
    cont.innerHTML = pasoEnviadoHTML();
    pie.innerHTML = `
      <button type="button" class="carrito-principal" data-accion="nuevo">Hacer un pedido nuevo</button>
      <button type="button" class="enlace-secundario carrito-volver" data-accion="volver">Volver a mi carrito</button>`;
  } else {
    carritoPaso = 'carrito';
    encabezadoCarrito('Tu carrito', false);
    cont.innerHTML = pasoCarritoHTML();
    pie.innerHTML = carrito.length ? `
      <div class="carrito-total-fila"><span>Subtotal · ${n} ${n === 1 ? 'artículo' : 'artículos'}</span><span class="carrito-total-monto">${formatoPrecio(sub)}</span></div>
      ${hayPendientes ? '<p class="carrito-total-nota">Hay productos con precio por confirmar; no están incluidos en el subtotal.</p>' : ''}
      <button type="button" class="carrito-principal" data-accion="continuar">Continuar con el envío</button>` : '';
  }
}

function irAPaso(paso) {
  carritoPaso = paso;
  envioErrores = {};
  renderCarrito();
  const items = document.getElementById('carrito-items');
  if (items) items.scrollTop = 0;
  // El foco va al título del paso para que el lector de pantalla lo anuncie.
  document.getElementById('carrito-titulo')?.focus();
}

function leerFormEnvio(form) {
  const fd = new FormData(form);
  Object.keys(envio).forEach(k => { if (fd.has(k)) envio[k] = String(fd.get(k)).trim(); });
}

function validarEnvio() {
  const e = {};
  if (!envio.entrega) e.entrega = 'Elige si lo recibes en Monterrey o por envío nacional.';
  if (!envio.pago) e.pago = 'Elige cómo prefieres pagar.';
  CAMPOS_ENVIO.forEach(c => { if (c.requerido && !envio[c.id]) e[c.id] = `Escribe ${c.etiqueta.replace(/ \(.*\)$/, '').toLowerCase()}.`; });
  const tel = envio.telefono.replace(/\D/g, '').replace(/^52(?=\d{10}$)/, '');
  if (envio.telefono && tel.length !== 10) e.telefono = 'El teléfono debe tener 10 dígitos, por ejemplo 81 1234 5678.';
  if (envio.cp && !/^\d{5}$/.test(envio.cp.replace(/\s/g, ''))) e.cp = 'El código postal tiene 5 dígitos.';
  return e;
}

// ----- Panel del carrito (diálogo) -----
let carritoFocoPrevio = null;

function carritoAbierto() {
  const panel = document.getElementById('carrito-panel');
  return panel && !panel.hidden;
}

function abrirCarrito() {
  if (carritoPaso === 'envio') carritoPaso = 'carrito';
  renderCarrito();
  ocultarAviso();
  const overlay = document.getElementById('carrito-overlay');
  const panel = document.getElementById('carrito-panel');
  if (!panel) return;
  carritoFocoPrevio = document.activeElement;
  overlay.hidden = false;
  panel.hidden = false;
  document.documentElement.classList.add('carrito-bloqueo');
  requestAnimationFrame(() => {
    overlay.classList.add('visible');
    panel.classList.add('abierto');
    panel.querySelector('.carrito-cerrar')?.focus();
  });
}

function cerrarCarrito() {
  if (!carritoAbierto()) return;
  const overlay = document.getElementById('carrito-overlay');
  const panel = document.getElementById('carrito-panel');
  overlay.classList.remove('visible');
  panel.classList.remove('abierto');
  document.documentElement.classList.remove('carrito-bloqueo');
  setTimeout(() => {
    overlay.hidden = true;
    panel.hidden = true;
  }, 300);
  const previo = carritoFocoPrevio && carritoFocoPrevio !== document.body && document.contains(carritoFocoPrevio) ? carritoFocoPrevio : null;
  (previo || document.getElementById('carrito-boton'))?.focus();
}

function atraparFocoCarrito(e) {
  if (e.key !== 'Tab' || !carritoAbierto()) return;
  const enfocables = Array.from(document.getElementById('carrito-panel')
    .querySelectorAll('a[href], button:not([disabled]), input:not([disabled]), textarea:not([disabled]), select:not([disabled])'))
    .filter(el => !el.hidden && el.offsetParent !== null);
  if (!enfocables.length) return;
  const primero = enfocables[0];
  const ultimo = enfocables[enfocables.length - 1];
  if (e.shiftKey && document.activeElement === primero) { e.preventDefault(); ultimo.focus(); }
  else if (!e.shiftKey && document.activeElement === ultimo) { e.preventDefault(); primero.focus(); }
}

// ----- Aviso al agregar -----
let avisoTimer = null;

function mostrarAviso(texto) {
  const aviso = document.getElementById('carrito-aviso');
  if (!aviso) return;
  aviso.innerHTML = `<span class="carrito-aviso-texto"><strong>${escaparHTML(texto)}</strong> agregado al carrito</span>
    <button type="button" class="carrito-aviso-ver">Ver carrito</button>`;
  aviso.hidden = false;
  requestAnimationFrame(() => aviso.classList.add('visible'));
  clearTimeout(avisoTimer);
  avisoTimer = setTimeout(ocultarAviso, 5000);
}

function ocultarAviso() {
  const aviso = document.getElementById('carrito-aviso');
  if (!aviso || aviso.hidden) return;
  clearTimeout(avisoTimer);
  aviso.classList.remove('visible');
  setTimeout(() => { if (!aviso.classList.contains('visible')) aviso.hidden = true; }, 250);
}

// ----- Selector de tamaño (decants) -----
let selectorBotonOrigen = null;

function abrirSelectorTamano(perfume, boton) {
  const cont = document.getElementById('selector-tamano');
  if (!cont) return;
  selectorBotonOrigen = boton;
  cont.setAttribute('role', 'dialog');
  cont.setAttribute('aria-label', `Elige la medida de ${perfume.alt || perfume.nombre}`);
  cont.innerHTML = ['3ml', '5ml', '10ml'].map(tamano => {
    const precioStr = perfume.precios[tamano];
    return `<button type="button" class="selector-tamano-opcion" data-tamano="${tamano}">
      <span class="selector-tamano-ml">${textoTamano(tamano)}</span>
      <span class="selector-tamano-precio">${precioStr ? escaparHTML(precioStr) : 'Precio a confirmar'}</span>
    </button>`;
  }).join('');
  cont.dataset.casa = perfume.casa;
  cont.dataset.nombre = perfume.nombre;
  cont.hidden = false;

  // #selector-tamano es position:fixed → las coordenadas van relativas al
  // viewport (las que ya da getBoundingClientRect), sin sumar el scroll.
  const r = boton.getBoundingClientRect();
  const ancho = cont.offsetWidth;
  const alto = cont.offsetHeight;

  let left = r.right - ancho;
  if (left < 8) left = 8;
  if (left + ancho > window.innerWidth - 8) left = window.innerWidth - 8 - ancho;

  let top = r.bottom + 6;
  if (top + alto > window.innerHeight - 8) top = Math.max(8, r.top - alto - 6);

  cont.style.top = top + 'px';
  cont.style.left = left + 'px';
  cont.querySelector('.selector-tamano-opcion')?.focus();
}

function cerrarSelectorTamano(devolverFoco) {
  const cont = document.getElementById('selector-tamano');
  if (!cont || cont.hidden) return;
  cont.hidden = true;
  if (devolverFoco && selectorBotonOrigen && document.contains(selectorBotonOrigen)) selectorBotonOrigen.focus();
}

// ----- WhatsApp -----
function generarNumeroPedido() {
  // Aleatorio criptográfico (no Math.random) para minimizar la probabilidad
  // de choque entre pedidos, ya que no hay base de datos que valide unicidad.
  const buffer = new Uint32Array(1);
  crypto.getRandomValues(buffer);
  return String(10000000 + (buffer[0] % 90000000));
}

function abrirWhatsApp(mensaje) {
  const url = `https://wa.me/${CARRITO_WHATSAPP_NUMERO}?text=${encodeURIComponent(mensaje)}`;
  // Si el navegador bloquea la ventana nueva, se abre en la misma pestaña
  // para que el pedido nunca se pierda en silencio.
  // (Sin 'noopener' en las opciones: con él, window.open siempre devuelve
  // null y no se podría distinguir un bloqueo.)
  const ventana = window.open(url, '_blank');
  if (ventana) ventana.opener = null;
  else window.location.href = url;
}

function mensajePedido(numeroPedido) {
  const sub = calcularTotal();
  const est = envioEstimado(envio.entrega, sub);
  const lineas = carrito.map(item => {
    const cantidadTexto = item.cantidad > 1 ? ` x${item.cantidad}` : '';
    if (item.precio == null) {
      return `• ${item.casa} ${item.nombre} (${item.tamano})${cantidadTexto} — Precio a confirmar`;
    }
    const subtotal = item.precio * item.cantidad;
    const precioTexto = item.cantidad > 1
      ? `${formatoPrecio(item.precio)} c/u = ${formatoPrecio(subtotal)}`
      : formatoPrecio(item.precio);
    return `• ${item.casa} ${item.nombre} (${item.tamano})${cantidadTexto} — ${precioTexto}`;
  });
  const tel = envio.telefono.replace(/\D/g, '').replace(/^52(?=\d{10}$)/, '');
  let m = 'Hola, me gustaría realizar el siguiente pedido:\n\n'
    + `Número de pedido: ${numeroPedido}\n\n`
    + lineas.join('\n')
    + `\n\nSubtotal: ${formatoPrecio(sub)}`
    + `\nEnvío (${ENVIO[envio.entrega].etiqueta}): ${est.texto}`
    + `\nTotal estimado: ${est.monto != null ? formatoPrecio(sub + est.monto) : formatoPrecio(sub) + ' + envío'}`
    + `\nForma de pago: ${envio.pago}`
    + '\n\nDatos de envío:'
    + `\nNombre: ${envio.nombre}`
    + `\nTeléfono: ${tel}`
    + `\nDirección: ${envio.calle}, col. ${envio.colonia}, C.P. ${envio.cp.replace(/\s/g, '')}, ${envio.ciudad}, ${envio.estado}`
    + (envio.referencias ? `\nReferencias: ${envio.referencias}` : '');
  if (carrito.some(item => item.precio == null)) {
    m += '\n\n(Nota: hay productos con precio por confirmar, no incluidos en el total.)';
  }
  if (hayCompletos()) {
    m += '\n\n(Incluye perfumes completos: sobre pedido, 7 a 10 días hábiles; el envío se confirma por WhatsApp.)';
  }
  return m;
}

function checkoutWhatsApp(form) {
  if (!carrito.length) return;
  leerFormEnvio(form);
  guardarEnvio();
  envioErrores = validarEnvio();
  if (Object.keys(envioErrores).length) {
    renderCarrito();
    const primero = Object.keys(envioErrores)[0];
    const destino = ['entrega', 'pago'].includes(primero)
      ? document.querySelector(`#form-envio input[name="${primero}"]`)
      : document.getElementById(`envio-${primero}`);
    destino?.focus();
    return;
  }
  const numero = generarNumeroPedido();
  const mensaje = mensajePedido(numero);
  ultimoPedido = { numero, mensaje, entrega: envio.entrega, pago: envio.pago, conCompletos: hayCompletos() };
  abrirWhatsApp(mensaje);
  irAPaso('enviado');
}

document.addEventListener('click', (e) => {
  const btnConsultarCompleto = e.target.closest('.btn-consultar-completo');
  if (btnConsultarCompleto) {
    enviarConsultaDisponibilidad(btnConsultarCompleto.dataset.nombre, btnConsultarCompleto.dataset.casa);
    return;
  }

  const btnAgregarCompleto = e.target.closest('.btn-agregar-completo');
  if (btnAgregarCompleto) {
    const perfume = PERFUMES_COMPLETOS.find(p => p.casa === btnAgregarCompleto.dataset.casa && p.nombre === btnAgregarCompleto.dataset.nombre && p.concentracion === btnAgregarCompleto.dataset.concentracion);
    if (perfume) agregarCompletoAlCarrito(perfume);
    return;
  }

  // Botones de medida del catálogo: agregan directo, sin selector.
  const medida = e.target.closest('.fila-medida');
  if (medida) {
    const perfume = PERFUMES.find(p => p.casa === medida.dataset.casa && p.nombre === medida.dataset.nombre);
    if (perfume) {
      agregarAlCarrito(perfume, medida.dataset.ml);
      medida.classList.add('agregado');
      setTimeout(() => medida.classList.remove('agregado'), 900);
    }
    return;
  }

  const btnAgregar = e.target.closest('.btn-agregar');
  if (btnAgregar) {
    const perfume = PERFUMES.find(p => p.casa === btnAgregar.dataset.casa && p.nombre === btnAgregar.dataset.nombre);
    if (perfume) abrirSelectorTamano(perfume, btnAgregar);
    return;
  }

  const opcion = e.target.closest('.selector-tamano-opcion');
  if (opcion) {
    const cont = document.getElementById('selector-tamano');
    const perfume = PERFUMES.find(p => p.casa === cont.dataset.casa && p.nombre === cont.dataset.nombre);
    if (perfume) agregarAlCarrito(perfume, opcion.dataset.tamano);
    cerrarSelectorTamano(true);
    return;
  }

  const cantidadBtn = e.target.closest('.carrito-cantidad-btn');
  if (cantidadBtn) {
    cambiarCantidad(Number(cantidadBtn.dataset.indice), cantidadBtn.dataset.cantidad === 'mas' ? 1 : -1);
    return;
  }

  const quitar = e.target.closest('.carrito-item-quitar');
  if (quitar) {
    quitarDelCarrito(Number(quitar.dataset.indice));
    return;
  }

  if (e.target.closest('.carrito-aviso-ver')) { abrirCarrito(); return; }
  if (e.target.closest('#carrito-boton')) { abrirCarrito(); return; }
  const accion = e.target.closest('[data-accion]');
  if (accion && accion.closest('#carrito-panel')) {
    const a = accion.dataset.accion;
    if (a === 'continuar') { irAPaso('envio'); return; }
    if (a === 'reenviar' && ultimoPedido) { abrirWhatsApp(ultimoPedido.mensaje); return; }
    if (a === 'volver') { irAPaso('carrito'); return; }
    if (a === 'nuevo') {
      carrito = []; ultimoPedido = null; carritoCambio(); irAPaso('carrito'); return;
    }
  }
  if (e.target.closest('#carrito-atras')) { irAPaso('carrito'); return; }
  if (e.target.closest('.carrito-cerrar') || e.target.id === 'carrito-overlay') { cerrarCarrito(); return; }
  // Un enlace dentro del carrito (ej. "Explorar decants" con el carrito vacío)
  // navega y cierra el panel.
  if (e.target.closest('#carrito-panel a[href]')) { cerrarCarrito(); return; }

  if (!e.target.closest('#selector-tamano')) cerrarSelectorTamano(false);
});

document.addEventListener('submit', (e) => {
  if (e.target.id !== 'form-envio') return;
  e.preventDefault();
  checkoutWhatsApp(e.target);
});

document.addEventListener('change', (e) => {
  const form = e.target.closest('#form-envio');
  if (!form) return;
  leerFormEnvio(form);
  // Al elegir entrega local se sugiere la ciudad y el estado si están vacíos.
  if (e.target.name === 'entrega' && envio.entrega === 'local') {
    if (!envio.ciudad) envio.ciudad = 'Monterrey';
    if (!envio.estado) envio.estado = 'Nuevo León';
  }
  guardarEnvio();
  if (e.target.type === 'radio') {
    delete envioErrores[e.target.name];
    const activo = e.target.value, nombre = e.target.name;
    renderCarrito();
    document.querySelector(`#form-envio input[name="${nombre}"][value="${activo}"]`)?.focus();
  }
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    const selector = document.getElementById('selector-tamano');
    if (selector && !selector.hidden) { cerrarSelectorTamano(true); return; }
    cerrarCarrito();
    ocultarAviso();
    return;
  }
  atraparFocoCarrito(e);
});

function enviarCotizacion(nombrePerfume, marca) {
  abrirWhatsApp(marca
    ? `Hola, me gustaría cotizar ${nombrePerfume} de la marca ${marca}, por favor.`
    : `Hola, me gustaría cotizar ${nombrePerfume}, por favor.`);
}

function enviarConsultaDisponibilidad(nombrePerfume, marca) {
  abrirWhatsApp(`Hola, estoy interesado en ${nombrePerfume} de ${marca}, ¿me podrían brindar información de costo y tiempo de entrega?`);
}

document.addEventListener('DOMContentLoaded', () => {
  cargarCarrito();
  cargarEnvio();
  actualizarBadge();
  renderCarrito();

  const formCotizar = document.getElementById('form-cotizar');
  formCotizar?.addEventListener('submit', (e) => {
    e.preventDefault();
    const nombrePerfume = document.getElementById('cotizar-nombre').value.trim();
    const marca = document.getElementById('cotizar-marca').value.trim();
    if (!nombrePerfume) return;
    enviarCotizacion(nombrePerfume, marca);
    formCotizar.reset();
  });
});

// Si el carrito cambia en otra pestaña, esta se pone al día.
window.addEventListener('storage', (e) => {
  if (e.key !== CARRITO_STORAGE_KEY) return;
  cargarCarrito();
  actualizarBadge();
  renderCarrito();
});
