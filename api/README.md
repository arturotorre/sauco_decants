# sauco-zona-envio-api

Una sola función serverless: resuelve si una dirección de Monterrey cae en
zona regular o extendida de la paquetería local (Líder Express), para que la
API key de Google Maps nunca llegue al navegador — ver `js/carrito.js`
(`resolverZonaLocal()`), que le hace `fetch` a esta función en vez de cargar
el SDK de Google Maps directo en el sitio.

## Por qué existe este backend

Geocodificar directo desde el navegador requiere una API key visible en el
código fuente. Restringirla por HTTP referrer (`saucodecants.com`) ayuda,
pero no es un secreto real: cualquiera puede copiar la key y mandarle
peticiones a Google con un header `Referer` falso (no pasan por el
navegador, así que el referrer no se puede verificar de verdad), generando
cargos a la cuenta de Google Cloud del dueño. Esta función resuelve eso
manteniendo la key solo en el servidor, como variable de entorno.

## Desplegar

1. En Vercel: **Add New → Project**, importar este mismo repo de GitHub.
2. Dejar el *Root Directory* en blanco (la raíz del repo) — Vercel detecta
   automáticamente los archivos bajo `api/` como funciones.
3. Copiar las variables de `.env.example` a Settings → Environment Variables
   con los valores reales.
4. Deploy. Vercel da una URL tipo `https://sauco-zona-envio-xxxx.vercel.app`
   — pégala en la constante `ZONA_API_BASE` de `js/carrito.js`.

## Probar

```bash
curl -X POST https://<tu-url>.vercel.app/api/zona-envio \
  -H "Content-Type: application/json" \
  -d '{"calle":"Av. Constitución 400","colonia":"Centro","ciudad":"Monterrey","estado":"Nuevo León","cp":"64000"}'
# Debe responder algo como: {"zona":"regular"}
```

## Nota sobre el mapa de cobertura

Los polígonos en `_zonas.js` son una copia estática del mapa real del dueño
en Google My Maps. Si la paquetería actualiza su cobertura, hay que volver a
descargar el KML (`/maps/d/kml?mid=<id-del-mapa>&forcekml=1`) y regenerar los
arreglos de coordenadas ahí — ver el comentario al inicio de ese archivo.
