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
    "Le Labo|Another 13 EDP": {
        "slug": "le-labo-another-13",
        "meta_descripcion": (
            "Decant de Another 13 de Le Labo (3ml, 5ml, 10ml), 100% original. "
            "Amaderado ambarado y almizclado, unisex — nacido de la colaboración "
            "con AnOther Magazine. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Pera", "Manzana", "Cítricos"],
        "notas_corazon": ["Ambreta", "Musgo", "Jazmín"],
        "notas_fondo": ["Ámbar gris", "Almizcle", "Madera"],
        "parrafos": [
            "Another 13, lanzada en 2010 por Le Labo en colaboración con AnOther "
            "Magazine, es una fragancia moderna y adictiva construida alrededor de "
            "un acorde de ámbar gris y almizcle. Abre con pera, manzana y cítricos "
            "jugosos, se despliega en un corazón limpio de ambreta, musgo y jazmín, "
            "y cierra en una base envolvente de ámbar gris, almizcle y madera que "
            "recuerda a piel recién lavada.",

            "Es completamente unisex y funciona todo el año — un perfume "
            "'segunda piel' discreto pero magnético, ideal tanto para el día a día "
            "como para capas con otros perfumes gracias a su carácter limpio y "
            "adictivo.",
        ],
        "ideal_para": "Uso diario, todo el año — discreto, limpio y magnético.",
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
    "Guerlain|Mon Guerlain EDP": {
        "slug": "guerlain-mon-guerlain",
        "meta_descripcion": (
            "Decant de Mon Guerlain de Guerlain (3ml, 5ml, 10ml), 100% original. "
            "Amaderado oriental dulce y polvoriento — lavanda, iris y vainilla. "
            "Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Lavanda", "Bergamota"],
        "notas_corazon": ["Iris", "Jazmín sambac", "Rosa"],
        "notas_fondo": ["Vainilla de Tahití", "Sándalo", "Regaliz", "Benjuí", "Pachulí"],
        "parrafos": [
            "Mon Guerlain, lanzada en 2017 por Thierry Wasser y Delphine Jelk, "
            "reinterpreta la lavanda —tradicionalmente masculina en la casa "
            "Guerlain— dentro de un bouquet floral femenino y contemporáneo. Abre "
            "con lavanda y bergamota frescas, se despliega en un corazón "
            "polvoriento de iris, jazmín sambac y rosa, y cierra en una base "
            "gourmand de vainilla de Tahití, sándalo y regaliz.",

            "Es una fragancia amaderada oriental dulce y envolvente, con un "
            "carácter moderno que combina frescura aromática y calidez golosa — "
            "funciona todo el año, ideal para el uso diario y también para la "
            "noche.",
        ],
        "ideal_para": "Uso diario y noche — todo el año.",
        "duracion": "6 a 8 horas en piel, proyección moderada.",
    },
    "Dolce & Gabbana|Light Blue EDT": {
        "slug": "dolce-gabbana-light-blue-decant",
        "meta_descripcion": (
            "Decant de Light Blue de Dolce&Gabbana (3ml, 5ml, 10ml), 100% "
            "original. Fresco frutal-amaderado icónico — limón siciliano, "
            "manzana y jazmín. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Limón siciliano", "Manzana verde", "Campanilla"],
        "notas_corazon": ["Rosa blanca", "Bambú", "Jazmín"],
        "notas_fondo": ["Ámbar", "Almizcle", "Cedro"],
        "parrafos": [
            "Light Blue, lanzada por Dolce&Gabbana en 2001, es una de las "
            "fragancias femeninas más icónicas del mercado — el aroma del "
            "verano en Capri en un frasco. Abre con limón siciliano, manzana "
            "verde y campanilla, se despliega en un corazón floral de rosa "
            "blanca, bambú y jazmín, y cierra en una base de ámbar, almizcle y "
            "cedro.",

            "Es una fragancia fresca y afrutada-amaderada, perfecta para "
            "primavera y verano — ligera, energizante y versátil, ideal para el "
            "uso diario de día.",
        ],
        "ideal_para": "Primavera y verano, uso diario — energizante y fresca.",
        "duracion": "5 a 7 horas en piel.",
    },
    "Calvin Klein|CK One EDT": {
        "slug": "calvin-klein-ck-one",
        "meta_descripcion": (
            "Decant de CK One de Calvin Klein (3ml, 5ml, 10ml), 100% original. "
            "Fresco cítrico floral unisex, el clásico de los 90 que definió la "
            "categoría. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Limón", "Bergamota", "Piña", "Cardamomo", "Papaya"],
        "notas_corazon": ["Muguete", "Jazmín", "Violeta", "Rosa", "Nuez moscada"],
        "notas_fondo": ["Almizcle", "Cedro", "Sándalo", "Musgo de roble", "Ámbar"],
        "parrafos": [
            "CK One, lanzada por Calvin Klein en 1994, fue una de las primeras "
            "fragancias unisex en volverse un fenómeno masivo y sigue siendo un "
            "clásico imprescindible. Abre con limón, bergamota y piña frescos, "
            "se despliega en un corazón floral verde de muguete, jazmín y "
            "violeta, y cierra en una base limpia de almizcle, cedro y musgo "
            "de roble.",

            "Es una fragancia fresca, ligera y versátil, ideal para primavera "
            "y verano — perfecta para el uso diario, la oficina o el gimnasio, "
            "con ese carácter limpio e inconfundible que la volvió icónica.",
        ],
        "ideal_para": "Primavera y verano, uso diario — oficina, gimnasio, día a día.",
        "duracion": "4 a 6 horas en piel.",
    },
    "Lacoste|Red EDT": {
        "slug": "lacoste-red",
        "meta_descripcion": (
            "Decant de Lacoste Red (3ml, 5ml, 10ml), 100% original. Fougère "
            "afrutado energético — manzana, pino y patchouli. Envíos a todo "
            "México desde Monterrey."
        ),
        "notas_salida": ["Manzana", "Cedro"],
        "notas_corazon": ["Pino", "Jazmín"],
        "notas_fondo": ["Patchouli", "Vetiver"],
        "parrafos": [
            "Lacoste Red, lanzada en 2004, es una fragancia fougère afrutada "
            "pensada para el hombre activo. Abre con manzana verde crujiente "
            "que se equilibra con un toque de cedro, se despliega en un "
            "corazón herbal de pino y jazmín, y cierra en una base amaderada "
            "de patchouli y vetiver.",

            "Es una fragancia enérgica y versátil, ideal para primavera y "
            "verano de día — perfecta para el uso diario, deportivo o "
            "casual, con un carácter fresco y directo.",
        ],
        "ideal_para": "Primavera y verano, día — uso diario, deportivo y casual.",
        "duracion": "5 a 7 horas en piel.",
    },
    "Armani Privé|Oud Royal EDP": {
        "slug": "armani-prive-oud-royal",
        "meta_descripcion": (
            "Decant de Oud Royal de Armani Privé (3ml, 5ml, 10ml), 100% "
            "original. Oriental amaderado de lujo — azafrán, rosa y oud de "
            "Laos. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Azafrán", "Incienso"],
        "notas_corazon": ["Rosa", "Especias orientales", "Ámbar"],
        "notas_fondo": ["Sándalo", "Oud", "Mirra"],
        "parrafos": [
            "Oud Royal, parte de la colección Armani Privé Les Mille et Une "
            "Nuits, alberga la preciosa y excepcional madera de oud de Laos "
            "en un elixir oriental cautivador. Abre con azafrán e incienso "
            "envolventes, se despliega en un corazón de rosa y especias "
            "orientales sobre un fondo de ámbar, y cierra en una base "
            "profunda de sándalo y oud.",

            "Es una fragancia oriental amaderada intensa y lujosa, ideal "
            "para otoño e invierno — perfecta para la noche y ocasiones "
            "especiales donde buscas un aroma memorable con carácter de "
            "alta perfumería.",
        ],
        "ideal_para": "Otoño e invierno, noche — ocasiones especiales.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Nasomatto|Black Afgano Parfum": {
        "slug": "nasomatto-black-afgano",
        "nombre_mostrar": "Black Afgano",
        "meta_descripcion": (
            "Decant de Black Afgano de Nasomatto (3ml, 5ml, 10ml), 100% "
            "original. Oriental amaderado resinoso y ahumado — cannabis, "
            "tabaco y oud. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Cannabis", "Notas verdes", "Azafrán", "Tomillo"],
        "notas_corazon": ["Resinas", "Tabaco", "Café", "Canela"],
        "notas_fondo": ["Oud", "Incienso", "Ámbar", "Almizcle", "Vainilla"],
        "parrafos": [
            "Black Afgano, lanzada en 2009 por Alessandro Gualtieri tras "
            "seis años de desarrollo, es una de las fragancias más "
            "hipnóticas y poco convencionales de la perfumería de nicho, "
            "inspirada en el hachís de alta calidad. Abre con cannabis y "
            "notas verdes crudas, se despliega en un corazón ahumado de "
            "resinas, tabaco y café, y cierra en una base densa de oud, "
            "incienso y ámbar.",

            "Es una fragancia oriental amaderada oscura e intensa, con una "
            "estela que dura horas — ideal para otoño e invierno y uso "
            "nocturno, pensada para quien busca un aroma verdaderamente "
            "distinto y de carácter.",
        ],
        "ideal_para": "Otoño e invierno, noche — para un carácter distinto y audaz.",
        "duracion": "10+ horas en piel, con proyección muy fuerte.",
    },
    "Le Labo|Tonka 25 EDP": {
        "slug": "le-labo-tonka-25",
        "meta_descripcion": (
            "Decant de Tonka 25 de Le Labo (3ml, 5ml, 10ml), 100% original. "
            "Amaderado almizclado cálido — flor de azahar, cedro y haba "
            "tonka. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Flor de azahar"],
        "notas_corazon": ["Cedro", "Estoraque"],
        "notas_fondo": ["Haba tonka", "Almizcle", "Vainilla"],
        "parrafos": [
            "Tonka 25, lanzada en 2018 por la perfumista Daphné Bugey, "
            "evoca la calidez de la piel y la madera resinosa en una "
            "composición sutil y adictiva. Abre con flor de azahar, se "
            "despliega en un corazón de cedro y estoraque, y cierra en una "
            "base de haba tonka tratada con contención — revelando su "
            "carácter suave y polvoriento en vez del gourmand dulzón que "
            "muchos esperarían de un nombre 'tonka'.",

            "Es una fragancia amaderada almizclada cálida y cercana a la "
            "piel, ideal para todo el año — perfecta para quien busca un "
            "nicho discreto pero magnético, más sofisticado que dulce.",
        ],
        "ideal_para": "Uso diario, todo el año — discreta y sofisticada.",
        "duracion": "6 a 8 horas en piel, con estela moderada.",
    },
    "Kilian|Black Phantom “Memento Mori” EDP": {
        "slug": "kilian-black-phantom-memento-mori",
        "nombre_mostrar": "Black Phantom “Memento Mori”",
        "meta_descripcion": (
            "Decant de Black Phantom “Memento Mori” de Kilian (3ml, 5ml, "
            "10ml), 100% original. Oriental vainilla intenso — ron, café y "
            "sándalo. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Ron"],
        "notas_corazon": ["Café", "Vetiver"],
        "notas_fondo": ["Ámbar", "Caña de azúcar", "Sándalo"],
        "parrafos": [
            "Black Phantom “Memento Mori”, parte de la colección The "
            "Cellars de Kilian, evoca la aventura pirata y los tesoros "
            "escondidos tras aguas negras y misteriosas. Abre con un "
            "acorde de ron que recuerda la bebida favorita de la era "
            "pirata, se despliega en un corazón intenso de café equilibrado "
            "por vetiver, y cierra en una base golosa de caña de azúcar y "
            "sándalo cremoso.",

            "Es una fragancia oriental vainilla intensa y adictiva, ideal "
            "para otoño e invierno y uso nocturno — perfecta para quien "
            "busca un nicho con carácter dulce, oscuro y memorable.",
        ],
        "ideal_para": "Otoño e invierno, noche — carácter dulce y memorable.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
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
    "Carolina Herrera|Bad Boy Cobalt|EDP": {
        "slug": "carolina-herrera-bad-boy-cobalt",
        "meta_descripcion": (
            "Bad Boy Cobalt de Carolina Herrera, 100% original, botella "
            "completa. Amaderado aromático audaz — pimienta rosa, ciruela "
            "y trufa. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Pimienta rosa", "Lavanda"],
        "notas_corazon": ["Geranio", "Ciruela", "Trufa"],
        "notas_fondo": ["Vetiver", "Cedro", "Haba tonka"],
        "parrafos": [
            "Bad Boy Cobalt reinterpreta el icónico Bad Boy de Carolina "
            "Herrera con un carácter más mineral y audaz, en un frasco azul "
            "cobalto. Abre con pimienta rosa y lavanda, revela un corazón "
            "floral-masculino de geranio y ciruela anclado por un acorde de "
            "trufa ahumada, y cierra en una base de vetiver, cedro y haba "
            "tonka.",

            "Es una fragancia amaderada aromática versátil, con carácter "
            "bold y sofisticado a la vez — funciona igual de bien de día "
            "que de noche, ideal para cualquier época del año.",
        ],
        "ideal_para": "Todo el año, día y noche — versátil para cualquier ocasión.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Carolina Herrera|Bad Boy Elixir|EDP": {
        "slug": "carolina-herrera-bad-boy-elixir",
        "meta_descripcion": (
            "Bad Boy Elixir de Carolina Herrera, 100% original, botella "
            "completa. Oriental amaderado intenso — cuero, iris y "
            "franquincienso. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Salvia", "Lavanda"],
        "notas_corazon": ["Cuero", "Iris"],
        "notas_fondo": ["Cedro", "Franquincienso", "Haba tonka"],
        "parrafos": [
            "Bad Boy Elixir lleva el ADN de Bad Boy hacia una versión más "
            "concentrada e intensa, con un cuero limpio y magnético en el "
            "centro de la composición. Abre con salvia y lavanda, se "
            "despliega en un corazón de cuero e iris, y cierra en una base "
            "cálida de cedro, franquincienso y haba tonka.",

            "Es una fragancia oriental amaderada de gran fijación, ideal "
            "para climas fríos y uso nocturno — perfecta para quien busca "
            "una versión más fuerte y sofisticada del Bad Boy original.",
        ],
        "ideal_para": "Otoño e invierno, noche — versión intensa y sofisticada.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Carolina Herrera|Good Girl Blush|EDP": {
        "slug": "carolina-herrera-good-girl-blush",
        "meta_descripcion": (
            "Good Girl Blush de Carolina Herrera, 100% original, botella "
            "completa. Floral chipre luminoso — peonía, ylang ylang y "
            "vainilla. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Bergamota", "Almendra amarga"],
        "notas_corazon": ["Peonía", "Ylang ylang"],
        "notas_fondo": ["Vainilla", "Cumarina"],
        "parrafos": [
            "Good Girl Blush reinterpreta el universo Good Girl con una "
            "versión más ligera, radiante y polvorienta, en un frasco rosa "
            "pastel. Abre con bergamota y almendra amarga, revela un "
            "corazón floral de peonía y ylang ylang, y cierra en una base "
            "cálida de vainilla y cumarina.",

            "Es una fragancia floral chipre luminosa, ideal para primavera "
            "y verano, aunque su fondo cálido la hace funcionar todo el "
            "año — perfecta para el día a día con un toque femenino y "
            "sofisticado.",
        ],
        "ideal_para": "Primavera y verano, uso diario — con un toque sofisticado.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Carolina Herrera|Very Good Girl|EDP": {
        "slug": "carolina-herrera-very-good-girl",
        "meta_descripcion": (
            "Very Good Girl de Carolina Herrera, 100% original, botella "
            "completa. Floral afrutado sensual — lichi, rosa y vainilla. "
            "Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Lichi", "Grosella roja"],
        "notas_corazon": ["Rosa"],
        "notas_fondo": ["Vainilla", "Vetiver"],
        "parrafos": [
            "Very Good Girl es una versión más frutal y sensual dentro del "
            "universo Good Girl de Carolina Herrera. Abre con lichi y "
            "grosella roja jugosos, se despliega en un corazón de rosa, y "
            "cierra en una base cálida de vainilla y vetiver.",

            "Es una fragancia floral afrutada versátil, dulce sin ser "
            "empalagosa — funciona bien todo el año, tanto de día como de "
            "noche, ideal para quien busca un Good Girl más fresco y "
            "juguetón.",
        ],
        "ideal_para": "Todo el año, día y noche — versátil y juguetona.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Dior|Miss Dior|EDP": {
        "slug": "dior-miss-dior",
        "meta_descripcion": (
            "Miss Dior Eau de Parfum, 100% original, botella completa. "
            "Floral oriental romántico — rosa centifolia, peonía y "
            "vainilla. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Iris", "Peonía", "Lirio de los valles"],
        "notas_corazon": ["Rosa centifolia", "Chabacano", "Durazno"],
        "notas_fondo": ["Vainilla", "Almizcle", "Haba tonka", "Sándalo", "Benjuí"],
        "parrafos": [
            "Miss Dior Eau de Parfum reinterpreta el icónico perfume de "
            "Dior como una oda floral moderna y romántica. Abre con iris, "
            "peonía y lirio de los valles, se despliega en un corazón "
            "aterciopelado de rosa centifolia con toques de chabacano y "
            "durazno, y cierra en una base cálida de vainilla, almizcle y "
            "sándalo.",

            "Es una fragancia floral oriental delicada y a la vez intensa, "
            "ideal para cualquier época del año — perfecta tanto para el "
            "día a día como para ocasiones especiales donde buscas un "
            "aroma romántico y memorable.",
        ],
        "ideal_para": "Todo el año — uso diario y ocasiones especiales.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Dior|Miss Dior Originale|EDT": {
        "slug": "dior-miss-dior-originale",
        "meta_descripcion": (
            "Miss Dior Originale Eau de Toilette, 100% original, botella "
            "completa. Chipre floral fresco y refinado — galbanum, jazmín "
            "y pachulí. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Galbanum"],
        "notas_corazon": ["Jazmín sambac", "Rosa de Grasse"],
        "notas_fondo": ["Pachulí"],
        "parrafos": [
            "Miss Dior Originale (antes simplemente Miss Dior) es la "
            "versión más clásica y refinada de la línea, con un carácter "
            "verde y chipre atemporal. Abre con la frescura penetrante del "
            "galbanum, revela un corazón floral de jazmín sambac y rosa de "
            "Grasse, y cierra en una base de pachulí que le da su "
            "personalidad distintiva.",

            "Es una fragancia chipre floral elegante y sutil, con "
            "proyección moderada — ideal para quien busca sofisticación "
            "discreta más que un aroma que se imponga, funciona bien todo "
            "el año.",
        ],
        "ideal_para": "Todo el año — sofisticación discreta, uso diario.",
        "duracion": "5 a 7 horas en piel.",
    },
    "Dior|Sauvage|Parfum": {
        "slug": "dior-sauvage-parfum",
        "meta_descripcion": (
            "Sauvage Parfum de Dior, 100% original, botella completa. La "
            "versión más cálida y envolvente del icónico Sauvage — "
            "sándalo, vainilla y olíbano. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Bergamota", "Mandarina"],
        "notas_corazon": ["Sándalo"],
        "notas_fondo": ["Olíbano", "Vainilla", "Haba tonka"],
        "parrafos": [
            "Sauvage Parfum es la interpretación más cálida y envolvente "
            "del ADN Sauvage de Dior, con un carácter más suave y cremoso "
            "que la EDT y la EDP. Abre con bergamota y mandarina frescas, "
            "revela un corazón de sándalo aterciopelado, y cierra en una "
            "base especiada de olíbano, vainilla y haba tonka.",

            "Es una fragancia amaderada oriental refinada, ideal para "
            "otoño e invierno y ocasiones especiales — la elección "
            "perfecta para quien ya conoce el Sauvage EDT o EDP y busca "
            "una versión más pulida y sofisticada.",
        ],
        "ideal_para": "Otoño e invierno, ocasiones especiales — versión más pulida.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Dolce & Gabbana|Light Blue|EDT": {
        "slug": "dolce-gabbana-light-blue",
        "meta_descripcion": (
            "Light Blue Eau de Toilette de Dolce&Gabbana, 100% original, "
            "botella completa. Fresco frutal-amaderado icónico — manzana, "
            "cedro y jazmín. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Manzana", "Limón siciliano", "Campanilla"],
        "notas_corazon": ["Bambú", "Jazmín", "Manzana verde"],
        "notas_fondo": ["Cedro", "Almizcle", "Ámbar"],
        "parrafos": [
            "Light Blue, lanzada por Dolce&Gabbana en 2001, es una de las "
            "fragancias femeninas más icónicas del mercado — el aroma del "
            "verano en Capri en un frasco. Abre con manzana verde jugosa, "
            "limón siciliano y campanilla, se despliega en un corazón "
            "floral de bambú y jazmín, y cierra en una base de cedro, "
            "almizcle y ámbar.",

            "Es una fragancia fresca y afrutada-amaderada, perfecta para "
            "primavera y verano — ligera, energizante y versátil, ideal "
            "para el uso diario de día.",
        ],
        "ideal_para": "Primavera y verano, uso diario — energizante y fresca.",
        "duracion": "5 a 7 horas en piel.",
    },
    "Dolce & Gabbana|Light Blue Pour Homme|EDT": {
        "slug": "dolce-gabbana-light-blue-pour-homme",
        "meta_descripcion": (
            "Light Blue Pour Homme de Dolce&Gabbana, 100% original, "
            "botella completa. Fresco mediterráneo icónico — toronja, "
            "romero y almizcle. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Toronja", "Bergamota", "Mandarina siciliana", "Enebro"],
        "notas_corazon": ["Pimienta", "Romero", "Palo de rosa brasileño"],
        "notas_fondo": ["Almizcle", "Incienso", "Musgo de roble"],
        "parrafos": [
            "Light Blue Pour Homme, lanzada en 2007, captura el espíritu "
            "aventurero y dinámico del hombre mediterráneo moderno. Abre "
            "con toronja, bergamota y mandarina siciliana, se desarrolla "
            "en un corazón aromático de pimienta y romero envuelto por "
            "palo de rosa brasileño, y cierra en una base de almizcle, "
            "incienso y musgo de roble.",

            "Es una fragancia fresca y vibrante, ideal para climas cálidos "
            "— funciona igual de bien para la oficina de día que para "
            "reuniones casuales de noche, especialmente en primavera y "
            "verano.",
        ],
        "ideal_para": "Primavera y verano, día y noche — oficina y salidas casuales.",
        "duracion": "5 a 7 horas en piel.",
    },
    "Giorgio Armani|Acqua Di Gio|EDT": {
        "slug": "armani-acqua-di-gio",
        "meta_descripcion": (
            "Acqua Di Gio Eau de Toilette de Giorgio Armani, 100% "
            "original, botella completa. Acuático fresco clásico — "
            "bergamota, jazmín y pachulí. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Bergamota calabresa", "Neroli", "Mandarina verde"],
        "notas_corazon": ["Jazmín", "Rosa", "Salvia"],
        "notas_fondo": ["Pachulí", "Ámbar gris", "Almizcle"],
        "parrafos": [
            "Acqua Di Gio, lanzada por Giorgio Armani en 1996, es una de "
            "las fragancias masculinas más vendidas de la historia y un "
            "referente absoluto del género acuático fresco. Abre con "
            "bergamota calabresa, neroli y mandarina verde, revela un "
            "corazón marino de jazmín, rosa y salvia, y cierra en una base "
            "amaderada de pachulí, ámbar gris y almizcle.",

            "Es una fragancia acuática fresca perfecta para climas "
            "cálidos y húmedos — ideal para el día a día, la oficina o "
            "unas vacaciones en la playa, ligera pero reconocible.",
        ],
        "ideal_para": "Primavera y verano, uso diario — playa, oficina, clima cálido.",
        "duracion": "3 a 5 horas en piel.",
    },
    "Jean Paul Gaultier|Le Beau|EDT": {
        "slug": "jean-paul-gaultier-le-beau",
        "meta_descripcion": (
            "Le Beau Eau de Toilette de Jean Paul Gaultier, 100% "
            "original, botella completa. Amaderado aromático tropical — "
            "bergamota, coco y haba tonka. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Bergamota"],
        "notas_corazon": ["Coco"],
        "notas_fondo": ["Haba tonka"],
        "parrafos": [
            "Le Beau, lanzada por Jean Paul Gaultier en 2019, es una "
            "fragancia amaderada aromática con un carácter tropical y "
            "solar poco común en perfumería masculina. Abre con bergamota "
            "ácida que se funde en un corazón lechoso y cálido de coco, y "
            "cierra en una base dulce de haba tonka.",

            "Es una fragancia veraniega por excelencia, fresca y "
            "envolvente a la vez — perfecta para vacaciones, playa y "
            "clima cálido, con un carácter relajado y magnético.",
        ],
        "ideal_para": "Primavera y verano — playa, vacaciones, clima cálido.",
        "duracion": "5 a 7 horas en piel.",
    },
    "Jean Paul Gaultier|Le Beau Le Parfum|EDP": {
        "slug": "jean-paul-gaultier-le-beau-le-parfum",
        "meta_descripcion": (
            "Le Beau Le Parfum de Jean Paul Gaultier, 100% original, "
            "botella completa. Oriental amaderado intenso — piña, coco y "
            "ámbar gris. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Piña", "Iris", "Jengibre", "Ciprés"],
        "notas_corazon": ["Coco", "Notas amaderadas"],
        "notas_fondo": ["Haba tonka", "Sándalo", "Ámbar", "Ámbar gris"],
        "parrafos": [
            "Le Beau Le Parfum intensifica el ADN tropical de Le Beau con "
            "una versión más rica, cálida y de mayor fijación. Abre con "
            "piña, iris y jengibre, se despliega en un corazón lechoso de "
            "coco y maderas, y cierra en una base envolvente de haba "
            "tonka, sándalo y ámbar gris.",

            "Es una fragancia oriental amaderada adictiva, ideal para "
            "noches de verano donde el calor ayuda a que el coco y el "
            "ámbar se abran por completo, aunque también funciona bien en "
            "otoño e invierno gracias a su base cálida.",
        ],
        "ideal_para": "Noches de verano, otoño e invierno — base cálida y envolvente.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Jean Paul Gaultier|Scandal|EDT": {
        "slug": "jean-paul-gaultier-scandal-pour-homme-edt",
        "meta_descripcion": (
            "Scandal Pour Homme Eau de Toilette de Jean Paul Gaultier, "
            "100% original, botella completa. Ambarado amaderado dulce — "
            "mandarina, caramelo y vetiver. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Salvia esclarea", "Mandarina"],
        "notas_corazon": ["Caramelo", "Haba tonka"],
        "notas_fondo": ["Vetiver"],
        "parrafos": [
            "Scandal Pour Homme, lanzada en 2021, lleva el carácter "
            "provocador de Scandal al universo masculino con una "
            "fragancia ambarada amaderada dulce y energética. Abre con "
            "salvia esclarea y mandarina, revela un corazón goloso de "
            "caramelo y haba tonka, y cierra en una base terrosa de "
            "vetiver.",

            "Es una fragancia dulce con carácter, ideal para climas fríos "
            "— funciona muy bien de noche, perfecta para salidas y "
            "ocasiones donde buscas un aroma magnético y fácil de "
            "reconocer.",
        ],
        "ideal_para": "Otoño e invierno, noche — salidas y ocasiones para destacar.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Jean Paul Gaultier|Scandal|EDP": {
        "slug": "jean-paul-gaultier-scandal-pour-homme-edp",
        "meta_descripcion": (
            "Scandal Pour Homme Eau de Parfum de Jean Paul Gaultier, 100% "
            "original, botella completa. Más intenso y dulce que la "
            "versión EDT. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Salvia esclarea", "Mandarina"],
        "notas_corazon": ["Caramelo", "Haba tonka"],
        "notas_fondo": ["Vetiver"],
        "parrafos": [
            "Scandal Pour Homme Eau de Parfum comparte el mismo ADN dulce "
            "y ambarado que la versión EDT, pero con mayor concentración, "
            "riqueza y fijación en piel. Abre con salvia esclarea y "
            "mandarina, se despliega en un corazón de caramelo y haba "
            "tonka, y cierra en una base envolvente de vetiver.",

            "Comparada con la EDT, la EDP es más densa e intensa — ideal "
            "para clima frío y uso nocturno, perfecta para quien quiere "
            "una mayor duración y proyección sin perder el carácter dulce "
            "característico de la línea.",
        ],
        "ideal_para": "Otoño e invierno, noche — mayor duración y proyección.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Lancôme|La Vie Est Belle|EDP": {
        "slug": "lancome-la-vie-est-belle",
        "meta_descripcion": (
            "La Vie Est Belle de Lancôme, 100% original, botella "
            "completa. Floral gourmand icónico — iris, praliné y "
            "vainilla. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Grosella negra", "Pera"],
        "notas_corazon": ["Iris", "Jazmín", "Flor de azahar"],
        "notas_fondo": ["Praliné", "Vainilla", "Pachulí", "Haba tonka"],
        "parrafos": [
            "La Vie Est Belle, lanzada por Lancôme en 2012, es una de las "
            "fragancias femeninas más exitosas de la última década — un "
            "manifiesto floral gourmand sobre la felicidad. Abre con "
            "grosella negra y pera jugosas, se despliega en un corazón "
            "floral de iris, jazmín y flor de azahar, y cierra en una base "
            "golosa de praliné, vainilla y pachulí.",

            "Es una fragancia floral gourmand dulce y envolvente, ideal "
            "para otoño e invierno, aunque su carácter alegre la hace "
            "funcionar todo el año — perfecta para el uso diario y "
            "ocasiones donde buscas un aroma cálido y memorable.",
        ],
        "ideal_para": "Otoño e invierno, uso diario — cálida y memorable.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Paco Rabanne|Invictus Parfum|EDP": {
        "slug": "paco-rabanne-invictus-parfum",
        "meta_descripcion": (
            "Invictus Parfum de Paco Rabanne, 100% original, botella "
            "completa. Aromático acuático — notas marinas, lavanda y "
            "sándalo. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Notas marinas", "Lavanda", "Pimienta rosa"],
        "notas_corazon": ["Jabón", "Hoja de violeta", "Mirto"],
        "notas_fondo": ["Almizcle", "Cashmerán", "Sándalo"],
        "parrafos": [
            "Invictus Parfum lleva el espíritu de victoria de la línea "
            "Invictus a una versión más rica y sofisticada. Abre con "
            "notas marinas, lavanda y pimienta rosa que dan una apertura "
            "fresca y enérgica, se desarrolla en un corazón limpio de "
            "jabón, hoja de violeta y mirto, y cierra en una base cálida "
            "de almizcle, cashmerán y sándalo.",

            "Es una fragancia aromática acuática con carácter atlético y "
            "refinado a la vez — funciona bien todo el año, tanto de día "
            "como de noche, ideal para quien busca un Invictus con mayor "
            "profundidad y fijación.",
        ],
        "ideal_para": "Todo el año, día y noche — versión con mayor profundidad.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Paco Rabanne|Lady Million|EDP": {
        "slug": "paco-rabanne-lady-million",
        "meta_descripcion": (
            "Lady Million de Paco Rabanne, 100% original, botella "
            "completa. Floral afrutado glamoroso — frambuesa, jazmín y "
            "miel blanca. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Frambuesa", "Neroli", "Limón de Amalfi"],
        "notas_corazon": ["Jazmín", "Azahar africano", "Gardenia"],
        "notas_fondo": ["Miel blanca", "Pachulí", "Ámbar"],
        "parrafos": [
            "Lady Million, lanzada por Paco Rabanne en 2010, es una "
            "fragancia floral afrutada glamorosa y segura de sí misma, "
            "con un frasco icónico en forma de anillo dorado. Abre con "
            "frambuesa, neroli y limón de Amalfi chispeantes, se despliega "
            "en un corazón floral de jazmín, azahar africano y gardenia, y "
            "cierra en una base cálida de miel blanca, pachulí y ámbar.",

            "Es una fragancia opulenta y femenina, ideal para otoño e "
            "invierno y para uso nocturno — perfecta para eventos "
            "especiales, citas y ocasiones donde buscas proyectar "
            "confianza y lujo.",
        ],
        "ideal_para": "Otoño e invierno, noche — eventos especiales y citas.",
        "duracion": "7 a 10 horas en piel, con muy buena proyección.",
    },
    "Paco Rabanne|Olympéa|EDP": {
        "slug": "paco-rabanne-olympea",
        "meta_descripcion": (
            "Olympéa de Paco Rabanne, 100% original, botella completa. "
            "Oriental fresco salado — jazmín acuático, vainilla y sal. "
            "Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Jazmín acuático", "Mandarina verde", "Flor de jengibre"],
        "notas_corazon": ["Vainilla", "Sal"],
        "notas_fondo": ["Madera de cachemira", "Ámbar gris", "Sándalo"],
        "parrafos": [
            "Olympéa, lanzada por Paco Rabanne en 2015, es la contraparte "
            "femenina de Invictus, inspirada en el concepto de una diosa "
            "griega moderna — fuerza, dinamismo y conquista. Abre con "
            "jazmín acuático, mandarina verde y flor de jengibre "
            "chispeantes, se despliega en un corazón inesperado de "
            "vainilla salada, y cierra en una base de madera de cachemira, "
            "ámbar gris y sándalo.",

            "Es una fragancia oriental fresca con un toque salado único, "
            "ideal para primavera y verano por las noches — magnética y "
            "moderna, perfecta para salidas y ocasiones donde buscas "
            "destacar.",
        ],
        "ideal_para": "Primavera y verano, noche — salidas y ocasiones para destacar.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Valentino|Uomo|EDT": {
        "slug": "valentino-uomo",
        "meta_descripcion": (
            "Valentino Uomo Eau de Toilette, 100% original, botella "
            "completa. Amaderado aromático elegante — bergamota, café y "
            "avellana. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Bergamota", "Mirto"],
        "notas_corazon": ["Café", "Chocolate", "Nuez moscada", "Avellana"],
        "notas_fondo": ["Vainilla", "Vetiver", "Cedro"],
        "parrafos": [
            "Valentino Uomo, lanzada en 2014, encarna la elegancia "
            "italiana clásica con un toque contemporáneo y gourmand. Abre "
            "con bergamota y mirto frescos, se despliega en un corazón "
            "cálido de café y chocolate con nuez moscada y avellana, y "
            "cierra en una base envolvente de vainilla, vetiver y cedro.",

            "Es una fragancia amaderada aromática sofisticada, ideal para "
            "otoño e invierno — perfecta para la oficina, cenas y "
            "ocasiones formales donde buscas un aroma elegante y "
            "reconfortante.",
        ],
        "ideal_para": "Otoño e invierno — oficina, cenas, ocasiones formales.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Versace|Eros|EDT": {
        "slug": "versace-eros-edt",
        "meta_descripcion": (
            "Eros Eau de Toilette de Versace, 100% original, botella "
            "completa. Fougère oriental fresco y potente — menta, "
            "manzana verde y vainilla. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Menta", "Manzana verde", "Limón"],
        "notas_corazon": ["Haba tonka", "Ambroxan", "Geranio", "Rosa"],
        "notas_fondo": ["Vainilla", "Vetiver", "Musgo de roble", "Cedro atlas"],
        "parrafos": [
            "Eros, lanzada por Versace en 2012 e inspirada en el dios "
            "griego del amor, es una de las fragancias masculinas más "
            "populares y reconocibles del mercado. Abre con menta, "
            "manzana verde y limón vibrantes, se desarrolla en un corazón "
            "cálido de haba tonka, ambroxan y geranio, y cierra en una "
            "base envolvente de vainilla, vetiver y musgo de roble.",

            "Es una fragancia fougère oriental fresca y potente, con gran "
            "proyección — ideal para primavera y verano de día, aunque su "
            "base cálida también funciona bien en otoño, perfecta para "
            "salidas y ocasiones donde buscas dejar una impresión.",
        ],
        "ideal_para": "Primavera y verano, día y noche — salidas y ocasiones sociales.",
        "duracion": "6 a 8 horas en piel, con muy buena proyección.",
    },
    "Valentino|Uomo Born In Roma Intense|EDP": {
        "slug": "valentino-uomo-born-in-roma-intense-completo",
        "meta_descripcion": (
            "Uomo Born In Roma Intense de Valentino, 100% original, "
            "botella completa. Oriental vainilla intenso — jengibre, "
            "lavanda y vainilla salada. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Hoja de violeta", "Jengibre", "Bergamota"],
        "notas_corazon": ["Lavanda", "Salvia esclarea"],
        "notas_fondo": ["Vetiver", "Vainilla salada"],
        "parrafos": [
            "Uomo Born In Roma Intense lleva el ADN romano y contemporáneo "
            "de Born In Roma hacia una versión más profunda y sensual. "
            "Abre con hoja de violeta, jengibre y bergamota vibrantes, se "
            "despliega en un corazón aromático de lavanda y salvia "
            "esclarea, y cierra en una base envolvente de vetiver y "
            "vainilla salada.",

            "Es una fragancia oriental vainilla intensa, un vaivén entre "
            "frescura explosiva y sensualidad profunda — ideal para otoño "
            "e invierno, perfecta tanto para reuniones casuales como para "
            "ocasiones más formales.",
        ],
        "ideal_para": "Otoño e invierno — reuniones casuales y ocasiones formales.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Valentino|Donna|EDP": {
        "slug": "valentino-donna",
        "meta_descripcion": (
            "Valentino Donna Eau de Parfum, 100% original, botella "
            "completa. Chipre floral elegante — rosa, iris y pachulí. "
            "Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Toronja", "Bergamota", "Grosella negra"],
        "notas_corazon": ["Rosa", "Durazno", "Iris"],
        "notas_fondo": ["Pachulí", "Vainilla", "Praliné"],
        "parrafos": [
            "Valentino Donna celebra la feminidad en todas sus formas con "
            "una fragancia chipre floral suave y sensual a la vez. Abre "
            "con toronja, bergamota y grosella negra chispeantes, revela "
            "un corazón polvoriento de rosa, durazno e iris, y cierra en "
            "una base cálida de pachulí, vainilla y praliné.",

            "Es una fragancia elegante y versátil, ideal para todo el año "
            "— perfecta tanto para el día a día como para ocasiones más "
            "formales, con un carácter refinado y atemporal.",
        ],
        "ideal_para": "Todo el año — uso diario y ocasiones formales.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Tom Ford|Velvet Orchid|EDP": {
        "slug": "tom-ford-velvet-orchid",
        "meta_descripcion": (
            "Velvet Orchid de Tom Ford, 100% original, botella completa. "
            "Floral oriental opulento — orquídea, miel y sándalo. Envíos "
            "a todo México desde Monterrey."
        ),
        "notas_salida": ["Bergamota italiana", "Mandarina", "Ron", "Miel"],
        "notas_corazon": ["Orquídea", "Jazmín", "Flor de azahar", "Rosa turca"],
        "notas_fondo": ["Bálsamo de Perú", "Mirra", "Labdanum", "Sándalo", "Vainilla"],
        "parrafos": [
            "Velvet Orchid, la hermana más luminosa de Black Orchid, "
            "envuelve a quien la usa en un velo espeso y brillante de "
            "flores oscuras y dulzura embriagadora. Abre con bergamota "
            "italiana, mandarina, ron y miel, se despliega en un corazón "
            "floral de orquídea, jazmín y rosa turca, y cierra en una base "
            "cálida de bálsamo de Perú, mirra, sándalo y vainilla.",

            "Es una fragancia floral oriental opulenta, ideal para otoño "
            "e invierno — su carácter cálido y lujoso la hace perfecta "
            "para la noche y ocasiones donde buscas un aroma memorable y "
            "sofisticado.",
        ],
        "ideal_para": "Otoño e invierno, noche — ocasiones sofisticadas.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Prada|Paradoxe Intense|EDP": {
        "slug": "prada-paradoxe-intense-completo",
        "meta_descripcion": (
            "Paradoxe Intense de Prada, 100% original, botella completa. "
            "Floral oriental intenso — neroli, jazmín y vainilla bourbon. "
            "Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Bergamota", "Neroli", "Pera"],
        "notas_corazon": ["Neroli", "Jazmín superinfusión", "Musgo"],
        "notas_fondo": ["Vainilla bourbon", "Almizcle ambarado"],
        "parrafos": [
            "Paradoxe Intense celebra la fuerza y la delicadeza como dos "
            "caras de una misma mujer, en una versión más rica y densa "
            "del Paradoxe original. Abre con bergamota, neroli y pera "
            "frescos, se despliega en un corazón floral intenso de neroli "
            "y jazmín superinfusión, y cierra en una base envolvente de "
            "vainilla bourbon y almizcle ambarado.",

            "Es una fragancia floral oriental lujosa e intensificada, "
            "ideal para climas fríos — perfecta para la noche y ocasiones "
            "especiales donde buscas un aroma que combine fuerza y "
            "elegancia.",
        ],
        "ideal_para": "Otoño e invierno, noche — ocasiones especiales.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Prada|Paradoxe Virtual Flower|EDP": {
        "slug": "prada-paradoxe-virtual-flower",
        "meta_descripcion": (
            "Paradoxe Virtual Flower de Prada, 100% original, botella "
            "completa. Floral almizclado luminoso — bergamota, jazmín y "
            "ambretta. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Bergamota"],
        "notas_corazon": ["Jazmín", "Neroli"],
        "notas_fondo": ["Almizcle", "Ambretta"],
        "parrafos": [
            "Paradoxe Virtual Flower reinterpreta el jazmín a través de "
            "una lente moderna y luminosa, con una fórmula desarrollada "
            "con apoyo de inteligencia artificial. Abre con bergamota "
            "fresca y cítrica, se despliega en un corazón floral aéreo de "
            "jazmín y neroli, y cierra en una base limpia de almizcle y "
            "ambretta.",

            "Es una fragancia floral almizclada ligera y de gran "
            "fijación, ideal para primavera y verano — perfecta para el "
            "uso diario, con un carácter fresco, luminoso y moderno.",
        ],
        "ideal_para": "Primavera y verano, uso diario — fresca y luminosa.",
        "duracion": "8+ horas en piel.",
    },
    "YSL|Y Intense|EDP": {
        "slug": "ysl-y-intense",
        "meta_descripcion": (
            "Y Intense de Yves Saint Laurent, 100% original, botella "
            "completa. Aromático amaderado maduro — enebro, lavanda y "
            "pachulí. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Bayas de enebro"],
        "notas_corazon": ["Lavanda", "Geranio"],
        "notas_fondo": ["Cedro", "Pachulí"],
        "parrafos": [
            "Y Intense lleva el ADN del Y original hacia una versión más "
            "madura y potente, con mayor peso amaderado y aromático. Abre "
            "con bayas de enebro, se despliega en un corazón de lavanda y "
            "geranio, y cierra en una base terrosa de cedro y pachulí.",

            "Comparada con el Y EDP, la versión Intense es más rica, "
            "amaderada y menos dulce — una propuesta sofisticada y adulta "
            "que funciona todo el año, ideal para quien busca un aroma "
            "con carácter e impacto duradero.",
        ],
        "ideal_para": "Todo el año — carácter sofisticado y adulto.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "YSL|Mon Paris Intensement|EDP": {
        "slug": "ysl-mon-paris-intensement",
        "meta_descripcion": (
            "Mon Paris Intensément de Yves Saint Laurent, 100% original, "
            "botella completa. Chipre floral amaderado apasionado — "
            "grosella negra, rosa y vainilla. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Frambuesa", "Grosella negra", "Pera", "Naranja", "Bergamota"],
        "notas_corazon": ["Rosa de mayo", "Rosa búlgara", "Peonía", "Datura", "Fresia"],
        "notas_fondo": ["Vainilla", "Pachulí", "Almizcle blanco", "Benjuí", "Cashmerán"],
        "parrafos": [
            "Mon Paris Intensément intensifica la declaración de amor de "
            "Mon Paris con una versión más rica y de mayor fijación. Abre "
            "con frambuesa, grosella negra y pera jugosas, se despliega en "
            "un corazón rosado sensual y elegante de rosa de mayo y "
            "peonía, y cierra en una base envolvente de vainilla, pachulí "
            "y almizcle blanco.",

            "Es una fragancia chipre floral amaderada intensa, ideal para "
            "la noche y climas fríos — perfecta para ocasiones donde "
            "buscas un aroma apasionado y de larga duración.",
        ],
        "ideal_para": "Otoño e invierno, noche — ocasiones especiales.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "YSL|Libre L'Eau Nue Parfum de Peau|EDP": {
        "slug": "ysl-libre-eau-nue",
        "meta_descripcion": (
            "Libre L'Eau Nue Parfum de Peau de Yves Saint Laurent, 100% "
            "original, botella completa. Fresco cítrico floral sin "
            "alcohol — mandarina, azahar y lavanda. Envíos a todo México "
            "desde Monterrey."
        ),
        "notas_salida": ["Mandarina verde", "Bergamota"],
        "notas_corazon": ["Flor de azahar"],
        "notas_fondo": ["Lavanda"],
        "parrafos": [
            "Libre L'Eau Nue Parfum de Peau es la primera versión sin "
            "alcohol de Libre, formulada para sentirse como luz de sol "
            "sobre la piel desnuda. Abre con mandarina verde y bergamota "
            "frescas, se despliega en un corazón luminoso de flor de "
            "azahar, y cierra en una base de lavanda que aporta el toque "
            "característico de la línea Libre.",

            "Es una fragancia cítrica floral fresca y cercana a la piel, "
            "ideal para primavera y verano — perfecta para el uso diario "
            "con un carácter limpio, moderno y nada empalagoso.",
        ],
        "ideal_para": "Primavera y verano, uso diario — fresca y cercana a la piel.",
        "duracion": "5 a 7 horas en piel.",
    },
    "Versace|Pour Homme Dylan Blue|EDT": {
        "slug": "versace-pour-homme-dylan-blue",
        "meta_descripcion": (
            "Dylan Blue Pour Homme de Versace, 100% original, botella "
            "completa. Aromático acuático fresco — toronja, higuera y "
            "ámbar. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Toronja", "Hoja de higuera", "Notas acuáticas", "Pimienta negra"],
        "notas_corazon": ["Hoja de violeta", "Papiro", "Pachulí", "Ámbar"],
        "notas_fondo": ["Almizcle", "Azafrán", "Incienso", "Haba tonka"],
        "parrafos": [
            "Dylan Blue Pour Homme, lanzada por Versace en 2016, es una "
            "fragancia aromática acuática fresca y contemporánea. Abre con "
            "toronja, hoja de higuera y notas acuáticas vivaces, se "
            "desarrolla en un corazón de hoja de violeta, papiro y "
            "pachulí, y cierra en una base cálida de almizcle, azafrán e "
            "incienso.",

            "Es una fragancia fresca y limpia, ideal para primavera y "
            "verano — perfecta para la oficina y salidas de día, aunque su "
            "base amaderada y almizclada la hace funcionar también en "
            "citas nocturnas.",
        ],
        "ideal_para": "Primavera y verano, día y noche — oficina y citas.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Versace|Pour Femme Dylan Blue|EDP": {
        "slug": "versace-pour-femme-dylan-blue",
        "meta_descripcion": (
            "Dylan Blue Pour Femme de Versace, 100% original, botella "
            "completa. Floral acuático refrescante — grosella negra, "
            "manzana y rosa. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Grosella negra", "Manzana verde", "Trébol"],
        "notas_corazon": ["Rosa silvestre", "Jazmín", "Durazno"],
        "notas_fondo": ["Pachulí", "Estoraque", "Musgo blanco", "Almizcle"],
        "parrafos": [
            "Dylan Blue Pour Femme equilibra acordes frescos y acuáticos "
            "con un corazón floral delicado. Abre con grosella negra, "
            "manzana verde y trébol, se despliega en un corazón de rosa "
            "silvestre, jazmín y durazno helado, y cierra en una base "
            "cremosa de pachulí, estoraque y musgo blanco.",

            "Es una fragancia floral acuática refinada y sensual, ideal "
            "para primavera y verano — su base amaderada y almizclada "
            "también le da suficiente calidez para el otoño, perfecta "
            "para el día a día.",
        ],
        "ideal_para": "Primavera y verano, uso diario — fresca y sensual.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Paco Rabanne|Invictus Victory|EDP": {
        "slug": "paco-rabanne-invictus-victory",
        "meta_descripcion": (
            "Invictus Victory de Paco Rabanne, 100% original, botella "
            "completa. Aromático amaderado triunfal — pimienta rosa, "
            "incienso y vainilla. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Cítricos", "Pimienta rosa"],
        "notas_corazon": ["Incienso", "Lavanda"],
        "notas_fondo": ["Haba tonka", "Ámbar exótico", "Vainilla"],
        "parrafos": [
            "Invictus Victory celebra el espíritu de la victoria con una "
            "fragancia que combina energía y calidez. Abre con un golpe "
            "cítrico y de pimienta rosa vigorizante, se desarrolla en un "
            "corazón floral e incienso con lavanda, y cierra en una base "
            "envolvente de haba tonka, ámbar exótico y vainilla.",

            "Es una fragancia aromática amaderada versátil, con carácter "
            "vigorizante y a la vez reconfortante — ideal para otoño e "
            "invierno, perfecta para quien busca sentirse como un "
            "campeón en cualquier ocasión.",
        ],
        "ideal_para": "Otoño e invierno — energía y confianza en cualquier ocasión.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Paco Rabanne|Olympéa Parfum|EDP": {
        "slug": "paco-rabanne-olympea-parfum",
        "meta_descripcion": (
            "Olympéa Parfum de Paco Rabanne, 100% original, botella "
            "completa. Más intenso que la versión EDP clásica — jazmín "
            "acuático, vainilla salada y sándalo. Envíos a todo México "
            "desde Monterrey."
        ),
        "notas_salida": ["Jazmín acuático", "Mandarina verde", "Flor de jengibre"],
        "notas_corazon": ["Vainilla", "Sal"],
        "notas_fondo": ["Madera de cachemira", "Ámbar gris", "Sándalo"],
        "parrafos": [
            "Olympéa Parfum comparte el mismo ADN salado y floral que la "
            "Olympéa EDP original, pero en una concentración mayor que le "
            "da más riqueza y fijación en piel. Abre con jazmín acuático, "
            "mandarina verde y flor de jengibre, se despliega en un "
            "corazón de vainilla salada, y cierra en una base de madera de "
            "cachemira, ámbar gris y sándalo.",

            "Comparada con la EDP, esta versión Parfum es más densa y "
            "duradera — ideal para climas fríos y uso nocturno, perfecta "
            "para quien ya conoce Olympéa y busca mayor intensidad.",
        ],
        "ideal_para": "Otoño e invierno, noche — mayor intensidad y duración.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Paco Rabanne|One Million Parfum|EDP": {
        "slug": "paco-rabanne-one-million-parfum",
        "meta_descripcion": (
            "One Million Parfum de Paco Rabanne, 100% original, botella "
            "completa. Amaderado especiado intenso — cuero, tuberosa y "
            "ámbar. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Toronja", "Cardamomo", "Artemisia", "Pimienta rosa"],
        "notas_corazon": ["Cuero", "Tuberosa", "Notas amaderadas"],
        "notas_fondo": ["Ámbar", "Cashmerán", "Labdanum"],
        "parrafos": [
            "One Million Parfum lleva el icónico ADN de One Million hacia "
            "una versión más intensa y sensual, dominada por un cuero "
            "curtido al sol. Abre con toronja, cardamomo y pimienta rosa, "
            "se desarrolla en un corazón inesperado de cuero y tuberosa, y "
            "cierra en una base cálida de ámbar, cashmerán y labdanum.",

            "Es una fragancia amaderada especiada intensa y magnética, "
            "ideal para otoño e invierno y uso nocturno — perfecta para "
            "quien busca una versión más audaz y madura del clásico One "
            "Million.",
        ],
        "ideal_para": "Otoño e invierno, noche — versión audaz y madura.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Salvatore Ferragamo|Signorina Libera|EDP": {
        "slug": "salvatore-ferragamo-signorina-libera",
        "meta_descripcion": (
            "Signorina Libera de Salvatore Ferragamo, 100% original, "
            "botella completa. Floral afrutado luminoso — pera, ciruela y "
            "cashmerán. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Pera", "Bergamota", "Elemí"],
        "notas_corazon": ["Iris", "Ciruela", "Rosa"],
        "notas_fondo": ["Azúcar", "Ambroxan", "Cashmerán"],
        "parrafos": [
            "Signorina Libera celebra la libertad y el optimismo con una "
            "fragancia floral afrutada luminosa y vibrante como la luz del "
            "sol. Abre con pera, bergamota y elemí, se despliega en un "
            "corazón de iris, ciruela y rosa, y cierra en una base dulce "
            "de azúcar, ambroxan y cashmerán.",

            "Es una fragancia solar y optimista, ideal para primavera y "
            "verano — perfecta para el uso diario de una mujer libre y "
            "segura de sí misma.",
        ],
        "ideal_para": "Primavera y verano, uso diario — luminosa y optimista.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Salvatore Ferragamo|Signorina Unica|EDP": {
        "slug": "salvatore-ferragamo-signorina-unica",
        "meta_descripcion": (
            "Signorina Unica de Salvatore Ferragamo, 100% original, "
            "botella completa. Floral gourmand amaderado moderno — "
            "mandarina, violeta y tiramisú. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Mandarina", "Caña de azúcar", "Notas marinas", "Bergamota"],
        "notas_corazon": ["Madera de cachemira", "Violeta", "Grosella negra", "Azalea blanca"],
        "notas_fondo": ["Ambroxan", "Tiramisú", "Vainilla absoluta", "Haba tonka", "Pachulí"],
        "parrafos": [
            "Signorina Unica celebra la individualidad de la mujer moderna "
            "con una fragancia floral gourmand amaderada poco convencional. "
            "Abre con mandarina, caña de azúcar y notas marinas, se "
            "despliega en un corazón de madera de cachemira, violeta y "
            "grosella negra, y cierra en una base golosa de tiramisú, "
            "vainilla y haba tonka.",

            "Es una fragancia gourmand amaderada original y contemporánea, "
            "ideal para otoño e invierno — perfecta para quien busca "
            "distinguirse con un aroma fuera de lo común.",
        ],
        "ideal_para": "Otoño e invierno — un aroma distintivo y original.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Jean Paul Gaultier|Scandal Intense|EDP": {
        "slug": "jean-paul-gaultier-scandal-pour-homme-intense",
        "meta_descripcion": (
            "Scandal Pour Homme Intense de Jean Paul Gaultier, 100% "
            "original, botella completa. Amaderado cuero potente — salvia "
            "esclarea, vetiver y cuero. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Salvia esclarea"],
        "notas_corazon": ["Vetiver"],
        "notas_fondo": ["Cuero"],
        "parrafos": [
            "Scandal Pour Homme Intense construye sobre el acorde de "
            "salvia esclarea y vetiver de la línea Scandal, enriquecido "
            "con un acorde de cuero profundo y sensual. Abre con un golpe "
            "revitalizante de salvia esclarea, se desarrolla en un corazón "
            "aromático y ligeramente dulce de vetiver, y seca en un fondo "
            "terroso donde el cuero se vuelve protagonista.",

            "Es una fragancia amaderada de cuero potente y carismática, "
            "ideal para climas fríos y uso nocturno — perfecta para quien "
            "busca destacar la fuerza de su carácter.",
        ],
        "ideal_para": "Otoño e invierno, noche — fuerza de carácter.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Jean Paul Gaultier|Le Male Elixir|Parfum": {
        "slug": "jean-paul-gaultier-le-male-elixir",
        "meta_descripcion": (
            "Le Male Elixir de Jean Paul Gaultier, 100% original, botella "
            "completa. Fougère ámbar adictivo — lavanda, miel y tabaco. "
            "Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Lavanda", "Menta"],
        "notas_corazon": ["Vainilla", "Benjuí"],
        "notas_fondo": ["Miel", "Haba tonka", "Tabaco"],
        "parrafos": [
            "Le Male Elixir es una de las versiones más golosas y "
            "adictivas de la línea Le Male. Abre con lavanda y menta "
            "frescas que rápidamente dan paso a un corazón rico de "
            "vainilla y benjuí, y cierra en una base cálida y ligeramente "
            "ahumada de miel, haba tonka y tabaco.",

            "Es una fragancia fougère ámbar cálida y envolvente, ideal "
            "para otoño e invierno y para la noche — perfecta para citas, "
            "fiestas y ocasiones donde buscas un aroma dulce e "
            "inconfundible.",
        ],
        "ideal_para": "Otoño e invierno, noche — citas y fiestas.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Lancôme|La Vie Est Belle Iris Absolu|EDP": {
        "slug": "lancome-la-vie-est-belle-iris-absolu",
        "meta_descripcion": (
            "La Vie Est Belle Iris Absolu de Lancôme, 100% original, "
            "botella completa. Floral afrutado gourmand con iris — "
            "grosella negra, higo y pachulí. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Grosella negra", "Higo", "Flor de azahar"],
        "notas_corazon": ["Flor de azahar", "Jazmín"],
        "notas_fondo": ["Iris", "Acorde gourmand", "Pachulí"],
        "parrafos": [
            "La Vie Est Belle Iris Absolu enriquece el ADN floral gourmand "
            "de La Vie Est Belle con una concentración diez veces mayor de "
            "iris. Abre con grosella negra, higo y flor de azahar, se "
            "despliega en un corazón floral de azahar y jazmín, y cierra "
            "en una base de iris pallida, acorde gourmand y pachulí.",

            "Es una fragancia floral afrutada gourmand radiante, ideal "
            "para primavera y verano, aunque su base dulce y cálida "
            "también funciona muy bien en noches de otoño — perfecta para "
            "quien ama La Vie Est Belle y busca una versión más elegante.",
        ],
        "ideal_para": "Primavera y verano, noches de otoño — versión más elegante.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Giorgio Armani|Stronger With You|Parfum": {
        "slug": "armani-stronger-with-you",
        "meta_descripcion": (
            "Stronger With You Parfum de Giorgio Armani, 100% original, "
            "botella completa. Fougère oriental cálido — pimienta rosa, "
            "canela y cuero. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Pimienta rosa", "Mandarina"],
        "notas_corazon": ["Lavanda", "Canela", "Salvia"],
        "notas_fondo": ["Castaña", "Vainilla", "Cuero"],
        "parrafos": [
            "Stronger With You Parfum lleva el romance cálido de la línea "
            "a una versión más rica y envolvente, ideal para las noches "
            "más frías. Abre con pimienta rosa y mandarina, se despliega "
            "en un corazón especiado de lavanda y canela, y cierra en una "
            "base golosa de castaña, vainilla y cuero.",

            "Es una fragancia fougère oriental cálida e íntima, perfecta "
            "para el invierno y ocasiones nocturnas — ideal para citas y "
            "momentos especiales donde buscas un aroma envolvente y "
            "romántico.",
        ],
        "ideal_para": "Invierno, noche — citas y momentos especiales.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Guerlain|Vetiver|EDT": {
        "slug": "guerlain-vetiver",
        "meta_descripcion": (
            "Vetiver de Guerlain, 100% original, botella completa. "
            "Amaderado aromático clásico — bergamota, vetiver y tabaco. "
            "Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Bergamota", "Cilantro", "Limón", "Mandarina", "Neroli"],
        "notas_corazon": ["Vetiver", "Nuez moscada", "Pimienta"],
        "notas_fondo": ["Tabaco", "Haba tonka", "Cedro"],
        "parrafos": [
            "Vetiver, creada por Jean-Paul Guerlain en 1961 y relanzada en "
            "2000, es un clásico absoluto de la perfumería masculina — "
            "elegancia inglesa y sofisticación francesa en un solo frasco. "
            "Abre con bergamota, cilantro y neroli frescos, se despliega "
            "en un corazón especiado y refinado de vetiver, nuez moscada y "
            "pimienta, y cierra en una base terrosa de tabaco, haba tonka "
            "y cedro.",

            "Es una fragancia amaderada aromática atemporal, elegante y "
            "confiable más que llamativa — ideal para otoño e invierno, "
            "perfecta para la oficina y ocasiones formales donde buscas un "
            "aroma clásico y sofisticado.",
        ],
        "ideal_para": "Otoño e invierno — oficina y ocasiones formales.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Adolfo Domínguez|Jazmín Tonka|EDP": {
        "slug": "adolfo-dominguez-jazmin-tonka",
        "meta_descripcion": (
            "Jazmín Tonka de Adolfo Domínguez, 100% original, botella "
            "completa. Floral polvoriento amaderado — jazmín egipcio, "
            "ylang ylang y haba tonka. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Durazno", "Alcaravea", "Mandarina", "Naranja"],
        "notas_corazon": ["Jazmín egipcio", "Fresia", "Ylang ylang", "Magnolia"],
        "notas_fondo": ["Almizcle", "Cashmerán", "Haba tonka", "Notas amaderadas"],
        "parrafos": [
            "Jazmín Tonka, lanzada por Adolfo Domínguez en 2023, es una "
            "fragancia floral blanca y polvorienta con un fondo cálido y "
            "amaderado. Abre con durazno, alcaravea y cítricos, se "
            "despliega en un corazón de jazmín egipcio, fresia y ylang "
            "ylang, y cierra en una base envolvente de almizcle, "
            "cashmerán y haba tonka.",

            "Es una fragancia floral polvorienta elegante y versátil, "
            "ideal para todo el año — perfecta para el uso diario con un "
            "carácter suave, femenino y fácil de llevar.",
        ],
        "ideal_para": "Todo el año, uso diario — suave y femenina.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Azzaro|The Most Wanted|EDT": {
        "slug": "azzaro-the-most-wanted",
        "meta_descripcion": (
            "The Most Wanted de Azzaro, 100% original, botella completa. "
            "Oriental especiado audaz — cardamomo, toffee y madera "
            "ambarada. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Cardamomo"],
        "notas_corazon": ["Toffee"],
        "notas_fondo": ["Madera ambarada"],
        "parrafos": [
            "The Most Wanted, de Azzaro, es una fragancia masculina "
            "traviesa, sexy y audaz que combina especias, dulzura y "
            "madera en una composición simple pero magnética. Abre con "
            "cardamomo vibrante y especiado, se despliega en un corazón "
            "goloso de toffee lechoso, y cierra en una base de madera "
            "ambarada agresiva y duradera.",

            "Es una fragancia oriental especiada con carácter fuerte, "
            "ideal para otoño e invierno y uso nocturno — perfecta para "
            "quien busca destacar con un aroma dulce pero masculino.",
        ],
        "ideal_para": "Otoño e invierno, noche — destacar con carácter.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Billie Eilish|Billie Eilish|EDP": {
        "slug": "billie-eilish",
        "meta_descripcion": (
            "Eilish de Billie Eilish, 100% original, botella completa. "
            "Ámbar gourmand cálido — bayas rojas, vainilla bourbon y "
            "musgo cremoso. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Bayas rojas", "Mandarina", "Pétalos azucarados"],
        "notas_corazon": ["Vainilla bourbon", "Especias suaves", "Cacao"],
        "notas_fondo": ["Almizcle cálido", "Maderas cremosas", "Haba tonka"],
        "parrafos": [
            "Eilish, el primer perfume de Billie Eilish lanzado en 2021, "
            "es un ámbar gourmand cálido y magnético diseñado para todos. "
            "Abre con bayas rojas, mandarina y pétalos azucarados, se "
            "despliega en un corazón de vainilla bourbon, especias suaves "
            "y cacao, y cierra en una base envolvente de almizcle cálido, "
            "maderas cremosas y haba tonka.",

            "Es una fragancia ámbar gourmand sensual y cercana a la piel, "
            "ideal para otoño e invierno — perfecta para quien busca un "
            "aroma cálido, dulce y con personalidad propia.",
        ],
        "ideal_para": "Otoño e invierno — cálida y cercana a la piel.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Burberry|Her|EDP": {
        "slug": "burberry-her",
        "meta_descripcion": (
            "Burberry Her Eau de Parfum, 100% original, botella completa. "
            "Floral afrutado gourmand londinense — moras, jazmín y ámbar. "
            "Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Zarzamora", "Arándano", "Frambuesa"],
        "notas_corazon": ["Jazmín", "Violeta"],
        "notas_fondo": ["Ámbar seco", "Almizcle"],
        "parrafos": [
            "Burberry Her, creada por Francis Kurkdjian, es la primera "
            "fragancia gourmand de la casa con un toque muy británico, "
            "inspirada en el espíritu joven, creativo y aventurero de "
            "Londres. Abre con un estallido de frutos rojos y oscuros — "
            "zarzamora, arándano y frambuesa —, se despliega en un "
            "corazón floral de jazmín y violeta, y cierra en una base "
            "cálida de ámbar seco y almizcle.",

            "Es una fragancia floral afrutada gourmand luminosa, ideal "
            "para el uso diario — perfecta para la oficina, salidas "
            "casuales o cenas informales, con un carácter dulce sin ser "
            "empalagoso.",
        ],
        "ideal_para": "Todo el año, uso diario — oficina y salidas casuales.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Burberry|My Burberry Blush|EDP": {
        "slug": "burberry-my-burberry-blush",
        "meta_descripcion": (
            "My Burberry Blush de Burberry, 100% original, botella "
            "completa. Floral afrutado fresco — granada, manzana verde y "
            "jazmín. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Granada", "Limón"],
        "notas_corazon": ["Manzana verde", "Pétalos de rosa", "Geranio"],
        "notas_fondo": ["Glicina", "Jazmín"],
        "parrafos": [
            "My Burberry Blush, creada por Francis Kurkdjian, evoca un "
            "jardín londinense despertando con la primera luz del día. "
            "Abre con granada y limón frescos, se despliega en un corazón "
            "de manzana verde, pétalos de rosa y geranio, y cierra en una "
            "base delicada de glicina y jazmín.",

            "Es una fragancia floral afrutada fresca y radiante, ideal "
            "para primavera y verano — perfecta para el día, con un "
            "carácter alegre y elegante a la vez.",
        ],
        "ideal_para": "Primavera y verano, día — alegre y elegante.",
        "duracion": "5 a 7 horas en piel.",
    },
    "Carolina Herrera|Bad Boy Cobalt Elixir|EDP": {
        "slug": "carolina-herrera-bad-boy-cobalt-elixir",
        "meta_descripcion": (
            "Bad Boy Cobalt Elixir de Carolina Herrera, 100% original, "
            "botella completa. Amaderado especiado intenso — pimienta "
            "negra, trufa y franquincienso. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Pimienta negra", "Salvia"],
        "notas_corazon": ["Trufa", "Notas amaderadas"],
        "notas_fondo": ["Vainilla", "Franquincienso"],
        "parrafos": [
            "Bad Boy Cobalt Elixir lleva el carácter mineral de Bad Boy "
            "Cobalt hacia una versión más rica, intensa y de mayor "
            "fijación. Abre con pimienta negra y salvia, se despliega en "
            "un corazón de trufa y maderas, y cierra en una base "
            "resinosa de vainilla y franquincienso.",

            "Es una fragancia amaderada especiada de alta concentración, "
            "ideal para climas fríos y uso nocturno — perfecta para quien "
            "busca la versión más audaz e intensa dentro de la línea "
            "Cobalt.",
        ],
        "ideal_para": "Otoño e invierno, noche — versión más audaz de Cobalt.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Carolina Herrera|Good Girl Blush Elixir|EDP": {
        "slug": "carolina-herrera-good-girl-blush-elixir",
        "meta_descripcion": (
            "Good Girl Blush Elixir de Carolina Herrera, 100% original, "
            "botella completa. Chipre ambarado intenso — rosa, vainilla y "
            "pachulí. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Bergamota", "Naranja mandarina"],
        "notas_corazon": ["Ylang ylang", "Rosa"],
        "notas_fondo": ["Vainilla", "Pachulí"],
        "parrafos": [
            "Good Girl Blush Elixir intensifica el ADN luminoso de Good "
            "Girl Blush con una concentración mayor de rosa, vainilla y "
            "pachulí. Abre con bergamota y mandarina, se despliega en un "
            "corazón de ylang ylang y rosa, y cierra en una base "
            "incandescente de vainilla y pachulí ahumado.",

            "Es una fragancia chipre ambarada intensa y misteriosa a la "
            "vez, ideal para el día y la noche — perfecta para quien "
            "busca una versión más envolvente de Good Girl Blush.",
        ],
        "ideal_para": "Todo el año, día y noche — versión más envolvente.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Coach|Coach New York|EDP": {
        "slug": "coach-new-york",
        "meta_descripcion": (
            "Coach New York Eau de Parfum, 100% original, botella "
            "completa. Floral afrutado urbano — frambuesa, rosa turca y "
            "sándalo. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Hoja de frambuesa", "Pera", "Pimienta rosa"],
        "notas_corazon": ["Rosa turca", "Gardenia", "Ciclamen"],
        "notas_fondo": ["Ante", "Almizcle", "Cashmerán", "Sándalo"],
        "parrafos": [
            "Coach New York captura la energía espontánea y el estilo "
            "cool de Nueva York en una fragancia floral afrutada "
            "moderna. Abre con hoja de frambuesa, pera y pimienta rosa "
            "chispeantes, se despliega en un corazón floral de rosa "
            "turca, gardenia y ciclamen, y cierra en una base cálida de "
            "ante, almizcle y sándalo.",

            "Es una fragancia versátil y urbana, ideal para todo el año "
            "— perfecta para el día a día con un carácter fresco por "
            "arriba y cálido por debajo.",
        ],
        "ideal_para": "Todo el año, uso diario — carácter urbano y versátil.",
        "duracion": "6 a 8 horas en piel.",
    },
    "DKNY|Be Delicious|EDP": {
        "slug": "dkny-be-delicious",
        "meta_descripcion": (
            "Be Delicious de DKNY, 100% original, botella completa. "
            "Fresco afrutado icónico — manzana verde, pepino y sándalo. "
            "Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Pepino", "Toronja", "Magnolia", "Manzana verde"],
        "notas_corazon": ["Tuberosa", "Violeta", "Muguete", "Rosa"],
        "notas_fondo": ["Ámbar blanco", "Maderas", "Sándalo", "Almizcle"],
        "parrafos": [
            "Be Delicious, lanzada por DKNY en 2004, es una fragancia "
            "icónica que capturó la energía fresca y urbana de Nueva "
            "York en un frasco con forma de manzana. Abre con pepino, "
            "toronja y manzana verde crujiente, se despliega en un "
            "corazón floral de tuberosa, violeta y muguete, y cierra en "
            "una base limpia de ámbar blanco, sándalo y almizcle.",

            "Es una fragancia fresca y afrutada juvenil, ideal para "
            "primavera y verano — perfecta para el día a día, ligera y "
            "vibrante.",
        ],
        "ideal_para": "Primavera y verano, uso diario — fresca y vibrante.",
        "duracion": "5 a 7 horas en piel.",
    },
    "Dolce & Gabbana|Light Blue Capri In Love Pour Homme|EDP": {
        "slug": "dolce-gabbana-light-blue-capri-in-love-pour-homme",
        "meta_descripcion": (
            "Light Blue Capri In Love Pour Homme de Dolce&Gabbana, 100% "
            "original, botella completa. Amaderado especiado "
            "mediterráneo — pimienta negra, higo y pachulí. Envíos a "
            "todo México desde Monterrey."
        ),
        "notas_salida": ["Pimienta negra"],
        "notas_corazon": ["Higo verde"],
        "notas_fondo": ["Pachulí"],
        "parrafos": [
            "Light Blue Capri In Love Pour Homme transporta a la brisa "
            "salada y la luz dorada de Capri en una fragancia "
            "mediterránea masculina. Abre con el calor sutil de la "
            "pimienta negra, se despliega en un corazón verde y jugoso de "
            "higo de Capri, y cierra en una base elegante y masculina de "
            "pachulí.",

            "Es una fragancia amaderada especiada fresca, ideal para "
            "primavera y verano — perfecta para escapadas a la playa y "
            "días soleados con un carácter mediterráneo relajado.",
        ],
        "ideal_para": "Primavera y verano — playa y días soleados.",
        "duracion": "5 a 7 horas en piel.",
    },
    "Dolce & Gabbana|Light Blue Capri In Love|EDP": {
        "slug": "dolce-gabbana-light-blue-capri-in-love",
        "meta_descripcion": (
            "Light Blue Capri In Love de Dolce&Gabbana, 100% original, "
            "botella completa. Floral especiado romántico — té de "
            "jazmín, manzana y longoza. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Té de jazmín"],
        "notas_corazon": ["Manzana"],
        "notas_fondo": ["Longoza"],
        "parrafos": [
            "Light Blue Capri In Love crea un romance mediterráneo "
            "veraniego con una fragancia floral especiada delicada. Abre "
            "con el aroma calmante del té de jazmín, se despliega en un "
            "corazón crujiente de manzana, y cierra en una base "
            "especiada y sofisticada de longoza.",

            "Es una fragancia floral especiada romántica y luminosa, "
            "ideal para primavera y verano — perfecta para noches de "
            "verano mediterráneo, ligera y envolvente a la vez.",
        ],
        "ideal_para": "Primavera y verano — noches de verano mediterráneo.",
        "duracion": "5 a 7 horas en piel.",
    },
    "Dolce & Gabbana|Light Blue Summer Vibes|EDT": {
        "slug": "dolce-gabbana-light-blue-summer-vibes",
        "meta_descripcion": (
            "Light Blue Summer Vibes de Dolce&Gabbana, 100% original, "
            "botella completa. Floral amaderado almizclado veraniego — "
            "bergamota, durazno y cedro. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Bergamota calabresa"],
        "notas_corazon": ["Durazno"],
        "notas_fondo": ["Cedro"],
        "parrafos": [
            "Light Blue Summer Vibes, edición veraniega de la línea "
            "Light Blue, captura la energía vibrante del verano "
            "italiano. Abre con un estallido vivaz de bergamota "
            "calabresa, se despliega en un corazón jugoso y aterciopelado "
            "de durazno, y cierra en una base amaderada de cedro.",

            "Es una fragancia floral amaderada almizclada perfecta para "
            "el calor — ideal para primavera y verano, ligera, dulce y "
            "energizante para el uso diario.",
        ],
        "ideal_para": "Primavera y verano, uso diario — ligera y energizante.",
        "duracion": "5 a 7 horas en piel.",
    },
    "Dolce & Gabbana|Queen|EDP": {
        "slug": "dolce-gabbana-queen",
        "meta_descripcion": (
            "Q by Dolce&Gabbana Eau de Parfum, 100% original, botella "
            "completa. Floral afrutado audaz — limón siciliano, cereza y "
            "cedro. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Limón siciliano", "Naranja sanguina", "Jazmín"],
        "notas_corazon": ["Cereza", "Heliotropo"],
        "notas_fondo": ["Almizcle", "Cedro"],
        "parrafos": [
            "Q by Dolce&Gabbana celebra a la mujer contemporánea como una "
            "reina moderna, en un frasco coronado con un icónico tapón "
            "dorado. Abre con limón siciliano, naranja sanguina y "
            "jazmín, se despliega en un corazón contrastante de cereza y "
            "heliotropo, y cierra en una base de almizcle y cedro.",

            "Es una fragancia floral afrutada refinada pero audaz, ideal "
            "para primavera y verano — perfecta para el día a día con un "
            "carácter seguro y radiante.",
        ],
        "ideal_para": "Primavera y verano, uso diario — segura y radiante.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Dolce & Gabbana|The Only One Intense|EDP": {
        "slug": "dolce-gabbana-the-only-one-intense",
        "meta_descripcion": (
            "The Only One Intense de Dolce&Gabbana, 100% original, "
            "botella completa. Floral oriental sensual — azahar dorado y "
            "vainilla negra. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Neroli", "Manzana verde", "Mandarina italiana"],
        "notas_corazon": ["Jazmín", "Coco", "Flor de azahar"],
        "notas_fondo": ["Vainilla", "Madera de cachemira", "Cedro"],
        "parrafos": [
            "The Only One Intense sorprende con el contraste entre un "
            "deslumbrante azahar dorado y una vainilla negra hipnótica. "
            "Abre con neroli, manzana verde y mandarina italiana, se "
            "despliega en un corazón de jazmín, coco y flor de azahar, y "
            "cierra en una base envolvente de vainilla, madera de "
            "cachemira y cedro.",

            "Es una fragancia floral oriental adictiva y magnética, "
            "ideal para la noche y ocasiones especiales — perfecta para "
            "primavera, verano y otoños templados donde buscas dejar una "
            "impresión duradera.",
        ],
        "ideal_para": "Noche, ocasiones especiales — magnética y duradera.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Givenchy|Pi|EDT": {
        "slug": "givenchy-pi",
        "meta_descripcion": (
            "Pi de Givenchy EDT, 100% original, botella completa. "
            "Amaderado ámbar clásico — romero, muguete y vainilla. "
            "Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Romero", "Albahaca", "Estragón", "Mandarina"],
        "notas_corazon": ["Muguete", "Neroli", "Geranio", "Anís"],
        "notas_fondo": ["Vainilla", "Almendra", "Haba tonka", "Cedro", "Benjuí"],
        "parrafos": [
            "Pi, lanzada por Givenchy en 1998, es un clásico de la "
            "perfumería masculina de los noventa con un corazón "
            "magnético entre lo aromático y lo dulce. Abre con romero, "
            "albahaca y mandarina frescos, se despliega en un corazón "
            "floral de muguete, neroli y geranio, y cierra en una base "
            "cálida de vainilla, almendra y haba tonka.",

            "Es una fragancia amaderada ámbar seductora y clásica, ideal "
            "para climas fríos — perfecta para el invierno, con un "
            "carácter cómodo, versátil y fácil de llevar a diario.",
        ],
        "ideal_para": "Otoño e invierno — cómoda y fácil de llevar a diario.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Jean Paul Gaultier|Divine|EDP": {
        "slug": "jean-paul-gaultier-divine",
        "meta_descripcion": (
            "Gaultier Divine de Jean Paul Gaultier, 100% original, "
            "botella completa. Floral gourmand marino — jazmín, "
            "ylang-ylang y merengue. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Bergamota", "Bayas rojas", "Calypsone"],
        "notas_corazon": ["Jazmín", "Ylang-ylang", "Lirio"],
        "notas_fondo": ["Almizcle", "Pachulí", "Merengue"],
        "parrafos": [
            "Gaultier Divine celebra la divinidad y singularidad de cada "
            "mujer con una fragancia floral gourmand y marina en el "
            "icónico frasco de corsé de la casa. Abre con bergamota y "
            "bayas rojas frescas, se despliega en un corazón radiante de "
            "lirio, jazmín y ylang-ylang, y cierra en una base golosa de "
            "almizcle, pachulí y un toque de merengue.",

            "Es una fragancia floral gourmand acuática y polvorienta, "
            "ideal para primavera y verano — perfecta para el día a día, "
            "fresca y dulce sin ser empalagosa.",
        ],
        "ideal_para": "Primavera y verano, uso diario — fresca y dulce.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Jean Paul Gaultier|La Belle Paradise Garden|EDP": {
        "slug": "jean-paul-gaultier-la-belle-paradise-garden",
        "meta_descripcion": (
            "La Belle Paradise Garden de Jean Paul Gaultier, 100% "
            "original, botella completa. Floral ambarado — loto azul, "
            "iris y vainilla. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Loto azul"],
        "notas_corazon": ["Iris"],
        "notas_fondo": ["Vainilla"],
        "parrafos": [
            "La Belle Paradise Garden transporta al jardín exuberante y "
            "flamboyante inspirado en las pasarelas de Jean Paul "
            "Gaultier, lleno de flores misteriosas y criaturas únicas. "
            "Abre con el aroma acuático y misterioso del loto azul, se "
            "despliega en un corazón delicado de iris, y cierra en una "
            "base sensual de vainilla.",

            "Es una fragancia floral ambarada dulce y delicada, ideal "
            "para primavera y verano — perfecta para quien busca un "
            "aroma fresco, romántico y ligeramente goloso.",
        ],
        "ideal_para": "Primavera y verano — fresca, romántica y delicada.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Jean Paul Gaultier|Le Beau Paradise Garden|EDP": {
        "slug": "jean-paul-gaultier-le-beau-paradise-garden",
        "meta_descripcion": (
            "Le Beau Paradise Garden de Jean Paul Gaultier, 100% "
            "original, botella completa. Amaderado acuático tropical — "
            "coco, higo y sándalo. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Notas verdes", "Notas acuáticas", "Menta", "Jengibre"],
        "notas_corazon": ["Coco", "Higo", "Sal"],
        "notas_fondo": ["Sándalo", "Haba tonka"],
        "parrafos": [
            "Le Beau Paradise Garden encapsula la esencia de un paraíso "
            "tropical directo del jardín de Gaultier. Abre con notas "
            "verdes, acuáticas, menta y jengibre vivaces, se despliega "
            "en un corazón salado y jugoso de coco e higo verde, y "
            "cierra en una base cálida de sándalo y haba tonka bañada "
            "por el sol.",

            "Es una fragancia amaderada acuática verde y tropical, ideal "
            "para primavera y verano — perfecta para vacaciones y días "
            "de playa con un carácter fresco y solar.",
        ],
        "ideal_para": "Primavera y verano — vacaciones y playa.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Lacoste|Blanc|EDT": {
        "slug": "lacoste-blanc",
        "meta_descripcion": (
            "L.12.12 Blanc de Lacoste, 100% original, botella completa. "
            "Amaderado aromático fresco y audaz — toronja, tuberosa y "
            "cuero. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Toronja", "Romero", "Cardamomo"],
        "notas_corazon": ["Ylang-ylang", "Tuberosa"],
        "notas_fondo": ["Cedro de Virginia", "Ante", "Vetiver", "Cuero"],
        "parrafos": [
            "L.12.12 Blanc, inspirada en la icónica polo blanca de "
            "Lacoste, es una fragancia masculina limpia y elegante con "
            "un giro amaderado inesperado. Abre con toronja, romero y "
            "cardamomo frescos, se despliega en un corazón floral de "
            "ylang-ylang y tuberosa, y cierra en una base de cedro de "
            "Virginia, ante y cuero.",

            "Es una fragancia amaderada aromática fresca y audaz a la "
            "vez, ideal para primavera y verano de día — perfecta para "
            "el trabajo y salidas casuales con un carácter limpio y "
            "confiable.",
        ],
        "ideal_para": "Primavera y verano, uso diario — trabajo y salidas casuales.",
        "duracion": "5 a 7 horas en piel.",
    },
    "Montblanc|Explorer|EDP": {
        "slug": "montblanc-explorer",
        "meta_descripcion": (
            "Explorer de Montblanc, 100% original, botella completa. "
            "Amaderado aromático aventurero — bergamota, cuero y cacao. "
            "Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Bergamota", "Pimienta rosa", "Salvia esclarea"],
        "notas_corazon": ["Vetiver", "Cuero"],
        "notas_fondo": ["Ambroxan", "Akigalawood", "Pachulí", "Cacao"],
        "parrafos": [
            "Explorer, lanzada por Montblanc en 2019, evoca el espíritu "
            "aventurero de conquistar nuevas alturas en una fragancia "
            "amaderada aromática cálida y sofisticada. Abre con "
            "bergamota, pimienta rosa y salvia esclarea, se despliega en "
            "un corazón terroso de vetiver y cuero, y cierra en una base "
            "envolvente de ambroxan, pachulí y cacao.",

            "Es una fragancia amaderada cálida y magnética, ideal para "
            "otoño e invierno — perfecta para la oficina y ocasiones "
            "formales donde buscas proyectar sofisticación aventurera.",
        ],
        "ideal_para": "Otoño e invierno — oficina y ocasiones formales.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Moschino|Fresh Couture Gold|EDP": {
        "slug": "moschino-fresh-couture-gold",
        "meta_descripcion": (
            "Gold Fresh Couture de Moschino, 100% original, botella "
            "completa. Floral afrutado amaderado — pera, mango y jazmín. "
            "Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Pera", "Mango", "Durazno blanco", "Mandarina"],
        "notas_corazon": ["Orquídea", "Jazmín", "Muguete"],
        "notas_fondo": ["Vainilla", "Almizcle", "Sándalo", "Pachulí"],
        "parrafos": [
            "Gold Fresh Couture, presentada en el icónico frasco con "
            "forma de producto de limpieza de Moschino, es una versión "
            "más rica y dorada de Fresh Couture. Abre con pera, mango y "
            "durazno blanco jugosos, se despliega en un corazón floral "
            "de orquídea, jazmín y muguete, y cierra en una base cálida "
            "de vainilla, almizcle y sándalo.",

            "Es una fragancia floral afrutada amaderada dulce y "
            "luminosa, ideal para primavera y verano, aunque su fondo "
            "cálido funciona bien todo el año — perfecta para el uso "
            "diario con un carácter juguetón.",
        ],
        "ideal_para": "Primavera y verano, uso diario — dulce y juguetona.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Moschino|Fresh Couture Pink|EDT": {
        "slug": "moschino-fresh-couture-pink",
        "meta_descripcion": (
            "Pink Fresh Couture de Moschino, 100% original, botella "
            "completa. Cítrico floral afrutado — toronja rosa, granada y "
            "musgo blanco. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Toronja rosa", "Grosella negra", "Muguete"],
        "notas_corazon": ["Granada", "Jacinto rosa", "Rosa silvestre"],
        "notas_fondo": ["Cedro", "Ambrox", "Almizcle"],
        "parrafos": [
            "Pink Fresh Couture lleva el ADN limpio y fresco de Fresh "
            "Couture hacia una versión más frutal y rosada. Abre con "
            "toronja rosa, grosella negra y muguete chispeantes, se "
            "despliega en un corazón de granada y jacinto rosa, y cierra "
            "en una base ligera de cedro, ambrox y almizcle.",

            "Es una fragancia cítrica floral afrutada fresca y juguetona, "
            "ideal para primavera y verano — perfecta para el día a día "
            "con un carácter vibrante y femenino.",
        ],
        "ideal_para": "Primavera y verano, uso diario — vibrante y femenina.",
        "duracion": "5 a 7 horas en piel.",
    },
    "Moschino|Fresh Couture|EDT": {
        "slug": "moschino-fresh-couture",
        "meta_descripcion": (
            "Fresh Couture de Moschino, 100% original, botella completa. "
            "Floral afrutado limpio — bergamota, peonía y cedro. Envíos "
            "a todo México desde Monterrey."
        ),
        "notas_salida": ["Bergamota", "Mandarina", "Ylang-ylang"],
        "notas_corazon": ["Peonía", "Frambuesa", "Osmanthus"],
        "notas_fondo": ["Cedro", "Ambrox", "Pachulí"],
        "parrafos": [
            "Fresh Couture, presentada en el icónico frasco con forma de "
            "producto de limpieza de Moschino, es una fragancia floral "
            "afrutada vibrante y con espíritu vanguardista. Abre con "
            "bergamota, mandarina y ylang-ylang, se despliega en un "
            "corazón de peonía, frambuesa y osmanthus, y cierra en una "
            "base limpia de cedro, ambrox y pachulí.",

            "Es una fragancia ligera y aireada, ideal para primavera y "
            "verano — perfecta para el uso diario con un carácter fresco, "
            "juguetón y desenfadado.",
        ],
        "ideal_para": "Primavera y verano, uso diario — fresca y desenfadada.",
        "duracion": "5 a 7 horas en piel.",
    },
    "Salvatore Ferragamo|Signorina Estuche 3 Piezas|EDP": {
        "slug": "salvatore-ferragamo-signorina-estuche",
        "meta_descripcion": (
            "Set de regalo Signorina de Salvatore Ferragamo (EDP + "
            "loción corporal + miniatura), 100% original. Floral "
            "afrutado chic — grosella negra, rosa y panna cotta. Envíos "
            "a todo México desde Monterrey."
        ),
        "notas_salida": ["Rosa", "Pimienta rosa", "Grosella negra"],
        "notas_corazon": ["Jazmín", "Peonía", "Rosa"],
        "notas_fondo": ["Pachulí", "Almizcle", "Panna cotta"],
        "parrafos": [
            "Signorina, lanzada por Salvatore Ferragamo en 2011, celebra "
            "a la mujer chic e independiente con una fragancia floral "
            "afrutada sofisticada y golosa a la vez. Abre con grosella "
            "negra y pimienta rosa, se despliega en un corazón floral de "
            "jazmín, peonía y rosa, y cierra en una base cremosa de "
            "pachulí, almizcle y un original acorde de panna cotta.",

            "Es una fragancia versátil que funciona igual en la oficina "
            "que en una salida nocturna, ideal para todo el año. Este "
            "set incluye el Eau de Parfum, loción corporal y una "
            "miniatura de viaje, ideal para regalo.",
        ],
        "ideal_para": "Todo el año, día y noche — oficina y salidas.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Valentino|Donna Born In Roma Yellow Dream|EDP": {
        "slug": "valentino-donna-born-in-roma-yellow-dream",
        "meta_descripcion": (
            "Donna Born In Roma Yellow Dream de Valentino, 100% "
            "original, botella completa. Floral fresco romano — limón, "
            "rosa turca y almizcle blanco. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Limón", "Bergamota"],
        "notas_corazon": ["Rosa turca"],
        "notas_fondo": ["Almizcle blanco", "Vainilla de Madagascar", "Cedro de Virginia"],
        "parrafos": [
            "Donna Born In Roma Yellow Dream reinterpreta el estilo "
            "callejero romano con una fragancia fresca, limpia y "
            "femenina, inspirada en la luz cálida de las mañanas en "
            "Roma. Abre con limón y bergamota vibrantes, se despliega en "
            "un corazón delicado de rosa turca, y cierra en una base "
            "suave de almizcle blanco, vainilla y cedro.",

            "Es una fragancia floral fresca y espontánea, ideal para "
            "primavera y verano — perfecta para el uso diario casual con "
            "un carácter joven y radiante.",
        ],
        "ideal_para": "Primavera y verano, uso diario — joven y radiante.",
        "duracion": "5 a 7 horas en piel.",
    },
    "Valentino|Uomo Born In Roma Coral Fantasy|EDT": {
        "slug": "valentino-uomo-born-in-roma-coral-fantasy",
        "meta_descripcion": (
            "Uomo Born In Roma Coral Fantasy de Valentino, 100% "
            "original, botella completa. Amaderado aromático fresco — "
            "manzana roja, salvia y tabaco. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Manzana roja"],
        "notas_corazon": ["Geranio", "Salvia esclarea"],
        "notas_fondo": ["Pachulí", "Tabaco"],
        "parrafos": [
            "Uomo Born In Roma Coral Fantasy celebra la diversidad y los "
            "atardeceres deslumbrantes de Roma en una fragancia fresca y "
            "con carácter. Abre con un toque afrutado y moderno de "
            "manzana roja, se despliega en un corazón herbal y terroso "
            "de geranio y salvia esclarea, y cierra en una base ahumada "
            "de pachulí y tabaco.",

            "Es una fragancia amaderada aromática fresca con un fondo "
            "cálido inesperado, ideal para primavera y verano — perfecta "
            "para el día a día con un carácter moderno y desenfadado.",
        ],
        "ideal_para": "Primavera y verano, uso diario — moderna y desenfadada.",
        "duracion": "5 a 7 horas en piel.",
    },
    "Valentino|Uomo Born In Roma Green Stravaganza|EDT": {
        "slug": "valentino-uomo-born-in-roma-green-stravaganza",
        "meta_descripcion": (
            "Uomo Born In Roma Green Stravaganza de Valentino, 100% "
            "original, botella completa. Fougère ambarado vibrante — "
            "bergamota calabresa, café y vetiver. Envíos a todo México "
            "desde Monterrey."
        ),
        "notas_salida": ["Bergamota calabresa"],
        "notas_corazon": ["Acorde de café"],
        "notas_fondo": ["Vetiver"],
        "parrafos": [
            "Uomo Born In Roma Green Stravaganza revela un carácter "
            "magnético a través de la frescura verde de la bergamota "
            "calabresa combinada con la energía de un acorde de café. "
            "Abre con bergamota vibrante y verde, se despliega en un "
            "corazón enérgico de café, y cierra en una base elegante y "
            "amaderada de vetiver.",

            "Es una fragancia fougère ambarada fresca y vigorizante, "
            "ideal para primavera y verano — perfecta para el uso diario "
            "con un carácter joven y lleno de energía.",
        ],
        "ideal_para": "Primavera y verano, uso diario — joven y enérgica.",
        "duracion": "5 a 7 horas en piel.",
    },
    "Valentino|Uomo Born In Roma Yellow Dream|EDT": {
        "slug": "valentino-uomo-born-in-roma-yellow-dream",
        "meta_descripcion": (
            "Uomo Born In Roma Yellow Dream de Valentino, 100% original, "
            "botella completa. Oriental especiado vibrante — piña, "
            "jengibre y vainilla. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Piña", "Mandarina"],
        "notas_corazon": ["Especias", "Pan de jengibre", "Jengibre"],
        "notas_fondo": ["Vainilla absoluta", "Cedro"],
        "parrafos": [
            "Uomo Born In Roma Yellow Dream aporta un carácter vibrante "
            "y afrutado a la línea Born In Roma con un giro especiado "
            "inesperado. Abre con piña y mandarina jugosas, se despliega "
            "en un corazón cálido de especias, pan de jengibre y "
            "jengibre, y cierra en una base dulce de vainilla absoluta y "
            "cedro.",

            "Es una fragancia oriental especiada vibrante y afrutada, "
            "ideal para primavera y verano — perfecta como fragancia "
            "casual diaria con un carácter divertido y radiante.",
        ],
        "ideal_para": "Primavera y verano, uso diario casual — divertida y radiante.",
        "duracion": "5 a 7 horas en piel.",
    },
    "Carolina Herrera|Bad Boy Cobalt Estuche 3 Piezas|EDP": {
        "slug": "carolina-herrera-bad-boy-cobalt-estuche",
        "meta_descripcion": (
            "Set de regalo Bad Boy Cobalt de Carolina Herrera (EDP + gel "
            "de baño + miniatura), 100% original. Amaderado aromático "
            "audaz — pimienta rosa, ciruela y trufa. Envíos a todo "
            "México desde Monterrey."
        ),
        "notas_salida": ["Pimienta rosa", "Lavanda"],
        "notas_corazon": ["Geranio", "Ciruela", "Trufa"],
        "notas_fondo": ["Vetiver", "Cedro", "Haba tonka"],
        "parrafos": [
            "Bad Boy Cobalt reinterpreta el icónico Bad Boy de Carolina "
            "Herrera con un carácter más mineral y audaz, en un frasco "
            "azul cobalto. Abre con pimienta rosa y lavanda, revela un "
            "corazón floral-masculino de geranio y ciruela anclado por "
            "un acorde de trufa ahumada, y cierra en una base de "
            "vetiver, cedro y haba tonka.",

            "Es una fragancia amaderada aromática versátil, ideal para "
            "cualquier época del año. Este set incluye el Eau de Parfum, "
            "gel de baño a juego y una miniatura de viaje, ideal para "
            "regalo.",
        ],
        "ideal_para": "Todo el año, día y noche — ideal para regalo.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Carolina Herrera|Bad Boy Elixir Estuche 3 Piezas|EDP": {
        "slug": "carolina-herrera-bad-boy-elixir-estuche",
        "meta_descripcion": (
            "Set de regalo Bad Boy Elixir de Carolina Herrera (EDP + gel "
            "de baño + miniatura), 100% original. Oriental amaderado "
            "intenso — cuero, iris y franquincienso. Envíos a todo "
            "México desde Monterrey."
        ),
        "notas_salida": ["Salvia", "Lavanda"],
        "notas_corazon": ["Cuero", "Iris"],
        "notas_fondo": ["Cedro", "Franquincienso", "Haba tonka"],
        "parrafos": [
            "Bad Boy Elixir lleva el ADN de Bad Boy hacia una versión "
            "más concentrada e intensa, con un cuero limpio y magnético "
            "en el centro de la composición. Abre con salvia y lavanda, "
            "se despliega en un corazón de cuero e iris, y cierra en una "
            "base cálida de cedro, franquincienso y haba tonka.",

            "Es una fragancia oriental amaderada de gran fijación, ideal "
            "para climas fríos y uso nocturno. Este set incluye el Eau "
            "de Parfum, gel de baño a juego y una miniatura de viaje, "
            "ideal para regalo.",
        ],
        "ideal_para": "Otoño e invierno, noche — ideal para regalo.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Carolina Herrera|Bad Boy Estuche 3 Piezas|EDT": {
        "slug": "carolina-herrera-bad-boy-estuche",
        "meta_descripcion": (
            "Set de regalo Bad Boy de Carolina Herrera EDT (perfume + "
            "gel de baño + miniatura), 100% original. Oriental "
            "especiado, ahumado y seductor. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Bergamota", "Pimienta negra", "Pimienta blanca"],
        "notas_corazon": ["Cedro", "Salvia"],
        "notas_fondo": ["Haba tonka", "Madera ambarada", "Cacao"],
        "parrafos": [
            "Bad Boy, lanzada por Carolina Herrera en 2019, es una "
            "fragancia oriental especiada con una personalidad "
            "seductora y ligeramente rebelde. Abre con bergamota y un "
            "dúo de pimienta negra y blanca, se desarrolla en un "
            "corazón de cedro y salvia, y cierra en una base cálida de "
            "haba tonka, madera ambarada y cacao.",

            "Es una fragancia especiada, ahumada y sensual, ideal para "
            "uso nocturno. Este set incluye el Eau de Toilette, gel de "
            "baño a juego y una miniatura de viaje, ideal para regalo.",
        ],
        "ideal_para": "Noche, otoño e invierno — ideal para regalo.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Carolina Herrera|Good Girl Estuche 3 Piezas|EDP": {
        "slug": "carolina-herrera-good-girl-estuche",
        "meta_descripcion": (
            "Set de regalo Good Girl de Carolina Herrera (EDP + loción "
            "corporal + miniatura), 100% original. Floriental gourmand "
            "icónico — tuberosa, jazmín y haba tonka tostada. Envíos a "
            "todo México desde Monterrey."
        ),
        "notas_salida": ["Almendra", "Café", "Bergamota", "Limón"],
        "notas_corazon": ["Tuberosa", "Jazmín sambac", "Flor de azahar", "Rosa búlgara"],
        "notas_fondo": ["Haba tonka", "Cacao", "Vainilla", "Sándalo"],
        "parrafos": [
            "Good Girl, lanzada por Carolina Herrera en 2016, es una de "
            "las fragancias femeninas más reconocibles del mercado — su "
            "icónico frasco en forma de zapato de tacón es tan famoso "
            "como el perfume mismo. Abre con almendra, café y bergamota, "
            "revela un corazón floral intenso de tuberosa y jazmín "
            "sambac, y cierra en una base gourmand de haba tonka "
            "tostada, cacao y vainilla.",

            "Es una fragancia floriental gourmand icónica, ideal para la "
            "noche. Este set incluye el Eau de Parfum, loción corporal a "
            "juego y una miniatura de viaje, ideal para regalo.",
        ],
        "ideal_para": "Noche, otoño e invierno — ideal para regalo.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Carolina Herrera|Very Good Girl Elixir Estuche 3 Piezas|EDP": {
        "slug": "carolina-herrera-very-good-girl-elixir-estuche",
        "meta_descripcion": (
            "Set de regalo Very Good Girl Elixir de Carolina Herrera "
            "(EDP + loción corporal + miniatura), 100% original. "
            "Floriental gourmand intenso — cereza negra, rosa y cacao. "
            "Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Cereza negra", "Almendra amarga"],
        "notas_corazon": ["Rosa", "Tuberosa"],
        "notas_fondo": ["Vainilla", "Cacao"],
        "parrafos": [
            "Very Good Girl Elixir intensifica el carácter frutal de "
            "Very Good Girl con una versión más golosa y sensual. Abre "
            "con cereza negra y almendra amarga, se despliega en un "
            "corazón floral de rosa y tuberosa, y cierra en una base "
            "envolvente de vainilla y cacao.",

            "Es una fragancia floriental gourmand intensa, ideal para "
            "otoño e invierno. Este set incluye el Eau de Parfum, loción "
            "corporal a juego y una miniatura de viaje, ideal para "
            "regalo.",
        ],
        "ideal_para": "Otoño e invierno, noche — ideal para regalo.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Carolina Herrera|Very Good Girl Elixir|EDP": {
        "slug": "carolina-herrera-very-good-girl-elixir",
        "meta_descripcion": (
            "Very Good Girl Elixir de Carolina Herrera, 100% original, "
            "botella completa. Floriental gourmand intenso — cereza "
            "negra, rosa y cacao. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Cereza negra", "Almendra amarga"],
        "notas_corazon": ["Rosa", "Tuberosa"],
        "notas_fondo": ["Vainilla", "Cacao"],
        "parrafos": [
            "Very Good Girl Elixir, lanzada en 2024, intensifica el "
            "carácter frutal de Very Good Girl con una versión más "
            "golosa y sensual. Abre con cereza negra y almendra amarga, "
            "se despliega en un corazón floral de rosa y tuberosa, y "
            "cierra en una base envolvente de vainilla y cacao.",

            "Es una fragancia floriental gourmand intensa, ideal para "
            "otoño e invierno y uso nocturno — perfecta para quien busca "
            "una versión más rica y sensual de Very Good Girl.",
        ],
        "ideal_para": "Otoño e invierno, noche — versión más rica y sensual.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Carolina Herrera|Very Good Girl Estuche 3 Piezas|EDP": {
        "slug": "carolina-herrera-very-good-girl-estuche",
        "meta_descripcion": (
            "Set de regalo Very Good Girl de Carolina Herrera (EDP + "
            "loción corporal + miniatura), 100% original. Floral "
            "afrutado sensual — lichi, rosa y vainilla. Envíos a todo "
            "México desde Monterrey."
        ),
        "notas_salida": ["Lichi", "Grosella roja"],
        "notas_corazon": ["Rosa"],
        "notas_fondo": ["Vainilla", "Vetiver"],
        "parrafos": [
            "Very Good Girl es una versión más frutal y sensual dentro "
            "del universo Good Girl de Carolina Herrera. Abre con lichi "
            "y grosella roja jugosos, se despliega en un corazón de "
            "rosa, y cierra en una base cálida de vainilla y vetiver.",

            "Es una fragancia floral afrutada versátil, dulce sin ser "
            "empalagosa. Este set incluye el Eau de Parfum, loción "
            "corporal a juego y una miniatura de viaje, ideal para "
            "regalo.",
        ],
        "ideal_para": "Todo el año, día y noche — ideal para regalo.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Jean Paul Gaultier|Le Beau Estuche 2 Piezas|EDT": {
        "slug": "jean-paul-gaultier-le-beau-estuche",
        "meta_descripcion": (
            "Set de regalo Le Beau de Jean Paul Gaultier (EDT + "
            "miniatura), 100% original. Amaderado aromático tropical — "
            "bergamota, coco y haba tonka. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Bergamota"],
        "notas_corazon": ["Coco"],
        "notas_fondo": ["Haba tonka"],
        "parrafos": [
            "Le Beau, lanzada por Jean Paul Gaultier en 2019, es una "
            "fragancia amaderada aromática con un carácter tropical y "
            "solar poco común en perfumería masculina. Abre con "
            "bergamota ácida que se funde en un corazón lechoso y cálido "
            "de coco, y cierra en una base dulce de haba tonka.",

            "Es una fragancia veraniega por excelencia, fresca y "
            "envolvente a la vez. Este set incluye el Eau de Toilette "
            "más una miniatura de viaje, ideal para regalo.",
        ],
        "ideal_para": "Primavera y verano — ideal para regalo.",
        "duracion": "5 a 7 horas en piel.",
    },
    "Jean Paul Gaultier|Le Male Estuche 3 Piezas|EDT": {
        "slug": "jean-paul-gaultier-le-male-estuche",
        "meta_descripcion": (
            "Set de regalo Le Male de Jean Paul Gaultier (EDT + "
            "desodorante + gel de baño), 100% original. Oriental "
            "fougère icónico — lavanda, vainilla y cardamomo. Envíos a "
            "todo México desde Monterrey."
        ),
        "notas_salida": ["Artemisia", "Menta", "Cardamomo", "Bergamota"],
        "notas_corazon": ["Lavanda", "Flor de azahar", "Canela", "Comino"],
        "notas_fondo": ["Sándalo", "Vainilla", "Cedro", "Haba tonka", "Ámbar"],
        "parrafos": [
            "Le Male, lanzada por Jean Paul Gaultier en 1995 y creada "
            "por Francis Kurkdjian, es uno de los perfumes masculinos "
            "más influyentes de las últimas tres décadas, reconocible "
            "por su frasco en forma de torso marinero. Abre con "
            "artemisia, menta y cardamomo, se desarrolla en un corazón "
            "especiado de lavanda y canela, y cierra en una base cálida "
            "de vainilla, sándalo y haba tonka.",

            "Es una fragancia oriental fougère atemporal que combina "
            "frescura y calidez sensual. Este set incluye el Eau de "
            "Toilette, desodorante y gel de baño a juego, ideal para "
            "regalo.",
        ],
        "ideal_para": "Todo el año, día y noche — ideal para regalo.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Paco Rabanne|Invictus Estuche 3 Piezas|EDT": {
        "slug": "paco-rabanne-invictus-estuche",
        "meta_descripcion": (
            "Set de regalo Invictus de Paco Rabanne (EDT + desodorante "
            "+ miniatura), 100% original. Amaderado aromático, fresco y "
            "versátil. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Pomelo", "Mandarina", "Acorde marino"],
        "notas_corazon": ["Laurel", "Jazmín (hedione)"],
        "notas_fondo": ["Madera de guayaco", "Patchouli", "Musgo de roble"],
        "parrafos": [
            "Invictus, lanzada por Paco Rabanne en 2013, es una de las "
            "fragancias masculinas más populares de la casa — energía, "
            "vitalidad y espíritu de victoria en un frasco. Abre con "
            "pomelo fresco, mandarina y un acorde marino, se desarrolla "
            "en un corazón aromático de laurel y jazmín hedione, y "
            "cierra en una base amaderada de guayaco, patchouli y musgo "
            "de roble.",

            "Es una fragancia amaderada aromática versátil, ideal para "
            "primavera y verano. Este set incluye el Eau de Toilette, "
            "desodorante y una miniatura de viaje, ideal para regalo.",
        ],
        "ideal_para": "Primavera y verano, día y noche — ideal para regalo.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Paco Rabanne|Invictus Victory Estuche 2 Piezas|EDP": {
        "slug": "paco-rabanne-invictus-victory-estuche",
        "meta_descripcion": (
            "Set de regalo Invictus Victory de Paco Rabanne (EDP + "
            "shampoo), 100% original. Aromático amaderado triunfal — "
            "pimienta rosa, incienso y vainilla. Envíos a todo México "
            "desde Monterrey."
        ),
        "notas_salida": ["Cítricos", "Pimienta rosa"],
        "notas_corazon": ["Incienso", "Lavanda"],
        "notas_fondo": ["Haba tonka", "Ámbar exótico", "Vainilla"],
        "parrafos": [
            "Invictus Victory celebra el espíritu de la victoria con una "
            "fragancia que combina energía y calidez. Abre con un golpe "
            "cítrico y de pimienta rosa vigorizante, se desarrolla en un "
            "corazón floral e incienso con lavanda, y cierra en una base "
            "envolvente de haba tonka, ámbar exótico y vainilla.",

            "Es una fragancia aromática amaderada versátil, con carácter "
            "vigorizante y a la vez reconfortante. Este set incluye el "
            "Eau de Parfum más shampoo a juego, ideal para regalo.",
        ],
        "ideal_para": "Otoño e invierno — ideal para regalo.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Paco Rabanne|Million Gold For Her Estuche 3 Piezas|EDP": {
        "slug": "paco-rabanne-million-gold-for-her-estuche",
        "meta_descripcion": (
            "Set de regalo Million Gold For Her de Paco Rabanne (EDP + "
            "loción corporal + miniatura), 100% original. Floral "
            "afrutado sensual — pera, rosa y vainilla. Envíos a todo "
            "México desde Monterrey."
        ),
        "notas_salida": ["Pera", "Rosa", "Lavanda"],
        "notas_corazon": ["Ylang-ylang", "Jazmín"],
        "notas_fondo": ["Vainilla", "Almizcle", "Musgo"],
        "parrafos": [
            "Million Gold For Her irradia la energía dorada y "
            "resplandeciente del universo Million en una fragancia "
            "floral afrutada intensamente sensual. Abre con pera, rosa "
            "chispeante y lavanda, se despliega en un corazón de flores "
            "blancas de ylang-ylang y jazmín, y cierra en una base "
            "envolvente de vainilla, almizcle mineral y musgo.",

            "Es una fragancia floral afrutada opulenta y adictiva, "
            "ideal para otoño e invierno y uso nocturno. Este set "
            "incluye el Eau de Parfum, loción corporal a juego y una "
            "miniatura de viaje, ideal para regalo.",
        ],
        "ideal_para": "Otoño e invierno, noche — ideal para regalo.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Paco Rabanne|Olympéa Estuche 2 Piezas|EDP": {
        "slug": "paco-rabanne-olympea-estuche",
        "meta_descripcion": (
            "Set de regalo Olympéa de Paco Rabanne (EDP + loción "
            "corporal), 100% original. Oriental fresco salado — jazmín "
            "acuático, vainilla y sal. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Jazmín acuático", "Mandarina verde", "Flor de jengibre"],
        "notas_corazon": ["Vainilla", "Sal"],
        "notas_fondo": ["Madera de cachemira", "Ámbar gris", "Sándalo"],
        "parrafos": [
            "Olympéa, lanzada por Paco Rabanne en 2015, es la "
            "contraparte femenina de Invictus, inspirada en el concepto "
            "de una diosa griega moderna. Abre con jazmín acuático, "
            "mandarina verde y flor de jengibre chispeantes, se "
            "despliega en un corazón inesperado de vainilla salada, y "
            "cierra en una base de madera de cachemira, ámbar gris y "
            "sándalo.",

            "Es una fragancia oriental fresca con un toque salado único, "
            "ideal para primavera y verano por las noches. Este set "
            "incluye el Eau de Parfum más loción corporal a juego, ideal "
            "para regalo.",
        ],
        "ideal_para": "Primavera y verano, noche — ideal para regalo.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Paco Rabanne|One Million Estuche 3 Piezas|EDT": {
        "slug": "paco-rabanne-one-million-estuche",
        "meta_descripcion": (
            "Set de regalo One Million de Paco Rabanne (EDT + "
            "desodorante + miniatura), 100% original. Amaderado "
            "especiado icónico — canela, cuero y ámbar. Envíos a todo "
            "México desde Monterrey."
        ),
        "notas_salida": ["Mandarina sanguina", "Toronja", "Menta"],
        "notas_corazon": ["Canela", "Especias", "Rosa"],
        "notas_fondo": ["Ámbar", "Cuero", "Notas amaderadas", "Patchouli"],
        "parrafos": [
            "One Million, lanzada por Paco Rabanne en 2008, es una de "
            "las fragancias masculinas más icónicas de la última década "
            "— su frasco en forma de lingote de oro es tan reconocible "
            "como el aroma mismo. Abre con mandarina sanguina, toronja y "
            "menta, revela un corazón especiado de canela y rosa, y "
            "cierra en una base amaderada de cuero, ámbar y patchouli "
            "indio.",

            "Es una fragancia amaderada especiada versátil, perfecta "
            "para salidas casuales y formales. Este set incluye el Eau "
            "de Toilette, desodorante y una miniatura de viaje, ideal "
            "para regalo.",
        ],
        "ideal_para": "Otoño e invierno, día y noche — ideal para regalo.",
        "duracion": "4 a 6 horas en piel.",
    },
    "Carolina Herrera|Bad Boy Cobalt Absolute|EDP": {
        "slug": "carolina-herrera-bad-boy-cobalt-absolute",
        "meta_descripcion": (
            "Bad Boy Cobalt Absolute de Carolina Herrera, 100% original, "
            "botella completa. Oriental amaderado intenso — lavanda "
            "azul, trufa y oud. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Lavanda azul", "Salvia azul", "Elemí"],
        "notas_corazon": ["Trufa", "Geranio", "Oud"],
        "notas_fondo": ["Vainilla", "Roble", "Vetiver"],
        "parrafos": [
            "Bad Boy Cobalt Absolute, lanzada en 2025, ofrece la "
            "interpretación más intensa y seductora dentro de la línea "
            "Bad Boy Cobalt. Abre con lavanda azul, salvia azul y elemí "
            "frescos, se despliega en un corazón denso de trufa, "
            "geranio y oud, y cierra en una base cálida de vainilla, "
            "roble y vetiver.",

            "Es una fragancia oriental amaderada de gran profundidad y "
            "fijación, ideal para climas fríos y uso nocturno — "
            "perfecta para quien busca una versión más audaz y "
            "concentrada dentro de la línea Cobalt.",
        ],
        "ideal_para": "Otoño e invierno, noche — versión más audaz de Cobalt.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Jean Paul Gaultier|Le Beau Narcisse|EDP": {
        "slug": "jean-paul-gaultier-le-beau-narcisse",
        "meta_descripcion": (
            "Le Beau Narcisse de Jean Paul Gaultier, 100% original, "
            "botella completa. Floral amaderado almizclado — bergamota, "
            "coco y flor de azahar. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Bergamota", "Coco"],
        "notas_corazon": ["Almizcle", "Flor de azahar"],
        "notas_fondo": ["Vainilla", "Haba tonka", "Vetiver"],
        "parrafos": [
            "Le Beau Narcisse construye sobre el ADN tropical de Le "
            "Beau con una composición ambarada-almizclada definida por "
            "calidez e intensidad discreta. Abre con un chispazo fresco "
            "de bergamota y coco, se despliega en un corazón carnal de "
            "almizcle suavizado por flor de azahar, y cierra en una "
            "base envolvente de vainilla, haba tonka y vetiver.",

            "Es una fragancia floral amaderada almizclada cálida y "
            "adictiva, ideal para primavera y noches templadas — "
            "perfecta para quien busca una versión más floral y sutil "
            "dentro del universo Le Beau.",
        ],
        "ideal_para": "Primavera, noche — cálida y adictiva.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Jean Paul Gaultier|Le Male Elixir Absolu|Parfum": {
        "slug": "jean-paul-gaultier-le-male-elixir-absolu",
        "meta_descripcion": (
            "Le Male Elixir Absolu de Jean Paul Gaultier, 100% "
            "original, botella completa. Amaderado aromático intenso — "
            "ciruela, lavanda y haba tonka. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Ciruela", "Canela", "Cardamomo", "Bergamota"],
        "notas_corazon": ["Lavanda", "Davana", "Artemisia"],
        "notas_fondo": ["Haba tonka", "Benjuí", "Ambrette", "Patchouli", "Labdanum"],
        "parrafos": [
            "Le Male Elixir Absolu, lanzada en 2025, lleva el carácter "
            "goloso de la línea Elixir hacia una versión más profunda y "
            "sofisticada. Abre con un golpe crujiente de lavanda que da "
            "paso a un corazón jugoso de ciruela, canela y cardamomo, y "
            "cierra en una base rica de haba tonka, benjuí, ambrette y "
            "patchouli.",

            "Es una fragancia amaderada aromática cálida, dulce y "
            "especiada, ideal para otoño e invierno y uso nocturno — "
            "con suficiente elegancia para no resultar abrumadora, "
            "perfecta para ocasiones especiales.",
        ],
        "ideal_para": "Otoño e invierno, noche — ocasiones especiales.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "Jean Paul Gaultier|La Belle Rosea|EDP": {
        "slug": "jean-paul-gaultier-la-belle-rosea",
        "meta_descripcion": (
            "La Belle Rosea de Jean Paul Gaultier, 100% original, "
            "botella completa. Floral acuático ambarado — peonía, rosa "
            "y vainilla. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Notas acuáticas", "Bergamota"],
        "notas_corazon": ["Peonía", "Rosa", "Violeta"],
        "notas_fondo": ["Vainilla", "Almizcle", "Cedro"],
        "parrafos": [
            "La Belle Rosea equilibra frescura y sensualidad suave en "
            "una fragancia floral acuática luminosa. Abre con un acorde "
            "acuático cristalino y bergamota, se despliega en un "
            "corazón radiante de peonía, rosa y violeta, y cierra en "
            "una base cálida de vainilla, almizcle y cedro que deja una "
            "estela sedosa y delicada.",

            "Es una fragancia floral acuática fresca y femenina, ideal "
            "para primavera y verano — perfecta para el día a día con "
            "un carácter luminoso y romántico.",
        ],
        "ideal_para": "Primavera y verano, uso diario — luminosa y romántica.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Carolina Herrera|CH Swing|EDP": {
        "slug": "carolina-herrera-ch-swing",
        "meta_descripcion": (
            "CH Swing de Carolina Herrera, 100% original, botella "
            "completa. Oriental vainilla vibrante — lima, pera y coco. "
            "Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Lima", "Pera"],
        "notas_corazon": ["Coco", "Ylang ylang"],
        "notas_fondo": ["Sándalo", "Avellana", "Cedro", "Vainilla"],
        "parrafos": [
            "CH Swing, edición limitada de Carolina Herrera inspirada "
            "en la precisión y energía del golf, reinterpreta CH con un "
            "carácter vibrante y adictivo. Abre con lima y pera "
            "chispeantes, se despliega en un corazón cremoso de coco y "
            "ylang ylang, y cierra en una base cálida de sándalo, "
            "avellana y vainilla.",

            "Es una fragancia oriental vainilla enérgica y golosa, "
            "ideal para primavera y verano — perfecta para el día a día "
            "con un carácter fresco, moderno y distintivo.",
        ],
        "ideal_para": "Primavera y verano, uso diario — fresca y distintiva.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Paco Rabanne|Million Gold For Her Pure Diamonds|EDP": {
        "slug": "paco-rabanne-million-gold-pure-diamonds",
        "meta_descripcion": (
            "Million Gold For Her Pure Diamonds de Paco Rabanne, 100% "
            "original, botella completa. Floral afrutado radiante — "
            "durazno, ylang ylang y vainilla. Envíos a todo México "
            "desde Monterrey."
        ),
        "notas_salida": ["Durazno", "Bergamota"],
        "notas_corazon": ["Ylang ylang", "Jazmín"],
        "notas_fondo": ["Vainilla", "Almizcle"],
        "parrafos": [
            "Million Gold For Her Pure Diamonds, edición limitada "
            "lanzada para celebrar los 60 años de la maison, rinde "
            "tributo a la maestría de Paco Rabanne con los diamantes. "
            "Abre con durazno y bergamota jugosos, se despliega en un "
            "corazón floral de ylang ylang y jazmín, y cierra en una "
            "base cálida de vainilla y almizcle.",

            "Es una fragancia floral afrutada radiante y dulce, ideal "
            "para primavera y verano — perfecta para el día a día con "
            "un carácter luminoso y festivo.",
        ],
        "ideal_para": "Primavera y verano, uso diario — luminosa y festiva.",
        "duracion": "6 a 8 horas en piel.",
    },
    "Paco Rabanne|Million Gold For Her|Parfum": {
        "slug": "paco-rabanne-million-gold-parfum",
        "meta_descripcion": (
            "Million Gold For Her Parfum de Paco Rabanne, 100% "
            "original, botella completa. Oriental floral intenso — "
            "rosa, jazmín y sándalo. Envíos a todo México desde "
            "Monterrey."
        ),
        "notas_salida": ["Jazmín", "Rosa", "Cítricos", "Limón"],
        "notas_corazon": ["Ylang-ylang", "Notas solares", "Lavanda"],
        "notas_fondo": ["Sándalo", "Vainilla"],
        "parrafos": [
            "Million Gold For Her Parfum lleva el ADN dorado y sensual "
            "de Million Gold hacia una concentración mayor, más rica y "
            "duradera. Abre con jazmín, rosa y cítricos vibrantes, se "
            "despliega en un corazón floral de ylang-ylang con notas "
            "solares y lavanda, y cierra en una base envolvente de "
            "sándalo y vainilla.",

            "Es una fragancia oriental floral opulenta e intensa, ideal "
            "para otoño e invierno y uso nocturno — perfecta para "
            "quien busca una versión más rica y sofisticada dentro del "
            "universo Million Gold.",
        ],
        "ideal_para": "Otoño e invierno, noche — versión rica y sofisticada.",
        "duracion": "8+ horas en piel, con muy buena proyección.",
    },
    "YSL|Y|EDP": {
        "slug": "ysl-y-completo",
        "meta_descripcion": (
            "Y de Yves Saint Laurent Eau de Parfum, 100% original, "
            "botella completa. Aromático herbal fresco — bergamota, "
            "jengibre y vetiver. Envíos a todo México desde Monterrey."
        ),
        "notas_salida": ["Bergamota", "Jengibre", "Manzana"],
        "notas_corazon": ["Salvia", "Geranio", "Bayas de enebro"],
        "notas_fondo": ["Vetiver", "Cedro", "Haba tonka", "Madera ambarada", "Olíbano"],
        "parrafos": [
            "Y, lanzada por Yves Saint Laurent en 2018, celebra al "
            "hombre que se atreve a labrar su propio camino con una "
            "fragancia aromática herbal fresca y moderna. Abre con "
            "bergamota, jengibre y manzana vibrantes, se despliega en "
            "un corazón limpio de salvia, geranio y bayas de enebro, y "
            "cierra en una base amaderada de vetiver, cedro y haba "
            "tonka con un toque dulce de madera ambarada.",

            "Es una fragancia aromática versátil y de gran fijación, "
            "ideal para todo el año — funciona igual de bien en la "
            "oficina que en una salida casual o un evento nocturno.",
        ],
        "ideal_para": "Todo el año, día y noche — oficina, salidas y eventos.",
        "duracion": "8 a 10 horas en piel, con muy buena proyección.",
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
