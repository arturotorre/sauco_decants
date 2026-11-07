# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Saúco vende a un mercado de nivel económico medio-alto en México. Hay dos perfiles principales, con peso parecido:

- **Quien sale de viaje o a un evento.** Viaja por trabajo o va a una boda, cena o salida, y quiere llevar un perfume que lo haga resaltar sin cargar una botella completa. Su tarea: elegir rápido una fragancia adecuada en un formato práctico (5 ml "Viaje", 10 ml "Mensual").
- **Quien quiere probar el lujo.** Le atraen los perfumes caros de diseñador y de nicho (Le Labo, Kilian, Xerjoff, Francis Kurkdjian, Louis Vuitton) y quiere vivirlos sin pagar la botella completa. Su tarea: probar una fragancia de alto precio en 3–10 ml y, si le convence, pasar después a la botella.

Un tercer uso, secundario, es la compra de perfumes completos y sets de regalo por encargo.

## Product Purpose

Saúco Decants vende perfumes 100% originales en decants de 3 ml, 5 ml y 10 ml, y también en botella completa, con envíos a todo México desde Monterrey. Así, perfumes de lujo y de nicho están al alcance en la cantidad que cada persona realmente necesita: "El lujo que mereces, en tu medida preferida."

El éxito es que el visitante encuentre una fragancia que le interese, la agregue al carrito y mande su pedido por WhatsApp.

## Positioning

- **Originalidad garantizada.** Los decants se sacan de botellas originales. Es el argumento central del negocio y nunca debe diluirse ni ponerse en duda.
- **Selección curada.** Un catálogo elegido con criterio, que mezcla nicho y diseñador. No compite por tener el catálogo más grande.

Saúco no se posiciona por precio bajo. Ningún texto debe venderlo como "el más barato".

## Operating Context

- Los visitantes llegan sobre todo desde Instagram (@sauco.decants), TikTok (@saucodecants) y Facebook, y muchos desde el celular.
- El flujo de compra es: catálogo → página de producto → elegir tamaño → carrito → "Confirmar Pedido", que abre WhatsApp (+52 56 1256 7245) con el pedido ya escrito y un número de pedido. No hay pago en línea ni cuentas de usuario.
- Los perfumes completos no se tienen en existencia: se piden por encargo y la entrega tarda de 7 a 10 días hábiles. Si un perfume no está en el catálogo, se cotiza por WhatsApp.

## Capabilities and Constraints

- Sitio estático: HTML, CSS y JS sin framework (`index.html`, `css/`, `js/data.js`, `js/main.js`, `js/carrito.js`), servido con dominio propio en saucodecants.com (`CNAME`).
- Las páginas de producto son estáticas: `decants/<slug>/` y `completos/<slug>/`, generadas con `tools/generar_pagina_producto.py`. Hay un `sitemap.xml`.
- El catálogo de decants se filtra por Todos/Hombre/Mujer y tiene buscador. El de completos tiene filtros (Dama, Caballero, Sets de regalo; Nicho, Diseñador, Árabe; marca) y orden.
- Términos: "decant", "perfume completo", "atomizaciones" (3 ml ≈ 60, 5 ml ≈ 90, 10 ml ≈ 180), "Dama/Caballero" en completos y "Hombre/Mujer" en decants.
- Idioma: español de México (`lang="es"`, `es_MX`).
- No hay backend ni base de datos. El carrito vive en el navegador.

## Brand Commitments

- Nombre: **Saúco** / Saúco Decants, con acento.
- Lema: "El lujo que mereces, en tu medida preferida."
- Las promesas "100% originales" y "Envíos a todo México desde Monterrey" se mantienen.
- Tono: lujo accesible, cercano y en español, con trato de "tú".
- Color de identidad: **café/chocolate**. Identifica a Saúco y debe estar presente, pero no puede dominar la página porque el dueño lo considera demasiado oscuro para un sitio web. La paleta se arma alrededor de él para que combine.

## Evidence on Hand

- Existen y se pueden pedir al dueño: **reseñas reales de clientes**, **fotos propias** de decants, empaques y botellas, y **números del negocio** (pedidos, clientes, tiempo operando). Ninguno está en el repositorio todavía. No se debe publicar ninguna reseña, cifra ni foto "propia" hasta que el dueño la entregue.
- Ya están en el repo: fichas de producto con descripciones y notas olfativas (`decants/*/index.html`, `completos/*/index.html`), imágenes de producto en `imagenes/` y el logo `imagenes/Saúco_2.png`.

## Product Principles

1. **La originalidad es lo primero.** Todo lo que toque la confianza (origen de las botellas, pruebas, mensajes) refuerza que el producto es auténtico.
2. **Lujo en la medida justa.** El valor está en vivir un perfume caro sin pagar la botella entera. Cada tamaño se explica por cómo se usa (muestra, viaje, mes).
3. **Curaduría antes que volumen.** Es mejor una selección con criterio y bien presentada que un catálogo interminable.
4. **De descubrir a WhatsApp, sin fricción.** El camino hasta mandar el pedido debe ser corto y claro, sobre todo en el celular.
5. **Pruebas reales o ninguna.** La prueba social solo se muestra con material verdadero que entregue el dueño.
