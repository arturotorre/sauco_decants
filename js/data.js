// Fuente única de verdad del catálogo. Para agregar/editar un perfume,
// agrega o modifica un objeto aquí — el resto del sitio se genera solo.
//
// genero: "Masculino" | "Femenino" | "Unisex"
// tier:   "nicho" | "disenador"
// precios: deja "" en un valor si el decant aún no tiene precio (se verá vacío en la tarjeta)
// bestseller: true marca los perfumes que aparecen en el carrusel "Los más vendidos"

const PERFUMES = [
  // ---- NICHO ----
  {
    casa: "Xerjoff",
    nombre: "Erba Pura EDP",
    genero: "Unisex",
    tier: "nicho",
    imagen: "imagenes/erba pura.webp",
    alt: "Erba Pura",
    notas: ["Naranja siciliana", "Bergamota", "Limón", "Vainilla", "Ámbar", "Almizcle blanco"],
    precios: { "3ml": "$360", "5ml": "$575", "10ml": "$1,093" },
    bestseller: false
  },
  {
    casa: "Le Labo",
    nombre: "Santal 33 EDP",
    genero: "Unisex",
    tier: "nicho",
    imagen: "imagenes/santal 33.webp",
    alt: "Santal 33",
    notas: ["Cardamomo", "Iris", "Violeta", "Sándalo", "Cuero", "Almizcle", "Cedro"],
    precios: { "3ml": "$390", "5ml": "$620", "10ml": "$1,159" },
    bestseller: true
  },
  {
    casa: "Francis Kurkdjian",
    nombre: "Baccarat Rouge 540 EDP",
    genero: "Unisex",
    tier: "nicho",
    imagen: "imagenes/baccarat rouge 540.webp",
    alt: "Baccarat Rouge 540",
    notas: ["Azafrán", "Jazmín", "Cedro ambarado", "Eritroxileno", "Almizcle"],
    precios: { "3ml": "$490", "5ml": "$790", "10ml": "$1,390" },
    bestseller: false
  },
  {
    casa: "Maison Margiela",
    nombre: "Replica By the Fireplace EDT",
    genero: "Unisex",
    tier: "nicho",
    imagen: "imagenes/replica by the fireplace.webp",
    alt: "By the Fireplace",
    notas: ["Clavo", "Pimienta rosa", "Castaña", "Madera de guayaco", "Vainilla"],
    precios: { "3ml": "$140", "5ml": "$200", "10ml": "$360" },
    bestseller: false
  },

  // ---- DISEÑADOR ----
  {
    casa: "Louis Vuitton",
    nombre: "Imagination EDP",
    genero: "Masculino",
    tier: "disenador",
    imagen: "imagenes/imagination.webp",
    alt: "Imagination",
    notas: ["Ambroxan", "Té negro", "Cedro", "Vainilla", "Iris"],
    precios: { "3ml": "$330", "5ml": "$530", "10ml": "$991" },
    bestseller: false
  },
  {
    casa: "Louis Vuitton",
    nombre: "L'Immensité EDP",
    genero: "Masculino",
    tier: "disenador",
    imagen: "imagenes/limmensité.webp",
    alt: "L'Immensité",
    notas: ["Jengibre", "Cardamomo", "Madera de haya", "Ambroxan", "Almizcle"],
    precios: { "3ml": "$330", "5ml": "$530", "10ml": "$991" },
    bestseller: false
  },
  {
    casa: "Dior",
    nombre: "Sauvage EDT",
    genero: "Masculino",
    tier: "disenador",
    imagen: "imagenes/sauvage.webp",
    alt: "Sauvage",
    notas: ["Bergamota", "Pimienta", "Lavanda", "Ambroxan", "Cedro", "Patchouli"],
    precios: { "3ml": "$140", "5ml": "$240", "10ml": "$440" },
    bestseller: false
  },
  {
    casa: "Chanel",
    nombre: "Bleu de Chanel EDP",
    genero: "Masculino",
    tier: "disenador",
    imagen: "imagenes/bleu de chanel.webp",
    alt: "Bleu de Chanel",
    notas: ["Limón", "Menta", "Jengibre", "Jazmín", "Incienso", "Sándalo", "Cedro"],
    precios: { "3ml": "$245", "5ml": "$390", "10ml": "$680" },
    bestseller: false
  },
  {
    casa: "YSL",
    nombre: "Libre EDP",
    genero: "Femenino",
    tier: "disenador",
    imagen: "imagenes/libre.webp",
    alt: "Libre",
    notas: ["Lavanda", "Mandarina", "Vainilla", "Almizcle blanco", "Cedro"],
    precios: { "3ml": "$220", "5ml": "$360", "10ml": "$595" },
    bestseller: false
  },
  {
    casa: "Valentino",
    nombre: "Uomo Born in Roma Intense EDP",
    genero: "Masculino",
    tier: "disenador",
    imagen: "imagenes/born in roma intense.webp",
    alt: "Born in Roma Intense",
    notas: ["Vainilla bourbon", "Lavanda", "Vetiver", "Madera ambarada"],
    precios: { "3ml": "$220", "5ml": "$335", "10ml": "$590" },
    bestseller: true
  },
  {
    casa: "Chanel",
    nombre: "Chance Eau Tendre EDP",
    genero: "Femenino",
    tier: "disenador",
    imagen: "imagenes/chance eau tendre.webp",
    alt: "Chance Eau Tendre",
    notas: ["Pomelo", "Jacinto", "Jazmín", "Almizcle blanco", "Cedro"],
    precios: { "3ml": "$245", "5ml": "$390", "10ml": "$680" },
    bestseller: true
  },
  {
    casa: "Prada",
    nombre: "Paradoxe Intense EDP",
    genero: "Femenino",
    tier: "disenador",
    imagen: "imagenes/paradoxe.webp",
    alt: "Paradoxe",
    notas: ["Neroli", "Flor de azahar", "Almizcle blanco", "Sándalo", "Ámbar"],
    precios: { "3ml": "$290", "5ml": "$390", "10ml": "$700" },
    bestseller: true
  },
  {
    casa: "Valentino",
    nombre: "Donna Born in Roma Intense EDP",
    genero: "Femenino",
    tier: "disenador",
    imagen: "imagenes/born in roma intense donna.webp",
    alt: "Donna Born in Roma Intense",
    notas: ["Bergamota", "Jazmín sambac", "Iris blanco", "Vainilla bourbon", "Almizcle"],
    precios: { "3ml": "$220", "5ml": "$335", "10ml": "$590" },
    bestseller: true
  },
  {
    casa: "YSL",
    nombre: "Y EDP",
    genero: "Masculino",
    tier: "disenador",
    imagen: "imagenes/y edp.webp",
    alt: "Y EDP",
    notas: ["Manzana", "Jengibre", "Bergamota", "Salvia", "Haba tonka", "Cedro"],
    precios: { "3ml": "$160", "5ml": "$240", "10ml": "$430" },
    bestseller: false
  },
  {
    casa: "Armani",
    nombre: "Acqua di Gio Profondo EDP",
    genero: "Masculino",
    tier: "disenador",
    imagen: "imagenes/acqua di gio profondo.webp",
    alt: "Acqua di Gio",
    notas: ["Bergamota", "Menta acuática", "Lavanda marina", "Patchouli", "Almizcle"],
    precios: { "3ml": "$190", "5ml": "$295", "10ml": "$550" },
    bestseller: false
  },
  {
    casa: "Lancôme",
    nombre: "La Vie Est Belle EDP",
    genero: "Femenino",
    tier: "disenador",
    imagen: "imagenes/la vie est belle.webp",
    alt: "La Vie Est Belle",
    notas: ["Iris", "Jazmín", "Praline", "Vainilla", "Patchouli", "Gourmand"],
    precios: { "3ml": "$165", "5ml": "$260", "10ml": "$470" },
    bestseller: false
  },
  {
    casa: "Paco Rabanne",
    nombre: "1 Million EDT",
    genero: "Masculino",
    tier: "disenador",
    imagen: "imagenes/1 million.webp",
    alt: "1 Million",
    notas: ["Menta", "Pomelo", "Rosa", "Canela", "Cuero", "Ámbar", "Patchouli"],
    precios: { "3ml": "$145", "5ml": "$195", "10ml": "$375" },
    bestseller: false
  },
  {
    casa: "Paco Rabanne",
    nombre: "Olympéa EDP",
    genero: "Femenino",
    tier: "disenador",
    imagen: "imagenes/olympea.webp",
    alt: "Olympéa",
    notas: ["Flor de té verde", "Sal marina", "Pimienta blanca", "Vainilla", "Cachemir"],
    precios: { "3ml": "$145", "5ml": "$195", "10ml": "$375" },
    bestseller: false
  }
];
