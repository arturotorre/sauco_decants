// Carrito de compras: estado (localStorage), selector de tamaño flotante,
// panel del carrito y checkout por WhatsApp. Depende de PERFUMES (js/data.js).

const CARRITO_STORAGE_KEY = 'sauco_carrito';
const CARRITO_WHATSAPP_NUMERO = '525612567245';

function perfumeId(p) {
  return (p.casa + ' ' + p.nombre)
    .toLowerCase()
    .normalize('NFD').replace(/\p{Diacritic}/gu, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '');
}

function formatoPrecio(valor) {
  return '$' + valor.toLocaleString('es-MX');
}

let carrito = [];

function cargarCarrito() {
  try {
    const guardado = JSON.parse(localStorage.getItem(CARRITO_STORAGE_KEY));
    carrito = Array.isArray(guardado) ? guardado : [];
  } catch (e) {
    carrito = [];
  }
}

function guardarCarrito() {
  localStorage.setItem(CARRITO_STORAGE_KEY, JSON.stringify(carrito));
}

function agregarAlCarrito(perfume, tamano) {
  const id = perfumeId(perfume);
  const precioStr = perfume.precios[tamano];
  const precio = precioStr ? Number(precioStr.replace(/[^0-9.]/g, '')) : null;
  const existente = carrito.find(item => item.perfumeId === id && item.tamano === tamano);

  if (existente) {
    existente.cantidad += 1;
  } else {
    carrito.push({
      perfumeId: id,
      casa: perfume.casa,
      nombre: perfume.nombre,
      imagen: perfume.imagen,
      alt: perfume.alt,
      tamano,
      precio,
      cantidad: 1
    });
  }

  guardarCarrito();
  actualizarBadge();
  renderCarrito();
}

function quitarDelCarrito(indice) {
  carrito.splice(indice, 1);
  guardarCarrito();
  actualizarBadge();
  renderCarrito();
}

function calcularTotal() {
  return carrito.reduce((suma, item) => item.precio != null ? suma + item.precio * item.cantidad : suma, 0);
}

function totalArticulos() {
  return carrito.reduce((suma, item) => suma + item.cantidad, 0);
}

function actualizarBadge() {
  const badge = document.getElementById('carrito-contador');
  const n = totalArticulos();
  badge.textContent = String(n);
  badge.hidden = n === 0;
}

function carritoItemHTML(item, indice) {
  const precioTexto = item.precio != null ? formatoPrecio(item.precio) : 'Precio a confirmar';
  const cantidadTexto = item.cantidad > 1 ? ` ×${item.cantidad}` : '';
  return `
  <div class="carrito-item">
    <button class="carrito-item-quitar" data-indice="${indice}" aria-label="Quitar ${item.nombre} del carrito">×</button>
    <div class="carrito-item-foto"><img src="${item.imagen}" alt="${item.alt}" onerror="this.style.display='none'"></div>
    <div class="carrito-item-info">
      <div class="carrito-item-casa">${item.casa}</div>
      <div class="carrito-item-nombre">${item.nombre}</div>
      <div class="carrito-item-detalle">${item.tamano}${cantidadTexto} · ${precioTexto}</div>
    </div>
  </div>`;
}

function renderCarrito() {
  const cont = document.getElementById('carrito-items');
  const totalEl = document.getElementById('carrito-total');

  cont.innerHTML = carrito.length
    ? carrito.map(carritoItemHTML).join('')
    : '<p class="carrito-vacio">Tu carrito está vacío.</p>';

  const total = calcularTotal();
  const hayPendientes = carrito.some(item => item.precio == null);
  totalEl.innerHTML = `
    <div class="carrito-total-monto">Total: ${formatoPrecio(total)}</div>
    ${hayPendientes ? '<div class="carrito-total-nota">Hay productos con precio por confirmar, no incluidos en el total.</div>' : ''}
  `;
}

function abrirCarrito() {
  renderCarrito();
  const overlay = document.getElementById('carrito-overlay');
  const panel = document.getElementById('carrito-panel');
  overlay.hidden = false;
  panel.hidden = false;
  requestAnimationFrame(() => {
    overlay.classList.add('visible');
    panel.classList.add('abierto');
  });
}

function cerrarCarrito() {
  const overlay = document.getElementById('carrito-overlay');
  const panel = document.getElementById('carrito-panel');
  overlay.classList.remove('visible');
  panel.classList.remove('abierto');
  setTimeout(() => {
    overlay.hidden = true;
    panel.hidden = true;
  }, 300);
}

function abrirSelectorTamano(perfume, boton) {
  const cont = document.getElementById('selector-tamano');
  cont.innerHTML = ['3ml', '5ml', '10ml'].map(tamano => {
    const precioStr = perfume.precios[tamano];
    const label = precioStr ? `${tamano} — ${precioStr}` : `${tamano} — Precio a confirmar`;
    return `<button class="selector-tamano-opcion" data-tamano="${tamano}">${label}</button>`;
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
  if (top + alto > window.innerHeight - 8) top = r.top - alto - 6;

  cont.style.top = top + 'px';
  cont.style.left = left + 'px';
}

function cerrarSelectorTamano() {
  document.getElementById('selector-tamano').hidden = true;
}

function generarNumeroPedido() {
  // Aleatorio criptográfico (no Math.random) para minimizar la probabilidad
  // de choque entre pedidos, ya que no hay base de datos que valide unicidad.
  const buffer = new Uint32Array(1);
  crypto.getRandomValues(buffer);
  return String(10000000 + (buffer[0] % 90000000));
}

function checkoutWhatsApp() {
  if (!carrito.length) return;

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

  let mensaje = 'Hola, me gustaría realizar un pedido de los siguientes decants:\n\n'
    + `Número de pedido: ${numeroPedido}\n\n`
    + lineas.join('\n')
    + `\n\nTotal: ${formatoPrecio(calcularTotal())}`;

  if (carrito.some(item => item.precio == null)) {
    mensaje += '\n\n(Nota: hay productos con precio por confirmar, no incluidos en el total.)';
  }

  window.open(`https://wa.me/${CARRITO_WHATSAPP_NUMERO}?text=${encodeURIComponent(mensaje)}`, '_blank');
}

document.addEventListener('click', (e) => {
  const btnCotizar = e.target.closest('.btn-cotizar');
  if (btnCotizar) {
    enviarCotizacionPerfume(btnCotizar.dataset.nombre, btnCotizar.dataset.casa, btnCotizar.dataset.concentracion);
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
    cerrarSelectorTamano();
    return;
  }

  const quitar = e.target.closest('.carrito-item-quitar');
  if (quitar) {
    quitarDelCarrito(Number(quitar.dataset.indice));
    return;
  }

  if (e.target.closest('#carrito-boton')) { abrirCarrito(); return; }
  if (e.target.closest('#carrito-checkout-whatsapp')) { checkoutWhatsApp(); return; }
  if (e.target.closest('.carrito-cerrar') || e.target.id === 'carrito-overlay') { cerrarCarrito(); return; }

  if (!e.target.closest('#selector-tamano')) cerrarSelectorTamano();
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    cerrarSelectorTamano();
    cerrarCarrito();
  }
});

function enviarCotizacion(nombrePerfume, marca) {
  const mensaje = `Hola, me gustaría cotizar ${nombrePerfume} de la marca ${marca}, por favor.`;
  window.open(`https://wa.me/${CARRITO_WHATSAPP_NUMERO}?text=${encodeURIComponent(mensaje)}`, '_blank');
}

function enviarCotizacionPerfume(nombrePerfume, marca, concentracion) {
  const mensaje = `¡Hola! Me gustaría cotizar el perfume ${nombrePerfume} de ${marca} en su versión ${concentracion} por favor.`;
  window.open(`https://wa.me/${CARRITO_WHATSAPP_NUMERO}?text=${encodeURIComponent(mensaje)}`, '_blank');
}

document.addEventListener('DOMContentLoaded', () => {
  cargarCarrito();
  actualizarBadge();

  const formCotizar = document.getElementById('form-cotizar');
  formCotizar.addEventListener('submit', (e) => {
    e.preventDefault();
    const nombrePerfume = document.getElementById('cotizar-nombre').value.trim();
    const marca = document.getElementById('cotizar-marca').value.trim() || 'N/A';
    if (!nombrePerfume) return;
    enviarCotizacion(nombrePerfume, marca);
    formCotizar.reset();
  });
});
