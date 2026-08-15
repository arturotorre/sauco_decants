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
    "Maison Margiela|Replica By the Fireplace EDT": {
        "slug": "maison-margiela-replica-by-the-fireplace",
        "meta_descripcion": (
            "Decant de Replica By the Fireplace de Maison Margiela (3ml, 5ml, "
            "10ml), 100% original. Ahumado, gourmand y unisex — para noches "
            "frías. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Pimienta rosa", "Clavo", "Bergamota"],
        "notas_corazon": ["Castaña", "Madera de guayaco"],
        "notas_fondo": ["Vainilla", "Bálsamo de Perú"],
        "parrafos": [
            "Replica By the Fireplace, de la línea Replica de Maison Margiela, busca "
            "recrear la sensación exacta de estar sentado frente a una chimenea en "
            "una noche de invierno. Abre con pimienta rosa, clavo y bergamota, se "
            "calienta en un corazón de castaña asada y madera de guayaco, y cierra en "
            "una base envolvente de vainilla y bálsamo de Perú.",

            "Es una fragancia unisex ahumada, gourmand y amaderada, hecha para los "
            "meses fríos — perfecta para el otoño e invierno, noches relajadas o "
            "reuniones frente al fuego. Tiene muy buena fijación, entre 8 y 10 horas.",
        ],
        "ideal_para": "Otoño e invierno — noches frías, reuniones relajadas.",
        "duracion": "8 a 10 horas en piel, con proyección moderada-fuerte.",
    },
    "Louis Vuitton|Imagination EDP": {
        "slug": "louis-vuitton-imagination",
        "meta_descripcion": (
            "Decant de Imagination de Louis Vuitton (3ml, 5ml, 10ml), 100% "
            "original. Cítrico, aromático y elegante — ideal para climas cálidos. "
            "Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Cidra", "Bergamota de Calabria", "Naranja siciliana"],
        "notas_corazon": ["Neroli", "Jengibre", "Canela de Ceylán"],
        "notas_fondo": ["Té negro chino", "Ambroxan", "Madera de guayaco"],
        "parrafos": [
            "Imagination, creada por Jacques Cavallier Belletrud en 2021, es una oda "
            "al viaje y la mente sin límites. Abre con un cítrico luminoso de cidra, "
            "bergamota de Calabria y naranja siciliana, revela un corazón especiado "
            "de neroli, jengibre y canela de Ceylán, y cierra en una base de té negro "
            "chino, ambroxan y madera de guayaco.",

            "Es una fragancia cítrica-aromática fresca y elegante, con muy buen "
            "rendimiento en clima cálido — ideal para primavera y verano, uso diario "
            "o cualquier ocasión donde quieras un cítrico con carácter.",
        ],
        "ideal_para": "Primavera y verano, uso diario — climas cálidos.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Louis Vuitton|L'Immensité EDP": {
        "slug": "louis-vuitton-limmensite",
        "meta_descripcion": (
            "Decant de L'Immensité de Louis Vuitton (3ml, 5ml, 10ml), 100% "
            "original. Fresco, especiado y ligero — ideal para el día. Envíos a "
            "todo México desde Monterrey."
        ),
        "notas_salida": ["Pomelo", "Bergamota", "Jengibre"],
        "notas_corazon": ["Romero", "Salvia", "Geranio"],
        "notas_fondo": ["Ambroxan", "Ámbar", "Labdanum"],
        "parrafos": [
            "L'Immensité, también de Jacques Cavallier Belletrud (2018), evoca la "
            "sensación de libertad y horizontes abiertos. Abre con pomelo, bergamota "
            "y jengibre chispeante, se suaviza en un corazón herbal de romero, salvia "
            "y geranio, y cierra en una base ambarada de ambroxan y labdanum.",

            "Es una fragancia fresca-especiada de buen rendimiento diurno, "
            "especialmente pensada para climas cálidos y uso ligero — ideal para "
            "primavera y verano, día a día.",
        ],
        "ideal_para": "Primavera y verano, día a día — uso ligero.",
        "duracion": "5 a 7 horas en piel, proyección moderada.",
    },
    "YSL|Y EDP": {
        "slug": "ysl-y",
        "meta_descripcion": (
            "Decant de Y Eau de Parfum de YSL (3ml, 5ml, 10ml), 100% original. "
            "Fresco, especiado y versátil — para cualquier ocasión. Envíos a todo "
            "México desde Monterrey."
        ),
        "notas_salida": ["Manzana", "Jengibre", "Bergamota"],
        "notas_corazon": ["Salvia", "Bayas de enebro", "Geranio"],
        "notas_fondo": ["Madera ambarada", "Haba tonka", "Cedro", "Vetiver"],
        "parrafos": [
            "Y Eau de Parfum, creada por Dominique Ropion en 2018, es la "
            "interpretación de YSL de la masculinidad moderna. Abre con un golpe "
            "fresco de bergamota, manzana y jengibre, se desarrolla en un corazón "
            "limpio de salvia, bayas de enebro y geranio, y cierra en una base "
            "ligeramente dulce de madera ambarada, haba tonka, cedro y vetiver.",

            "Es una fragancia aromática fougère versátil y de excelente rendimiento "
            "— funciona para la escuela, el trabajo, un día casual o una salida "
            "nocturna, prácticamente cualquier ocasión, todo el año.",
        ],
        "ideal_para": "Cualquier ocasión — trabajo, día casual, salidas nocturnas, todo el año.",
        "duracion": "8 a 10 horas en piel, con buena proyección.",
    },
    "Lancôme|La Vie Est Belle EDP": {
        "slug": "lancome-la-vie-est-belle",
        "meta_descripcion": (
            "Decant de La Vie Est Belle de Lancôme (3ml, 5ml, 10ml), 100% "
            "original. Floral afrutado gourmand, cálido y envolvente. Envíos a "
            "todo México desde Monterrey."
        ),
        "notas_salida": ["Grosella negra", "Pera"],
        "notas_corazon": ["Iris", "Jazmín", "Flor de azahar"],
        "notas_fondo": ["Praline", "Vainilla", "Patchouli", "Haba tonka"],
        "parrafos": [
            "La Vie Est Belle, lanzada por Lancôme en 2012, es una de las fragancias "
            "femeninas más exitosas de la última década. Abre con grosella negra y "
            "pera jugosas, se despliega en un corazón floral de iris, jazmín y flor "
            "de azahar, y cierra en una base gourmand de praline, vainilla, "
            "patchouli y haba tonka.",

            "Es una fragancia floral afrutada gourmand cálida y envolvente, ideal "
            "para ocasiones especiales — citas, fiestas, bodas. Su carácter dulce y "
            "acogedor la hace brillar especialmente en otoño e invierno, aunque se "
            "puede usar todo el año.",
        ],
        "ideal_para": "Ocasiones especiales — citas, fiestas — sobre todo otoño e invierno.",
        "duracion": "8+ horas en piel, buena proyección.",
    },
    "Paco Rabanne|1 Million EDT": {
        "slug": "paco-rabanne-1-million",
        "meta_descripcion": (
            "Decant de 1 Million de Paco Rabanne (3ml, 5ml, 10ml), 100% original. "
            "Especiado, amaderado y statement — una de las fragancias masculinas "
            "más icónicas. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Mandarina sangre", "Pomelo", "Menta"],
        "notas_corazon": ["Canela", "Especias", "Rosa"],
        "notas_fondo": ["Ámbar", "Cuero", "Patchouli"],
        "parrafos": [
            "1 Million, lanzada por Paco Rabanne en 2008, es una de las fragancias "
            "masculinas más icónicas y reconocibles del mercado. Abre con mandarina "
            "sangre, pomelo y menta frescos, se calienta en un corazón especiado de "
            "canela y rosa, y cierra en una base de ámbar, cuero y patchouli.",

            "Es una fragancia especiada-amaderada audaz y statement, con muy buena "
            "fijación (6 a 8 horas). Funciona todo el año, aunque su carácter cálido "
            "y especiado brilla especialmente en otoño e invierno, ideal para "
            "salidas nocturnas y ocasiones donde quieres notarse.",
        ],
        "ideal_para": "Salidas nocturnas y ocasiones para destacar — otoño e invierno.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Paco Rabanne|Olympéa EDP": {
        "slug": "paco-rabanne-olympea",
        "meta_descripcion": (
            "Decant de Olympéa de Paco Rabanne (3ml, 5ml, 10ml), 100% original. "
            "Oriental floral salado y sensual — para la noche. Envíos a todo "
            "México desde Monterrey."
        ),
        "notas_salida": ["Flor de té verde", "Pimienta blanca"],
        "notas_corazon": ["Sal marina", "Vainilla"],
        "notas_fondo": ["Cachemir"],
        "parrafos": [
            "Olympéa, lanzada por Paco Rabanne en 2015, es la versión femenina y "
            "equivalente de Invictus — inspirada en una diosa griega moderna: "
            "fuerza, dinamismo y conquista. Abre con flor de té verde y pimienta "
            "blanca chispeante, se funde en un corazón salado-dulce de sal marina y "
            "vainilla, y cierra en una base cálida de cachemir.",

            "Es una fragancia oriental floral salada y sensual, pensada para la "
            "noche y ocasiones especiales — perfecta para una cita o un evento donde "
            "buscas dejar una impresión memorable. Funciona todo el año.",
        ],
        "ideal_para": "Noche y ocasiones especiales — citas, eventos.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Dolce & Gabbana|Light Blue Pour Homme EDT": {
        "slug": "dolce-gabbana-light-blue-pour-homme",
        "meta_descripcion": (
            "Decant de Light Blue Pour Homme de Dolce & Gabbana (3ml, 5ml, 10ml), "
            "100% original. Amaderado aromático, limpio y mediterráneo. Envíos a "
            "todo México desde Monterrey."
        ),
        "notas_salida": ["Limón"],
        "notas_corazon": ["Romero"],
        "notas_fondo": ["Pachulí"],
        "parrafos": [
            "Light Blue Pour Homme es la versión 2025 del clásico masculino de "
            "Dolce & Gabbana, reformulada por Alberto Morillas combinando lo mejor "
            "de la línea Light Blue original, la Intense y la Summer Vibes. Abre con "
            "limón siciliano vibrante, se funde en un corazón herbal de romero, y "
            "cierra en una base cálida y terrosa de pachulí.",

            "Es una fragancia amaderada aromática limpia y mediterránea, ideal para "
            "el día, el verano y climas cálidos — evoca costas soleadas y aguas "
            "color turquesa. Perfecta para uso diario.",
        ],
        "ideal_para": "Día a día, verano y climas cálidos.",
        "duracion": "5 a 7 horas en piel.",
    },
    "Jean Paul Gaultier|Le Beau Le Parfum EDP": {
        "slug": "jean-paul-gaultier-le-beau-le-parfum",
        "meta_descripcion": (
            "Decant de Le Beau Le Parfum de Jean Paul Gaultier (3ml, 5ml, 10ml), "
            "100% original. Cálido, ambarado y sofisticado — un verano con giro "
            "elegante. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Piña", "Iris", "Jengibre"],
        "notas_corazon": ["Coco"],
        "notas_fondo": ["Haba tonka", "Sándalo", "Ámbar"],
        "parrafos": [
            "Le Beau Le Parfum, de Jean Paul Gaultier, es una versión más intensa y "
            "sofisticada del clásico veraniego de la casa. Abre con piña jugosa, "
            "iris y un toque de jengibre, se suaviza en un corazón cremoso de coco, "
            "y cierra en una base cálida de haba tonka, sándalo y ámbar.",

            "Es un \"verano en una botella\" con un giro más elegante y cálido — "
            "funciona muy bien en otoño e invierno gracias a su fondo ambarado, "
            "ideal para cenas románticas, eventos y salidas nocturnas donde buscas "
            "dejar una impresión duradera.",
        ],
        "ideal_para": "Cenas románticas, eventos y salidas nocturnas — otoño e invierno.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Carolina Herrera|Good Girl Blush EDP": {
        "slug": "carolina-herrera-good-girl-blush",
        "meta_descripcion": (
            "Decant de Good Girl Blush de Carolina Herrera (3ml, 5ml, 10ml), 100% "
            "original. Floral fresco y romántico — ideal para primavera y verano. "
            "Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Lychee", "Pimienta rosa"],
        "notas_corazon": ["Peonía", "Rosa"],
        "notas_fondo": ["Sándalo", "Almizcle blanco"],
        "parrafos": [
            "Good Girl Blush es la versión más suave y romántica de la icónica Good "
            "Girl de Carolina Herrera. Abre con un chispazo de lychee y pimienta "
            "rosa, se despliega en un corazón floral de peonía y rosa, y cierra en "
            "una base cálida de sándalo y almizcle blanco.",

            "Es una fragancia floral fresca y femenina, ideal para primavera y "
            "verano, aunque su fondo cálido le permite funcionar también en meses "
            "más fríos. Perfecta para citas de día, bodas de temporada cálida y "
            "brunches de fin de semana.",
        ],
        "ideal_para": "Primavera y verano — citas de día, bodas, brunch.",
        "duracion": "6 a 8 horas en piel, proyección moderada.",
    },
}

# --- Contenido editorial para Perfumes completos (botella completa) -----
# clave: "casa|nombre|concentracion" tal como aparece en js/data.js
# (PERFUMES_COMPLETOS) — a diferencia de los decants, el nombre NO incluye
# la concentración, así que hace falta para desambiguar (ej. Scandal EDP
# vs Scandal EDT). Solo se generan páginas para productos con precio fijo.
CONTENIDO_COMPLETOS = {
    "Carolina Herrera|Good Girl|EDP": {
        "slug": "carolina-herrera-good-girl",
        "meta_descripcion": (
            "Good Girl de Carolina Herrera, 100% original, botella completa. "
            "Floriental gourmand icónico — tuberosa, jazmín y haba tonka "
            "tostada. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Almendra", "Café", "Bergamota", "Limón"],
        "notas_corazon": ["Tuberosa", "Jazmín sambac", "Flor de azahar", "Rosa búlgara"],
        "notas_fondo": ["Haba tonka", "Cacao", "Vainilla", "Sándalo"],
        "parrafos": [
            "Good Girl, lanzada por Carolina Herrera en 2016, es una de las "
            "fragancias femeninas más reconocibles del mercado — su icónico "
            "frasco en forma de zapato de tacón es tan famoso como el perfume "
            "mismo. Abre con almendra, café y bergamota, revela un corazón "
            "floral intenso de tuberosa y jazmín sambac, y cierra en una base "
            "gourmand de haba tonka tostada, cacao y vainilla.",

            "Es una fragancia floriental gourmand que representa el contraste "
            "entre luz y oscuridad, dulzura y sensualidad — funciona mejor de "
            "noche, especialmente en otoño e invierno, aunque su carácter "
            "statement la hace perfecta para cualquier ocasión donde quieras "
            "dejar una impresión memorable.",
        ],
        "ideal_para": "Noche, otoño e invierno — ocasiones donde quieres notarse.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Paco Rabanne|Invictus|EDT": {
        "slug": "paco-rabanne-invictus",
        "meta_descripcion": (
            "Invictus de Paco Rabanne EDT, 100% original, botella completa. "
            "Amaderado aromático, fresco y versátil. Envíos a todo México "
            "desde Monterrey."
        ),
        "notas_salida": ["Pomelo", "Mandarina", "Acorde marino"],
        "notas_corazon": ["Laurel", "Jazmín (hedione)"],
        "notas_fondo": ["Madera de guayaco", "Patchouli", "Musgo de roble"],
        "parrafos": [
            "Invictus, lanzada por Paco Rabanne en 2013, es una de las fragancias "
            "masculinas más populares de la casa — energía, vitalidad y espíritu "
            "de victoria en un frasco. Abre con pomelo fresco, mandarina y un "
            "acorde marino, se desarrolla en un corazón aromático de laurel y "
            "jazmín hedione, y cierra en una base amaderada de guayaco, patchouli "
            "y musgo de roble.",

            "Es una fragancia amaderada aromática versátil, ideal para primavera "
            "y verano, aunque funciona bien todo el año tanto de día como de "
            "noche — perfecta para el trabajo, salidas casuales o eventos "
            "sociales.",
        ],
        "ideal_para": "Primavera y verano, día y noche — trabajo, salidas casuales, eventos.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Dior|Sauvage|EDP": {
        "slug": "dior-sauvage-edp",
        "meta_descripcion": (
            "Sauvage Eau de Parfum de Dior, 100% original, botella completa. "
            "Más intenso y cálido que la versión EDT. Envíos a todo México "
            "desde Monterrey."
        ),
        "notas_salida": ["Bergamota", "Pimienta de Sichuan"],
        "notas_corazon": ["Lavanda", "Pimienta rosa", "Geranio"],
        "notas_fondo": ["Ambroxan", "Cedro", "Labdanum"],
        "parrafos": [
            "Sauvage Eau de Parfum es la versión más intensa y duradera del "
            "clásico de Dior — mismo ADN que la versión EDT, pero más cálida y "
            "especiada. Abre con bergamota y pimienta de Sichuan, revela un "
            "corazón de lavanda, pimienta rosa y geranio, y cierra en una base "
            "envolvente de ambroxan, cedro y labdanum.",

            "Comparada con la EDT (más fresca y cítrica), la EDP es más dulce, "
            "rica y magnética — ideal para clima frío, ocasiones especiales y "
            "uso nocturno, aunque funciona bien todo el año. Tiene una fijación "
            "excelente, de 8 a 10 horas.",
        ],
        "ideal_para": "Ocasiones especiales, clima frío, uso nocturno — todo el año.",
        "duracion": "8 a 10 horas en piel, con muy buena proyección.",
    },
    "Versace|Eros|EDP": {
        "slug": "versace-eros-edp",
        "meta_descripcion": (
            "Eros Eau de Parfum de Versace, 100% original, botella completa. "
            "Amaderado aromático, audaz y magnético. Envíos a todo México "
            "desde Monterrey."
        ),
        "notas_salida": ["Menta", "Manzana verde", "Limón"],
        "notas_corazon": ["Haba tonka", "Ambroxan", "Geranio", "Rosa"],
        "notas_fondo": ["Vainilla", "Vetiver", "Musgo de roble", "Cedro de Atlas"],
        "parrafos": [
            "Eros Eau de Parfum es la versión más intensa y sensual del icónico "
            "Eros de Versace — inspirada en el dios griego del amor y el deseo. "
            "Abre con menta, manzana verde y limón frescos, se despliega en un "
            "corazón dulce de haba tonka, ambroxan, geranio y rosa, y cierra en "
            "una base cálida de vainilla, vetiver y musgo de roble.",

            "Es una fragancia amaderada aromática audaz y magnética, con muy "
            "buena proyección y fijación. Brilla especialmente en primavera y "
            "verano por su apertura fresca, aunque su base amaderada le permite "
            "funcionar también en otoño — ideal para citas, salidas nocturnas y "
            "eventos especiales.",
        ],
        "ideal_para": "Citas, salidas nocturnas y eventos — primavera, verano y otoño.",
        "duracion": "8+ horas en piel, con excelente proyección.",
    },
    "Carolina Herrera|Bad Boy|EDT": {
        "slug": "carolina-herrera-bad-boy",
        "meta_descripcion": (
            "Bad Boy de Carolina Herrera EDT, 100% original, botella completa. "
            "Oriental especiado, ahumado y seductor. Envíos a todo México "
            "desde Monterrey."
        ),
        "notas_salida": ["Bergamota", "Pimienta negra", "Pimienta blanca"],
        "notas_corazon": ["Cedro", "Salvia"],
        "notas_fondo": ["Haba tonka", "Madera ambarada", "Cacao"],
        "parrafos": [
            "Bad Boy, lanzada por Carolina Herrera en 2019, es una fragancia "
            "oriental especiada con una personalidad seductora y ligeramente "
            "rebelde. Abre con bergamota y un dúo de pimienta negra y blanca, se "
            "desarrolla en un corazón de cedro y salvia, y cierra en una base "
            "cálida de haba tonka, madera ambarada y cacao.",

            "Es una fragancia especiada, ahumada y sensual, ideal para uso "
            "nocturno — funciona muy bien en otoño e invierno, aunque también se "
            "puede usar de día. Perfecta para salidas, citas y ocasiones donde "
            "buscas proyectar confianza.",
        ],
        "ideal_para": "Noche, otoño e invierno — salidas, citas, ocasiones para destacar.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Paco Rabanne|Lady Million Estuche 2 Piezas|EDP": {
        "slug": "paco-rabanne-lady-million-estuche",
        "meta_descripcion": (
            "Set de regalo Lady Million de Paco Rabanne (EDP 80ml + loción "
            "corporal 100ml), 100% original. Floral afrutado, opulento y "
            "festivo. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Frambuesa", "Limón de Amalfi", "Neroli"],
        "notas_corazon": ["Jazmín", "Flor de azahar", "Gardenia"],
        "notas_fondo": ["Miel", "Patchouli", "Ámbar"],
        "parrafos": [
            "Lady Million, lanzada por Paco Rabanne en 2010, es una fragancia "
            "floral afrutada opulenta y sensual, con un frasco icónico en forma "
            "de anillo dorado. Abre con frambuesa, limón de Amalfi y neroli "
            "chispeantes, se despliega en un corazón floral lechoso de jazmín, "
            "flor de azahar y gardenia, y cierra en una base cálida de miel, "
            "patchouli y ámbar.",

            "Es una fragancia festiva y sensual, ideal para la noche — perfecta "
            "para fiestas, eventos formales, citas y ocasiones especiales. Este "
            "set incluye el Eau de Parfum de 80ml más loción corporal de 100ml, "
            "ideal para regalo.",
        ],
        "ideal_para": "Noche — fiestas, eventos formales, citas, ocasiones especiales.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Dior|J'adore Parfum d'Eau|EDP": {
        "slug": "dior-jadore-parfum-deau",
        "meta_descripcion": (
            "J'adore Parfum d'Eau de Dior, 100% original, botella completa. "
            "Bouquet floral fresco sin alcohol, jazmín sambac, neroli y "
            "magnolia. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Neroli", "Notas verdes"],
        "notas_corazon": ["Jazmín sambac", "Magnolia", "Madreselva", "Rosa"],
        "notas_fondo": ["Almizcle blanco"],
        "parrafos": [
            "J'adore Parfum d'Eau reinventa el icónico J'adore de Dior en una "
            "formulación sin alcohol, pensada como una oda fresca y espontánea "
            "a las flores blancas. Rompe con la estructura clásica de salida, "
            "corazón y fondo: jazmín sambac, neroli y magnolia se entrelazan "
            "desde el primer momento en una sincronía floral luminosa.",

            "Es una fragancia floral fresca, abundante y sensual, ideal para "
            "primavera y verano — su formulación sin alcohol la hace además "
            "más suave sobre la piel, perfecta para el día a día y cualquier "
            "ocasión donde busques un aroma limpio y radiante.",
        ],
        "ideal_para": "Primavera y verano, uso diario — cualquier ocasión.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Tom Ford|Black Orchid|EDP": {
        "slug": "tom-ford-black-orchid",
        "meta_descripcion": (
            "Black Orchid de Tom Ford, 100% original, botella completa. "
            "Amaderado oriental opulento — orquídea negra, trufa y chocolate. "
            "Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Trufa negra", "Gardenia", "Grosella negra", "Bergamota"],
        "notas_corazon": ["Orquídea negra", "Especias", "Ylang-ylang", "Loto"],
        "notas_fondo": ["Chocolate", "Patchouli", "Vainilla", "Incienso", "Sándalo"],
        "parrafos": [
            "Black Orchid, lanzada por Tom Ford en 2006, es una fragancia "
            "unisex densa y magnética que combina dulzura, calidez y un fondo "
            "casi gótico. Abre con trufa negra, gardenia y grosella, se funde "
            "en un corazón de orquídea negra —un acorde creado especialmente "
            "para evocar una flor que no existe en la naturaleza— con especias "
            "y flores blancas, y cierra en una base envolvente de chocolate, "
            "patchouli, incienso y sándalo.",

            "Es una fragancia amaderada oriental opulenta, de gran fijación y "
            "proyección, ideal para la noche y climas fríos — perfecta para "
            "eventos especiales y ocasiones donde buscas dejar una huella "
            "inolvidable.",
        ],
        "ideal_para": "Noche, otoño e invierno — eventos especiales.",
        "duracion": "8+ horas en piel, con excelente proyección.",
    },
    "Paco Rabanne|One Million|EDT": {
        "slug": "paco-rabanne-one-million",
        "meta_descripcion": (
            "One Million de Paco Rabanne EDT, 100% original, botella completa. "
            "Amaderado especiado icónico — canela, cuero y ámbar. Envíos a "
            "todo México desde Monterrey."
        ),
        "notas_salida": ["Mandarina sanguina", "Toronja", "Menta"],
        "notas_corazon": ["Canela", "Especias", "Rosa"],
        "notas_fondo": ["Ámbar", "Cuero", "Notas amaderadas", "Patchouli"],
        "parrafos": [
            "One Million, lanzada por Paco Rabanne en 2008, es una de las "
            "fragancias masculinas más icónicas de la última década — su "
            "frasco en forma de lingote de oro es tan reconocible como el "
            "aroma mismo. Abre con mandarina sanguina, toronja y menta, "
            "revela un corazón especiado de canela y rosa, y cierra en una "
            "base amaderada de cuero, ámbar y patchouli indio.",

            "Es una fragancia amaderada especiada versátil, perfecta para "
            "salidas casuales y formales, especialmente en otoño e invierno "
            "— aunque su carácter magnético la hace funcionar todo el año, "
            "de día o de noche.",
        ],
        "ideal_para": "Otoño e invierno, día y noche — salidas casuales y formales.",
        "duracion": "4 a 6 horas en piel.",
    },
    "YSL|Libre|EDP": {
        "slug": "ysl-libre",
        "meta_descripcion": (
            "Libre de Yves Saint Laurent, 100% original, botella completa. "
            "Oriental fougère audaz — lavanda, azahar y vainilla de "
            "Madagascar. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Lavanda", "Mandarina", "Grosella negra", "Petitgrain"],
        "notas_corazon": ["Flor de azahar", "Jazmín", "Lavanda"],
        "notas_fondo": ["Vainilla de Madagascar", "Almizcle", "Cedro", "Ámbar gris"],
        "parrafos": [
            "Libre, lanzada por Yves Saint Laurent en 2019, reinterpreta la "
            "lavanda —tradicionalmente masculina— dentro de un bouquet "
            "floral femenino, creando un contraste audaz entre lo aromático "
            "y lo sensual. Abre con lavanda, mandarina y grosella negra, se "
            "despliega en un corazón floral de azahar y jazmín, y cierra en "
            "una base cálida de vainilla de Madagascar, almizcle y cedro.",

            "Es una fragancia oriental fougère versátil que celebra la "
            "libertad y la autoexpresión — funciona igual de bien de día que "
            "de noche, ideal para primavera y verano, aunque su fondo cálido "
            "la hace válida todo el año.",
        ],
        "ideal_para": "Todo el año, día y noche — cualquier ocasión.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Dolce & Gabbana|King|EDP": {
        "slug": "dolce-gabbana-king",
        "meta_descripcion": (
            "K by Dolce&Gabbana Eau de Parfum, 100% original, botella "
            "completa. Amaderado especiado audaz — higo, lavanda y "
            "vetiver. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Naranja sanguina", "Bayas de enebro", "Pimienta gorda", "Limón"],
        "notas_corazon": ["Néctar de higo", "Lavanda", "Geranio", "Salvia"],
        "notas_fondo": ["Cedro", "Patchouli", "Vetiver", "Nagarmotha"],
        "parrafos": [
            "K by Dolce&Gabbana Eau de Parfum ofrece una mirada íntima al "
            "carácter de un hombre seguro de sí mismo, con una fragancia "
            "amaderada y especiada. Abre con naranja sanguina, enebro y "
            "pimienta gorda, revela un corazón inesperado de néctar de higo "
            "y lavanda, y cierra en una base terrosa de cedro, patchouli y "
            "vetiver.",

            "Es una fragancia amaderada especiada audaz, ideal para la noche "
            "— perfecta para cenas, reuniones exclusivas y ocasiones donde "
            "buscas hacerte notar sin decir una palabra. Funciona bien todo "
            "el año, especialmente en clima templado y frío.",
        ],
        "ideal_para": "Noche, todo el año — cenas, reuniones, ocasiones especiales.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Jean Paul Gaultier|Le Male|EDT": {
        "slug": "jean-paul-gaultier-le-male",
        "meta_descripcion": (
            "Le Male de Jean Paul Gaultier EDT, 100% original, botella "
            "completa. Oriental fougère icónico — lavanda, vainilla y "
            "cardamomo. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Artemisia", "Menta", "Cardamomo", "Bergamota"],
        "notas_corazon": ["Lavanda", "Flor de azahar", "Canela", "Comino"],
        "notas_fondo": ["Sándalo", "Vainilla", "Cedro", "Haba tonka", "Ámbar"],
        "parrafos": [
            "Le Male, lanzada por Jean Paul Gaultier en 1995 y creada por "
            "Francis Kurkdjian, es uno de los perfumes masculinos más "
            "influyentes de las últimas tres décadas, reconocible por su "
            "frasco en forma de torso marinero. Abre con artemisia, menta y "
            "cardamomo, se desarrolla en un corazón especiado de lavanda y "
            "canela, y cierra en una base cálida de vainilla, sándalo y haba "
            "tonka.",

            "Es una fragancia oriental fougère atemporal que combina frescura "
            "y calidez sensual — versátil para cualquier época del año, de "
            "día o de noche, perfecta tanto para el uso diario como para "
            "ocasiones especiales.",
        ],
        "ideal_para": "Todo el año, día y noche — uso diario y ocasiones especiales.",
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


NAV_HTML = """<nav class="nav-lateral" id="nav-lateral">
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
</nav>"""

CARRITO_Y_FOOTER_HTML = """<button id="carrito-boton" aria-label="Ver carrito">
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

{NAV_HTML}

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

{CARRITO_Y_FOOTER_HTML}"""


def render_pagina_completo(perfume, contenido):
    casa = perfume["casa"]
    nombre_mostrar = contenido.get("nombre_mostrar") or perfume["nombre"]
    genero = perfume["genero"]
    concentracion = perfume["concentracion"]
    tamano = perfume.get("tamano")
    categoria = perfume["categoria"]
    categoria_label = {"nicho": "Nicho", "disenador": "Diseñador", "arabe": "Árabe"}.get(categoria, "Diseñador")
    dot = "dot-nicho" if categoria == "nicho" else "dot-disenador"
    es_set = bool(perfume.get("esSet"))
    imagen_rel = perfume["imagen"]
    conc_y_tamano = f"{concentracion} {tamano}" if tamano else concentracion
    titulo = f"{casa} {nombre_mostrar} {conc_y_tamano} — Perfume {genero} | Saúco Decants"
    meta_desc = contenido["meta_descripcion"]
    url = f"https://saucodecants.com/completos/{contenido['slug']}/"
    alt_img = f"{casa} {nombre_mostrar} {conc_y_tamano} - perfume {'set de regalo' if es_set else 'de botella completa'}"

    parrafos_html = "".join(f"<p>{p}</p>" for p in contenido["parrafos"])

    precio_num = perfume["precio"].replace("$", "").replace(",", "")
    oferta = f'''  "offers": {{
    "@type": "Offer",
    "price": "{precio_num}",
    "priceCurrency": "MXN",
    "availability": "https://schema.org/InStock",
    "url": "{url}"
  }}'''

    genero_linea = f"{conc_y_tamano} · {genero}" + (" · Set de regalo" if es_set else "")
    contenido_set_html = ""
    if es_set and perfume.get("contenido"):
        tags = "".join(f'<span class="nota-tag">{c}</span>' for c in perfume["contenido"])
        contenido_set_html = f'''
      <div class="producto-set-incluye">
        <span class="notas-label">Incluye</span>
        <div class="notas-tags">{tags}</div>
      </div>'''

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
  "name": "{casa} {nombre_mostrar} {conc_y_tamano}",
  "brand": {{ "@type": "Brand", "name": "{casa}" }},
  "description": "{meta_desc}",
  "image": "https://saucodecants.com{perfume['imagen']}",
  "url": "{url}",
{oferta}
}}
</script>
</head>
<body>

{NAV_HTML}

<div class="main-content producto-detalle">
  <nav class="breadcrumb" aria-label="Ruta de navegación">
    <a href="/">Inicio</a> › <a href="/#completos/todos">Perfumes completos</a> › <span>{nombre_mostrar}</span>
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
      <div class="card-genero">{genero_linea}</div>{contenido_set_html}
      <div class="card-divider"></div>
      <div class="card-precio-unico producto-precio-unico">{perfume['precio']}</div>
      <button class="btn-agregar btn-agregar-completo producto-btn-agregar" data-casa="{casa}" data-nombre="{perfume['nombre']}" data-concentracion="{concentracion}" aria-label="Agregar {nombre_mostrar} al carrito">
        <span class="btn-agregar-texto">Agregar al carrito</span>
        <span class="btn-agregar-icono" aria-hidden="true">🛒</span>
      </button>
      <div class="card-footer-text">{categoria_label} · Original</div>
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
      <a href="/#completos/todos">← Ver todos los perfumes completos</a>
    </div>
  </div>
</div>

{CARRITO_Y_FOOTER_HTML}"""


def generar_sitemap(slugs, slugs_completos=None):
    """Reescribe sitemap.xml con la home + una entrada por cada página de
    producto generada, para que quede sincronizado automáticamente en cada
    corrida en vez de mantenerse a mano y quedar desactualizado."""
    urls = (
        ["https://saucodecants.com/"]
        + [f"https://saucodecants.com/decants/{slug}/" for slug in sorted(slugs)]
        + [f"https://saucodecants.com/completos/{slug}/" for slug in sorted(slugs_completos or [])]
    )
    entradas = "\n".join(
        f'  <url>\n    <loc>{u}</loc>\n    <changefreq>weekly</changefreq>\n    <priority>{"1.0" if u.endswith(".com/") else "0.8"}</priority>\n  </url>'
        for u in urls
    )
    contenido = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entradas}\n"
        "</urlset>\n"
    )
    (RAIZ / "sitemap.xml").write_text(contenido, encoding="utf-8")


def main():
    catalogo = leer_catalogo_propio()
    perfumes_por_clave = {f"{p['casa']}|{p['nombre']}": p for p in catalogo["PERFUMES"]}
    completos_por_clave = {
        f"{p['casa']}|{p['nombre']}|{p['concentracion']}": p for p in catalogo["PERFUMES_COMPLETOS"]
    }

    generados = []
    slugs = []
    for clave, contenido in CONTENIDO_DECANTS.items():
        perfume = perfumes_por_clave.get(clave)
        if not perfume:
            print(f"  ⚠ no encontrado en js/data.js (PERFUMES), se omite: {clave}")
            continue
        html = render_pagina(perfume, contenido)
        destino = RAIZ / "decants" / contenido["slug"] / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(html, encoding="utf-8")
        generados.append(destino.relative_to(RAIZ))
        slugs.append(contenido["slug"])

    generados_completos = []
    slugs_completos = []
    for clave, contenido in CONTENIDO_COMPLETOS.items():
        perfume = completos_por_clave.get(clave)
        if not perfume:
            print(f"  ⚠ no encontrado en js/data.js (PERFUMES_COMPLETOS), se omite: {clave}")
            continue
        if not perfume.get("precio"):
            print(f"  ⚠ sin precio fijo, se omite por ahora: {clave}")
            continue
        html = render_pagina_completo(perfume, contenido)
        destino = RAIZ / "completos" / contenido["slug"] / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(html, encoding="utf-8")
        generados_completos.append(destino.relative_to(RAIZ))
        slugs_completos.append(contenido["slug"])

    generar_sitemap(slugs, slugs_completos)

    print(f"Generadas {len(generados)} página(s) de decants:")
    for g in generados:
        print(f"  - {g}")
    print(f"Generadas {len(generados_completos)} página(s) de perfumes completos:")
    for g in generados_completos:
        print(f"  - {g}")
    print(f"sitemap.xml actualizado con {len(slugs) + len(slugs_completos) + 1} URLs.")


if __name__ == "__main__":
    main()
