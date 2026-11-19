'use strict';

// El frontend vive en saucodecants.com (GitHub Pages) y llama a esta función
// en un dominio de Vercel aparte: hace falta CORS explícito.
function aplicarCORS(req, res) {
  const origen = process.env.SITE_ORIGIN || 'https://saucodecants.com';
  res.setHeader('Access-Control-Allow-Origin', origen);
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') {
    res.status(204).end();
    return true; // el llamador debe hacer return tras esto
  }
  return false;
}

module.exports = { aplicarCORS };
