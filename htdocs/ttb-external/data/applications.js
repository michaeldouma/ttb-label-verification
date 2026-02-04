/**
 * COLA Application Index (from fake TTB external API)
 *
 * Lightweight manifest of available applications for the agent view.
 * Only contains ttbId and classTypeCode (for category filtering).
 *
 * GENERATED FILE - Do not edit directly!
 * Edit applications.tsv and run: node generate_from_tsv.js
 *
 * Full application data is fetched from sharded paths:
 *   /ttb-external/data/applicant/{d1}/{d2}/{d3}/{d4}/{d5}/{d6}/{d7}/{d8}/{remainder}.json
 *
 * Example: TTB ID 24028001000106 ->
 *   /ttb-external/data/applicant/2/4/0/2/8/0/0/1/000106.json
 *
 * Categories by classTypeCode:
 *   Wine:             80-89
 *   Malt Beverages:   900-959
 *   Distilled Spirits: 100-799
 */

const COLA_APPLICATIONS = [
  { ttbId: "24028001000106", classTypeCode: "101" },  // IRON RIDGE DISTILLING STRAIGHT
  { ttbId: "24030001000213", classTypeCode: "906" },  // BREEZY WAVE MANGO HARD SELTZER
  { ttbId: "24017001000212", classTypeCode: "902" },  // BURNETT BREW WINTER ALE
  { ttbId: "24027001000310", classTypeCode: "80A" },  // LIGHTHOUSE CELLARS ROSÉ
  { ttbId: "24026001000309", classTypeCode: "80" },  // TTB IMPORTS NIAGARA PENINSULA 
  { ttbId: "24001001000101", classTypeCode: "439" },  // 12345 IMPORTS RUM WITH COCONUT
  { ttbId: "24002001000102", classTypeCode: "102" },  // A.B.C. SINGLE BARREL STRAIGHT 
  { ttbId: "24003001000103", classTypeCode: "439" },  // POLLY'S SPICE RUM
  { ttbId: "24004001000104", classTypeCode: "339" },  // SUNNYSIDE DISTILLERY APPLE VOD
  { ttbId: "24005001000105", classTypeCode: "200" },  // CHIMES DISTILLERY GIN
  { ttbId: "24031001000108", classTypeCode: "472" },  // COINTREAU L'UNIQUE LIQUEUR
  { ttbId: "24032001000109", classTypeCode: "331" },  // LUKSUSOWA TRIPLE DISTILLED POT
  { ttbId: "24033001000110", classTypeCode: "478" },  // RICARD PASTIS DE MARSEILLE
  { ttbId: "24034001000111", classTypeCode: "410" },  // CALVADOS MORIN SÉLECTION APPLE
  { ttbId: "24035001000112", classTypeCode: "200" },  // DROP OF THE CREATOR GIN
  { ttbId: "24006001000201", classTypeCode: "902" },  // EXAMPLE BREWING CO. INDIA PALE
  { ttbId: "24007001000202", classTypeCode: "901" },  // EXAMPLE BREWING CO. WHEAT BEER
  { ttbId: "24008001000203", classTypeCode: "901" },  // MALT & HOP BREWERY NENE'S BEER
  { ttbId: "24009001000204", classTypeCode: "902" },  // EXAMPLE BREWING CO. MILO'S ALE
  { ttbId: "24010001000205", classTypeCode: "902" },  // EXAMPLE BREWING CO. AXEL CREAM
  { ttbId: "24011001000206", classTypeCode: "902" },  // EXAMPLE BREWING CO. LIGHT CREA
  { ttbId: "24012001000207", classTypeCode: "902" },  // MALT & HOP BREWERY PALE ALE
  { ttbId: "24013001000208", classTypeCode: "902" },  // MALT & HOP BREWING CO. DARK AL
  { ttbId: "24014001000209", classTypeCode: "907" },  // EXAMPLE BREWING CO. NON-ALCOHO
  { ttbId: "24015001000210", classTypeCode: "902" },  // MALT & HOP BREWERY TIGER'S SPE
  { ttbId: "24016001000211", classTypeCode: "906" },  // TASTY COLLECTION WILD CHERRY
  { ttbId: "24029001000107", classTypeCode: "943" },  // CASA DORADO REPOSADO TEQUILA
  { ttbId: "24038001000214", classTypeCode: "901" },  // SCHÖFFERHOFER HEFEWEIZEN BIER 
  { ttbId: "24039001000215", classTypeCode: "902" },  // BODDINGTONS PUB ALE
  { ttbId: "24018001000301", classTypeCode: "80" },  // ABC WINES AMERICAN RED WINE
  { ttbId: "24020001000303", classTypeCode: "82" },  // BIG BLACK CAT MARGARITA
  { ttbId: "24021001000304", classTypeCode: "81" },  // WINE FOR A RAINY DAY ALBARINO
  { ttbId: "24022001000305", classTypeCode: "81" },  // CHIMES VINEYARD CHARDONNAY
  { ttbId: "24023001000306", classTypeCode: "80" },  // PAPAS WINERY TABLE WINE (50% M
  { ttbId: "24024001000307", classTypeCode: "81" },  // LOST WINES 
  { ttbId: "24025001000308", classTypeCode: "80" },  // SPARE YOU WINES OREGON RED WIN
  { ttbId: "24036001000313", classTypeCode: "81" },  // GATO NEGRO SAUVIGNON BLANC
  { ttbId: "24037001000314", classTypeCode: "84" },  // MARTINI & ROSSI EXTRA DRY VERM
];
