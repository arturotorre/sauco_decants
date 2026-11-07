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
typography:
  display:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(3.5rem, 15vw, 6rem)"
    fontWeight: 200
    lineHeight: 0.92
    letterSpacing: "-0.02em"
    fontVariation: "'wdth' 125"
  numeral:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "40px"
    fontWeight: 200
    lineHeight: 1
    letterSpacing: "-0.03em"
    fontVariation: "'wdth' 112"
    fontFeature: "'lnum'"
  headline:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(1.75rem, 7vw, 2.75rem)"
    fontWeight: 300
    lineHeight: 1.05
    letterSpacing: "-0.01em"
    fontVariation: "'wdth' 125"
  title:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "22px"
    fontWeight: 500
    lineHeight: 1.2
    fontVariation: "'wdth' 112"
  body-lg:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.6
  body:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
    fontSize: "13px"
    fontWeight: 600
    letterSpacing: "0.08em"
  button:
    fontFamily: "Archivo, Helvetica Neue, Arial, sans-serif"
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
---

# Design System: Saúco Decants

## Overview

**Creative North Star: "El atelier del perfumista"**

Saúco se presenta como el taller de un perfumista: un muro de yeso gris cálido y claro, repisas de roble claro con canto de chocolate, frascos reales fotografiados sobre ellas y tiras de papel secante blancas que llevan la medida (3 · 5 · 10) en cifras grandes. El chocolate de la marca es tinta, no pintura de pared: escribe, traza líneas y llena el botón principal, y solo cubre una superficie completa en el pie.

La voz tipográfica es una sola familia, Archivo, en dos anchos: extendida y delgada para el nombre, los títulos y las cifras; ancho normal para leer. La densidad es baja y la composición es de taller, no de tienda en cuadrícula: las fotos se posan sobre repisas, no dentro de tarjetas. El movimiento es breve y con ease-out; las tiras se abren en abanico una vez al cargar y la elegida se levanta.

Alcance actual: este mundo cubre la portada (vista-home de `index.html`), el nav global, el carrito completo (botón, panel, selector de medida y aviso al agregar) y el pie. El catálogo (`#catalogo`, `#completos`) y las fichas (`decants/*`, `completos/*`) siguen en el sistema heredado (ver la nota al final de Do's and Don'ts); es deuda de migración, no parte de este sistema.

**Key Characteristics:**
- Muro de yeso neutro (#E2E1DE) como único fondo de sección; nunca crema.
- Chocolate como tinta: texto, líneas, botón principal y pie.
- Archivo variable: ancho 125 % y peso 200–300 para nombre, títulos y cifras; ancho normal para texto.
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
- **Línea** (linea): chocolate al 16 % para bordes del nav, divisores entre secciones y el botón de carrito.

### Named Rules
**The Chocolate Is Ink Rule.** El chocolate escribe; no pinta paredes. Ninguna sección completa lleva fondo chocolate salvo el pie global.

**The Neutral Plaster Rule.** El yeso es #E2E1DE a propósito. Un yeso más cálido (#E5E2DD, #E6E3DF) se lee como crema y el detector lo marca; no lo calientes.

**The No Cream, No Terracotta Rule.** Crema, arena, terracota y cobre pertenecen al sistema heredado y no entran en superficies nuevas.

## Typography

**Display Font:** Archivo variable (ancho 62–125 %, peso 100–900, autohospedada en `fonts/`), con Helvetica Neue, Arial
**Body Font:** Archivo en ancho normal

**Character:** Una sola familia que cambia de voz con el ancho: extendida y delgada suena a rótulo de atelier y a cifra grabada; normal es clara y cercana para leer en el celular.

### Hierarchy
- **Display** (200, ancho 125 %, clamp(3.5rem, 15vw, 6rem), 0.92): el nombre «Saúco» en la portada y el sello «100% originales» (hasta 6rem).
- **Numeral** (200 en reposo, 500 elegida; ancho 112 % en móvil, 125 % y 64px en escritorio; cifras de forro): las medidas 3 · 5 · 10 en las tiras y los números de los pasos (44px).
- **Headline** (300, ancho 125 %, clamp(1.75rem, 7vw, 2.75rem), 1.05): títulos de sección.
- **Title** (500, ancho 112 %, 22px, 1.2): subtítulos de rutas; los títulos de paso usan 18px/600 en ancho normal.
- **Body large** (400, 17px, 1.6, máx. 60ch): párrafos largos como el de originalidad.
- **Body** (400, 15–16px, 1.5–1.55, máx. 36–46ch): lema secundario, descripciones, precios, enlaces del nav.
- **Label** (600, 12–13px, 0.08–0.14em, mayúsculas): botón principal, marca del perfume en el estante, nombres de las tiras, desplegables del nav, nombres de redes en el pie.

### Named Rules
**The Two Widths Rule.** El ancho extendido (112–125 %) y los pesos 200–300 son para el nombre, los títulos y las cifras; todo lo que se lee va en ancho normal y peso 400–600.

**The Number Is the Product Rule.** La medida se compone como cifra grande y delgada, con la unidad (ml) pequeña debajo. Precios y lecturas de atomizaciones usan cifras tabulares.

## Layout

Móvil primero (390px). El nav es una barra superior de 56px en móvil y una columna lateral fija de 200px desde 861px; el contenido se desplaza en consecuencia. Contenedor máximo de 1240px, márgenes de 1.25rem en móvil y clamp(2rem, 4vw, 4rem) en escritorio.

La primera pantalla es una cuadrícula de tres zonas (texto, escena, acciones) que ocupa `100svh` menos el nav, con el botón principal visible sin desplazarse. En escritorio pasa a dos columnas (0.9fr / 1.1fr): texto y acciones a la izquierda, repisa y tiras a la derecha.

Las secciones bajo la portada llevan 4.5rem arriba, se separan con una línea de 1px y abren con una cabecera que alinea el título y un enlace secundario en la misma línea base. Los estantes de producto se desplazan en horizontal con snap en móvil y se reparten en fila en escritorio; rutas y pasos pasan a 2 y 3 columnas desde 640px.

Breakpoints observados: 640px (rejillas de rutas y pasos), 860/861px (nav y portada).

## Elevation & Depth

La profundidad es física, no de interfaz: viene de los objetos del atelier. Las tiras de papel proyectan una sombra suave como grupo; la repisa principal arroja una sombra corta hacia abajo; el canto de chocolate (3px sólidos bajo la franja de roble) es el borde de la madera, no una sombra de tarjeta. Las superficies de interfaz (secciones, nav) son planas.

### Shadow Vocabulary
- **Sombra de papel** (`filter: drop-shadow(0 6px 8px rgba(59,35,24,0.18))`): el grupo de tiras.
- **Sombra de repisa** (`box-shadow: 0 14px 18px -12px rgba(59,35,24,0.45)`): bajo la repisa principal de la portada.
- **Sombra del carrito** (`box-shadow: 0 4px 14px -6px rgba(59,35,24,0.35)`): el botón flotante de carrito en escritorio; se quita en móvil, donde vive dentro de la barra.
- **Sombra del menú** (`box-shadow: 0 18px 30px -18px rgba(59,35,24,0.35)`): el menú desplegado en móvil.

### Named Rules
**The Objects Cast Shadows Rule.** Solo los objetos del atelier (papel, repisa) y las capas flotantes (carrito, menú abierto) tienen sombra, siempre teñida de chocolate. Las secciones y los textos son planos.

## Shapes

Formas rectas y artesanales. Las tiras son rectángulos de papel con la punta cortada en V (`clip-path` a 90 % / 100 %) y giradas ±8° en abanico desde un eje bajo. Las repisas son franjas horizontales de roble de 10–12px con canto chocolate de 3px. El botón principal tiene esquinas apenas suavizadas (2px); el botón de carrito y su contador son círculos. No hay tarjetas redondeadas ni contenedores con borde alrededor de las fotos.

## Components

### Buttons
- **Shape:** casi recto (2px).
- **Primary:** fondo tinta, texto papel, etiqueta en mayúsculas 15px/600 con 0.1em, altura mínima 56px, 0 1.75rem de relleno; ancho completo en móvil, ancho natural en escritorio.
- **Hover / Focus:** hover a chocolate hondo; activo baja 1px; foco con contorno tinta de 2px separado 3px.
- **Secondary:** enlace de texto tinta 15px/500 con subrayado de 1px separado 5px; en hover el subrayado sube a 2px.

### Tiras de prueba (Signature Component)
Selector de medida como tiras de papel secante. Tres botones `aria-pressed` (Muestra 3 ml, Viaje 5 ml, Mensual 10 ml), papel blanco, 68×180px en móvil y 112×292px en escritorio, cifra grande arriba, unidad debajo y nombre en vertical. Al cargar se abren en abanico (0.9s, ease-out `cubic-bezier(.16,1,.3,1)`). La elegida sube 16px, su cifra pasa de 200 a 500 y un relleno de roble claro sube desde abajo. Debajo, una lectura en vivo muestra atomizaciones y el precio real del perfume. Con `prefers-reduced-motion` todo queda fijo.

### Repisa y estante
Soporte de toda foto de producto. Fotos reales en `object-fit: contain` con `mix-blend-mode: multiply` para fundir el fondo blanco al yeso, apoyadas sobre una franja de roble con canto chocolate y hundidas un 3–4 % en la madera; en hover suben a la superficie. Cada foto puede ajustar su tamaño relativo con el campo opcional `escala` de `js/data.js` (variable `--escala`). Bajo el estante: marca en etiqueta, nombre 18px/500 y «Desde $X · 3 ml» en tinta suave.

### Navigation
- **Escritorio:** columna de yeso de 200px con borde derecho en línea; «SAÚCO» en Archivo ancho 125 %, 22px/300, mayúsculas; desplegables Decants y Perfumes completos como etiquetas 13px/600 con flecha de trazo; enlaces 15px en tinta suave, tinta en hover, activo subrayado y con borde izquierdo tinta.
- **Móvil:** barra de 56px (hamburguesa de tres trazos, marca, carrito); el menú cae como panel de yeso con sombra.

### Panel del carrito
Diálogo lateral (`role="dialog"`, `aria-modal`) de yeso, 400px máx., que entra desde la derecha con ease-out; al abrirse bloquea el scroll de la página, lleva el foco al botón de cerrar (aspa dibujada con dos trazos), lo atrapa dentro y lo devuelve al cerrar. Cada artículo: foto sobre una mini repisa de roble, marca en etiqueta, nombre 16px/500, medida y precio unitario, control de cantidad −/+ (botones de 40px sobre papel, − deshabilitado en 1) y subtotal; «Quitar» como enlace de texto. Pie: total con número de artículos y monto en Archivo 112 %, nota de precios por confirmar, botón principal «Enviar pedido por WhatsApp» (deshabilitado con el carrito vacío) y una línea que explica qué pasa al enviarlo. Vacío: mensaje y enlace «Explorar decants».

### Selector de medida y aviso
El selector flotante de medida es una lista de papel con opciones de 48px (medida en Archivo 112 %, precio en tinta suave); recibe el foco al abrirse y lo devuelve al botón de origen. Al agregar aparece un aviso tinta en la parte baja («Santal 33 · 5 ml agregado al carrito» + botón papel «Ver carrito»), anunciado por `role="status"`, que se retira solo a los 5 s.

### Botón de carrito
Círculo papel de 44px (40px en móvil) con borde en línea y un ícono de bolsa en SVG de trazo 1.6. El contador es una píldora tinta con cifra papel 12px/600, oculta cuando está vacía.

### Pie
La única superficie chocolate. «SAÚCO» en Archivo ancho 125 %, 40px/200, color yeso, sobre dos líneas finas de roble claro; datos en etiqueta, contacto en 15px yeso y redes como pares etiqueta de roble claro + usuario en yeso.

## Do's and Don'ts

### Do:
- **Do** usar yeso (#E2E1DE) como fondo de toda sección y reservar el fondo chocolate para el pie.
- **Do** poner cada foto de producto sobre una repisa de roble con canto chocolate, fundida con `multiply`.
- **Do** componer medidas y números con Archivo extendido y delgado, y el texto de lectura en ancho normal.
- **Do** teñir toda sombra con chocolate (rgba(59,35,24,…)) y limitarla a objetos y capas flotantes.
- **Do** mantener el botón principal visible sin desplazarse en el primer viewport del celular.
- **Do** dejar fijo todo movimiento con `prefers-reduced-motion`.

### Don't:
- **Don't** usar el chocolate como fondo de sección fuera del pie.
- **Don't** calentar el yeso hacia crema (#E5E2DD, #E6E3DF se leen como crema).
- **Don't** usar crema, arena, terracota, cobre ni los puntos morado/verde del sistema heredado en superficies nuevas.
- **Don't** usar emoji como íconos; los íconos son SVG de trazo en tinta.
- **Don't** encerrar fotos de producto en tarjetas con borde o esquinas redondeadas.
- **Don't** introducir Cormorant Garamond ni Jost en superficies nuevas.

**Sistema heredado (deuda de migración, no normativo):** el catálogo, completos y las fichas siguen en Cormorant Garamond + Jost con `--chocolate` #3D2314, `--terracota`, `--cobre`, `--arena`, `--crema` y `--fondo`, y puntos de nivel morado (#6B5B9E) y verde (#1D7A5A). Al migrar cada superficie, pásala a los tokens de arriba y retira los heredados.

**Pendiente:** el logo definitivo. Mientras tanto, «Saúco» se compone en Archivo extendido peso 200; no lo trates como logotipo final.
