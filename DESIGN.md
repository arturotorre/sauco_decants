---
name: Saúco Decants
description: Perfumes originales de lujo en 3, 5 y 10 ml; el atelier de un perfumista sobre muro de yeso.
colors:
  tinta: "#3B2318"
  tinta-hondo: "#2A170E"
  tinta-suave: "#64503F"
  linea: "rgba(59,35,24,0.16)"
  yeso: "#E2E1DE"
  papel: "#FFFFFF"
  roble: "#B08A5A"
  roble-claro: "#CDAE86"
  pie-suave: "#D7CABD"
typography:
  display:
    fontFamily: "Bodoni Moda, Didot, Bodoni 72, Georgia, serif"
    fontSize: "clamp(3.5rem, 15vw, 6rem)"
    fontWeight: 500
    lineHeight: 0.92
    letterSpacing: "-0.02em"
  numeral:
    fontFamily: "Bodoni Moda, Didot, Bodoni 72, Georgia, serif"
    fontSize: "40px"
    fontWeight: 500
    lineHeight: 1
    letterSpacing: "-0.03em"
    fontFeature: "'lnum'"
  headline:
    fontFamily: "Bodoni Moda, Didot, Bodoni 72, Georgia, serif"
    fontSize: "clamp(1.75rem, 7vw, 2.75rem)"
    fontWeight: 500
    lineHeight: 1.05
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Bodoni Moda, Didot, Bodoni 72, Georgia, serif"
    fontSize: "22px"
    fontWeight: 500
    lineHeight: 1.2
  body-lg:
    fontFamily: "Hanken Grotesk, Helvetica Neue, Arial, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.6
  body:
    fontFamily: "Hanken Grotesk, Helvetica Neue, Arial, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Hanken Grotesk, Helvetica Neue, Arial, sans-serif"
    fontSize: "13px"
    fontWeight: 600
    letterSpacing: "0.08em"
  button:
    fontFamily: "Hanken Grotesk, Helvetica Neue, Arial, sans-serif"
    fontSize: "15px"
    fontWeight: 600
    letterSpacing: "0.1em"
rounded:
  none: "0px"
  xs: "2px"
  full: "9999px"
spacing:
  gutter: "1.25rem"
  gutter-desktop: "clamp(2rem, 4vw, 4rem)"
  stack-sm: "0.6rem"
  stack-md: "1.75rem"
  section: "4.5rem"
components:
  button-primary:
    backgroundColor: "{colors.tinta}"
    textColor: "{colors.papel}"
    typography: "{typography.button}"
    rounded: "{rounded.xs}"
    padding: "0 1.75rem"
    height: "56px"
  button-primary-hover:
    backgroundColor: "{colors.tinta-hondo}"
  link-secondary:
    textColor: "{colors.tinta}"
    typography: "{typography.body}"
    padding: "0.6rem 0.5rem"
  tira:
    backgroundColor: "{colors.papel}"
    textColor: "{colors.tinta}"
    typography: "{typography.numeral}"
    rounded: "{rounded.none}"
    width: "68px"
    height: "180px"
  cart-button:
    backgroundColor: "{colors.papel}"
    textColor: "{colors.tinta}"
    rounded: "{rounded.full}"
    size: "44px"
  nav:
    backgroundColor: "{colors.yeso}"
    textColor: "{colors.tinta-suave}"
    typography: "{typography.body}"
  footer:
    backgroundColor: "{colors.tinta}"
    textColor: "{colors.yeso}"
    padding: "3.5rem 1.5rem 3rem"
  button-secondary:
    textColor: "{colors.tinta}"
    rounded: "{rounded.xs}"
    padding: "0 1.1rem"
    height: "44px"
  button-secondary-hover:
    backgroundColor: "{colors.tinta}"
    textColor: "{colors.papel}"
  button-row:
    textColor: "{colors.tinta}"
    rounded: "{rounded.xs}"
    padding: "0 1rem"
    height: "40px"
  button-row-hover:
    backgroundColor: "{colors.tinta}"
    textColor: "{colors.papel}"
  link-inline:
    textColor: "{colors.tinta}"
    padding: "0"
  chip-filter:
    backgroundColor: "{colors.papel}"
    textColor: "{colors.tinta}"
    rounded: "{rounded.full}"
    padding: "0 1rem"
    height: "40px"
  chip-filter-active:
    backgroundColor: "{colors.tinta}"
    textColor: "{colors.papel}"
  search-field:
    backgroundColor: "{colors.papel}"
    textColor: "{colors.tinta}"
    rounded: "{rounded.xs}"
    padding: "0 1rem 0 2.75rem"
    height: "48px"
  catalog-row:
    textColor: "{colors.tinta}"
    padding: "1rem 0"
  catalog-row-photo:
    rounded: "{rounded.none}"
    size: "72px"
  vitrina:
    rounded: "{rounded.none}"
    height: "96px"
  dropdown-toggle:
    backgroundColor: "{colors.papel}"
    textColor: "{colors.tinta}"
    rounded: "{rounded.xs}"
    padding: "0 1rem"
    height: "40px"
  dropdown-panel:
    backgroundColor: "{colors.papel}"
    textColor: "{colors.tinta}"
    rounded: "{rounded.xs}"
    padding: "1.1rem"
  empty-state:
    textColor: "{colors.tinta}"
    padding: "2rem 0"
  ficha-repisa:
    backgroundColor: "{colors.yeso}"
    rounded: "{rounded.none}"
    width: "120px"
    height: "130px"
  ficha-medida:
    textColor: "{colors.tinta}"
    rounded: "{rounded.xs}"
    height: "60px"
  ficha-medida-hover:
    backgroundColor: "{colors.tinta}"
    textColor: "{colors.papel}"
  ficha-agregar:
    backgroundColor: "{colors.tinta}"
    textColor: "{colors.papel}"
    typography: "{typography.button}"
    rounded: "{rounded.xs}"
    padding: "0 1.5rem"
    height: "56px"
  ficha-fila:
    textColor: "{colors.tinta}"
    padding: "0.8rem 0"
---

# Design System: Saúco Decants

## Overview

**Creative North Star: "El atelier del perfumista"**

Saúco se presenta como el taller de un perfumista: un muro de yeso gris cálido y claro, repisas de roble claro con canto de chocolate, frascos reales fotografiados sobre ellas y tiras de papel secante blancas que llevan la medida (3 · 5 · 10) en cifras grandes. El chocolate de la marca es tinta, no pintura de pared: escribe, traza líneas y llena el botón principal, y solo cubre una superficie completa en dos lugares: la banda de «100% originales» en la portada y el pie.

El sitio se recorre por **salas**: cada sección es una franja a todo lo ancho con su propio fondo (yeso, papel o, una sola vez, chocolate) y un título centrado sobre una regla de roble; el cambio de fondo es lo que separa, no una línea. Arriba manda un **encabezado de casa de perfumes**: el logo grande al centro y el menú en una fila debajo, que se compacta al bajar.

La voz tipográfica son dos familias: Bodoni Moda, un Didone de alto contraste, habla en el nombre, los títulos y las cifras; Hanken Grotesk, una grotesca sobria, se lee y se opera en todo lo demás. La densidad es baja y la composición es de taller, no de tienda en cuadrícula: las fotos se posan sobre repisas, no dentro de tarjetas. El movimiento es breve y con ease-out; las tiras se abren en abanico una vez al cargar y la elegida se levanta.

Alcance actual: este mundo cubre todo el sitio: la portada (vista-home de `index.html`), los dos catálogos (`#catalogo` de decants y `#completos` de perfumes completos, con su formulario de cotización), las 134 fichas de producto (`decants/*`, `completos/*`, generadas por `tools/generar_pagina_producto.py`), el nav global, el carrito completo (botón, panel, selector de medida y aviso al agregar) y el pie. La migración está completa; lo que queda del sistema heredado en `css/styles.css` y `css/fonts.css` son restos sin uso (ver la nota al final de Do's and Don'ts), deuda de limpieza y no parte de este sistema. El `theme-color` del navegador es yeso (#E2E1DE) en la portada y en todas las fichas.

**Key Characteristics:**
- Salas a todo lo ancho: yeso (#E2E1DE) como muro base, papel (#fff) donde se exhiben frascos y una sola banda chocolate (originalidad); nunca crema.
- Encabezado de casa: logo al centro, menú en fila entre dos líneas, compacto al bajar.
- Chocolate como tinta: texto, líneas, botón principal y pie.
- Bodoni Moda para nombre, títulos y cifras; Hanken Grotesk para texto, etiquetas, botones y nav.
- Repisas de roble con canto chocolate como soporte de toda foto de producto.
- Tiras de papel blanco como selector de medida, con la cifra como protagonista.
- Fotos reales de frascos fundidas al muro con `multiply`; sin tarjetas ni marcos.

## Colors

Un muro neutro casi gris, madera clara y una sola tinta oscura de chocolate; sin acentos saturados.

### Primary
- **Tinta chocolate** (tinta): el color de identidad. Texto principal, títulos, botón principal, canto de las repisas, contorno de foco, selección de texto y fondo del pie.
- **Chocolate hondo** (tinta-hondo): solo el estado hover del botón principal.

### Secondary
- **Roble** (roble): el cuerpo de las repisas (franja de 10–12px bajo cada fila de frascos) y el pulgar de la barra de desplazamiento.
- **Roble claro** (roble-claro): relleno que sube por la tira elegida (al 55 % de opacidad), las líneas finas y las etiquetas de redes en el pie.

### Neutral
- **Yeso** (yeso): fondo de página, del nav y de toda sección; texto sobre el pie chocolate.
- **Papel** (papel): las tiras de prueba, el botón de carrito y el texto del botón principal.
- **Tinta suave** (tinta-suave): texto secundario, precios, enlaces del nav en reposo, marca del perfume en el estante.
- **Pie suave** (pie-suave, #D7CABD): texto secundario sobre el pie chocolate.
- **Línea** (linea): chocolate al 16 % para bordes del nav, divisores entre secciones y entre renglones del catálogo, el botón de carrito y el borde en reposo de chips, buscador y desplegables.

### Named Rules
**The Chocolate Is Ink Rule.** El chocolate escribe; casi nunca pinta paredes. Solo dos superficies completas llevan fondo chocolate: la banda «100% originales» de la portada (aprobada por el dueño el 2026-11-08, porque es la prueba central del negocio) y el pie global. No agregues una tercera: el dueño pidió que el chocolate identifique sin dominar.

**The Rooms Rule.** Las secciones se separan por cambio de fondo a todo lo ancho, no por líneas de 1px: yeso para el muro y la conversación, papel para exhibir frascos (más vendidos, sala del catálogo, «¿Te convenció?» de la ficha), chocolate solo en originalidad. Dos salas seguidas nunca comparten fondo. Cada sala abre con su título centrado y una regla de roble de 64×3px debajo.

**The Neutral Plaster Rule.** El yeso es #E2E1DE a propósito. Un yeso más cálido (#E5E2DD, #E6E3DF) se lee como crema y el detector lo marca; no lo calientes.

**The No Cream, No Terracotta Rule.** Crema, arena, terracota y cobre pertenecen al sistema heredado y no entran en superficies nuevas.

## Typography

**Display Font:** Bodoni Moda variable (óptico 6–96, peso 400–900, autohospedada en `fonts/`), con Didot, Bodoni 72, Georgia, serif
**Body Font:** Hanken Grotesk variable (peso 100–900, autohospedada en `fonts/`), con Helvetica Neue, Arial, sans-serif

**Character:** Un Didone de contraste alto, de etiqueta de perfumería, para lo que se nombra y se mide; una grotesca neutra y clara para leer y operar en el celular. El contraste lo pone el trazo de Bodoni, no el peso: los títulos van en 400.

Por qué esta pareja: el dueño rechazó Archivo extendido porque «se siente como una marca de autos tipo Porsche, no de perfume»; no vuelvas a una sans geométrica extendida para la voz de display.

### Hierarchy
- **Display** (Bodoni Moda 500, clamp(3.5rem, 15vw, 6rem) en móvil y clamp(4.5rem, 8vw, 6rem) desde 861px, 0.92, -0.02em): el nombre «Saúco» en la portada; el sello «100% originales» a clamp(3rem, 14vw, 6rem) con interlínea 0.95. La marca del nav (22px) y del pie (40px) usa Bodoni 500 en mayúsculas con 0.06em.
- **Numeral** (Bodoni Moda 500 en reposo, 700 elegida; 40px en móvil, 64px desde 861px; -0.03em; cifras de forro): las medidas 3 · 5 · 10 en las tiras y los números de los pasos (44px/500). Las sumas sueltas también son cifra Bodoni con cifras tabulares: total del carrito 26px/500, precio de la ficha de completos 30px/500 y la medida del selector flotante 17px/500.
- **Headline** (Bodoni Moda 500, clamp(1.75rem, 7vw, 2.75rem), 1.05, -0.01em): títulos de sección. En los catálogos, el título de página va a clamp(2.125rem, 9vw, 3.25rem) con interlínea 1 y -0.015em; los títulos de sección de la lista («Nicho», «Diseñador»), el de cotización y el «Tu pedido» del carrito bajan a 24–26px/500, con el conteo a la derecha en Hanken 14px/400 tinta suave.
- **Nombre de ficha** (Bodoni Moda 500, clamp(2.1rem, 9.5vw, 3.75rem) en móvil y clamp(3.25rem, 5.2vw, 5rem) desde 861px, interlínea 1, -0.015em, `text-wrap: balance`): el nombre del perfume en su ficha, dentro del mismo `h1` que la casa. El «Sobre esta fragancia» de la ficha usa la voz headline a clamp(1.6rem, 6vw, 2.25rem) con interlínea 1.1.
- **Title** (Bodoni Moda 500, 22px, 1.2): subtítulos de rutas y el titular del estado sin resultados. Los títulos de paso (18px/600), el nombre del perfume en el estante (18px/500), en cada renglón del catálogo (17px/500, 19px desde 700px) y en el carrito (16px/500) van en Hanken.
- **Body large** (Hanken 400, 17px, 1.6, máx. 60ch): párrafos largos como el de originalidad; «Sobre esta fragancia» a 17px/1.65, 65ch.
- **Body** (Hanken 400, 15–16px, 1.5–1.55, máx. 36–46ch): lema secundario, descripciones, precios de renglón y botón, enlaces del nav. El lema de la portada sube a clamp(1.15rem, 4.8vw, 1.6rem)/1.25.
- **Label** (Hanken 600, 12–13px, 0.08–0.14em, mayúsculas): botón principal (15px/600, 0.1em), marca del perfume en estante, renglón y ficha, nombres de las tiras, desplegables del nav, nombres de redes en el pie.

### Named Rules
**The Bodoni Speaks Rule.** Bodoni Moda habla: el nombre «Saúco», los títulos, el nombre del perfume en su ficha y las cifras que son el producto o su suma (medidas, pasos, total, precio de ficha). Hanken Grotesk lee y opera: texto, etiquetas, botones, nav, campos, chips y todo precio dentro de un botón o renglón. Bodoni nunca va en peso menor a 500 ni por debajo de 17px, y siempre en su óptica de texto (`opsz` 16, fijada en `html` con `font-optical-sizing: none`): la óptica automática de tamaños grandes deja trazos finos ilegibles, y el dueño la rechazó por legibilidad. El logo usa óptica 11, peso 600; Hanken nunca compone un encabezado de sección, el nombre de la ficha ni la marca.

**The Number Is the Product Rule.** La medida se compone como cifra Bodoni grande (500 en reposo, 700 elegida), con la unidad (ml) pequeña debajo en Hanken 13–15px/500. Precios de renglón y botón, subtotales y lecturas de atomizaciones van en Hanken con cifras tabulares; el total del carrito y el precio de la ficha son cifra Bodoni tabular.

## Layout

Móvil primero (390px). El encabezado es fijo arriba en todo el sitio: fila del logo (88px en escritorio, 52px en móvil) y fila del menú (48px / 44px); el contenido lleva de margen superior el alto completo (`--enc-alto`), así que al compactarse no mueve la página. Contenedor máximo de 1240px, márgenes de 1.25rem en móvil y clamp(2rem, 4vw, 4rem) en escritorio.

La primera pantalla es una cuadrícula de tres zonas (texto, escena, acciones) que ocupa `100svh` menos el nav, con el botón principal visible sin desplazarse. En escritorio pasa a dos columnas (0.9fr / 1.1fr): texto y acciones a la izquierda, repisa y tiras a la derecha.

La portada es una sola columna centrada: el lema como `h1` en Bodoni, el texto de apoyo y, en escritorio, el botón principal arriba de la escena (repisa y tiras, 620px máx.); en móvil el botón queda al pie del primer viewport. Debajo, las salas a todo lo ancho (4.5rem arriba y abajo en móvil, 6rem en escritorio; contenido a 1240px máx. con el relleno lateral calculado para que el fondo llegue al borde): más vendidos en papel, «Dos formas de empezar» en yeso, «100% originales» en chocolate y «Cómo pedir» en yeso. Cada sala abre con su título centrado sobre la regla de roble y, si lo tiene, el enlace secundario centrado debajo. Los estantes de producto se desplazan en horizontal con snap en móvil y se reparten en fila en escritorio; rutas y pasos pasan a 2 y 3 columnas desde 640px.

Los catálogos tienen dos salas: la cabecera en yeso (título centrado con regla, nota, buscador y filtros; alineada a la izquierda en móvil) y una sala de papel a todo lo ancho con la vitrina y la lista (fondo extendido con `box-shadow` de 100vmax y `clip-path`, sin cambiar el marcado de la columna). Son una sola columna de lectura de 820px máx. (1.75rem arriba y 1.25rem a los lados en móvil; 3rem arriba y clamp(2rem, 4vw, 4rem) a los lados desde 861px). Orden fijo: título, nota opcional, buscador a ancho completo, chips, vitrina (solo decants y solo sin búsqueda) y luego secciones de lista separadas 2.5rem. Cada renglón es una rejilla de tres columnas (foto 72px · texto · acción) con 1rem de relleno vertical y divisor de 1px; desde 700px la foto pasa a 96px, todo se centra en vertical y precio y botón se ponen en fila. En móvil los chips se desplazan en horizontal en una sola línea, sin barra visible.

Las fichas son una rejilla con áreas nombradas, 1080px máx. En móvil: dos columnas (texto · repisa de 120px) con ruta arriba, título a la izquierda y repisa a la derecha alineados abajo, y debajo a ancho completo la compra, la tabla, la descripción y el enlace de regreso (1rem arriba, 1.25rem a los lados). Desde 861px: texto a la izquierda (minmax(0, 1fr)) y repisa a la derecha (minmax(300px, 0.85fr)) ocupando todas las filas, fija con `position: sticky` a 3rem del borde mientras se lee; separación clamp(2.5rem, 5vw, 5rem) y 3rem arriba.

Breakpoints observados: 640px (rejillas de rutas y pasos), 699/700px (renglones, vitrina y chips del catálogo), 860/861px (nav, portada y márgenes del catálogo).

## Elevation & Depth

La profundidad es física, no de interfaz: viene de los objetos del atelier. Las tiras de papel proyectan una sombra suave como grupo; la repisa principal arroja una sombra corta hacia abajo; el canto de chocolate (3px sólidos bajo la franja de roble) es el borde de la madera, no una sombra de tarjeta. Las superficies de interfaz (secciones, nav) son planas.

### Shadow Vocabulary
- **Sombra de papel** (`filter: drop-shadow(0 6px 8px rgba(59,35,24,0.18))`): el grupo de tiras.
- **Sombra de repisa** (`box-shadow: 0 14px 18px -12px rgba(59,35,24,0.45)`): bajo la repisa principal de la portada.
- **Sombra del carrito** (`box-shadow: 0 4px 14px -6px rgba(59,35,24,0.35)`): el botón flotante de carrito en escritorio; se quita en móvil, donde vive dentro de la barra.
- **Sombra del encabezado compacto** (`box-shadow: 0 12px 26px -20px rgba(59,35,24,0.55)`): solo cuando el encabezado se compacta al bajar.
- **Sombra del submenú** (`box-shadow: 0 14px 30px -12px rgba(59,35,24,0.4)`): los paneles de Decants y Perfumes completos.
- **Sombra del desplegable** (`box-shadow: 0 14px 30px -12px rgba(59,35,24,0.4)`): los paneles de filtros y orden de perfumes completos.

La repisa de la ficha lleva en escritorio el canto de 3px más una sombra de repisa corta (`0 16px 20px -12px rgba(59,35,24,0.4)`); en móvil solo el canto.

Las mini repisas de los renglones (6px de roble con canto de 2px) y la vitrina (10px con canto de 3px) repiten el canto chocolate como borde de madera, sin sombra de repisa.

### Named Rules
**The Objects Cast Shadows Rule.** Solo los objetos del atelier (papel, repisa) y las capas flotantes (carrito, menú abierto, desplegables) tienen sombra, siempre teñida de chocolate. Las secciones y los textos son planos.

## Shapes

Formas rectas y artesanales. Las tiras son rectángulos de papel con la punta cortada en V (`clip-path` a 90 % / 100 %) y giradas ±8° en abanico desde un eje bajo. Las repisas son franjas horizontales de roble de 10–12px con canto chocolate de 3px. El botón principal, los botones de contorno, el buscador, los campos y los desplegables tienen esquinas apenas suavizadas (2px); el botón de carrito y su contador son círculos, y los chips de filtro son las únicas píldoras. Las mini repisas de los renglones (6px de roble, canto de 2px) son la versión pequeña de la repisa. No hay tarjetas redondeadas ni contenedores con borde alrededor de las fotos.

## Components

### Buttons
- **Shape:** casi recto (2px).
- **Primary:** fondo tinta, texto papel, etiqueta en mayúsculas 15px/600 con 0.1em, altura mínima 56px, 0 1.75rem de relleno; ancho completo en móvil, ancho natural en escritorio.
- **Hover / Focus:** hover a chocolate hondo; activo baja 1px; foco con contorno tinta de 2px separado 3px.
- **Secondary:** enlace de texto tinta 15px/500 con subrayado de 1px separado 5px; en hover el subrayado sube a 2px.
- **Botón de contorno:** borde tinta de 1px, fondo transparente, texto tinta 15px/500 en ancho normal sin mayúsculas, 44px de alto y 0 1.1rem de relleno; en hover se llena de tinta con texto papel. Para las acciones de recuperación del estado sin resultados.
- **Agregar en renglón (completos):** el mismo contorno a 40px de alto, 0 1rem, 14px/600; dice «Agregar» o «Consultar» (WhatsApp, cuando no hay precio) y se llena de tinta en hover.
- **Botones de medida (decants):** tres botones de contorno tinta, 52px de alto, con la medida en 13px/600 arriba y el precio en 15px con cifras tabulares abajo («A confirmar» si falta). Un toque agrega esa medida al carrito sin selector; se llenan de tinta en hover y durante 0.9 s tras agregar. En celular ocupan el ancho bajo el texto en tres columnas iguales; desde 700px van a la derecha, 84px cada uno.
- **Enlace en línea:** un botón que se lee como texto dentro de un párrafo: hereda la fuente, tinta 500, subrayado de 1px separado 4px que sube a 2px en hover. Para acciones dentro de una nota («¿No está en la lista? Te lo cotizamos»).

### Chips
- **Style:** píldoras papel de 40px con borde en línea, texto tinta 15px/500 (14px y 0.8rem de relleno a 400px o menos); son enlaces de filtro por género o tipo.
- **State:** el activo se llena de tinta con texto papel y lleva `aria-current="page"`; en hover el borde pasa a tinta. Dentro del panel de completos, los chips de categoría y marca son la misma píldora a 36px y 14px.

### Inputs / Fields
- **Style:** buscador de ancho completo, 48px, fondo papel, borde en línea, 2px de radio, texto 16px y una lupa de trazo 1.6 en tinta suave a la izquierda; placeholder en tinta suave. Los campos del formulario de cotización usan la misma caja con la etiqueta encima en 13px/600 tinta.
- **Focus:** el borde pasa a tinta con un anillo interior de 1px tinta (`box-shadow: 0 0 0 1px`).

### Desplegables de completos
Botones de contorno papel de 40px (borde en línea, tinta en hover y abiertos) con flecha dibujada por dos trazos de 1.5px que gira al abrir; el contador de filtros es una píldora tinta de 22px. El panel es papel, borde en línea, 2px de radio, 1.1rem de relleno, sombra del desplegable y alto máximo min(70vh, 520px) con scroll. Las opciones de orden son de 44px y la activa va en 600 con un punto tinta de 6px.

### Renglón de catálogo
Un perfume por renglón, sin tarjeta. A la izquierda la foto sobre una mini repisa (72px; 96px desde 700px) fundida con `multiply`, hundida 4 % y que sube en hover; al centro la casa en etiqueta 12px/600 tinta suave, el nombre (enlace a la ficha, subrayado en hover) y una línea meta en 14px tinta suave: en decants género corto y las tres primeras notas; en completos concentración, tamaño, género y «Set de regalo», más «Incluye:» en los sets. En decants, debajo (a la derecha desde 700px) los tres botones de medida con su precio; en completos, a la derecha el precio en 15px/600 con cifras tabulares (o «Precio por consultar» en 14px/400) y el botón Agregar o Consultar. Las secciones abren con su título y conteo sobre un divisor en línea.

### Vitrina
Repisa de los más vendidos al inicio del catálogo de decants: hasta cuatro frascos (tres en móvil) sobre roble de 10px con canto chocolate de 3px, 96px de alto en móvil y 170px desde 700px, con la leyenda «Los más vendidos» debajo en 14px tinta suave. Respeta el género elegido y se oculta mientras hay búsqueda o si no hay destacados.

### Ficha técnica (fichas de producto)
La ficha es la tarjeta técnica del perfumista, sin tarjeta: todo sobre el yeso. Orden: ruta como enlaces en 14px tinta suave con subrayado en línea («Decants › Nicho», «Perfumes completos › Sets de regalo»); título; repisa; compra; tabla; «Sobre esta fragancia»; enlace secundario de regreso al catálogo.
- **Título casa + nombre en un solo `h1`:** la casa es un `span` dentro del `h1` (etiqueta 13px/600, 0.1em, mayúsculas, tinta suave) y el nombre otro `span` en la voz de nombre de ficha. La casa es parte del título, nunca una etiqueta suelta encima de un encabezado.
- **Repisa:** `figure` de 130px de alto y 120px de ancho en móvil (alto clamp(320px, 52vh, 460px) y fija en escritorio), franja de roble de 8px (12px en escritorio) con canto chocolate de 3px, foto con `multiply`, hundida 4 % y que sube en hover, con `escala` desde la base. Lleva `background: var(--yeso)` (ver Repisa y estante).
- **Compra en decants:** los tres botones de medida del catálogo (`.fila-medida`) en tres columnas iguales a ancho completo (420px máx. en escritorio), 60px de alto, medida 14px y precio 17px con cifras tabulares; un toque agrega.
- **Compra en completos:** fila con el precio en Bodoni Moda 30px/500 con cifras tabulares, y el botón principal «Agregar al carrito» (56px, se estira en móvil, ancho natural en escritorio).
- **Garantía:** una línea 14px tinta suave bajo la compra (original, envío; en completos, «de 7 a 10 días hábiles»).
- **Tabla:** `dl` con filo superior de 1px tinta y renglones `div > dt + dd` separados por línea: término en etiqueta 12px/600 tinta suave en una columna de 7.25rem, valor en 16px/1.45. Decants: género, salida, corazón, fondo, duración, ideal para; completos añade presentación, incluye (sets) y categoría. Solo datos reales; un renglón sin dato no se muestra.
- **Sobre esta fragancia:** `h2` headline y párrafos 17px/1.65, 65ch máx.

### Estado sin resultados
Abre con un divisor en línea; titular en Bodoni Moda 22px/500 («No encontramos «X»»), una línea de ayuda 16px tinta suave y una fila de botones de contorno. Solo ofrece una salida cuando esa salida da resultados: ver los resultados sin el filtro de género, ver la búsqueda en el otro catálogo (la búsqueda viaja con el cambio de vista), limpiar la búsqueda y cotizar el nombre buscado por WhatsApp.

### Tiras de prueba (Signature Component)
Selector de medida como tiras de papel secante. Tres botones `aria-pressed` (Muestra 3 ml, Viaje 5 ml, Mensual 10 ml), papel blanco, 68×180px en móvil y 112×292px en escritorio, cifra grande arriba, unidad debajo y nombre en vertical. Al cargar se abren en abanico (0.9s, ease-out `cubic-bezier(.16,1,.3,1)`). La elegida sube 16px, su cifra Bodoni pasa de 500 a 700 y se tiñe solo la punta (11 % inferior, roble claro al 70 %, como una tira mojada en perfume) sin tocar el texto; el dueño pidió que el relleno fuera sutil. Debajo, en una fila, la lectura en vivo de atomizaciones (con «· Santal 33 en 5 ml» desde 700px) y un botón de contorno «Agregar 5 ml · $554» (44px, 14px/600) que agrega el más vendido en la medida elegida; la elección nunca se pierde. Con `prefers-reduced-motion` todo queda fijo.

### Repisa y estante
Soporte de toda foto de producto. Fotos reales en `object-fit: contain` con `mix-blend-mode: multiply` para fundir el fondo blanco al yeso, apoyadas sobre una franja de roble con canto chocolate y hundidas un 3–4 % en la madera; en hover suben a la superficie. Cada foto puede ajustar su tamaño relativo con el campo opcional `escala` de `js/data.js`, aplicado como `scale: var(--escala, 1)` con `transform-origin: 50% 100%` para que el frasco crezca o se encoja desde la base y siga posado en la madera; vale para el estante, las rutas, la vitrina y la repisa de la ficha (los renglones no lo aplican).

**Fondo yeso detrás de `multiply`:** `multiply` mezcla con lo que está detrás dentro de su contexto de apilamiento. Un contenedor que crea uno propio (`position: sticky`, `isolation`, `transform`, `opacity`, `z-index` con posición, `filter`) y no tiene fondo deja que el blanco de la foto se vea como caja. Todo contenedor así detrás de una foto fundida lleva `background: var(--yeso)`; la repisa fija de la ficha es el caso de referencia.

Bajo el estante: marca en etiqueta, nombre 18px/500 y «Desde $X · 3 ml» en tinta suave.

### Enlace para saltar al contenido
Primer elemento de cada página: «Saltar al contenido», fuera de la vista hasta recibir foco con teclado; entonces aparece arriba a la izquierda en tinta con texto papel. Lleva el foco a `main#app` sin cambiar el hash (el sitio usa el hash para sus vistas). La portada y las fichas tienen una sola región `<main id="app">`; los resultados del catálogo se anuncian con un estado discreto («3 perfumes», «Sin resultados») en lugar de releer la lista completa.

### Navigation
Encabezado de casa de perfumes (`header.encabezado`, elegido por el dueño el 2026-11-08 en lugar de la columna lateral). Fijo arriba, fondo yeso.
- **Fila del logo:** «WhatsApp 56 1256 7245» a la izquierda (Hanken 14px, subrayado roble), el ramillete + «Saúco» al centro (56px de alto; 32px en móvil) y el botón de carrito flotante alineado a la derecha.
- **Fila del menú:** entre una línea de 1px arriba y una tinta abajo; etiquetas Hanken 13px/600, 0.12em, mayúsculas: Decants ▾, Perfumes completos ▾, 100% originales, Cómo pedir. La sección activa lleva una raya de roble de 3px abajo. Los desplegables abren un panel de papel con filo chocolate de 2px y sombra de submenú; se cierran al elegir, al tocar fuera o con Escape.
- **Compacto (`html.compacto`, al bajar más de 24px):** la fila del logo se pliega (altura y opacidad, ease-out 0.35s), aparece un logo chico de 28px a la izquierda del menú y el carrito se encoge a 40px dentro de la barra.
- **Móvil:** sin hamburguesa; el menú queda siempre visible con nombres cortos (Decants, Completos, Originales; «Cómo pedir» solo en escritorio). Los paneles caen a todo lo ancho. Compacto, queda solo la fila del menú, recorrida a la izquierda para dejar lugar al carrito.

### Originalidad: proceso y qué recibes
En la portada, `#originalidad` (con `scroll-margin` para el nav fijo; se llega con `/#originalidad`): el titular «100% originales», una entrada en 17px y una lista ordenada de tres pasos con la cifra en Bodoni 40px/500 (columna de 2.75rem en móvil; tres columnas desde 640px con la cifra arriba), título 18px/600 y texto 16px tinta suave. Debajo, un enlace a WhatsApp para pedir foto o video de la botella original, y el bloque «Qué recibes»: título Bodoni 24px y una lista `dl` con regla tinta arriba y renglones en línea, la medida en Bodoni 22px junto a su nombre de uso y la descripción de la presentación. Todo el contenido es dato del dueño (ver PRODUCT.md); no se agregan afirmaciones nuevas sin confirmarlas.

### Significado de las medidas
Las medidas siempre se explican por su uso: Muestra (3 ml, ≈60 atomizaciones), Viaje (5 ml, ≈90) y Mensual (10 ml, ≈180). En el catálogo, una leyenda de una línea en 14px bajo los chips con enlace a «Qué recibes»; en la ficha, cada botón de medida tiene una tercera línea en 12px («Viaje · ≈90») que se aclara a yeso en hover y al agregar, más una nota de presentación en 13px; en el carrito, una línea de originalidad encabeza el resumen de envío y pago.

### Panel del carrito
Diálogo lateral (`role="dialog"`, `aria-modal`) de yeso, 400px máx., que entra desde la derecha con ease-out; bloquea el scroll de la página, lleva el foco al botón de cerrar o al título del paso, lo atrapa dentro (incluye campos del formulario) y lo devuelve al cerrar. Tres pasos, renderizados por `js/carrito.js` en `#carrito-items` y `#carrito-pie`:
- **Tu carrito:** artículos (foto sobre mini repisa, marca en etiqueta, nombre 16px/500, medida y precio, cantidad −/+ de 40px con aviso al llegar a 99, subtotal, «Quitar» como texto), un resumen de envío y pago en 14px tinta suave con los datos reales del negocio, subtotal y el botón principal «Continuar con el envío». Vacío: mensaje y enlace «Explorar decants».
- **Datos de envío:** botón de regreso (chevrón de trazo) y título con el número de paso («Datos de envío · 2 de 3», en Hanken 14px tinta suave; los tres pasos lo muestran). Arriba, un resumen plegable en papel («2 artículos · $1,944») que despliega los productos. Dos grupos de opciones como tarjetas de papel con radio en tinta y borde doble al elegir («¿Dónde lo recibes?»: Monterrey o nacional con su costo estimado y tiempo; «¿Cómo prefieres pagar?»: transferencia o tarjeta) y el grupo «¿A quién y a dónde lo enviamos?»: nombre, teléfono, calle y número, colonia, ciudad o municipio (con ejemplo «Monterrey, San Pedro, Guadalupe»; al elegir entrega local solo se sugiere el estado), estado, código postal, referencias y «¿Para cuándo lo necesitas?» (fecha opcional, sin promesa: «te confirmamos si llega a tiempo»). Campos de 48px y 16px para evitar zoom en iOS, `autocomplete` correcto, validación al enviar con mensajes en #8A1F1F y foco al primer error. En móvil, mientras hay un campo con foco, el pie se compacta a «Total estimado» y el botón (clase `escribiendo` en el panel). Los datos se recuerdan en el navegador.
- **Último paso:** «Pedido #número» en Bodoni 30px y un aviso de que el pedido llega a Saúco hasta que se envía desde WhatsApp; resumen en `dl` con regla tinta (productos, total estimado, entrega, dirección, pago), «Lo que sigue» con el horario real (lunes a sábado, 9:00 a 20:00) y una despedida en Bodoni 20px. El pie tiene «Abrir WhatsApp para enviarlo» como botón principal y dos enlaces: «Volver a mi carrito» y «Hacer un pedido nuevo», que primero pide confirmación. El pedido se guarda en el navegador con la firma del carrito: si el carrito no cambia, al recargar o reenviar se muestra el mismo pedido con el mismo número (sin duplicados).
- **Envío en carritos mixtos:** el mínimo de envío gratis y el costo se calculan solo con el subtotal de decants; si hay perfumes completos, su envío aparece aparte como «Se confirma por WhatsApp» y el total dice «+ envío de completos».

### Selector de medida y aviso
Los botones de medida (catálogo y ficha) llevan un «+» dibujado de 9px en la esquina superior derecha (dos trazos de 1.5px en el color del texto, 75 % de opacidad) para leerse como «agregar»; la leyenda del catálogo empieza con «Toca una medida para agregarla al carrito.». El selector flotante de medida (usado solo como respaldo) es una lista de papel con opciones de 48px que recibe el foco al abrirse. Al agregar aparece un aviso tinta («Santal 33 · 5 ml agregado» + «Deshacer» subrayado + botón papel «Ver carrito»), anunciado por `role="status"`, que se retira a los 4 s; «Deshacer» quita la última pieza agregada y confirma «Se quitó del carrito». En móvil el aviso aparece arriba, bajo la barra del menú, para no tapar los botones del siguiente renglón; en escritorio, abajo al centro.

### Botón de carrito
Círculo papel de 44px (40px en móvil) con borde en línea y un ícono de bolsa en SVG de trazo 1.6. El contador es una píldora tinta con cifra papel 12px/600, oculta cuando está vacía.

### Pie
La única superficie chocolate. «SAÚCO» en Bodoni Moda 40px/400, mayúsculas, color yeso, sobre dos líneas finas de roble claro; datos en etiqueta, contacto en 15px yeso y redes como pares etiqueta de roble claro + usuario en yeso.

## Do's and Don'ts

### Do:
- **Do** separar secciones con salas a todo lo ancho (yeso, papel, y chocolate solo en originalidad y el pie), con título centrado sobre regla de roble.
- **Do** poner cada foto de producto sobre una repisa de roble con canto chocolate, fundida con `multiply`.
- **Do** componer el nombre, los títulos, las medidas y los totales en Bodoni Moda (400 o más), y todo lo que se lee u opera en Hanken Grotesk.
- **Do** teñir toda sombra con chocolate (rgba(59,35,24,…)) y limitarla a objetos y capas flotantes.
- **Do** mantener el botón principal visible sin desplazarse en el primer viewport del celular.
- **Do** dejar fijo todo movimiento con `prefers-reduced-motion`.
- **Do** poner la casa dentro del título (`h1` con casa y nombre como `span`) en lugar de una etiqueta encima.
- **Do** dar `background: var(--yeso)` a todo contenedor fijo o aislado que tenga detrás una foto con `multiply`.

### Don't:
- **Don't** usar el chocolate como fondo de sección fuera de la banda de originalidad y el pie.
- **Don't** volver a separar secciones con líneas de 1px ni a una columna lateral de navegación: el dueño sentía el sitio plano y sin divisiones.
- **Don't** calentar el yeso hacia crema (#E5E2DD, #E6E3DF se leen como crema).
- **Don't** usar crema, arena, terracota, cobre ni los puntos morado/verde del sistema heredado en superficies nuevas.
- **Don't** usar emoji como íconos; los íconos son SVG de trazo en tinta.
- **Don't** encerrar fotos de producto en tarjetas con borde o esquinas redondeadas.
- **Don't** introducir Cormorant Garamond ni Jost en superficies nuevas.
- **Don't** volver a una sans geométrica extendida (Archivo 112–125 % u otra) para el display: el dueño la rechazó por leerse como marca de autos, no de perfume.
- **Don't** poner una etiqueta suelta (kicker) encima de un encabezado; si la casa o la categoría importan, van dentro del título o en la ruta.

**Limpieza del sistema heredado (2026-11-08):** se retiraron las reglas sin uso del CSS anterior (tarjetas `.card*`, página de producto `.producto-*`, migas `.breadcrumb`, líneas del pie del logo viejo, cotización plegable) y los `@font-face` y archivos de Cormorant Garamond y Jost. Quedan solo restos con uso: la barra, desplegables y chips de completos y el formulario de cotizar, reestilados bajo `.catalogo`, que todavía leen algunos tokens heredados (`--chocolate`, `--arena`, `--terracota`) en su regla base; al tocarlos, muévelos a los tokens del sistema.

**Deuda de imágenes (no normativo):** cinco fotos de producto tienen fondo gris, no blanco, y con `multiply` se ven como cajas grises sobre el yeso en lugar de frascos posados: `imagenes/oud royal.webp`, `imagenes/black afgano.webp`, `imagenes/black phantom.webp`, `imagenes/ombre leather.webp` e `imagenes/autumn vibes.webp`. Necesitan reemplazo del dueño con fondo blanco o recortadas; no se corrigen con CSS ni justifican tarjetas o marcos.

**Logo: dos marcas con funciones distintas** (aprobadas por el dueño; el sello solo junto al nombre se veía repetitivo, «S» + «Saúco» en la misma letra). Todos los archivos en `imagenes/logo/` llevan las letras convertidas a trazos (no dependen de fuentes) y existen en tinta y en versión `-claro` (yeso, para fondo chocolate).
- **El ramillete + nombre (marca principal):** una flor de saúco (umbela) a línea, con nueve florecitas de cinco pétalos en cúpula sobre un tallo, junto a «Saúco» en Bodoni Moda óptica 11, peso 600. El logo usa la óptica de texto y no la de cartel porque el dueño pidió legibilidad en tamaños chicos: con óptica 72 los trazos finos desaparecían a 14–20px; no regreses a la versión de alto contraste en el logo (el título de la portada, que es grande, sí usa la Bodoni del sitio). La flor de saúco es una nota real de perfumería y el origen del nombre. Archivos: `sauco-flor-horizontal.svg` (menú: 56px de alto en escritorio, 36px en móvil), `sauco-flor-vertical.svg` / `-claro` (pie a 140px, imagen al compartir `og-sauco.png`, tarjetas y empaque), `sauco-flor.svg` (la flor sola).
- **El sello (monograma):** una «S» de Bodoni Moda (óptica 11, peso 600) en un óvalo de doble línea, como sello de casa de perfumes. Para avatar de redes (`sauco-avatar-chocolate.png`, `sauco-avatar-yeso.png`, 1080×1080), ícono del sitio (`favicon-32.png`, `apple-touch-icon.png`, `icon-512.png`, y `sauco-sello-simple.svg` de un solo anillo para 48px o menos), etiquetas de decants y sello de empaque (`sauco-sello.svg`). El sello nunca va pegado al nombre «Saúco» (eso repite la S); existen `sauco-horizontal.svg` / `sauco-vertical.svg` con sello + nombre solo para usos donde el ramillete no cabe y el nombre se necesita, y no se usan en el sitio.
- `sauco-nombre.svg` / `-claro`: solo la palabra.
Reglas: tinta sobre yeso o papel, o yeso sobre tinta; nunca otros colores, sombras ni deformación. La flor no se usa debajo de 24px (sus tallos desaparecen); ahí va el sello simple. El título de la portada sigue siendo texto en Bodoni, no imagen. El anterior `imagenes/Saúco_2.png` ya no se usa en el sitio.
