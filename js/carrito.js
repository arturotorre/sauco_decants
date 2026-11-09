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
  ultimaAgregada = { tipo: datos.tipo, perfumeId: datos.perfumeId, tamano: datos.tamano };
  const item = existente || carrito[carrito.length - 1];
  mostrarAviso(`${datos.alt || datos.nombre} · ${textoTamano(datos.tamano)}`, item.cantidad);
  pulsarContador();
}

// Deshacer: quita la última pieza agregada (por si fue un toque accidental).
let ultimaAgregada = null;
function deshacerUltima() {
  if (!ultimaAgregada) return;
  const u = ultimaAgregada;
  const i = carrito.findIndex(item => item.tipo === u.tipo && item.perfumeId === u.perfumeId && item.tamano === u.tamano);
  if (i >= 0) {
    if (carrito[i].cantidad > 1) carrito[i].cantidad -= 1; else carrito.splice(i, 1);
    carritoCambio();
  }
  ultimaAgregada = null;
  const aviso = document.getElementById('carrito-aviso');
  if (aviso) {
    aviso.innerHTML = '<span class="carrito-aviso-texto">Se quitó del carrito</span>';
    anunciar('Se quitó del carrito');
    programarAviso(2500);
  }
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
const FORMAS_PAGO = [
  { valor: 'Transferencia', detalle: 'Te mandamos los datos bancarios por WhatsApp.' },
  { valor: 'Tarjeta', detalle: 'Te mandamos una liga de pago segura de Mercado Pago, sin comisión.' }
];
const HORARIO = 'de lunes a sábado, de 9:00 a 20:00';
// Datos del dueño (2026-11-08): corte de pedidos y política de reclamos.
const HORA_CORTE = 18;
const POLITICA_HTML = `<details class="envio-politica">
    <summary>¿Y si algo llega mal?</summary>
    <p>Si tu decant llega dañado o derramado, avísanos por WhatsApp en las primeras 24 horas después de recibirlo; si te llegó un perfume equivocado, tienes 48 horas. Te pediremos fotos del decant, de su etiqueta y del interior de la caja. Si el reclamo procede, te reponemos el decant sin costo.</p>
  </details>`;
const PEDIDO_STORAGE_KEY = 'sauco_pedido';
const ENVIO_STORAGE_KEY = 'sauco_envio';
// Orden del formulario: cuándo → a dónde → quién recibe (el pago va al final).
const CAMPOS_ENVIO = [
  { id: 'fecha', grupo: 'cuando', etiqueta: 'Fecha (opcional)', tipo: 'date', requerido: false },
  { id: 'cp', grupo: 'donde', etiqueta: 'Código postal', tipo: 'text', auto: 'postal-code', requerido: true, modo: 'numeric' },
  { id: 'calle', grupo: 'donde', etiqueta: 'Calle y número', tipo: 'text', auto: 'address-line1', requerido: true },
  { id: 'colonia', grupo: 'donde', etiqueta: 'Colonia', tipo: 'text', auto: 'address-line2', requerido: true },
  { id: 'ciudad', grupo: 'donde', etiqueta: 'Ciudad o municipio', tipo: 'text', auto: 'address-level2', requerido: true, ejemplo: 'Ej. Monterrey, San Pedro, Guadalupe' },
  { id: 'estado', grupo: 'donde', etiqueta: 'Estado', tipo: 'text', auto: 'address-level1', requerido: true },
  { id: 'referencias', grupo: 'donde', etiqueta: 'Referencias (opcional)', tipo: 'textarea', requerido: false, ayuda: 'Entre qué calles, color de la casa, etc.' },
  { id: 'nombre', grupo: 'quien', etiqueta: 'Nombre de quien recibe', tipo: 'text', auto: 'name', requerido: true },
  { id: 'telefono', grupo: 'quien', etiqueta: 'Teléfono (10 dígitos)', tipo: 'tel', auto: 'tel-national', requerido: true, modo: 'numeric' }
];

let carritoPaso = 'carrito'; // 'carrito' | 'envio' | 'enviado'
let envio = { entrega: '', pago: '', nombre: '', telefono: '', calle: '', colonia: '', ciudad: '', estado: '', cp: '', referencias: '', fecha: '' };
let envioErrores = {};
let ultimoPedido = null; // { numero, firma, mensaje, entrega, pago, conCompletos, resumen }
let confirmandoNuevo = false;
let verCarritoSinPedido = false;

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

// El envío gratis y los costos son de decants: el mínimo se calcula solo con
// el subtotal de decants. El envío de perfumes completos se confirma aparte.
function subtotalDecants() {
  return carrito.reduce((s, i) => i.tipo === 'decant' && i.precio != null ? s + i.precio * i.cantidad : s, 0);
}
function hayDecants() {
  return carrito.some(i => i.tipo === 'decant');
}
function envioPedido(entrega) {
  if (!hayDecants()) return { texto: 'Se confirma por WhatsApp', monto: null };
  return envioEstimado(entrega, subtotalDecants());
}
function totalEstimadoTexto(entrega) {
  const sub = calcularTotal();
  let est = envioPedido(entrega);
  // Sin entrega elegida: si ambas opciones salen gratis, el total ya es definitivo.
  if (!entrega && hayDecants() && envioPedido('local').monto === 0 && envioPedido('nacional').monto === 0) est = { monto: 0 };
  if (est.monto == null) return `${formatoPrecio(sub)} + envío`;
  return formatoPrecio(sub + est.monto) + (hayCompletos() ? ' + envío de completos' : '');
}

// Firma del carrito: si no cambia, un pedido ya generado conserva su número.
function firmaCarrito() {
  return JSON.stringify(carrito.map(i => [i.perfumeId, i.tipo, i.tamano, i.cantidad]));
}
function guardarPedido() {
  try { localStorage.setItem(PEDIDO_STORAGE_KEY, JSON.stringify(ultimoPedido)); } catch (e) { /* sin persistencia */ }
}
function cargarPedido() {
  try {
    const p = JSON.parse(localStorage.getItem(PEDIDO_STORAGE_KEY));
    if (p && typeof p.numero === 'string' && typeof p.mensaje === 'string') ultimoPedido = p;
  } catch (e) { /* sin datos */ }
}
function borrarPedido() {
  ultimoPedido = null;
  try { localStorage.removeItem(PEDIDO_STORAGE_KEY); } catch (e) { /* nada */ }
}
function pedidoVigente() {
  return ultimoPedido && carrito.length && ultimoPedido.firma === firmaCarrito();
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
    <p><strong>Envío:</strong> en Monterrey ${formatoPrecio(l.costo)} (${formatoPrecio(l.costoExtendida)} en zonas extendidas), gratis desde ${formatoPrecio(l.gratisDesde)}; nacional aprox. ${formatoPrecio(n.costoMin)}–${formatoPrecio(n.costoMax)} según tu código postal, gratis desde ${formatoPrecio(n.gratisDesde)}. Pedidos recibidos antes de las 18:00 se envían el siguiente día hábil (de lunes a viernes; lo del sábado sale el lunes).</p>
    <p><strong>Pago:</strong> transferencia, o tarjeta con liga segura de Mercado Pago sin comisión. Te respondemos por WhatsApp ${HORARIO}.</p>
    ${hayCompletos() ? '<p>Los perfumes completos se piden sobre pedido (7 a 10 días hábiles); su envío se confirma por WhatsApp.</p>' : ''}
    ${POLITICA_HTML}
  </div>`;
}

function encabezadoCarrito(titulo, conAtras, paso) {
  const h = document.getElementById('carrito-titulo');
  const atras = document.getElementById('carrito-atras');
  if (h) h.innerHTML = escaparHTML(titulo) + (paso ? ` <span class="carrito-paso">· ${paso} de 3</span>` : '');
  if (atras) atras.hidden = !conAtras;
}

function pasoCarritoHTML() {
  if (!carrito.length) {
    return `<div class="carrito-vacio">
      <p>Tu carrito está vacío.</p>
      <p class="carrito-vacio-sub">Prueba un perfume de lujo en&nbsp;3,&nbsp;5 o&nbsp;10&nbsp;ml.</p>
      <a class="carrito-principal" href="/#catalogo/todos">Explorar decants</a>
      <a class="enlace-secundario" href="/#completos/todos">Perfumes completos</a>
    </div>`;
  }
  return carrito.map(carritoItemHTML).join('') + resumenEnvioHTML();
}

function campoHTML(c) {
  const err = envioErrores[c.id];
  const idCampo = `envio-${c.id}`;
  const desc = [c.ayuda ? `${idCampo}-ayuda` : '', err ? `${idCampo}-error` : ''].filter(Boolean).join(' ');
  const hoy = new Date(); const minFecha = `${hoy.getFullYear()}-${String(hoy.getMonth() + 1).padStart(2, '0')}-${String(hoy.getDate()).padStart(2, '0')}`;
  const comunes = `id="${idCampo}" name="${c.id}" ${c.ejemplo ? `placeholder="${c.ejemplo}"` : ''} ${c.tipo === 'date' ? `min="${minFecha}"` : ''} ${c.auto ? `autocomplete="${c.auto}"` : ''} ${c.modo ? `inputmode="${c.modo}"` : ''} ${c.requerido ? 'required aria-required="true"' : ''} ${err ? 'aria-invalid="true"' : ''} ${desc ? `aria-describedby="${desc}"` : ''}`;
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
  const local = envioPedido('local'), nac = envioPedido('nacional');
  const n = totalArticulos();
  const est = envioPedido(envio.entrega);
  const mixto = hayCompletos() && hayDecants();
  // El desglose vive aquí arriba; el pie fijo solo lleva el total y el botón.
  const resumen = `<details class="envio-resumen">
    <summary>${n} ${n === 1 ? 'artículo' : 'artículos'} · ver desglose</summary>
    <ul>${carrito.map(i => `<li>${escaparHTML(i.alt || i.nombre)} · ${escaparHTML(textoTamano(i.tamano))}${i.cantidad > 1 ? ` ×${i.cantidad}` : ''}</li>`).join('')}</ul>
    <dl class="envio-desglose">
      <div><dt>Subtotal</dt><dd>${formatoPrecio(calcularTotal())}</dd></div>
      <div><dt>Envío${mixto ? ' de decants' : ''}</dt><dd>${envio.entrega || !hayDecants() ? est.texto : 'Según dónde lo recibas'}</dd></div>
      ${mixto ? '<div><dt>Envío de completos</dt><dd>Se confirma por WhatsApp</dd></div>' : ''}
      <div class="envio-desglose-total"><dt>Total estimado</dt><dd>${totalEstimadoTexto(envio.entrega)}</dd></div>
    </dl>
  </details>`;
  return `<form id="form-envio" class="envio-form" novalidate>
    ${resumen}
    ${opcionesHTML('entrega', [
      { valor: 'local', titulo: 'Entrega en Monterrey', detalle: `${local.texto} · ${ENVIO.local.tiempo}` },
      { valor: 'nacional', titulo: 'Envío nacional', detalle: `${nac.texto} · ${ENVIO.nacional.tiempo}` }
    ], envio.entrega, '¿Dónde lo recibes?')}
    <fieldset class="envio-datos"><legend>¿Para cuándo lo necesitas?</legend>
      ${grupoCampos('cuando')}
      <p class="envio-fecha-respuesta${estadoFecha() ? ' ' + estadoFecha() : ''}" id="envio-fecha-respuesta" aria-live="polite">${respuestaFecha()}</p>
    </fieldset>
    <fieldset class="envio-datos"><legend>¿A dónde lo enviamos?</legend>${grupoCampos('donde')}</fieldset>
    <fieldset class="envio-datos"><legend>¿Quién lo recibe?</legend>${grupoCampos('quien')}</fieldset>
    ${opcionesHTML('pago', FORMAS_PAGO.map(f => ({ valor: f.valor, titulo: f.valor, detalle: f.detalle })), envio.pago, '¿Cómo prefieres pagar?')}
    <div class="envio-confianza">
      <p><strong>100% original:</strong> preparamos tu decant de nuestra botella original, en frasco nuevo. Si quieres, te mandamos foto o video de la botella antes de pagar.</p>
      ${POLITICA_HTML}
    </div>
  </form>`;
}

function grupoCampos(grupo) {
  return CAMPOS_ENVIO.filter(c => c.grupo === grupo).map(campoHTML).join('');
}

function fechaISO(d) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

// Día en que sale el pedido (dato del dueño, 2026-11-08): lo recibido antes
// de las 18:00 cuenta ese día; después, al día siguiente. Sale el siguiente
// día hábil de paquetería (lunes a viernes): el sábado se prepara, pero la
// paquetería recolecta el lunes. Lo del domingo cuenta como recibido el
// lunes. No contempla días festivos.
function diaEnvio(ahora = new Date()) {
  const d = new Date(ahora.getFullYear(), ahora.getMonth(), ahora.getDate());
  // El sábado no aplica el corte: todo lo del sábado sale el lunes.
  if (ahora.getHours() >= HORA_CORTE && d.getDay() !== 6) d.setDate(d.getDate() + 1);
  if (d.getDay() === 0) d.setDate(d.getDate() + 1); // el domingo no se atiende: cuenta como lunes
  do { d.setDate(d.getDate() + 1); } while (d.getDay() === 0 || d.getDay() === 6);
  return d;
}

// Respuesta inmediata a la fecha: dice cuándo sale el pedido si se hace ahora;
// la llegada exacta se confirma por WhatsApp.
// Estado visual de la respuesta: «no-alcanza» (aviso), «justo» (atención) o nada.
function estadoFecha() {
  if (!envio.fecha) return '';
  const sale = fechaISO(diaEnvio());
  if (envio.fecha < sale) return 'no-alcanza';
  if (envio.fecha === sale) return 'justo';
  return '';
}

function respuestaFecha() {
  const sale = diaEnvio();
  const saleTexto = fechaLegible(fechaISO(sale));
  const llega = envio.entrega === 'local' ? ` En Monterrey llega en ${ENVIO.local.tiempo}.`
    : envio.entrega === 'nacional' ? ` Por envío nacional llega en ${ENVIO.nacional.tiempo}.` : '';
  if (!envio.fecha) return `Si haces tu pedido ahora, sale el ${saleTexto}.${llega} Si hubiera alguna demora, te avisamos.`;
  if (envio.fecha < fechaISO(sale)) return `No alcanza: si haces tu pedido ahora, sale el ${saleTexto}. Elige otra fecha o pregúntanos por WhatsApp.`;
  if (envio.fecha === fechaISO(sale)) return `Es justo: tu pedido sale ese mismo día, el ${saleTexto}. Te confirmamos por WhatsApp si llega a tiempo.`;
  return `Anotado para el ${fechaLegible(envio.fecha)}. Tu pedido sale el ${saleTexto}.${llega} Te confirmamos por WhatsApp.`;
}

// Cuenta los datos obligatorios que faltan, en el orden del formulario.
function datosFaltantes() {
  let n = envio.entrega ? 0 : 1;
  CAMPOS_ENVIO.forEach(c => { if (c.requerido && !envio[c.id]) n++; });
  if (!envio.pago) n++;
  return n;
}
function irAlPrimerFaltante() {
  let destino = null;
  if (!envio.entrega) destino = document.querySelector('#form-envio input[name="entrega"]');
  else {
    const c = CAMPOS_ENVIO.find(x => x.requerido && !envio[x.id]);
    if (c) destino = document.getElementById(`envio-${c.id}`);
    else if (!envio.pago) destino = document.querySelector('#form-envio input[name="pago"]');
  }
  if (!destino) return;
  destino.scrollIntoView({ block: 'center', behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
  destino.focus({ preventScroll: true });
}

function faltantesTexto() {
  const n = datosFaltantes();
  return n ? `Faltan ${n} ${n === 1 ? 'dato' : 'datos'} · ir al primero` : 'Listo para enviar';
}
function actualizarFaltantes() {
  const el = document.getElementById('envio-faltan');
  if (el) { el.textContent = faltantesTexto(); el.classList.toggle('completo', !datosFaltantes()); }
}

function pasoEnviadoHTML() {
  const p = ultimoPedido;
  const r = p.resumen || {};
  const productos = carrito.map(i => `<li>${escaparHTML(i.casa)} ${escaparHTML(i.nombre)} · ${escaparHTML(textoTamano(i.tamano))}${i.cantidad > 1 ? ` ×${i.cantidad}` : ''}</li>`).join('');
  return `<div class="pedido-enviado">
    <p class="pedido-numero">Pedido <strong>#${escaparHTML(p.numero)}</strong></p>
    <p class="pedido-aviso">Abrimos WhatsApp con tu pedido ya escrito. <strong>Envíalo desde ahí para que lo recibamos;</strong> si no se abrió, usa el botón de abajo.</p>
    <dl class="pedido-resumen">
      <div><dt>Productos</dt><dd><ul>${productos}</ul></dd></div>
      <div><dt>Total estimado</dt><dd>${escaparHTML(r.total || '')}</dd></div>
      <div><dt>Entrega</dt><dd>${escaparHTML(r.entrega || '')}</dd></div>
      <div><dt>Dirección</dt><dd>${escaparHTML(r.direccion || '')}</dd></div>
      <div><dt>Pago</dt><dd>${escaparHTML(p.pago)}</dd></div>
      ${r.fecha ? `<div><dt>Lo necesitas</dt><dd>${escaparHTML(r.fecha)} · te confirmamos si llega a tiempo</dd></div>` : ''}
    </dl>
    <h3 class="pedido-subtitulo">Lo que sigue</h3>
    <ol class="pedido-pasos">
      <li>Te respondemos por WhatsApp ${HORARIO}, para confirmar tu pedido y ${p.pago === 'Tarjeta' ? 'mandarte la liga de pago segura de Mercado Pago (sin comisión)' : 'mandarte los datos para la transferencia'}.</li>
      <li>Al confirmarse el pago, preparamos tus decants al momento. Pedidos recibidos antes de las 18:00 se envían el siguiente día hábil, de lunes a viernes.</li>
      <li>${p.entrega === 'local' ? `Entrega en Monterrey: ${ENVIO.local.tiempo}.` : `Envío nacional: ${ENVIO.nacional.tiempo}.`}${p.conCompletos ? ' Los perfumes completos tardan de 7 a 10 días hábiles.' : ''}</li>
      <li>Al recibirlo, revisa tu paquete: si algo llega dañado, avísanos en 24 horas; si es otro perfume, en 48 horas.</li>
    </ol>
    <p class="pedido-gracias">Gracias por elegir Saúco.</p>
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
    encabezadoCarrito('Datos de envío', true, 2);
    cont.innerHTML = pasoEnvioHTML();
    // Pie fijo mínimo: total, lo que falta (lleva al primer dato) y el botón.
    pie.innerHTML = `
      <div class="carrito-total-fila carrito-total-final envio-pie-total"><span>Total estimado</span><span class="carrito-total-monto">${totalEstimadoTexto(envio.entrega)}</span></div>
      <button type="button" class="envio-faltan${datosFaltantes() ? '' : ' completo'}" id="envio-faltan" data-accion="ir-faltante" aria-live="polite">${faltantesTexto()}</button>
      <button type="submit" form="form-envio" class="carrito-principal">Enviar pedido por WhatsApp</button>
      <p class="carrito-nota-whatsapp">Se abrirá WhatsApp con tu pedido y tus datos ya escritos.</p>`;
  } else if (carritoPaso === 'enviado' && pedidoVigente()) {
    encabezadoCarrito('Último paso', false, 3);
    cont.innerHTML = pasoEnviadoHTML();
    pie.innerHTML = confirmandoNuevo ? `
      <p class="carrito-confirmar">¿Vaciar el carrito y empezar otro pedido? El pedido #${escaparHTML(ultimoPedido.numero)} no se borra de WhatsApp si ya lo enviaste.</p>
      <button type="button" class="carrito-principal" data-accion="nuevo-si">Sí, vaciar el carrito</button>
      <button type="button" class="enlace-secundario carrito-volver" data-accion="nuevo-no">Cancelar</button>` : `
      <button type="button" class="carrito-principal" data-accion="reenviar">Abrir WhatsApp para enviarlo</button>
      <div class="carrito-enlaces">
        <button type="button" class="enlace-secundario" data-accion="volver">Volver a mi carrito</button>
        <button type="button" class="enlace-secundario" data-accion="nuevo">Hacer un pedido nuevo</button>
      </div>`;
  } else {
    carritoPaso = 'carrito';
    encabezadoCarrito('Tu carrito', false, carrito.length ? 1 : 0);
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
  // Las llaves se insertan en el orden del formulario: el foco va al primer error.
  const e = {};
  if (!envio.entrega) e.entrega = 'Elige si lo recibes en Monterrey o por envío nacional.';
  const tel = envio.telefono.replace(/\D/g, '').replace(/^52(?=\d{10}$)/, '');
  CAMPOS_ENVIO.forEach(c => {
    if (c.requerido && !envio[c.id]) e[c.id] = `Escribe ${c.etiqueta.replace(/ \(.*\)$/, '').toLowerCase()}.`;
    else if (c.id === 'fecha' && envio.fecha && new Date(envio.fecha + 'T23:59:59') < new Date()) e.fecha = 'Elige una fecha de hoy en adelante.';
    else if (c.id === 'cp' && envio.cp && !/^\d{5}$/.test(envio.cp.replace(/\s/g, ''))) e.cp = 'El código postal tiene 5 dígitos.';
    else if (c.id === 'telefono' && envio.telefono && tel.length !== 10) e.telefono = 'El teléfono debe tener 10 dígitos, por ejemplo 81 1234 5678.';
  });
  if (!envio.pago) e.pago = 'Elige cómo prefieres pagar.';
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
  confirmandoNuevo = false;
  carritoPaso = pedidoVigente() && !verCarritoSinPedido ? 'enviado' : (carritoPaso === 'enviado' ? 'carrito' : carritoPaso);
  renderCarrito();
  ocultarAviso();
  const overlay = document.getElementById('carrito-overlay');
  const panel = document.getElementById('carrito-panel');
  if (!panel) return;
  carritoFocoPrevio = document.activeElement;
  // Una entrada en el historial: el botón «atrás» del celular cierra el carrito
  // en lugar de salir de la página.
  if (!(history.state && history.state.carrito)) history.pushState({ carrito: true }, '');
  overlay.hidden = false;
  panel.hidden = false;
  document.documentElement.classList.add('carrito-bloqueo');
  requestAnimationFrame(() => {
    overlay.classList.add('visible');
    panel.classList.add('abierto');
    panel.querySelector('.carrito-cerrar')?.focus();
  });
}

// Cierre explícito (botón, fondo, Escape): consume la entrada del historial,
// y el cierre real llega por «popstate».
function cerrarCarritoUI() {
  if (!carritoAbierto()) return;
  if (history.state && history.state.carrito) history.back();
  else cerrarCarrito();
}
window.addEventListener('popstate', () => { if (carritoAbierto()) cerrarCarrito(); });

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
let avisoFin = 0;        // momento en que se oculta el aviso
let avisoRestante = 0;   // tiempo que quedaba al pausar
// 8 s para alcanzar a leer y deshacer; se pausa mientras el cliente lo toca,
// le pasa el cursor o tiene el foco en él (WCAG 2.2.1).
const AVISO_MS = 8000;

function programarAviso(ms) {
  clearTimeout(avisoTimer);
  avisoRestante = 0;
  avisoFin = Date.now() + ms;
  avisoTimer = setTimeout(ocultarAviso, ms);
}
function pausarAviso() {
  if (!avisoFin) return;
  clearTimeout(avisoTimer);
  avisoRestante = Math.max(avisoFin - Date.now(), 0);
  avisoFin = 0;
}
function reanudarAviso() {
  const aviso = document.getElementById('carrito-aviso');
  if (avisoFin || !aviso || aviso.hidden) return;
  if (aviso.contains(document.activeElement)) return;
  programarAviso(Math.max(avisoRestante, 3000));
}

// Región viva aparte: el aviso tiene botones y no debe ser él mismo un «status».
function anunciar(texto) {
  let r = document.getElementById('carrito-anuncio');
  if (!r) {
    r = document.createElement('p');
    r.id = 'carrito-anuncio';
    r.className = 'sr-only';
    r.setAttribute('aria-live', 'polite');
    document.body.appendChild(r);
  }
  r.textContent = '';
  setTimeout(() => { r.textContent = texto; }, 50);
}

function pulsarContador() {
  const badge = document.getElementById('carrito-contador');
  if (!badge || badge.hidden) return;
  badge.classList.remove('pulso');
  void badge.offsetWidth; // reinicia la animación si se agrega dos veces seguidas
  badge.classList.add('pulso');
}

function mostrarAviso(texto, cantidad = 1) {
  const aviso = document.getElementById('carrito-aviso');
  if (!aviso) return;
  const llevas = cantidad > 1 ? ` · ya llevas ${cantidad}` : '';
  aviso.innerHTML = `<span class="carrito-aviso-texto"><strong>${escaparHTML(texto)}</strong> agregado${llevas}</span>
    <span class="carrito-aviso-acciones">
      <button type="button" class="carrito-aviso-deshacer">Deshacer</button>
      <button type="button" class="carrito-aviso-ver">Ver carrito</button>
    </span>`;
  aviso.hidden = false;
  requestAnimationFrame(() => aviso.classList.add('visible'));
  anunciar(`${texto} agregado al carrito${llevas}.`);
  programarAviso(AVISO_MS);
}

function ocultarAviso() {
  const aviso = document.getElementById('carrito-aviso');
  if (!aviso || aviso.hidden) return;
  clearTimeout(avisoTimer);
  avisoFin = 0;
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
  const est = envioPedido(envio.entrega);
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
    + `\nEnvío${hayCompletos() && hayDecants() ? ' de decants' : ''} (${ENVIO[envio.entrega].etiqueta}): ${est.texto}`
    + `\nTotal estimado: ${totalEstimadoTexto(envio.entrega)}`
    + `\nForma de pago: ${envio.pago}`
    + '\n\nDatos de envío:'
    + `\nNombre: ${envio.nombre}`
    + `\nTeléfono: ${tel}`
    + `\nDirección: ${envio.calle}, col. ${envio.colonia}, C.P. ${envio.cp.replace(/\s/g, '')}, ${envio.ciudad}, ${envio.estado}`
    + (envio.referencias ? `\nReferencias: ${envio.referencias}` : '')
    + (envio.fecha ? `\n\nLo necesito para: ${fechaLegible(envio.fecha)}` : '');
  if (carrito.some(item => item.precio == null)) {
    m += '\n\n(Nota: hay productos con precio por confirmar, no incluidos en el total.)';
  }
  if (hayCompletos()) {
    m += '\n\n(Incluye perfumes completos: sobre pedido, 7 a 10 días hábiles; el envío se confirma por WhatsApp.)';
  }
  return m;
}

function fechaLegible(iso) {
  try { return new Date(iso + 'T12:00:00').toLocaleDateString('es-MX', { weekday: 'long', day: 'numeric', month: 'long' }).replace(',', ''); }
  catch (e) { return iso; }
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
  const firma = firmaCarrito();
  const numero = ultimoPedido && ultimoPedido.firma === firma ? ultimoPedido.numero : generarNumeroPedido();
  const mensaje = mensajePedido(numero);
  ultimoPedido = {
    numero, firma, mensaje, entrega: envio.entrega, pago: envio.pago, conCompletos: hayCompletos(),
    resumen: {
      total: totalEstimadoTexto(envio.entrega),
      entrega: `${ENVIO[envio.entrega].etiqueta} · ${envioPedido(envio.entrega).texto}`,
      direccion: `${envio.calle}, col. ${envio.colonia}, C.P. ${envio.cp.replace(/\s/g, '')}, ${envio.ciudad}, ${envio.estado}`,
      fecha: envio.fecha ? fechaLegible(envio.fecha) : ''
    }
  };
  guardarPedido();
  verCarritoSinPedido = false;
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

  if (e.target.closest('.carrito-aviso-deshacer')) { deshacerUltima(); return; }
  if (e.target.closest('.carrito-aviso-ver')) { abrirCarrito(); return; }
  if (e.target.closest('#carrito-boton')) { abrirCarrito(); return; }
  const accion = e.target.closest('[data-accion]');
  if (accion && accion.closest('#carrito-panel')) {
    const a = accion.dataset.accion;
    if (a === 'continuar') { irAPaso('envio'); return; }
    if (a === 'ir-faltante') { irAlPrimerFaltante(); return; }
    if (a === 'reenviar' && ultimoPedido) { abrirWhatsApp(ultimoPedido.mensaje); return; }
    if (a === 'volver') { verCarritoSinPedido = true; irAPaso('carrito'); return; }
    if (a === 'nuevo') { confirmandoNuevo = true; renderCarrito(); document.querySelector('[data-accion="nuevo-no"]')?.focus(); return; }
    if (a === 'nuevo-no') { confirmandoNuevo = false; renderCarrito(); document.querySelector('[data-accion="nuevo"]')?.focus(); return; }
    if (a === 'nuevo-si') {
      confirmandoNuevo = false; carrito = []; borrarPedido(); carritoCambio(); irAPaso('carrito'); return;
    }
  }
  if (e.target.closest('#carrito-atras')) { irAPaso('carrito'); return; }
  if (e.target.closest('.carrito-cerrar') || e.target.id === 'carrito-overlay') { cerrarCarritoUI(); return; }
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

document.addEventListener('input', (e) => {
  const form = e.target.closest('#form-envio');
  if (!form || e.target.type === 'radio') return;
  leerFormEnvio(form);
  actualizarFaltantes();
});

document.addEventListener('focusin', (e) => {
  if (e.target.matches('#form-envio input:not([type="radio"]), #form-envio textarea')) document.getElementById('carrito-panel')?.classList.add('escribiendo');
});
document.addEventListener('focusout', (e) => {
  if (e.target.closest('#form-envio')) setTimeout(() => {
    if (!document.activeElement?.matches('#form-envio input:not([type="radio"]), #form-envio textarea')) document.getElementById('carrito-panel')?.classList.remove('escribiendo');
  }, 0);
});

document.addEventListener('change', (e) => {
  const form = e.target.closest('#form-envio');
  if (!form) return;
  leerFormEnvio(form);
  // Al elegir entrega local se sugiere la ciudad y el estado si están vacíos.
  if (e.target.name === 'entrega' && envio.entrega === 'local') {
    if (!envio.estado) envio.estado = 'Nuevo León';
  }
  guardarEnvio();
  if (e.target.name === 'fecha') {
    const r = document.getElementById('envio-fecha-respuesta');
    if (r) { r.textContent = respuestaFecha(); r.className = 'envio-fecha-respuesta' + (estadoFecha() ? ' ' + estadoFecha() : ''); }
  }
  actualizarFaltantes();
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
    cerrarCarritoUI();
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
  cargarPedido();
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

// Pausa del aviso mientras se interactúa con él.
(function () {
  const aviso = document.getElementById('carrito-aviso');
  if (!aviso) return;
  aviso.removeAttribute('role');
  aviso.removeAttribute('aria-live');
  aviso.addEventListener('pointerenter', pausarAviso);
  aviso.addEventListener('pointerleave', reanudarAviso);
  aviso.addEventListener('focusin', pausarAviso);
  aviso.addEventListener('focusout', () => setTimeout(reanudarAviso, 0));
  aviso.addEventListener('touchstart', pausarAviso, { passive: true });
  aviso.addEventListener('touchend', () => setTimeout(reanudarAviso, 0), { passive: true });
})();
