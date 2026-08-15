#!/usr/bin/env python3
"""
Genera páginas HTML estáticas por producto (una URL real y rastreable por
producto, con contenido editorial único) a partir de:
  1. Los datos base del catálogo (js/data.js) — casa, nombre, precios, notas.
  2. El contenido editorial curado a mano en CONTENIDO_DECANTS de este
     archivo (descripción, notas por pirámide, ocasión/duración) — nunca
     generado en automático: cada fragancia se investiga antes de escribirla,
     igual que se hizo para las notas olfativas del catálogo.

Uso:
  python3 tools/generar_pagina_producto.py

Genera una carpeta por producto en decants/<slug>/index.html (URL final:
https://saucodecants.com/decants/<slug>/), reutilizando el nav y el CSS
del sitio. Las páginas cargan js/data.js + js/main.js + js/carrito.js para
que "Agregar al carrito" funcione igual que en el catálogo.
"""

import json
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATA_JS = RAIZ / "js" / "data.js"

# --- Contenido editorial curado a mano, un producto a la vez ------------
# clave: "casa|nombre" tal como aparece en js/data.js (PERFUMES)
CONTENIDO_DECANTS = {
    "Le Labo|Santal 33 EDP": {
        "slug": "le-labo-santal-33",
        "meta_descripcion": (
            "Decant de Santal 33 de Le Labo (3ml, 5ml, 10ml), 100% original. "
            "Amaderado, especiado y unisex — el nicho más icónico de la última "
            "década. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Cardamomo", "Iris", "Violeta"],
        "notas_corazon": ["Sándalo", "Papiro", "Cuero"],
        "notas_fondo": ["Cedro", "Vainilla", "Ámbar"],
        "parrafos": [
            "Santal 33 es la fragancia insignia de Le Labo, lanzada en 2011 y creada por "
            "el perfumista Frank Voelkl. Abre con un golpe especiado de cardamomo junto a "
            "violeta e iris polvorientos, que da paso a un corazón cremoso de sándalo, "
            "papiro y cuero — la combinación que la volvió uno de los perfumes de nicho "
            "más reconocibles (y más imitados) de los últimos años. Cierra con cedro, "
            "vainilla y ámbar en un fondo cálido y terroso.",

            "Es completamente unisex y funciona todo el año, aunque su carácter amaderado "
            "y especiado brilla especialmente en otoño e invierno. Es versátil: sirve "
            "tanto para el día a día como para una cita o una salida nocturna, dejando una "
            "estela notable sin llegar a ser abrumadora.",
        ],
        "ideal_para": "Uso diario, citas y salidas nocturnas — todo el año, especialmente otoño e invierno.",
        "duracion": "6 a 8 horas en piel, con estela moderada.",
    },
}


def leer_catalogo_propio():
    """Igual que en verificar_precios.py: no se puede eval() directo porque
    las declaraciones const quedan fuera de alcance — se concatena el
    archivo con un console.log final y se corre como un solo script."""
    fuente = DATA_JS.read_text(encoding="utf-8")
    script = fuente + "\nconsole.log(JSON.stringify({PERFUMES, PERFUMES_COMPLETOS}));"
    resultado = subprocess.run(["node", "-e", script], capture_output=True, text=True, check=True)
    return json.loads(resultado.stdout)


def notas_tags_html(notas):
    return "".join(f'<span class="nota-tag">{n}</span>' for n in notas)


def precios_html(precios):
    filas = []
    for ml in ("3ml", "5ml", "10ml"):
        filas.append(
            f'<div class="precio-item"><span class="precio-ml">{ml}</span>'
            f'<span class="precio-val">{precios.get(ml, "")}</span></div>'
        )
    return "".join(filas)


def render_pagina(perfume, contenido):
    casa = perfume["casa"]
    nombre_mostrar = contenido.get("nombre_mostrar") or perfume["nombre"].replace(" EDP", "").replace(" EDT", "")
    genero = perfume["genero"]
    genero_lower = genero.lower()
    tier = perfume["tier"]
    tier_label = "Nicho" if tier == "nicho" else "Diseñador"
    dot = f"dot-{tier}"
    imagen_rel = perfume["imagen"]  # ya es absoluta desde la raíz (ej. "/imagenes/...")
    titulo = f"{casa} {nombre_mostrar} — Decant de Perfume {genero_lower.capitalize()} | Saúco Decants"
    meta_desc = contenido["meta_descripcion"]
    url = f"https://saucodecants.com/decants/{contenido['slug']}/"
    alt_img = f"{casa} {nombre_mostrar} - decant de perfume {genero_lower}"

    parrafos_html = "".join(f"<p>{p}</p>" for p in contenido["parrafos"])

    precios = perfume["precios"]
    precio_min = min(int(v.replace("$", "").replace(",", "")) for v in precios.values() if v)
    ofertas = "".join(
        f'''    {{
      "@type": "Offer",
      "name": "{casa} {nombre_mostrar} ({ml})",
      "price": "{precios[ml].replace("$", "").replace(",", "")}",
      "priceCurrency": "MXN",
      "availability": "https://schema.org/InStock",
      "url": "{url}"
    }}{"," if ml != "10ml" else ""}
'''
        for ml in ("3ml", "5ml", "10ml") if precios.get(ml)
    )

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="format-detection" content="telephone=no">
<title>{titulo}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#3D2314">

<meta property="og:type" content="product">
<meta property="og:site_name" content="Saúco Decants">
<meta property="og:locale" content="es_MX">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:image" content="https://saucodecants.com{perfume['imagen']}">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{titulo}">
<meta name="twitter:description" content="{meta_desc}">
<meta name="twitter:image" content="https://saucodecants.com{perfume['imagen']}">

<link rel="icon" type="image/png" href="/imagenes/Saúco_2.png">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&family=Jost:wght@200;300;400&display=swap" rel="stylesheet">
<link href="/css/styles.css" rel="stylesheet">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{casa} {nombre_mostrar}",
  "brand": {{ "@type": "Brand", "name": "{casa}" }},
  "description": "{meta_desc}",
  "image": "https://saucodecants.com{perfume['imagen']}",
  "url": "{url}",
  "offers": [
{ofertas}  ]
}}
</script>
</head>
<body>

<nav class="nav-lateral" id="nav-lateral">
  <button class="nav-hamburguesa" id="nav-toggle" aria-label="Abrir menú" aria-expanded="false">
    <span></span><span></span><span></span>
  </button>
  <a href="/#home" class="nav-marca">Saúco</a>
  <ul class="nav-links">
    <li class="nav-item-decants" id="nav-item-decants">
      <button type="button" class="nav-desplegable" id="nav-decants-toggle" aria-expanded="false" aria-controls="nav-decants-submenu">
        Decants
        <span class="nav-desplegable-flecha" aria-hidden="true">▾</span>
      </button>
      <ul class="nav-submenu" id="nav-decants-submenu">
        <li><a href="/#catalogo/todos" data-genero="todos">Todos</a></li>
        <li><a href="/#catalogo/hombre" data-genero="hombre">Hombre</a></li>
        <li><a href="/#catalogo/mujer" data-genero="mujer">Mujer</a></li>
      </ul>
    </li>
    <li class="nav-item-completos" id="nav-item-completos">
      <button type="button" class="nav-desplegable" id="nav-completos-toggle" aria-expanded="false" aria-controls="nav-completos-submenu">
        Perfumes completos
        <span class="nav-desplegable-flecha" aria-hidden="true">▾</span>
      </button>
      <ul class="nav-submenu" id="nav-completos-submenu">
        <li><a href="/#completos/todos" data-genero="completos-todos">Todos</a></li>
        <li><a href="/#completos/dama" data-genero="completos-dama">Dama</a></li>
        <li><a href="/#completos/caballero" data-genero="completos-caballero">Caballero</a></li>
        <li><a href="/#completos/sets" data-genero="completos-sets">Sets de regalo</a></li>
      </ul>
    </li>
  </ul>
</nav>

<div class="main-content producto-detalle">
  <nav class="breadcrumb" aria-label="Ruta de navegación">
    <a href="/">Inicio</a> › <a href="/#catalogo/todos">Decants</a> › <span>{nombre_mostrar}</span>
  </nav>

  <div class="producto-hero">
    <div class="producto-foto card-foto">
      <img src="{imagen_rel}" alt="{alt_img}" onerror="this.style.display='none';this.nextElementSibling.style.display='block'">
      <span class="foto-label" style="display:none">Sin imagen</span>
      <div class="card-tier-dot {dot}"></div>
    </div>
    <div class="producto-info">
      <div class="card-casa">{casa}</div>
      <h1 class="producto-nombre">{nombre_mostrar}</h1>
      <div class="card-genero">{genero}</div>
      <div class="notas-tags">{notas_tags_html(perfume["notas"])}</div>
      <div class="card-divider"></div>
      <div class="card-precios">{precios_html(precios)}</div>
      <button class="btn-agregar producto-btn-agregar" data-casa="{casa}" data-nombre="{perfume['nombre']}" aria-label="Agregar {nombre_mostrar} al carrito">
        <span class="btn-agregar-texto">Agregar al carrito</span>
        <span class="btn-agregar-icono" aria-hidden="true">🛒</span>
      </button>
      <div class="card-footer-text">{tier_label} · Original · Desde ${precio_min:,}</div>
    </div>
  </div>

  <div class="producto-editorial">
    <h2>Sobre esta fragancia</h2>
    {parrafos_html}

    <div class="producto-notas-detalle">
      <div><span class="notas-label">Notas de salida</span><div class="notas-tags">{notas_tags_html(contenido["notas_salida"])}</div></div>
      <div><span class="notas-label">Notas de corazón</span><div class="notas-tags">{notas_tags_html(contenido["notas_corazon"])}</div></div>
      <div><span class="notas-label">Notas de fondo</span><div class="notas-tags">{notas_tags_html(contenido["notas_fondo"])}</div></div>
    </div>

    <div class="producto-datos">
      <div><strong>Ideal para</strong>{contenido["ideal_para"]}</div>
      <div><strong>Duración</strong>{contenido["duracion"]}</div>
    </div>

    <div class="producto-volver">
      <a href="/#catalogo/todos">← Ver todos los decants</a>
    </div>
  </div>
</div>

<button id="carrito-boton" aria-label="Ver carrito">
  <span aria-hidden="true">🛒</span>
  <span id="carrito-contador" hidden>0</span>
</button>

<div id="carrito-overlay" hidden></div>
<aside id="carrito-panel" hidden aria-label="Carrito de compras">
  <div class="carrito-panel-header">
    <h2>Tu carrito</h2>
    <button class="carrito-cerrar" aria-label="Cerrar carrito">×</button>
  </div>
  <div id="carrito-items"></div>
  <div class="carrito-panel-footer">
    <div id="carrito-total"></div>
    <button id="carrito-checkout-whatsapp">Confirmar Pedido</button>
  </div>
</aside>

<div id="selector-tamano" hidden></div>

<div class="footer-global">
  <div class="footer-nombre">Saúco</div>
  <div class="footer-linea"></div>
  <div class="footer-linea2"></div>
  <div class="footer-sub">Decants · Monterrey · Envíos a todo México</div>
  <div class="footer-contacto">Escríbenos por WhatsApp o DM de Instagram para hacer tu pedido</div>
  <div class="footer-redes">
    <div class="red-item"><span class="red-icon" style="color:rgba(184,115,51,0.6)">Instagram</span><span class="red-handle-dark"><a href="https://www.instagram.com/sauco.decants/?utm_source=ig_web_button_share_sheet" target="_blank" rel="noopener noreferrer">@sauco.decants</a></span></div>
    <div class="red-item"><span class="red-icon" style="color:rgba(184,115,51,0.6)">TikTok</span><span class="red-handle-dark"><a href="https://www.tiktok.com/@saucodecants" target="_blank" rel="noopener noreferrer">@saucodecants</a></span></div>
    <div class="red-item"><span class="red-icon" style="color:rgba(184,115,51,0.6)">Facebook</span><span class="red-handle-dark"><a href="https://www.facebook.com/share/175fic6S1r/?mibextid=wwXIfr" target="_blank" rel="noopener noreferrer">Saúco Decants</a></span></div>
    <div class="red-item"><span class="red-icon" style="color:rgba(184,115,51,0.6)">WhatsApp</span><span class="red-handle-dark"><a href="https://wa.me/525612567245">56 1256 7245</a></span></div>
  </div>
</div>

<script src="/js/data.js"></script>
<script src="/js/main.js"></script>
<script src="/js/carrito.js"></script>
</body>
</html>
"""


def main():
    catalogo = leer_catalogo_propio()
    perfumes_por_clave = {f"{p['casa']}|{p['nombre']}": p for p in catalogo["PERFUMES"]}

    generados = []
    for clave, contenido in CONTENIDO_DECANTS.items():
        perfume = perfumes_por_clave.get(clave)
        if not perfume:
            print(f"  ⚠ no encontrado en js/data.js, se omite: {clave}")
            continue
        html = render_pagina(perfume, contenido)
        destino = RAIZ / "decants" / contenido["slug"] / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(html, encoding="utf-8")
        generados.append(destino.relative_to(RAIZ))

    print(f"Generadas {len(generados)} página(s):")
    for g in generados:
        print(f"  - {g}")


if __name__ == "__main__":
    main()
