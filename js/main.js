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
      <img src="${p.imagen}" alt="${p.casa} ${p.alt} - decant de perfume ${p.genero.toLowerCase()}" loading="lazy" onerror="this.style.display='none';this.nextElementSibling.style.display='block'">
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
  const disponible = p.precio != null;

  const boton = disponible
    ? `<button class="btn-agregar btn-agregar-completo" data-casa="${p.casa}" data-nombre="${p.nombre}" aria-label="Agregar ${p.nombre} al carrito">
        <span class="btn-agregar-texto">Agregar al carrito</span>
        <span class="btn-agregar-icono" aria-hidden="true">🛒</span>
      </button>`
    : `<button class="btn-agregar btn-consultar-completo" data-casa="${p.casa}" data-nombre="${p.nombre}" aria-label="Consultar disponibilidad de ${p.nombre}">
        <span class="btn-agregar-texto">Consultar</span>
        <span class="btn-agregar-icono" aria-hidden="true">💬</span>
      </button>`;

  const precioHTML = disponible
    ? `<div class="card-precio-unico">${p.precio}</div>`
    : `<div class="card-precio-unico card-precio-consultar">¡Pregunta por disponibilidad!</div>`;

  const contenidoHTML = p.contenido ? `
      <div class="card-notas">
        <span class="notas-label">Incluye</span>
        <div class="notas-tags">${p.contenido.map(c => `<span class="nota-tag">${c}</span>`).join('')}</div>
      </div>` : '';

  return `
  <div class="card card-completo">
    <div class="card-foto">
      <img src="${p.imagen}" alt="${p.casa} ${p.alt} ${p.concentracion} - perfume ${p.esSet ? 'set de regalo' : 'de botella completa'}" loading="lazy" onerror="this.style.display='none';this.nextElementSibling.style.display='block'">
      <span class="foto-label" style="display:none">Sin imagen</span>
    </div>
    <div class="card-info">
      <div class="card-casa">${p.casa}</div>
      <div class="card-nombre-fila">
        <div class="card-nombre">${p.nombre}</div>
        ${boton}
      </div>
      <div class="card-genero">${p.concentracion} · ${p.genero}${p.esSet ? ' · Set de regalo' : ''}</div>
      ${contenidoHTML}
      <div class="card-divider"></div>
      ${precioHTML}
    </div>
  </div>`;
}

let completosGenero = 'todos';
let completosMarca = 'todas';
let completosCategoria = 'todas';
let completosBusqueda = '';
let completosSoloSets = false;
let completosOrden = 'relevancia';

function normalizarTexto(s) {
  return s.toLowerCase().normalize('NFD').replace(/\p{Diacritic}/gu, '');
}

function completosMarcasDisponibles() {
  const base = PERFUMES_COMPLETOS.filter(p =>
    (completosGenero === 'todos' || p.genero === completosGenero || p.genero === 'Unisex') &&
    (completosCategoria === 'todas' || p.categoria === completosCategoria) &&
    (!completosSoloSets || p.esSet === true)
  );
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
  const okMarca = completosMarca === 'todas' || p.casa === completosMarca;
  const okCategoria = completosCategoria === 'todas' || p.categoria === completosCategoria;
  const okSet = !completosSoloSets || p.esSet === true;
  const busqueda = normalizarTexto(completosBusqueda.trim());
  const okBusqueda = !busqueda
    || normalizarTexto(p.nombre).includes(busqueda)
    || normalizarTexto(p.casa).includes(busqueda);
  return okMarca && okCategoria && okSet && okBusqueda;
}

function completosPrecioNumero(p) {
  if (!p.precio) return null;
  return Number(p.precio.replace(/[^0-9]/g, ''));
}

function ordenarCompletos(perfumes) {
  const arr = perfumes.slice();
  const porPrecio = (dir) => (a, b) => {
    const pa = completosPrecioNumero(a);
    const pb = completosPrecioNumero(b);
    if (pa === null && pb === null) return 0;
    if (pa === null) return 1;
    if (pb === null) return -1;
    return dir * (pa - pb);
  };
  switch (completosOrden) {
    case 'precio-asc': arr.sort(porPrecio(1)); break;
    case 'precio-desc': arr.sort(porPrecio(-1)); break;
    case 'marca': arr.sort((a, b) => a.casa.localeCompare(b.casa, 'es') || a.nombre.localeCompare(b.nombre, 'es')); break;
    case 'nombre': arr.sort((a, b) => a.nombre.localeCompare(b.nombre, 'es')); break;
    default: break;
  }
  return arr;
}

function establecerGeneroCompletos(genero) {
  completosGenero = genero;
  completosMarca = 'todas';
  document.querySelectorAll('#completos-filtro-genero .completos-chip').forEach(b => b.classList.toggle('activo', b.dataset.filtroGenero === genero));
  renderFiltroMarcaCompletos();
}

function establecerSetsCompletos(activo) {
  completosSoloSets = activo;
  document.getElementById('completos-filtro-set').classList.toggle('activo', activo);
  renderFiltroMarcaCompletos();
}

function actualizarTituloCompletos(sub) {
  const etiquetas = { dama: 'Dama', caballero: 'Caballero', sets: 'Sets de regalo' };
  const el = document.getElementById('completos-titulo-texto');
  el.textContent = etiquetas[sub] ? `Perfumes completos - ${etiquetas[sub]}` : 'Perfumes completos';
}

function aplicarFiltroCompletosDesdeNav(sub) {
  completosBusqueda = '';
  const buscador = document.getElementById('completos-busqueda');
  if (buscador) buscador.value = '';

  if (sub === 'dama') {
    establecerGeneroCompletos('Dama');
    establecerSetsCompletos(false);
  } else if (sub === 'caballero') {
    establecerGeneroCompletos('Caballero');
    establecerSetsCompletos(false);
  } else if (sub === 'sets') {
    establecerGeneroCompletos('todos');
    establecerSetsCompletos(true);
  } else {
    establecerGeneroCompletos('todos');
    establecerSetsCompletos(false);
  }
  actualizarTituloCompletos(sub);
  renderCompletos();
}

function actualizarContadorFiltrosCompletos() {
  const badge = document.getElementById('completos-filtros-contador');
  let n = 0;
  if (completosGenero !== 'todos') n++;
  if (completosCategoria !== 'todas') n++;
  if (completosMarca !== 'todas') n++;
  if (completosSoloSets) n++;
  badge.textContent = String(n);
  badge.hidden = n === 0;
}

function renderCompletos() {
  const contenedor = document.getElementById('completos-grid');
  const perfumes = ordenarCompletos(PERFUMES_COMPLETOS.filter(p => {
    const okGenero = completosGenero === 'todos' || p.genero === completosGenero || p.genero === 'Unisex';
    return okGenero && completosCoincide(p);
  }));

  contenedor.innerHTML = perfumes.length
    ? `<div class="cards-grid">${perfumes.map(completoCardHTML).join('')}</div>`
    : '<p class="completos-sin-resultados">No encontramos perfumes con ese filtro.</p>';
  actualizarContadorFiltrosCompletos();
}

function carruselSlideHTML(p) {
  return `
  <div class="card carrusel-slide">
    <div class="card-foto">
      <img src="${p.imagen}" alt="${p.casa} ${p.alt} - de los más vendidos en Saúco Decants" onerror="this.style.display='none';this.nextElementSibling.style.display='block'">
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

let decantsAbierto = false;
let completosNavAbierto = false;

function actualizarNavDecants(activo) {
  const item = document.getElementById('nav-item-decants');
  const toggle = document.getElementById('nav-decants-toggle');
  const esDecants = ['todos', 'hombre', 'mujer'].includes(activo);
  if (esDecants) decantsAbierto = true;
  item.classList.toggle('abierto', decantsAbierto);
  toggle.classList.toggle('activo', esDecants);
  toggle.setAttribute('aria-expanded', String(decantsAbierto));
}

function actualizarNavCompletos(activo) {
  const item = document.getElementById('nav-item-completos');
  const toggle = document.getElementById('nav-completos-toggle');
  const esCompletos = typeof activo === 'string' && activo.startsWith('completos-');
  if (esCompletos) completosNavAbierto = true;
  item.classList.toggle('abierto', completosNavAbierto);
  toggle.classList.toggle('activo', esCompletos);
  toggle.setAttribute('aria-expanded', String(completosNavAbierto));
}

function actualizarTituloPagina(seccion, filtro) {
  if (seccion === 'catalogo') {
    const etiquetas = { todos: 'Todos', hombre: 'Hombre', mujer: 'Mujer' };
    document.title = `Decants - ${etiquetas[filtro] || 'Todos'} | Saúco`;
  } else if (seccion === 'completos') {
    const etiquetas = { dama: 'Dama', caballero: 'Caballero', sets: 'Sets de regalo' };
    document.title = etiquetas[filtro] ? `Perfumes completos - ${etiquetas[filtro]} | Saúco` : 'Perfumes completos | Saúco';
  } else {
    document.title = 'Saúco — Catálogo de Fragancias';
  }
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
    const sub = filtro || 'todos';
    vistaCompletos.hidden = false;
    aplicarFiltroCompletosDesdeNav(sub);
    activo = 'completos-' + sub;
  } else {
    vistaHome.hidden = false;
  }

  navLinks.forEach(a => a.classList.toggle('activo', a.dataset.genero === activo));
  actualizarNavDecants(activo);
  actualizarNavCompletos(activo);
  actualizarTituloPagina(seccion, filtro);
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

  document.getElementById('nav-decants-toggle').addEventListener('click', () => {
    decantsAbierto = !decantsAbierto;
    document.getElementById('nav-item-decants').classList.toggle('abierto', decantsAbierto);
    document.getElementById('nav-decants-toggle').setAttribute('aria-expanded', String(decantsAbierto));
    completosNavAbierto = false;
    document.getElementById('nav-item-completos').classList.remove('abierto');
    document.getElementById('nav-completos-toggle').setAttribute('aria-expanded', 'false');
  });

  document.getElementById('nav-completos-toggle').addEventListener('click', () => {
    completosNavAbierto = !completosNavAbierto;
    document.getElementById('nav-item-completos').classList.toggle('abierto', completosNavAbierto);
    document.getElementById('nav-completos-toggle').setAttribute('aria-expanded', String(completosNavAbierto));
    decantsAbierto = false;
    document.getElementById('nav-item-decants').classList.remove('abierto');
    document.getElementById('nav-decants-toggle').setAttribute('aria-expanded', 'false');
  });

  document.getElementById('cotizar-toggle').addEventListener('click', () => {
    const panel = document.getElementById('cotizar-panel');
    const abrir = panel.hidden;
    panel.hidden = !abrir;
    document.getElementById('cotizar-toggle').setAttribute('aria-expanded', String(abrir));
  });

  document.getElementById('completos-filtro-genero').addEventListener('click', (e) => {
    const btn = e.target.closest('.completos-chip');
    if (!btn) return;
    establecerGeneroCompletos(btn.dataset.filtroGenero);
    renderCompletos();
  });

  document.getElementById('completos-filtro-categoria').addEventListener('click', (e) => {
    const btn = e.target.closest('.completos-chip');
    if (!btn) return;
    completosCategoria = btn.dataset.categoria;
    completosMarca = 'todas';
    document.querySelectorAll('#completos-filtro-categoria .completos-chip').forEach(b => b.classList.toggle('activo', b === btn));
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

  document.getElementById('completos-filtro-set').addEventListener('click', () => {
    establecerSetsCompletos(!completosSoloSets);
    renderCompletos();
  });

  document.getElementById('completos-orden-panel').addEventListener('click', (e) => {
    const btn = e.target.closest('.completos-orden-opcion');
    if (!btn) return;
    completosOrden = btn.dataset.orden;
    document.querySelectorAll('.completos-orden-opcion').forEach(b => b.classList.toggle('activo', b === btn));
    cerrarDesplegablesCompletos();
    renderCompletos();
  });

  function cerrarDesplegablesCompletos(exceptoId) {
    [['completos-filtros-panel', 'completos-filtros-toggle'], ['completos-orden-panel', 'completos-orden-toggle']].forEach(([panelId, toggleId]) => {
      if (panelId === exceptoId) return;
      const panel = document.getElementById(panelId);
      if (!panel.hidden) {
        panel.hidden = true;
        document.getElementById(toggleId).setAttribute('aria-expanded', 'false');
      }
    });
  }

  document.getElementById('completos-filtros-toggle').addEventListener('click', (e) => {
    e.stopPropagation();
    const panel = document.getElementById('completos-filtros-panel');
    const abrir = panel.hidden;
    cerrarDesplegablesCompletos(abrir ? 'completos-filtros-panel' : null);
    panel.hidden = !abrir;
    e.currentTarget.setAttribute('aria-expanded', String(abrir));
  });

  document.getElementById('completos-orden-toggle').addEventListener('click', (e) => {
    e.stopPropagation();
    const panel = document.getElementById('completos-orden-panel');
    const abrir = panel.hidden;
    cerrarDesplegablesCompletos(abrir ? 'completos-orden-panel' : null);
    panel.hidden = !abrir;
    e.currentTarget.setAttribute('aria-expanded', String(abrir));
  });

  document.addEventListener('click', (e) => {
    if (!e.target.closest('#completos-filtros-wrap') && !e.target.closest('#completos-orden-wrap')) {
      cerrarDesplegablesCompletos();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') cerrarDesplegablesCompletos();
  });
});

window.addEventListener('hashchange', route);
