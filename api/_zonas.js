'use strict';

// Zonas de cobertura de la paquetería local (Líder Express) para la entrega
// en Monterrey, tomadas del mapa real que comparte el dueño en Google My Maps:
// https://www.google.com/maps/d/edit?mid=1cjcadUQEPbJDTVBzB_qSSK7nUvQ8qnI
//
// Los polígonos de abajo son una copia estática de ese mapa (export KML:
// /maps/d/kml?mid=1cjcadUQEPbJDTVBzB_qSSK7nUvQ8qnI&forcekml=1), en pares
// [longitud, latitud] como maneja KML. No se vuelve a pedir ese mapa en cada
// llamada — es un dato que cambia muy de vez en cuando. Si la paquetería
// actualiza su cobertura, hay que volver a descargar ese KML y regenerar los
// arreglos de aquí abajo (cada Placemark del KML trae su <name> —
// "COBERTURA REGULAR" o "COBERTURA EXTENDIDA" — y sus coordenadas en
// <outerBoundaryIs>/<innerBoundaryIs>).
//
// Esta es la única copia de esta geometría en el repo: antes vivía también
// en js/zonas-envio.js para resolverse en el navegador, pero se movió aquí
// para que la API key de geocodificación nunca llegue al cliente (ver
// zona-envio.js en este mismo folder).
//
// ZONA_REGULAR: dos polígonos — el área principal (con un hueco interior de
// 4 puntos, una zona chica excluida dentro de la cobertura) y un segundo
// polígono separado, más al oriente. ZONA_EXTENDIDA: un polígono al norte.

const ZONA_REGULAR = [
  { outer: [[-100.256406,25.617091],[-100.257273,25.631406],[-100.25899,25.64781],[-100.248862,25.658023],[-100.232726,25.651679],[-100.213328,25.63899],[-100.20114,25.631716],[-100.188609,25.615928],[-100.182258,25.598745],[-100.162173,25.595649],[-100.125352,25.600448],[-100.124579,25.603699],[-100.11531,25.603622],[-100.107156,25.617631],[-100.093466,25.641388],[-100.090161,25.640344],[-100.089389,25.640924],[-100.078746,25.659493],[-100.069476,25.653768],[-100.072394,25.686878],[-100.084067,25.692601],[-100.090075,25.701573],[-100.083724,25.710544],[-100.090075,25.716267],[-100.108615,25.723226],[-100.116511,25.720133],[-100.130931,25.733123],[-100.128613,25.748741],[-100.116425,25.743947],[-100.107585,25.749436],[-100.093852,25.74271],[-100.09102,25.750828],[-100.106812,25.762655],[-100.128957,25.749746],[-100.125695,25.77054],[-100.154277,25.768839],[-100.165692,25.783138],[-100.144406,25.789784],[-100.153075,25.807249],[-100.17273,25.804776],[-100.188008,25.796044],[-100.19333,25.812426],[-100.203801,25.807944],[-100.206719,25.811035],[-100.209809,25.824788],[-100.225602,25.833595],[-100.241567,25.830814],[-100.254956,25.831123],[-100.269032,25.829578],[-100.326882,25.821079],[-100.391427,25.811189],[-100.400697,25.809335],[-100.405503,25.80609],[-100.421983,25.79728],[-100.431939,25.786152],[-100.449277,25.779351],[-100.493737,25.762346],[-100.475026,25.752451],[-100.44344,25.750905],[-100.413571,25.731268],[-100.383187,25.706523],[-100.381299,25.684248],[-100.393143,25.681618],[-100.419236,25.694613],[-100.461465,25.711008],[-100.518285,25.712709],[-100.514336,25.696933],[-100.515195,25.682237],[-100.478459,25.668467],[-100.44859,25.652375],[-100.434342,25.649126],[-100.416146,25.649126],[-100.396748,25.636591],[-100.388423,25.623477],[-100.371085,25.611713],[-100.331946,25.624096],[-100.32611,25.63524],[-100.317698,25.634621],[-100.310489,25.627037],[-100.305682,25.614964],[-100.283709,25.610165],[-100.269118,25.591124],[-100.286971,25.582299],[-100.285426,25.571615],[-100.278216,25.559381],[-100.264827,25.562788],[-100.253669,25.572699],[-100.242511,25.557678],[-100.214015,25.526236],[-100.221225,25.519575],[-100.213328,25.515857],[-100.190669,25.524223],[-100.234099,25.588647],[-100.256406,25.617091]], holes: [[[-100.256587,25.617321],[-100.255557,25.60308],[-100.256406,25.617091],[-100.256587,25.617321]]] },
  { outer: [[-100.11531,25.603622],[-100.006848,25.551665],[-99.964619,25.576133],[-99.967023,25.600595],[-99.981099,25.60462],[-99.998265,25.606478],[-100.007192,25.607716],[-100.041867,25.638672],[-100.069476,25.653768],[-100.078746,25.659493],[-100.089389,25.640924],[-100.093466,25.641388],[-100.11531,25.603622]], holes: [] }
];

const ZONA_EXTENDIDA = [
  { outer: [[-100.449416,25.80296],[-100.444266,25.795735],[-100.427487,25.79191],[-100.423066,25.796662],[-100.406115,25.806399],[-100.400697,25.809335],[-100.390665,25.81146],[-100.339381,25.819225],[-100.282175,25.828921],[-100.254956,25.831123],[-100.223123,25.878972],[-100.217373,25.888548],[-100.209562,25.882834],[-100.196516,25.891636],[-100.193426,25.871636],[-100.180981,25.859047],[-100.221235,25.877428],[-100.252477,25.83232],[-100.226385,25.836028],[-100.213339,25.833865],[-100.198919,25.814087],[-100.191709,25.815323],[-100.187589,25.798942],[-100.170767,25.809142],[-100.154974,25.810378],[-100.145361,25.804506],[-100.139181,25.79276],[-100.100385,25.801105],[-100.097639,25.793378],[-100.031034,25.769573],[-100.004598,25.785341],[-100.133344,25.848079],[-100.121672,25.85086],[-100.090944,25.895806],[-100.124762,25.909395],[-100.15669,25.928848],[-100.143988,25.962344],[-100.136434,25.985338],[-100.161669,25.991202],[-100.191023,25.961264],[-100.224325,25.940426],[-100.28269,25.919276],[-100.289213,25.873258],[-100.325605,25.873721],[-100.40045,25.87125],[-100.409719,25.854567],[-100.424654,25.856884],[-100.432379,25.844989],[-100.432894,25.813005],[-100.449416,25.80296]], holes: [] }
];

// Point-in-polygon por ray-casting (regla par-impar), con soporte de huecos:
// un punto está dentro de un polígono si cae dentro de su anillo exterior y
// fuera de todos sus huecos.
function puntoEnAnillo(lng, lat, anillo) {
  let dentro = false;
  for (let i = 0, j = anillo.length - 1; i < anillo.length; j = i++) {
    const [xi, yi] = anillo[i];
    const [xj, yj] = anillo[j];
    const cruza = (yi > lat) !== (yj > lat) && lng < (xj - xi) * (lat - yi) / (yj - yi) + xi;
    if (cruza) dentro = !dentro;
  }
  return dentro;
}

function puntoEnPoligono(lng, lat, poligono) {
  if (!puntoEnAnillo(lng, lat, poligono.outer)) return false;
  return !poligono.holes.some(hueco => puntoEnAnillo(lng, lat, hueco));
}

function puntoEnConjunto(lng, lat, poligonos) {
  return poligonos.some(p => puntoEnPoligono(lng, lat, p));
}

// Devuelve 'regular' | 'extendida' | null (fuera de toda cobertura conocida
// por el mapa — ninguna de las dos zonas definidas).
function zonaDeEnvio(lat, lng) {
  if (puntoEnConjunto(lng, lat, ZONA_REGULAR)) return 'regular';
  if (puntoEnConjunto(lng, lat, ZONA_EXTENDIDA)) return 'extendida';
  return null;
}

module.exports = { zonaDeEnvio };
