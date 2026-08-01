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

  // ---- DISEÑADOR ----
  {
    casa: "Maison Margiela",
    nombre: "Replica By the Fireplace EDT",
    genero: "Unisex",
    tier: "disenador",
    imagen: "imagenes/replica by the fireplace.webp",
    alt: "By the Fireplace",
    notas: ["Clavo", "Pimienta rosa", "Castaña", "Madera de guayaco", "Vainilla"],
    precios: { "3ml": "$140", "5ml": "$200", "10ml": "$360" },
    bestseller: false
  },
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

// Perfumes de línea completa (no decants): sin precio ni tamaños, se cotizan
// por WhatsApp. Fotos pendientes de agregar en imagenes/completos/<archivo>.
const PERFUMES_COMPLETOS = [
  // ---- CABALLERO ----
  { casa: "Paco Rabanne", nombre: "Invictus", concentracion: "EDT", genero: "Caballero", imagen: "imagenes/completos/invictus.webp", alt: "Invictus", precio: "$1,950" },
  { casa: "Azzaro", nombre: "The Most Wanted", concentracion: "EDT", genero: "Caballero", imagen: "imagenes/completos/the_most_wanted.webp", alt: "The Most Wanted", precio: "$1,630" },
  { casa: "Dolce & Gabbana", nombre: "King", concentracion: "EDP", genero: "Caballero", imagen: "imagenes/completos/king.webp", alt: "King", precio: "$1,940" },
  { casa: "Dior", nombre: "Sauvage", concentracion: "Parfum", genero: "Caballero", imagen: "imagenes/completos/sauvage_parfum.webp", alt: "Sauvage Parfum", precio: "$3,950" },
  { casa: "Valentino", nombre: "Uomo Born In Roma Intense", concentracion: "EDP", genero: "Caballero", imagen: "imagenes/completos/uomo_born_in_roma_intense.webp", alt: "Uomo Born In Roma Intense", precio: "$3,450" },
  { casa: "Valentino", nombre: "Uomo Born In Roma Yellow Dream", concentracion: "EDT", genero: "Caballero", imagen: "imagenes/completos/uomo_born_in_roma_yellow_dream.webp", alt: "Uomo Born In Roma Yellow Dream", precio: "$2,649" },
  { casa: "Valentino", nombre: "Uomo Born In Roma Green Stravaganza", concentracion: "EDT", genero: "Caballero", imagen: "imagenes/completos/uomo_born_in_roma_green_stravaganza.webp", alt: "Uomo Born In Roma Green Stravaganza", precio: "$2,800" },
  { casa: "Jean Paul Gaultier", nombre: "Le Male Elixir", concentracion: "Parfum", genero: "Caballero", imagen: "imagenes/completos/le_male_elixir.webp", alt: "Le Male Elixir", precio: "$2,422" },
  { casa: "Dior", nombre: "Sauvage", concentracion: "EDP", genero: "Caballero", imagen: "imagenes/completos/sauvage_edp.webp", alt: "Sauvage EDP", precio: "$3,494" },
  { casa: "Lacoste", nombre: "Blanc", concentracion: "EDT", genero: "Caballero", imagen: "imagenes/completos/blanc.webp", alt: "Blanc", precio: "$1,890" },
  { casa: "Versace", nombre: "Pour Homme Dylan Blue", concentracion: "EDT", genero: "Caballero", imagen: "imagenes/completos/dylan_blue.webp", alt: "Pour Homme Dylan Blue", precio: "$1,990" },
  { casa: "Paco Rabanne", nombre: "One Million Parfum", concentracion: "EDP", genero: "Caballero", imagen: "imagenes/completos/one_million_parfum.webp", alt: "One Million Parfum", precio: "$2,580" },
  { casa: "Paco Rabanne", nombre: "One Million", concentracion: "EDT", genero: "Caballero", imagen: "imagenes/completos/one_million_edt.webp", alt: "One Million", precio: "$2,100" },
  { casa: "Montblanc", nombre: "Explorer", concentracion: "EDP", genero: "Caballero", imagen: "imagenes/completos/explorer.webp", alt: "Explorer", precio: "$1,950" },
  { casa: "Jean Paul Gaultier", nombre: "Le Beau Le Parfum", concentracion: "EDP", genero: "Caballero", imagen: "imagenes/completos/le_beau_le_parfum.webp", alt: "Le Beau Le Parfum", precio: "$2,699" },
  { casa: "Jean Paul Gaultier", nombre: "Le Beau", concentracion: "EDT", genero: "Caballero", imagen: "imagenes/completos/le_beau_edt.webp", alt: "Le Beau", precio: "$2,299" },
  { casa: "Jean Paul Gaultier", nombre: "Le Male", concentracion: "EDT", genero: "Caballero", imagen: "imagenes/completos/le_male_edt.webp", alt: "Le Male", precio: "$2,199" },
  { casa: "YSL", nombre: "Y Intense", concentracion: "EDP", genero: "Caballero", imagen: "imagenes/completos/y_intense.webp", alt: "Y Intense", precio: "$2,990" },
  { casa: "Versace", nombre: "Eros", concentracion: "EDT", genero: "Caballero", imagen: "imagenes/completos/eros_edt.webp", alt: "Eros EDT", precio: "$1,999" },
  { casa: "Carolina Herrera", nombre: "Bad Boy Elixir", concentracion: "EDP", genero: "Caballero", imagen: "imagenes/completos/bad_boy_elixir.webp", alt: "Bad Boy Elixir", precio: "$2,690" },
  { casa: "Carolina Herrera", nombre: "Bad Boy Cobalt Elixir", concentracion: "EDP", genero: "Caballero", imagen: "imagenes/completos/bad_boy_cobalt_elixir.webp", alt: "Bad Boy Cobalt Elixir", precio: "$2,690" },
  { casa: "Carolina Herrera", nombre: "Bad Boy Cobalt", concentracion: "EDP", genero: "Caballero", imagen: "imagenes/completos/bad_boy_cobalt.webp", alt: "Bad Boy Cobalt", precio: "$2,290" },
  { casa: "Versace", nombre: "Eros", concentracion: "EDP", genero: "Caballero", imagen: "imagenes/completos/eros_edp.webp", alt: "Eros EDP", precio: "$2,490" },
  { casa: "Guerlain", nombre: "Vetiver", concentracion: "EDT", genero: "Caballero", imagen: "imagenes/completos/vetiver.webp", alt: "Vetiver", precio: "$2,150" },
  { casa: "Jean Paul Gaultier", nombre: "Le Beau Paradise Garden", concentracion: "EDP", genero: "Caballero", imagen: "imagenes/completos/le_beau_paradise_garden.webp", alt: "Le Beau Paradise Garden", precio: "$2,699" },
  { casa: "Paco Rabanne", nombre: "Invictus Parfum", concentracion: "EDP", genero: "Caballero", imagen: "imagenes/completos/invictus_parfum.webp", alt: "Invictus Parfum", precio: "$2,549" },
  { casa: "Paco Rabanne", nombre: "Invictus Victory", concentracion: "EDP", genero: "Caballero", imagen: "imagenes/completos/invictus_victory.webp", alt: "Invictus Victory", precio: "$2,560" },

  // ---- DAMA ----
  { casa: "Dior", nombre: "Miss Dior Originale", concentracion: "EDT", genero: "Dama", imagen: "imagenes/completos/miss_dior_originale.webp", alt: "Miss Dior Originale", precio: "$2,750" },
  { casa: "Dolce & Gabbana", nombre: "Queen", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/queen.webp", alt: "Queen", precio: "$2,450" },
  { casa: "Dolce & Gabbana", nombre: "Light Blue Capri In Love", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/light_blue_capri_in_love.webp", alt: "Light Blue Capri In Love", precio: "$2,550" },
  { casa: "YSL", nombre: "Libre L'Eau Nue Parfum de Peau", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/libre_leau_nue_parfum_de_peau.webp", alt: "Libre L'Eau Nue Parfum de Peau", precio: "$2,549" },
  { casa: "Burberry", nombre: "My Burberry Blush", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/my_burberry_blush.webp", alt: "My Burberry Blush", precio: "$2,450" },
  { casa: "Prada", nombre: "Paradoxe Virtual Flower", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/paradoxe_virtual_flower.webp", alt: "Paradoxe Virtual Flower", precio: "$2,995" },
  { casa: "Prada", nombre: "Paradoxe Intense", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/paradoxe_intense.webp", alt: "Paradoxe Intense", precio: "$2,950" },
  { casa: "Dior", nombre: "J'adore Parfum d'Eau", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/jadore_parfum_deau.webp", alt: "J'adore Parfum d'Eau", precio: "$3,300" },
  { casa: "Adolfo Domínguez", nombre: "Jazmín Tonka", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/jazmin_tonka.webp", alt: "Jazmín Tonka", precio: "$1,500" },
  { casa: "Salvatore Ferragamo", nombre: "Signorina Unica", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/signorina_unica.webp", alt: "Signorina Unica", precio: "$2,100" },
  { casa: "Salvatore Ferragamo", nombre: "Signorina Libera", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/signorina_libera.webp", alt: "Signorina Libera", precio: "$2,050" },
  { casa: "Carolina Herrera", nombre: "Very Good Girl Elixir", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/very_good_girl_elixir.webp", alt: "Very Good Girl Elixir", precio: "$2,990" },
  { casa: "Carolina Herrera", nombre: "Good Girl Blush Elixir", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/good_girl_blush_elixir.webp", alt: "Good Girl Blush Elixir", precio: "$2,990" },
  { casa: "Carolina Herrera", nombre: "Very Good Girl", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/very_good_girl.webp", alt: "Very Good Girl", precio: "$2,920" },
  { casa: "Carolina Herrera", nombre: "Good Girl", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/good_girl.webp", alt: "Good Girl", precio: "$2,850" },
  { casa: "Valentino", nombre: "Donna Born In Roma Yellow Dream", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/donna_born_in_roma_yellow_dream.webp", alt: "Donna Born In Roma Yellow Dream", precio: "$2,950" },
  { casa: "Lancôme", nombre: "La Vie Est Belle", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/la_vie_est_belle.webp", alt: "La Vie Est Belle", precio: "$2,850" },
  { casa: "Lancôme", nombre: "La Vie Est Belle Iris Absolu", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/la_vie_est_belle_iris_absolu.webp", alt: "La Vie Est Belle Iris Absolu", precio: "$2,850" },
  { casa: "Paco Rabanne", nombre: "Olympéa", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/olympea.webp", alt: "Olympéa", precio: "$2,500" },
  { casa: "Paco Rabanne", nombre: "Lady Million", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/lady_million.webp", alt: "Lady Million", precio: "$2,500" },
  { casa: "Paco Rabanne", nombre: "Olympéa Parfum", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/olympea_parfum.webp", alt: "Olympéa Parfum", precio: "$2,700" },
  { casa: "Tom Ford", nombre: "Black Orchid", concentracion: "EDP", genero: "Unisex", imagen: "imagenes/completos/black_orchid.webp", alt: "Black Orchid", precio: "$3,200" },
  { casa: "Tom Ford", nombre: "Velvet Orchid", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/velvet_orchid.webp", alt: "Velvet Orchid", precio: "$3,200" },
  { casa: "YSL", nombre: "Libre", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/libre.webp", alt: "Libre", precio: "$2,950" },
  { casa: "Coach", nombre: "Coach New York", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/coach_new_york.webp", alt: "Coach New York", precio: "$1,760" },
  { casa: "DKNY", nombre: "Be Delicious", concentracion: "EDP", genero: "Dama", imagen: "imagenes/completos/be_delicious.webp", alt: "Be Delicious", precio: "$1,500" },

  // ---- NICHO (sin precio fijo — disponibilidad sujeta a proveedor) ----
  { casa: "Xerjoff", nombre: "Erba Pura", concentracion: "EDP", genero: "Unisex", imagen: "imagenes/completos/erba_pura.webp", alt: "Erba Pura", precio: null },
  { casa: "Xerjoff", nombre: "Naxos", concentracion: "EDP", genero: "Unisex", imagen: "imagenes/completos/naxos.webp", alt: "Naxos", precio: null },
  { casa: "Xerjoff", nombre: "Torino 21", concentracion: "EDP", genero: "Unisex", imagen: "imagenes/completos/torino_21.webp", alt: "Torino 21", precio: null },
  { casa: "Parfums De Marly", nombre: "Althair", concentracion: "EDP", genero: "Unisex", imagen: "imagenes/completos/althair.webp", alt: "Althair", precio: null },
  { casa: "Parfums De Marly", nombre: "Greenley", concentracion: "EDP", genero: "Unisex", imagen: "imagenes/completos/greenley.webp", alt: "Greenley", precio: null },
  { casa: "Parfums De Marly", nombre: "Percival", concentracion: "EDP", genero: "Unisex", imagen: "imagenes/completos/percival.webp", alt: "Percival", precio: null },
  { casa: "Parfums De Marly", nombre: "Layton", concentracion: "EDP", genero: "Unisex", imagen: "imagenes/completos/layton.webp", alt: "Layton", precio: null },
  { casa: "Parfums De Marly", nombre: "Castley", concentracion: "EDP", genero: "Unisex", imagen: "imagenes/completos/castley.webp", alt: "Castley", precio: null },
  { casa: "Mancera", nombre: "Instant Crush", concentracion: "EDP", genero: "Unisex", imagen: "imagenes/completos/instant_crush.webp", alt: "Instant Crush", precio: null },
  { casa: "Mancera", nombre: "Cedrat Boisé", concentracion: "EDP", genero: "Unisex", imagen: "imagenes/completos/cedrat_boise.webp", alt: "Cedrat Boisé", precio: null },
  { casa: "Francis Kurkdjian", nombre: "Baccarat Rouge 540", concentracion: "EDP", genero: "Unisex", imagen: "imagenes/completos/baccarat_rouge_540.webp", alt: "Baccarat Rouge 540", precio: null },
  { casa: "Le Labo", nombre: "Santal 33", concentracion: "EDP", genero: "Unisex", imagen: "imagenes/completos/santal_33.webp", alt: "Santal 33", precio: null },
  { casa: "Le Labo", nombre: "Thé Noir 29", concentracion: "EDP", genero: "Unisex", imagen: "imagenes/completos/the_noir_29.webp", alt: "Thé Noir 29", precio: null },

  // ---- SETS DE REGALO ----
  { casa: "Paco Rabanne", nombre: "Lady Million Estuche 2 Piezas", concentracion: "EDP", genero: "Dama", esSet: true, contenido: ["EDP 80ml", "Loción corporal 100ml"], imagen: "imagenes/completos/lady_million_estuche.webp", alt: "Lady Million Estuche 2 Piezas", precio: "$2,800" },
  { casa: "Paco Rabanne", nombre: "Olympéa Estuche 2 Piezas", concentracion: "EDP", genero: "Dama", esSet: true, contenido: ["EDP 80ml", "Loción corporal 100ml"], imagen: "imagenes/completos/olympea_estuche.webp", alt: "Olympéa Estuche 2 Piezas", precio: "$2,700" },
  { casa: "Paco Rabanne", nombre: "Million Gold For Her Estuche 3 Piezas", concentracion: "EDP", genero: "Dama", esSet: true, contenido: ["EDP 90ml", "Loción corporal 100ml", "Miniatura 5ml"], imagen: "imagenes/completos/million_gold_for_her_estuche.webp", alt: "Million Gold For Her Estuche 3 Piezas", precio: "$2,800" },
  { casa: "Jean Paul Gaultier", nombre: "Divine Estuche 3 Piezas", concentracion: "EDP", genero: "Dama", esSet: true, contenido: ["EDP 100ml", "Loción corporal 75ml", "Miniatura 10ml"], imagen: "imagenes/completos/divine_estuche.webp", alt: "Divine Estuche 3 Piezas", precio: "$2,850" },
  { casa: "Carolina Herrera", nombre: "Very Good Girl Elixir Estuche 3 Piezas", concentracion: "EDP", genero: "Dama", esSet: true, contenido: ["EDP 80ml", "Loción corporal 100ml", "Miniatura 10ml"], imagen: "imagenes/completos/very_good_girl_elixir_estuche.webp", alt: "Very Good Girl Elixir Estuche 3 Piezas", precio: "$3,250" },
  { casa: "Carolina Herrera", nombre: "Very Good Girl Estuche 3 Piezas", concentracion: "EDP", genero: "Dama", esSet: true, contenido: ["EDP 80ml", "Loción corporal 100ml", "Miniatura 10ml"], imagen: "imagenes/completos/very_good_girl_estuche.webp", alt: "Very Good Girl Estuche 3 Piezas", precio: "$3,250" },
  { casa: "Carolina Herrera", nombre: "Good Girl Estuche 3 Piezas", concentracion: "EDP", genero: "Dama", esSet: true, contenido: ["EDP 80ml", "Loción corporal 100ml", "Miniatura 10ml"], imagen: "imagenes/completos/good_girl_estuche.webp", alt: "Good Girl Estuche 3 Piezas", precio: "$3,150" },
  { casa: "Jean Paul Gaultier", nombre: "Le Beau Estuche 2 Piezas", concentracion: "EDT", genero: "Caballero", esSet: true, contenido: ["EDT 125ml", "Miniatura 10ml"], imagen: "imagenes/completos/le_beau_estuche.webp", alt: "Le Beau Estuche 2 Piezas", precio: "$2,499" },
  { casa: "Paco Rabanne", nombre: "One Million Estuche 3 Piezas", concentracion: "EDT", genero: "Caballero", esSet: true, contenido: ["EDT 100ml", "Desodorante 150ml", "Miniatura 10ml"], imagen: "imagenes/completos/one_million_estuche.webp", alt: "One Million Estuche 3 Piezas", precio: "$2,350" },
  { casa: "Paco Rabanne", nombre: "Invictus Victory Estuche 2 Piezas", concentracion: "EDP", genero: "Caballero", esSet: true, contenido: ["EDP 100ml", "Shampoo 100ml"], imagen: "imagenes/completos/invictus_victory_estuche.webp", alt: "Invictus Victory Estuche 2 Piezas", precio: "$2,750" },
  { casa: "Jean Paul Gaultier", nombre: "Le Male Estuche 3 Piezas", concentracion: "EDT", genero: "Caballero", esSet: true, contenido: ["EDT 125ml", "Desodorante 150ml", "Gel de baño 75ml"], imagen: "imagenes/completos/le_male_estuche.webp", alt: "Le Male Estuche 3 Piezas", precio: "$2,450" },
  { casa: "Paco Rabanne", nombre: "Invictus Estuche 3 Piezas", concentracion: "EDT", genero: "Caballero", esSet: true, contenido: ["EDT 100ml", "Desodorante 150ml", "Miniatura 10ml"], imagen: "imagenes/completos/invictus_estuche.webp", alt: "Invictus Estuche 3 Piezas", precio: "$2,250" },
  { casa: "Carolina Herrera", nombre: "Bad Boy Cobalt Estuche 3 Piezas", concentracion: "EDP", genero: "Caballero", esSet: true, contenido: ["EDP 100ml", "Gel de baño 100ml", "Miniatura 10ml"], imagen: "imagenes/completos/bad_boy_cobalt_estuche.webp", alt: "Bad Boy Cobalt Estuche 3 Piezas", precio: "$2,550" },
  { casa: "Carolina Herrera", nombre: "Bad Boy Estuche 3 Piezas", concentracion: "EDT", genero: "Caballero", esSet: true, contenido: ["EDT 100ml", "Gel de baño 100ml", "Miniatura 10ml"], imagen: "imagenes/completos/bad_boy_estuche.webp", alt: "Bad Boy Estuche 3 Piezas", precio: "$2,450" }
];
