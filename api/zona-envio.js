'use strict';

const { aplicarCORS } = require('./_cors');
const { zonaDeEnvio } = require('./_zonas');

// Geocodifica del lado del servidor con la API key de Google (GOOGLE_MAPS_API_KEY,
// variable de entorno en Vercel — nunca llega al navegador). El endpoint REST
// es apto aquí porque la llamada es servidor-a-servidor (sin problema de CORS,
// a diferencia de llamarlo directo desde el navegador).
async function geocodificar(direccion) {
  const url = new URL('https://maps.googleapis.com/maps/api/geocode/json');
  url.searchParams.set('address', direccion);
  url.searchParams.set('region', 'mx');
  url.searchParams.set('components', 'country:MX');
  url.searchParams.set('key', process.env.GOOGLE_MAPS_API_KEY);

  const resp = await fetch(url);
  const datos = await resp.json().catch(() => ({}));
  if (!resp.ok || datos.status !== 'OK' || !datos.results || !datos.results[0]) {
    const err = new Error(`Geocodificación falló: ${datos.status || resp.status}`);
    err.geocodeStatus = datos.status;
    throw err;
  }
  return datos.results[0].geometry.location; // { lat, lng }
}

module.exports = async (req, res) => {
  if (aplicarCORS(req, res)) return;
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Método no permitido.' });
    return;
  }

  const { calle, colonia, ciudad, estado, cp } = req.body || {};
  if (![calle, colonia, ciudad, estado, cp].every(v => typeof v === 'string' && v.trim())) {
    res.status(400).json({ error: 'Dirección incompleta.' });
    return;
  }

  const direccion = `${calle}, ${colonia}, ${ciudad}, ${estado} ${cp}, México`;

  try {
    const { lat, lng } = await geocodificar(direccion);
    res.status(200).json({ zona: zonaDeEnvio(lat, lng) });
  } catch (e) {
    console.error('zona-envio:', e.message);
    res.status(502).json({ error: 'No se pudo geocodificar la dirección.' });
  }
};
