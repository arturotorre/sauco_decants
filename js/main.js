// Render de tarjetas, filtro por género, carrusel autoplay y ruteo por hash.
// Los datos viven en js/data.js (const PERFUMES).

function cardHTML(p) {
  const dot = 'dot-' + p.tier;
  const tierLabel = p.tier === 'nicho' ? 'Nicho' : 'Diseñador';
  const notas = p.notas.map(n => `<span class="nota-tag">${n}</span>`).join('');
  const precios = ['3ml', '5ml', '10ml'].map(ml => `
        <div class="precio-item"><span class="precio-ml">${ml}</span><span class="precio-val">${p.precios[ml] || ''}</span></div>`).join('');

  return `
  <div class="card">
    <div class="card-foto">
      <img src="${p.imagen}" alt="${p.alt}" onerror="this.style.display='none';this.nextElementSibling.style.display='block'">
      <span class="foto-label" style="display:none">Sin imagen</span>
      <div class="card-tier-dot ${dot}"></div>
    </div>
    <div class="card-info">
      <div class="card-casa">${p.casa}</div>
      <div class="card-nombre-fila">
        <div class="card-nombre">${p.nombre}</div>
        <button class="btn-agregar" data-casa="${p.casa}" data-nombre="${p.nombre}" aria-label="Agregar ${p.nombre} al carrito">
          <span class="btn-agregar-texto">Agregar al carrito</span>
          <span class="btn-agregar-icono" aria-hidden="true">🛒</span>
        </button>
      </div>
      <div class="card-genero">${p.genero}</div>
      <div class="card-notas">
        <span class="notas-label">Notas</span>
        <div class="notas-tags">${notas}</div>
      </div>
      <div class="card-divider"></div>
      <div class="card-precios">${precios}</div>
    </div>
    <div class="card-footer"><div class="card-footer-dot ${dot}"></div><span class="card-footer-text">${tierLabel} · Original</span></div>
  </div>`;
}

function coincideGenero(p, filtro) {
  if (filtro === 'todos') return true;
  if (p.genero === 'Unisex') return true;
  if (filtro === 'hombre') return p.genero === 'Masculino';
  if (filtro === 'mujer') return p.genero === 'Femenino';
  return true;
}

function renderCatalogo(filtro) {
  const contenedor = document.getElementById('vista-catalogo');
  const etiquetasGenero = { todos: 'Todos', hombre: 'Hombre', mujer: 'Mujer' };
  const tiers = [
    { key: 'nicho', clase: 'tier-nicho', label: 'Nicho' },
    { key: 'disenador', clase: 'tier-disenador', label: 'Diseñador' }
  ];

  const html = tiers.map(t => {
    const perfumes = PERFUMES.filter(p => p.tier === t.key && coincideGenero(p, filtro));
    if (!perfumes.length) return '';
    return `
    <div class="tier-header ${t.clase}">
      <div class="tier-line"></div><span class="tier-title">${t.label}</span><div class="tier-line"></div>
    </div>
    <div class="cards-grid">
      ${perfumes.map(cardHTML).join('')}
    </div>`;
  }).join('');

  contenedor.innerHTML = `<div class="main-content">
    <div class="vista-header"><h1>Decants - ${etiquetasGenero[filtro] || 'Todos'}</h1></div>
    ${html}
  </div>`;
}

function completoCardHTML(p) {
  return `
  <div class="card card-completo">
    <div class="card-foto">
      <img src="${p.imagen}" alt="${p.alt}" onerror="this.style.display='none';this.nextElementSibling.style.display='block'">
      <span class="foto-label" style="display:none">Sin imagen</span>
    </div>
    <div class="card-info">
      <div class="card-casa">${p.casa}</div>
      <div class="card-nombre-fila">
        <div class="card-nombre">${p.nombre}</div>
        <button class="btn-agregar btn-cotizar" data-casa="${p.casa}" data-nombre="${p.nombre}" data-concentracion="${p.concentracion}" aria-label="Cotizar ${p.nombre}">
          <span class="btn-agregar-texto">Cotizar</span>
          <span class="btn-agregar-icono" aria-hidden="true">💬</span>
        </button>
      </div>
      <div class="card-genero">${p.concentracion} · ${p.genero}</div>
    </div>
  </div>`;
}

let completosGenero = 'todos';
let completosMarca = 'todas';
let completosBusqueda = '';

function normalizarTexto(s) {
  return s.toLowerCase().normalize('NFD').replace(/\p{Diacritic}/gu, '');
}

function completosMarcasDisponibles() {
  const base = completosGenero === 'todos'
    ? PERFUMES_COMPLETOS
    : PERFUMES_COMPLETOS.filter(p => p.genero === completosGenero);
  return Array.from(new Set(base.map(p => p.casa))).sort((a, b) => a.localeCompare(b, 'es'));
}

function renderFiltroMarcaCompletos() {
  const cont = document.getElementById('completos-filtro-marca');
  const marcas = completosMarcasDisponibles();
  cont.innerHTML = ['<button type="button" class="completos-chip completos-chip-marca activo" data-marca="todas">Todas las marcas</button>']
    .concat(marcas.map(m => `<button type="button" class="completos-chip completos-chip-marca" data-marca="${m}">${m}</button>`))
    .join('');
}

function completosCoincide(p) {
  const okGenero = completosGenero === 'todos' || p.genero === completosGenero;
  const okMarca = completosMarca === 'todas' || p.casa === completosMarca;
  const busqueda = normalizarTexto(completosBusqueda.trim());
  const okBusqueda = !busqueda
    || normalizarTexto(p.nombre).includes(busqueda)
    || normalizarTexto(p.casa).includes(busqueda);
  return okGenero && okMarca && okBusqueda;
}

function renderCompletos() {
  const contenedor = document.getElementById('completos-grid');
  const grupos = [
    { key: 'Caballero', label: 'Caballero' },
    { key: 'Dama', label: 'Dama' }
  ];

  const html = grupos.map(g => {
    const perfumes = PERFUMES_COMPLETOS.filter(p => p.genero === g.key && completosCoincide(p));
    if (!perfumes.length) return '';
    return `
    <div class="completos-tier-header">
      <span class="completos-tier-titulo">${g.label}</span>
    </div>
    <div class="cards-grid">
      ${perfumes.map(completoCardHTML).join('')}
    </div>`;
  }).join('');

  contenedor.innerHTML = html.trim() ? html : '<p class="completos-sin-resultados">No encontramos perfumes con ese filtro.</p>';
}

function carruselSlideHTML(p) {
  return `
  <div class="card carrusel-slide">
    <div class="card-foto">
      <img src="${p.imagen}" alt="${p.alt}" onerror="this.style.display='none';this.nextElementSibling.style.display='block'">
      <span class="foto-label" style="display:none">Sin imagen</span>
    </div>
    <div class="card-info">
      <div class="card-casa">${p.casa}</div>
      <div class="card-nombre">${p.nombre}</div>
    </div>
  </div>`;
}

function renderCarrusel() {
  const destacados = PERFUMES.filter(p => p.bestseller);
  const track = document.getElementById('carrusel-track');
  const dotsWrap = document.getElementById('carrusel-dots');
  if (!track || !destacados.length) return;

  dotsWrap.innerHTML = destacados.map((_, i) => `<button class="carrusel-dot" data-i="${i}" aria-label="Ir al perfume ${i + 1}"></button>`).join('');
  const dots = Array.from(dotsWrap.children);

  let indice = 0;
  let timer = null;

  function mostrar(i) {
    indice = (i + destacados.length) % destacados.length;
    track.innerHTML = carruselSlideHTML(destacados[indice]);
    dots.forEach((d, idx) => d.classList.toggle('activo', idx === indice));
  }

  function iniciarAutoplay() { timer = setInterval(() => mostrar(indice + 1), 4500); }
  function detenerAutoplay() { clearInterval(timer); }
  function reiniciarAutoplay() { detenerAutoplay(); iniciarAutoplay(); }

  document.getElementById('carrusel-next').addEventListener('click', () => { mostrar(indice + 1); reiniciarAutoplay(); });
  document.getElementById('carrusel-prev').addEventListener('click', () => { mostrar(indice - 1); reiniciarAutoplay(); });
  dots.forEach(d => d.addEventListener('click', () => { mostrar(Number(d.dataset.i)); reiniciarAutoplay(); }));

  const viewport = document.querySelector('.carrusel-viewport');
  viewport.addEventListener('mouseenter', detenerAutoplay);
  viewport.addEventListener('mouseleave', iniciarAutoplay);
  viewport.addEventListener('touchstart', detenerAutoplay, { passive: true });
  viewport.addEventListener('touchend', iniciarAutoplay);

  mostrar(0);
  iniciarAutoplay();
}

function cerrarNavMovil() {
  const nav = document.getElementById('nav-lateral');
  const toggle = document.getElementById('nav-toggle');
  nav.classList.remove('nav-abierto');
  toggle.setAttribute('aria-expanded', 'false');
}

function route() {
  const hash = location.hash.replace(/^#\/?/, '');
  const [seccion, filtro] = hash.split('/');
  const vistaHome = document.getElementById('vista-home');
  const vistaCatalogo = document.getElementById('vista-catalogo');
  const vistaCompletos = document.getElementById('vista-completos');
  const navLinks = document.querySelectorAll('.nav-links a');

  vistaHome.hidden = true;
  vistaCatalogo.hidden = true;
  vistaCompletos.hidden = true;
  let activo = null;

  if (seccion === 'catalogo') {
    const genero = filtro || 'todos';
    vistaCatalogo.hidden = false;
    renderCatalogo(genero);
    activo = genero;
  } else if (seccion === 'completos') {
    vistaCompletos.hidden = false;
    activo = 'completos';
  } else {
    vistaHome.hidden = false;
  }

  navLinks.forEach(a => a.classList.toggle('activo', a.dataset.genero === activo));
  window.scrollTo(0, 0);
  cerrarNavMovil();
}

document.addEventListener('DOMContentLoaded', () => {
  renderCarrusel();
  renderFiltroMarcaCompletos();
  renderCompletos();
  route();

  document.getElementById('nav-toggle').addEventListener('click', () => {
    const nav = document.getElementById('nav-lateral');
    const abierto = nav.classList.toggle('nav-abierto');
    document.getElementById('nav-toggle').setAttribute('aria-expanded', String(abierto));
  });

  document.getElementById('completos-filtro-genero').addEventListener('click', (e) => {
    const btn = e.target.closest('.completos-chip');
    if (!btn) return;
    completosGenero = btn.dataset.filtroGenero;
    completosMarca = 'todas';
    document.querySelectorAll('#completos-filtro-genero .completos-chip').forEach(b => b.classList.toggle('activo', b === btn));
    renderFiltroMarcaCompletos();
    renderCompletos();
  });

  document.getElementById('completos-filtro-marca').addEventListener('click', (e) => {
    const btn = e.target.closest('.completos-chip');
    if (!btn) return;
    completosMarca = btn.dataset.marca;
    document.querySelectorAll('#completos-filtro-marca .completos-chip').forEach(b => b.classList.toggle('activo', b === btn));
    renderCompletos();
  });

  document.getElementById('completos-busqueda').addEventListener('input', (e) => {
    completosBusqueda = e.target.value;
    renderCompletos();
  });
});

window.addEventListener('hashchange', route);
