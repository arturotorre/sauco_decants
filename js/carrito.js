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
    </div>
    <button type="button" class="carrito-item-quitar" data-indice="${indice}">Quitar<span class="sr-only"> ${nombre} del carrito</span></button>
  </div>`;
}

function renderCarrito() {
  const cont = document.getElementById('carrito-items');
  const totalEl = document.getElementById('carrito-total');
  const checkout = document.getElementById('carrito-checkout-whatsapp');
  if (!cont || !totalEl) return;

  const vacio = carrito.length === 0;
  cont.innerHTML = vacio
    ? `<div class="carrito-vacio">
         <p>Tu carrito está vacío.</p>
         <a class="enlace-secundario" href="/#catalogo/todos">Explorar decants</a>
       </div>`
    : carrito.map(carritoItemHTML).join('');

  const hayPendientes = carrito.some(item => item.precio == null);
  const n = totalArticulos();
  totalEl.innerHTML = vacio ? '' : `
    <div class="carrito-total-fila"><span>Total · ${n} ${n === 1 ? 'artículo' : 'artículos'}</span><span class="carrito-total-monto">${formatoPrecio(calcularTotal())}</span></div>
    ${hayPendientes ? '<p class="carrito-total-nota">Hay productos con precio por confirmar; no están incluidos en el total.</p>' : ''}`;

  if (checkout) checkout.disabled = vacio;
  document.querySelector('.carrito-panel-footer')?.classList.toggle('vacio', vacio);
}

// ----- Panel del carrito (diálogo) -----
let carritoFocoPrevio = null;

function carritoAbierto() {
  const panel = document.getElementById('carrito-panel');
  return panel && !panel.hidden;
}

function abrirCarrito() {
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
    .querySelectorAll('a[href], button:not([disabled])'));
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

function checkoutWhatsApp() {
  if (!carrito.length) return;

  // TODO: pedir los datos de envío (nombre, dirección, ciudad, CP, teléfono)
  // antes de abrir WhatsApp e incluirlos en el mensaje del pedido. Hoy el
  // envío se coordina por WhatsApp después de recibir el pedido.

  const numeroPedido = generarNumeroPedido();

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

  let mensaje = 'Hola, me gustaría realizar el siguiente pedido:\n\n'
    + `Número de pedido: ${numeroPedido}\n\n`
    + lineas.join('\n')
    + `\n\nTotal: ${formatoPrecio(calcularTotal())}`;

  if (carrito.some(item => item.precio == null)) {
    mensaje += '\n\n(Nota: hay productos con precio por confirmar, no incluidos en el total.)';
  }

  abrirWhatsApp(mensaje);
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
  if (e.target.closest('#carrito-checkout-whatsapp')) { checkoutWhatsApp(); return; }
  if (e.target.closest('.carrito-cerrar') || e.target.id === 'carrito-overlay') { cerrarCarrito(); return; }
  // Un enlace dentro del carrito (ej. "Explorar decants" con el carrito vacío)
  // navega y cierra el panel.
  if (e.target.closest('#carrito-panel a[href]')) { cerrarCarrito(); return; }

  if (!e.target.closest('#selector-tamano')) cerrarSelectorTamano(false);
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
  abrirWhatsApp(`Hola, me gustaría cotizar ${nombrePerfume} de la marca ${marca}, por favor.`);
}

function enviarConsultaDisponibilidad(nombrePerfume, marca) {
  abrirWhatsApp(`Hola, estoy interesado en ${nombrePerfume} de ${marca}, ¿me podrían brindar información de costo y tiempo de entrega?`);
}

document.addEventListener('DOMContentLoaded', () => {
  cargarCarrito();
  actualizarBadge();
  renderCarrito();

  const formCotizar = document.getElementById('form-cotizar');
  formCotizar?.addEventListener('submit', (e) => {
    e.preventDefault();
    const nombrePerfume = document.getElementById('cotizar-nombre').value.trim();
    const marca = document.getElementById('cotizar-marca').value.trim() || 'N/A';
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
