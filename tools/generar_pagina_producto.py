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
    "Valentino|Uomo Born in Roma Intense EDP": {
        "slug": "valentino-uomo-born-in-roma-intense",
        "meta_descripcion": (
            "Decant de Uomo Born In Roma Intense de Valentino (3ml, 5ml, 10ml), 100% "
            "original. Cálido, especiado y amaderado — pensado para la noche. Envíos "
            "a todo México desde Monterrey."
        ),
        "notas_salida": ["Vainilla", "Jengibre"],
        "notas_corazon": ["Lavanda"],
        "notas_fondo": ["Vetiver ahumado"],
        "parrafos": [
            "Uomo Born In Roma Intense es la versión más intensa y nocturna de la línea "
            "Born In Roma de Valentino, lanzada en 2023. Abre con una infusión de "
            "vainilla y jengibre que sorprende por su dulzor especiado, se asienta en un "
            "corazón de lavanda vibrante, y cierra con vetiver ahumado — una combinación "
            "cálida, especiada y profundamente amaderada.",

            "Es una fragancia intensa, pensada para la noche: perfecta para salidas "
            "nocturnas y ocasiones especiales donde quieres dejar una estela notable. "
            "Tiene gran fijación y proyección, especialmente en las primeras horas.",
        ],
        "ideal_para": "Salidas nocturnas y ocasiones especiales — otoño e invierno.",
        "duracion": "8 a 10 horas en piel, con proyección fuerte.",
    },
    "Chanel|Chance Eau Tendre EDP": {
        "slug": "chanel-chance-eau-tendre",
        "meta_descripcion": (
            "Decant de Chance Eau Tendre de Chanel (3ml, 5ml, 10ml), 100% original. "
            "Floral afrutado, fresco y romántico — ideal para el día a día. Envíos a "
            "todo México desde Monterrey."
        ),
        "notas_salida": ["Membrillo", "Pomelo"],
        "notas_corazon": ["Rosa", "Jazmín"],
        "notas_fondo": ["Almizcle blanco"],
        "parrafos": [
            "Chance Eau Tendre es la versión más suave y luminosa de la familia Chance "
            "de Chanel, lanzada en 2010 (con una versión Eau de Parfum en 2019) por el "
            "perfumista Olivier Polge. Abre con membrillo y pomelo frescos, se suaviza "
            "en un corazón floral de rosa y jazmín, y cierra en un fondo de almizcle "
            "blanco limpio y delicado.",

            "\"Eau Tendre\" — agua tierna — describe bien su carácter: es una fragancia "
            "floral afrutada, fresca y romántica, ideal para el día a día. Funciona muy "
            "bien en primavera y verano, para un brunch, una primera cita o cualquier "
            "ocasión ligera.",
        ],
        "ideal_para": "Uso diario, primavera y verano — brunch, primeras citas, oficina.",
        "duracion": "5 a 7 horas en piel, estela discreta y fresca.",
    },
    "Prada|Paradoxe Intense EDP": {
        "slug": "prada-paradoxe-intense",
        "meta_descripcion": (
            "Decant de Paradoxe Intense de Prada (3ml, 5ml, 10ml), 100% original. "
            "Floral ambarado, cálido y sensual — de día o de noche. Envíos a todo "
            "México desde Monterrey."
        ),
        "notas_salida": ["Bergamota", "Neroli", "Pera"],
        "notas_corazon": ["Neroli", "Jazmín", "Musgo"],
        "notas_fondo": ["Ámbar", "Vainilla", "Almizcle blanco"],
        "parrafos": [
            "Paradoxe Intense es la versión nocturna y más profunda del Paradoxe "
            "original de Prada, lanzada en 2023. Abre con bergamota, neroli y pera, se "
            "despliega en un corazón floral de jazmín y neroli realzado con un toque de "
            "musgo, y cierra en una base cálida de ámbar, vainilla y almizcle blanco.",

            "Es una fragancia floral ambarada más dulce, sensual e intensa que la "
            "versión original, con muy buena fijación. Funciona tanto de día como de "
            "noche, y es una gran opción para reuniones importantes, citas románticas "
            "o eventos nocturnos donde buscas dejar huella.",
        ],
        "ideal_para": "Día o noche — citas, eventos y reuniones importantes.",
        "duracion": "6+ horas en piel, buena proyección.",
    },
    "Valentino|Donna Born in Roma Intense EDP": {
        "slug": "valentino-donna-born-in-roma-intense",
        "meta_descripcion": (
            "Decant de Donna Born In Roma Intense de Valentino (3ml, 5ml, 10ml), 100% "
            "original. Floral ambarado, magnético e intenso. Envíos a todo México "
            "desde Monterrey."
        ),
        "notas_salida": ["Grosella negra", "Bergamota"],
        "notas_corazon": ["Té de jazmín", "Jazmín sambac"],
        "notas_fondo": ["Vainilla bourbon", "Ámbar", "Benjuí"],
        "parrafos": [
            "Donna Born In Roma Intense es la versión más intensa de la línea femenina "
            "Born In Roma de Valentino, lanzada en 2023. Abre con grosella negra y "
            "bergamota frescas junto a vainilla bourbon y ámbar, revela un corazón "
            "floral de jazmín (té de jazmín y jazmín sambac), y cierra en una base "
            "envolvente de benjuí, vainilla bourbon y ámbar gris.",

            "Es una fragancia floral ambarada magnética, pensada para personalidades "
            "intensas y apasionadas. Aunque se puede usar todo el año, su carácter "
            "cálido brilla especialmente en otoño e invierno — ideal para salidas, "
            "citas románticas y eventos formales.",
        ],
        "ideal_para": "Salidas, citas y eventos formales — especialmente otoño e invierno.",
        "duracion": "Larga duración, buena proyección.",
    },
    "Xerjoff|Erba Pura EDP": {
        "slug": "xerjoff-erba-pura",
        "meta_descripcion": (
            "Decant de Erba Pura de Xerjoff (3ml, 5ml, 10ml), 100% original. "
            "Cítrico, afrutado y mediterráneo — unisex, ideal para primavera y "
            "verano. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Naranja siciliana", "Bergamota", "Limón"],
        "notas_corazon": ["Frutos mediterráneos"],
        "notas_fondo": ["Almizcle blanco", "Vainilla", "Ámbar"],
        "parrafos": [
            "Erba Pura es una de las fragancias más reconocibles de Xerjoff, con un "
            "carácter mediterráneo evidente desde el primer momento. Abre con un "
            "estallido cítrico de naranja siciliana, bergamota calabresa y limón, se "
            "suaviza en un corazón afrutado inspirado en la canasta de frutas del "
            "Mediterráneo, y cierra en una base cremosa de almizcle blanco, vainilla "
            "de Madagascar y ámbar.",

            "Es una fragancia versátil y elegante que rinde especialmente bien en "
            "primavera y verano, aunque su fondo cálido de vainilla y ámbar le permite "
            "funcionar también en ocasiones más formales o citas nocturnas. Tiene muy "
            "buena fijación, entre 8 y 12 horas en piel.",
        ],
        "ideal_para": "Primavera y verano — igual de bien para el día a día que para eventos formales o citas.",
        "duracion": "8 a 12 horas en piel.",
    },
    "Francis Kurkdjian|Baccarat Rouge 540 EDP": {
        "slug": "francis-kurkdjian-baccarat-rouge-540",
        "meta_descripcion": (
            "Decant de Baccarat Rouge 540 de Maison Francis Kurkdjian (3ml, 5ml, "
            "10ml), 100% original. Ámbar, dulce y con una estela enorme — el nicho "
            "más icónico de la última década. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Azafrán", "Jazmín"],
        "notas_corazon": ["Madera ambarada", "Ámbar gris", "Hedione"],
        "notas_fondo": ["Resina de abeto", "Cedro", "Ambroxan"],
        "parrafos": [
            "Baccarat Rouge 540 es, sin exagerar, una de las fragancias de nicho más "
            "icónicas de la última década. Creada por Francis Kurkdjian en 2015, abre "
            "con azafrán y jazmín en una combinación dulce, luminosa y ligeramente "
            "metálica, se despliega en un corazón de madera ambarada y ámbar gris, y "
            "cierra en una base resinosa de cedro, ambroxan y un toque de azúcar.",

            "Es una fragancia abstracta y muy reconocible, con una estela enorme y una "
            "fijación excepcional (10+ horas). Brilla especialmente en clima frío, de "
            "noche, y en ocasiones donde quieres destacar — puede resultar intensa "
            "para el día a día o el trabajo.",
        ],
        "ideal_para": "Noche, clima frío y ocasiones especiales — donde quieres destacar.",
        "duracion": "10+ horas en piel, con proyección muy fuerte.",
    },
    "Dior|Sauvage EDT": {
        "slug": "dior-sauvage",
        "meta_descripcion": (
            "Decant de Sauvage EDT de Dior (3ml, 5ml, 10ml), 100% original. Fresco, "
            "especiado y versátil — de las fragancias masculinas más vendidas del "
            "mundo. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Bergamota de Calabria", "Pimienta de Sichuan"],
        "notas_corazon": ["Lavanda", "Pimienta rosa", "Vetiver"],
        "notas_fondo": ["Ambroxan", "Labdanum", "Cedro"],
        "parrafos": [
            "Sauvage es una de las fragancias masculinas más vendidas del mundo, "
            "creada por François Demachy para Dior. La versión Eau de Toilette abre "
            "con bergamota de Calabria y pimienta de Sichuan, revela un corazón "
            "especiado de lavanda, pimienta rosa y vetiver, y cierra en una base "
            "amaderada de ambroxan, labdanum y cedro.",

            "Es una fragancia fresca, especiada y versátil que funciona igual de bien "
            "de día que de noche, en cualquier época del año — de las opciones más "
            "seguras para uso diario, oficina o cualquier ocasión casual.",
        ],
        "ideal_para": "Uso diario, cualquier ocasión — todo el año.",
        "duracion": "6 a 8 horas en piel, buena proyección.",
    },
    "Chanel|Bleu de Chanel EDP": {
        "slug": "chanel-bleu-de-chanel",
        "meta_descripcion": (
            "Decant de Bleu de Chanel EDP (3ml, 5ml, 10ml), 100% original. "
            "Amaderado aromático, versátil y fácil de llevar. Envíos a todo México "
            "desde Monterrey."
        ),
        "notas_salida": ["Pomelo", "Limón", "Menta", "Bergamota"],
        "notas_corazon": ["Jengibre", "Jazmín", "Nuez moscada"],
        "notas_fondo": ["Incienso", "Ámbar", "Sándalo", "Cedro"],
        "parrafos": [
            "Bleu de Chanel Eau de Parfum, creada por Jacques Polge en 2014, abre con "
            "un golpe cítrico brillante de pomelo, limón, menta y bergamota, se "
            "suaviza en un corazón de jengibre y jazmín, y cierra en una base "
            "amaderada de incienso, ámbar, sándalo y cedro con un toque salino casi "
            "marino.",

            "Es una fragancia amaderada aromática muy versátil, fácil de llevar en "
            "cualquier situación — funciona todo el año y es una de esas opciones "
            "seguras tanto para el día a día como para ocasiones más formales.",
        ],
        "ideal_para": "Uso diario y ocasiones formales — todo el año.",
        "duracion": "6 a 8 horas en piel.",
    },
    "YSL|Libre EDP": {
        "slug": "ysl-libre",
        "meta_descripcion": (
            "Decant de Libre Eau de Parfum de YSL (3ml, 5ml, 10ml), 100% original. "
            "Floral con carácter — contraste entre lavanda fresca y vainilla cálida. "
            "Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Lavanda", "Mandarina", "Grosella negra"],
        "notas_corazon": ["Lavanda", "Flor de azahar", "Jazmín"],
        "notas_fondo": ["Vainilla de Madagascar", "Almizcle", "Cedro"],
        "parrafos": [
            "Libre es la fragancia que representa la libertad femenina para Yves "
            "Saint Laurent. Abre con lavanda, mandarina y grosella negra frescas, se "
            "despliega en un corazón floral de flor de azahar marroquí y jazmín sobre "
            "más lavanda, y cierra en una base cálida de vainilla de Madagascar, "
            "almizcle y cedro.",

            "Es un contraste deliberado entre lo fresco-aromático de la lavanda y lo "
            "cálido-sensual de la vainilla — funciona bien tanto de día como de "
            "noche. Es una fragancia versátil, ideal para quien busca algo floral "
            "pero con carácter, no empalagoso.",
        ],
        "ideal_para": "Día y noche — todo el año, para quien busca un floral con carácter.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Armani|Acqua di Gio Profondo EDP": {
        "slug": "armani-acqua-di-gio-profondo",
        "meta_descripcion": (
            "Decant de Acqua di Gio Profondo de Giorgio Armani (3ml, 5ml, 10ml), "
            "100% original. Acuático, intenso y mineral — ideal para climas cálidos. "
            "Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Notas marinas", "Mandarina verde"],
        "notas_corazon": ["Romero", "Lavanda"],
        "notas_fondo": ["Notas minerales", "Ámbar gris", "Almizcle", "Cedro"],
        "parrafos": [
            "Acqua di Giò Profondo es la versión más intensa y marina de la icónica "
            "línea Acqua di Giò de Giorgio Armani. Abre con notas marinas y mandarina "
            "verde vibrantes, revela un corazón herbal de romero y lavanda, y cierra "
            "en una base mineral de ámbar gris, almizcle, cedro y patchouli.",

            "Es una fragancia acuática intensa que evoca el mar profundo, ideal para "
            "climas cálidos y días soleados, aunque funciona todo el año como una "
            "opción masculina madura. Es una gran opción para el día, eventos al aire "
            "libre o para hacer la transición a una cena casual por la noche.",
        ],
        "ideal_para": "Climas cálidos, día a día y eventos al aire libre — todo el año.",
        "duracion": "6 a 8 horas en piel.",
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
