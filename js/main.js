// Render de tarjetas, filtro por género, portada y ruteo por hash.
// Los datos viven en js/data.js (const PERFUMES).

function escaparTexto(t) {
  return String(t ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

const GENERO_CORTO = { Masculino: 'Hombre', Femenino: 'Mujer', Unisex: 'Unisex' };

function fotoFilaHTML(src, alt, url) {
  const img = `<img src="${src}" alt="${alt}" loading="lazy" onerror="this.style.visibility='hidden'">`;
  return url
    ? `<a class="fila-foto" href="${url}" tabindex="-1" aria-hidden="true">${img}</a>`
    : `<span class="fila-foto">${img}</span>`;
}

function cardHTML(p) {
  const url = p.slug ? `/decants/${p.slug}/` : null;
  const notas = p.notas.slice(0, 3).map((n, i) => i ? n.toLocaleLowerCase('es') : n).join(', ');
  const nombre = url ? `<a class="fila-nombre" href="${url}">${p.alt}</a>` : `<span class="fila-nombre">${p.alt}</span>`;
  // Cada medida es su propio botón: un toque agrega esa medida al carrito.
  const medidas = ['3ml', '5ml', '10ml'].map(ml => {
    const n = ml.replace('ml', '');
    const precio = p.precios[ml];
    return `<button type="button" class="fila-medida" data-casa="${p.casa}" data-nombre="${p.nombre}" data-ml="${ml}" aria-label="Agregar ${p.alt} de ${n} ml, ${precio || 'precio a confirmar'}, al carrito">
        <span class="fila-medida-ml">${n}&nbsp;ml</span>
        <span class="fila-medida-precio">${precio || 'A confirmar'}</span>
      </button>`;
  }).join('');
  return `
  <li class="fila fila-decant">
    ${fotoFilaHTML(p.imagen, `${p.casa} ${p.alt}, decant`, url)}
    <div class="fila-texto">
      <span class="fila-casa">${p.casa}</span>
      ${nombre}
      <span class="fila-meta">${GENERO_CORTO[p.genero] || p.genero} · ${notas}</span>
    </div>
    <div class="fila-medidas" role="group" aria-label="Elige la medida de ${p.alt}">${medidas}</div>
  </li>`;
}

function vitrinaHTML(p) {
  return `<a class="vitrina-frasco" href="/decants/${p.slug}/" style="--escala:${p.escala || 1}">
    <img src="${p.imagen}" alt="${p.casa} ${p.alt}" loading="lazy" onerror="this.style.visibility='hidden'">
  </a>`;
}

function coincideTexto(p, busqueda) {
  const b = normalizarTexto(busqueda.trim());
  return !b || normalizarTexto(p.nombre).includes(b) || normalizarTexto(p.casa).includes(b);
}

function sinResultadosHTML({ busqueda, filtroActivo, urlSinFiltro, etiquetaFiltro, otroCatalogo }) {
  const q = escaparTexto(busqueda.trim());
  const acciones = [];
  // Solo se ofrece quitar el filtro cuando eso sí devuelve resultados.
  if (filtroActivo) acciones.push(`<button type="button" class="btn-secundario" data-buscar-en="${urlSinFiltro}" data-q="${q}">Ver resultados en ${etiquetaFiltro}</button>`);
  if (otroCatalogo) acciones.push(`<button type="button" class="btn-secundario" data-buscar-en="${otroCatalogo.url}" data-q="${q}">Ver «${q}» en ${otroCatalogo.etiqueta}</button>`);
  if (q) acciones.push('<button type="button" class="btn-secundario" data-limpiar-busqueda>Limpiar búsqueda</button>');
  if (q) acciones.push(`<button type="button" class="btn-secundario" data-cotizar="${q}">Cotizar «${q}» por WhatsApp</button>`);
  return `<div class="sin-resultados">
    <p class="sin-resultados-titulo">${q ? `No encontramos «${q}»` : 'No hay perfumes con este filtro'}</p>
    <p class="sin-resultados-texto">${q ? 'Revisa cómo se escribe, prueba con la marca o pídenos que lo consigamos.' : 'Prueba con otro filtro.'}</p>
    <div class="sin-resultados-acciones">${acciones.join('')}</div>
  </div>`;
}

function coincideGenero(p, filtro) {
  if (filtro === 'todos') return true;
  if (p.genero === 'Unisex') return true;
  if (filtro === 'hombre') return p.genero === 'Masculino';
  if (filtro === 'mujer') return p.genero === 'Femenino';
  return true;
}

let catalogoFiltroGenero = 'todos';
let catalogoBusqueda = '';

function catalogoCoincideBusqueda(p) {
  const busqueda = normalizarTexto(catalogoBusqueda.trim());
  return !busqueda
    || normalizarTexto(p.nombre).includes(busqueda)
    || normalizarTexto(p.casa).includes(busqueda);
}

function renderCatalogo(filtro) {
  const contenedor = document.getElementById('catalogo-grid');
  if (!contenedor) return;
  catalogoFiltroGenero = filtro;

  document.querySelectorAll('#vista-catalogo .catalogo-chip').forEach(a => {
    const activo = a.dataset.chip === filtro;
    a.classList.toggle('activo', activo);
    if (activo) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
  });

  // Vitrina de más vendidos: solo sin búsqueda, respetando el género elegido.
  const vitrina = document.getElementById('catalogo-vitrina');
  const destacados = PERFUMES.filter(p => p.bestseller && p.slug && coincideGenero(p, filtro)).slice(0, 4);
  vitrina.hidden = !!catalogoBusqueda.trim() || destacados.length === 0;
  document.getElementById('vitrina-repisa').innerHTML = destacados.map(vitrinaHTML).join('');

  const tiers = [
    { key: 'nicho', label: 'Nicho' },
    { key: 'disenador', label: 'Diseñador' }
  ];

  const grupos = tiers
    .map(t => ({ t, perfumes: PERFUMES.filter(p => p.tier === t.key && coincideGenero(p, filtro) && catalogoCoincideBusqueda(p)) }))
    .filter(g => g.perfumes.length);

  contenedor.innerHTML = grupos.length
    ? grupos.map(({ t, perfumes }) => `
    <section class="seccion-lista" aria-labelledby="tier-${t.key}">
      <h2 class="tier-header seccion-titulo" id="tier-${t.key}">${t.label} <span>${perfumes.length} ${perfumes.length === 1 ? 'perfume' : 'perfumes'}</span></h2>
      <ul class="filas">${perfumes.map(cardHTML).join('')}</ul>
    </section>`).join('')
    : sinResultadosHTML({
        busqueda: catalogoBusqueda,
        filtroActivo: filtro !== 'todos' && PERFUMES.some(p => coincideTexto(p, catalogoBusqueda)),
        urlSinFiltro: '#catalogo/todos', etiquetaFiltro: 'todos los decants',
        otroCatalogo: catalogoBusqueda.trim() && PERFUMES_COMPLETOS.some(p => coincideTexto(p, catalogoBusqueda)) ? { url: '#completos/todos', etiqueta: 'perfumes completos' } : null
      });
}

function completoCardHTML(p) {
  const disponible = p.precio != null;
  const url = p.slug ? `/completos/${p.slug}/` : null;
  const nombre = url ? `<a class="fila-nombre" href="${url}">${p.nombre}</a>` : `<span class="fila-nombre">${p.nombre}</span>`;
  const detalle = [p.concentracion, p.tamano && String(p.tamano).replace(/(\d)\s*ml$/i, '$1\u00a0ml')].filter(Boolean).join(' ');
  const meta = [detalle, GENERO_CORTO[p.genero] || p.genero, p.esSet ? 'Set de regalo' : ''].filter(Boolean).join(' · ');
  const incluye = p.contenido ? `<span class="fila-meta">Incluye: ${p.contenido.join(', ')}</span>` : '';
  const accion = disponible
    ? `<span class="fila-precio">${p.precio}</span>
       <button type="button" class="btn-agregar btn-agregar-completo fila-agregar" data-casa="${p.casa}" data-nombre="${p.nombre}" data-concentracion="${p.concentracion}" aria-label="Agregar ${p.nombre} ${p.concentracion} al carrito">Agregar</button>`
    : `<span class="fila-precio fila-precio-pendiente">Precio por consultar</span>
       <button type="button" class="btn-agregar btn-consultar-completo fila-agregar" data-casa="${p.casa}" data-nombre="${p.nombre}" data-concentracion="${p.concentracion}" aria-label="Consultar ${p.nombre} por WhatsApp">Consultar</button>`;
  return `
  <li class="fila">
    ${fotoFilaHTML(p.imagen, `${p.casa} ${p.nombre} ${p.concentracion}`, url)}
    <div class="fila-texto">
      <span class="fila-casa">${p.casa}</span>
      ${nombre}
      <span class="fila-meta">${meta}</span>
      ${incluye}
    </div>
    <div class="fila-accion">${accion}</div>
  </li>`;
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
  if (!cont) return;
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
  renderFiltroMarcaCompletos();
}

function establecerSetsCompletos(activo) {
  completosSoloSets = activo;
  renderFiltroMarcaCompletos();
}

function actualizarTituloCompletos(sub) {
  const actual = 'completos-' + (sub || 'todos');
  document.querySelectorAll('#vista-completos .catalogo-chip').forEach(a => {
    const activo = a.dataset.chip === actual;
    a.classList.toggle('activo', activo);
    if (activo) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
  });
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
  if (completosCategoria !== 'todas') n++;
  if (completosMarca !== 'todas') n++;
  badge.textContent = String(n);
  badge.hidden = n === 0;
}

function renderCompletos() {
  const contenedor = document.getElementById('completos-grid');
  if (!contenedor) return;
  const perfumes = ordenarCompletos(PERFUMES_COMPLETOS.filter(p => {
    const okGenero = completosGenero === 'todos' || p.genero === completosGenero || p.genero === 'Unisex';
    return okGenero && completosCoincide(p);
  }));

  const filtrosActivos = completosGenero !== 'todos' || completosSoloSets || completosCategoria !== 'todas' || completosMarca !== 'todas';
  contenedor.innerHTML = perfumes.length
    ? `<p class="lista-conteo">${perfumes.length} ${perfumes.length === 1 ? 'perfume' : 'perfumes'}</p><ul class="filas">${perfumes.map(completoCardHTML).join('')}</ul>`
    : sinResultadosHTML({
        busqueda: completosBusqueda,
        filtroActivo: filtrosActivos && PERFUMES_COMPLETOS.some(p => coincideTexto(p, completosBusqueda)),
        urlSinFiltro: '#completos/todos', etiquetaFiltro: 'todos los perfumes',
        otroCatalogo: completosBusqueda.trim() && PERFUMES.some(p => coincideTexto(p, completosBusqueda)) ? { url: '#catalogo/todos', etiqueta: 'decants' } : null
      });
  actualizarContadorFiltrosCompletos();
}

// ===== Portada «Atelier del perfumista» =====
const ATOMIZACIONES = { '3ml': 60, '5ml': 90, '10ml': 180 };

function precioDesde(p) {
  return p.precios['3ml'] || p.precios['5ml'] || p.precios['10ml'] || '';
}

function frascoHTML(p, clase) {
  return `<a class="${clase}" href="/decants/${p.slug}/" aria-label="${p.casa} ${p.alt}" style="--escala:${p.escala || 1}">
    <img src="${p.imagen}" alt="${p.casa} ${p.alt}" loading="lazy" onerror="this.style.visibility='hidden'">
  </a>`;
}

function estanteItemHTML(p) {
  const desde = precioDesde(p);
  return `<a class="estante-item" href="/decants/${p.slug}/" style="--escala:${p.escala || 1}">
    <span class="estante-foto"><img src="${p.imagen}" alt="${p.casa} ${p.alt}, decant" loading="lazy" onerror="this.style.visibility='hidden'"></span>
    <span class="estante-texto">
      <span class="estante-casa">${p.casa}</span>
      <span class="estante-nombre">${p.alt}</span>
      <span class="estante-precio">${desde ? 'Desde ' + desde + ' · 3 ml' : 'Precio a consultar'}</span>
    </span>
  </a>`;
}

function renderPortada() {
  const estante = document.getElementById('estante-vendidos');
  if (!estante) return; // no es la portada

  const conFicha = PERFUMES.filter(p => p.slug);
  const destacados = conFicha.filter(p => p.bestseller);
  const heroe = destacados[0] || conFicha[0];

  // Repisa principal: el más vendido
  if (heroe) {
    document.getElementById('repisa-frasco').href = `/decants/${heroe.slug}/`;
    const img = document.getElementById('repisa-img');
    if (img.getAttribute('src') !== heroe.imagen) img.src = heroe.imagen;
    img.alt = `${heroe.casa} ${heroe.alt}, el decant más vendido de Saúco`;
    document.getElementById('repisa-nombre').textContent = `${heroe.casa} ${heroe.alt.replace(/ (\S+)$/, '\u00a0$1')}`;
  }

  // Tiras de prueba: elegir medida
  const lectura = document.getElementById('tira-lectura');
  const tiras = Array.from(document.querySelectorAll('.tira'));
  function elegir(ml) {
    tiras.forEach(t => t.setAttribute('aria-pressed', String(t.dataset.ml === ml)));
    const precio = heroe && heroe.precios[ml];
    const medida = ml.replace('ml', '\u00a0ml');
    lectura.innerHTML = `<strong>≈ ${ATOMIZACIONES[ml]} atomizaciones</strong>` +
      (heroe ? `<span class="tira-lectura-extra"> · ${heroe.alt} en ${medida}</span>` : '');
    if (botonAgregar && heroe) {
      botonAgregar.dataset.ml = ml;
      botonAgregar.textContent = `Agregar ${medida}${precio ? ' · ' + precio : ''}`;
      botonAgregar.setAttribute('aria-label', `Agregar ${heroe.casa} ${heroe.alt} de ${medida.replace('\u00a0', ' ')} al carrito${precio ? ', ' + precio : ''}`);
    }
  }
  // Agregar el más vendido en la medida elegida, sin salir de la portada.
  const botonAgregar = document.getElementById('tira-agregar');
  botonAgregar?.addEventListener('click', () => {
    if (!heroe || typeof agregarAlCarrito !== 'function') return;
    agregarAlCarrito(heroe, botonAgregar.dataset.ml);
    botonAgregar.classList.add('agregado');
    setTimeout(() => botonAgregar.classList.remove('agregado'), 900);
  });
  tiras.forEach(t => t.addEventListener('click', () => elegir(t.dataset.ml)));
  elegir((tiras.find(t => t.getAttribute('aria-pressed') === 'true') || tiras[1]).dataset.ml);

  // Estante de más vendidos
  estante.innerHTML = (destacados.length ? destacados : conFicha.slice(0, 5)).map(estanteItemHTML).join('');

  // Rutas: viaje (diseñador) y nicho
  const viaje = conFicha.filter(p => p.tier === 'disenador' && p.bestseller)
    .concat(conFicha.filter(p => p.tier === 'disenador' && !p.bestseller)).slice(0, 3);
  const nicho = conFicha.filter(p => p.tier === 'nicho').slice(0, 3);
  document.getElementById('ruta-viaje').innerHTML = viaje.map(p => frascoHTML(p, '')).join('');
  document.getElementById('ruta-nicho').innerHTML = nicho.map(p => frascoHTML(p, '')).join('');
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
    document.title = filtro && filtro !== 'todos' ? `Decants para ${etiquetas[filtro].toLowerCase()} | Saúco` : 'Decants | Saúco';
  } else if (seccion === 'completos') {
    const etiquetas = { dama: 'Dama', caballero: 'Caballero', sets: 'Sets de regalo' };
    document.title = etiquetas[filtro] ? `Perfumes completos: ${etiquetas[filtro]} | Saúco` : 'Perfumes completos | Saúco';
  } else {
    document.title = 'Saúco Decants — Perfumes 100% Originales | Envíos a todo México';
  }
}

// Búsqueda que se traslada a otra vista (ej. «Ver X en perfumes completos»).
let busquedaPendiente = '';

function route() {
  const vistaHome = document.getElementById('vista-home');
  if (!vistaHome) return; // esta página no es la SPA (ej. una página de producto standalone)

  const hash = location.hash.replace(/^#\/?/, '');
  const [seccion, filtro, ancla] = hash.split('/');
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
    catalogoBusqueda = busquedaPendiente;
    const catalogoInputBusqueda = document.getElementById('catalogo-busqueda');
    if (catalogoInputBusqueda) catalogoInputBusqueda.value = busquedaPendiente;
    renderCatalogo(genero);
    activo = genero;
  } else if (seccion === 'completos') {
    const sub = filtro || 'todos';
    vistaCompletos.hidden = false;
    aplicarFiltroCompletosDesdeNav(sub);
    if (busquedaPendiente) {
      completosBusqueda = busquedaPendiente;
      document.getElementById('completos-busqueda').value = busquedaPendiente;
      renderCompletos();
    }
    activo = 'completos-' + sub;
  } else {
    vistaHome.hidden = false;
  }
  const anclaHome = seccion === 'originalidad' ? document.getElementById('originalidad') : null;

  navLinks.forEach(a => a.classList.toggle('activo', a.dataset.genero === activo));
  actualizarNavDecants(activo);
  actualizarNavCompletos(activo);
  busquedaPendiente = '';
  actualizarTituloPagina(seccion, filtro);
  window.scrollTo(0, 0);
  if (anclaHome) anclaHome.scrollIntoView();
  if (seccion === 'catalogo' && ancla) {
    document.getElementById('tier-' + ancla)?.scrollIntoView();
  }
  cerrarNavMovil();
}

document.addEventListener('DOMContentLoaded', () => {
  // Nota: main.js se incluye tanto en la SPA (index.html) como en páginas
  // de producto standalone (ej. /decants/<slug>/) que reutilizan la misma
  // nav pero no tienen los elementos del catálogo/completos. Por eso cada
  // listener de abajo se engancha solo si su elemento existe en esta página.
  renderPortada();
  renderFiltroMarcaCompletos();
  renderCompletos();
  route();

  document.getElementById('nav-toggle')?.addEventListener('click', () => {
    const nav = document.getElementById('nav-lateral');
    const abierto = nav.classList.toggle('nav-abierto');
    document.getElementById('nav-toggle').setAttribute('aria-expanded', String(abierto));
  });

  document.getElementById('nav-decants-toggle')?.addEventListener('click', () => {
    decantsAbierto = !decantsAbierto;
    document.getElementById('nav-item-decants').classList.toggle('abierto', decantsAbierto);
    document.getElementById('nav-decants-toggle').setAttribute('aria-expanded', String(decantsAbierto));
    completosNavAbierto = false;
    document.getElementById('nav-item-completos').classList.remove('abierto');
    document.getElementById('nav-completos-toggle').setAttribute('aria-expanded', 'false');
  });

  document.getElementById('nav-completos-toggle')?.addEventListener('click', () => {
    completosNavAbierto = !completosNavAbierto;
    document.getElementById('nav-item-completos').classList.toggle('abierto', completosNavAbierto);
    document.getElementById('nav-completos-toggle').setAttribute('aria-expanded', String(completosNavAbierto));
    decantsAbierto = false;
    document.getElementById('nav-item-decants').classList.remove('abierto');
    document.getElementById('nav-decants-toggle').setAttribute('aria-expanded', 'false');
  });

  document.getElementById('cotizar-toggle')?.addEventListener('click', () => {
    const panel = document.getElementById('cotizar-panel');
    const abrir = panel.hidden;
    panel.hidden = !abrir;
    document.getElementById('cotizar-toggle').setAttribute('aria-expanded', String(abrir));
  });

  document.getElementById('completos-filtro-genero')?.addEventListener('click', (e) => {
    const btn = e.target.closest('.completos-chip');
    if (!btn) return;
    establecerGeneroCompletos(btn.dataset.filtroGenero);
    renderCompletos();
  });

  document.getElementById('completos-filtro-categoria')?.addEventListener('click', (e) => {
    const btn = e.target.closest('.completos-chip');
    if (!btn) return;
    completosCategoria = btn.dataset.categoria;
    completosMarca = 'todas';
    document.querySelectorAll('#completos-filtro-categoria .completos-chip').forEach(b => b.classList.toggle('activo', b === btn));
    renderFiltroMarcaCompletos();
    renderCompletos();
  });

  document.getElementById('completos-filtro-marca')?.addEventListener('click', (e) => {
    const btn = e.target.closest('.completos-chip');
    if (!btn) return;
    completosMarca = btn.dataset.marca;
    document.querySelectorAll('#completos-filtro-marca .completos-chip').forEach(b => b.classList.toggle('activo', b === btn));
    renderCompletos();
  });

  document.getElementById('completos-busqueda')?.addEventListener('input', (e) => {
    completosBusqueda = e.target.value;
    renderCompletos();
  });

  document.addEventListener('click', (e) => {
    if (e.target.closest('[data-limpiar-busqueda]')) {
      const vistaCompletosVisible = !document.getElementById('vista-completos').hidden;
      const input = document.getElementById(vistaCompletosVisible ? 'completos-busqueda' : 'catalogo-busqueda');
      input.value = '';
      input.dispatchEvent(new Event('input'));
      input.focus();
      return;
    }
    const buscarEn = e.target.closest('[data-buscar-en]');
    if (buscarEn) {
      busquedaPendiente = buscarEn.dataset.q;
      const destino = buscarEn.dataset.buscarEn;
      if (location.hash === destino) route(); else location.hash = destino;
      return;
    }
    if (e.target.closest('[data-ir-cotizar]')) {
      document.getElementById('cotizar-titulo')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      document.getElementById('cotizar-nombre')?.focus({ preventScroll: true });
      return;
    }
    const cotizar = e.target.closest('[data-cotizar]');
    if (cotizar && typeof abrirWhatsApp === 'function') {
      abrirWhatsApp(`Hola, ¿me pueden cotizar ${cotizar.dataset.cotizar}? No lo encontré en el catálogo.`);
    }
  });

  document.getElementById('catalogo-busqueda')?.addEventListener('input', (e) => {
    catalogoBusqueda = e.target.value;
    renderCatalogo(catalogoFiltroGenero);
  });

  document.getElementById('completos-filtro-set')?.addEventListener('click', () => {
    establecerSetsCompletos(!completosSoloSets);
    renderCompletos();
  });

  document.getElementById('completos-orden-panel')?.addEventListener('click', (e) => {
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
      if (!panel) return;
      if (!panel.hidden) {
        panel.hidden = true;
        document.getElementById(toggleId).setAttribute('aria-expanded', 'false');
      }
    });
  }

  document.getElementById('completos-filtros-toggle')?.addEventListener('click', (e) => {
    e.stopPropagation();
    const panel = document.getElementById('completos-filtros-panel');
    const abrir = panel.hidden;
    cerrarDesplegablesCompletos(abrir ? 'completos-filtros-panel' : null);
    panel.hidden = !abrir;
    e.currentTarget.setAttribute('aria-expanded', String(abrir));
  });

  document.getElementById('completos-orden-toggle')?.addEventListener('click', (e) => {
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
