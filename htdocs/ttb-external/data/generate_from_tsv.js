#!/usr/bin/env node
/**
 * Generate fake TTB COLA API data from applications.tsv
 *
 * Usage:
 *   cd htdocs/ttb-external/data
 *   node generate_from_tsv.js
 *
 * This reads applications.tsv (the source of truth) and generates:
 *   - applications.js (lightweight index for agent-view filtering)
 *   - applicant/{sharded-path}/{remainder}.json (full application data)
 *   - ../query/received/{date}/applications.json (date-based query endpoint for batch processor)
 *
 * Sharding scheme:
 *   TTB ID 24028001000106 becomes:
 *   applicant/2/4/0/2/8/0/0/1/000106.json
 *
 *   First 8 digits become 8 directory levels, remainder is filename.
 *   This scales to millions of records without filesystem issues.
 *
 * This simulates the external TTB COLA API that we'd authenticate with
 * and pull data from in production.
 */

const fs = require('fs');
const path = require('path');

const dataDir = __dirname;
const tsvPath = path.join(dataDir, '..', '..', '..', 'data', 'applications.tsv');
const applicantDir = path.join(dataDir, 'applicant');
const queryDir = path.join(dataDir, '..', 'query');

/**
 * Convert TTB ID to sharded path components
 * @param {string} ttbId - 14-character TTB ID like "24028001000106"
 * @returns {{ dirPath: string, filename: string }}
 */
function ttbIdToShardedPath(ttbId) {
  // First 8 characters become directory levels
  const prefix = ttbId.substring(0, 8);
  const remainder = ttbId.substring(8);

  // Split prefix into individual characters for directory path
  const dirParts = prefix.split('');
  const dirPath = dirParts.join(path.sep);

  return {
    dirPath,           // e.g., "2/4/0/2/8/0/0/1"
    filename: remainder + '.json'  // e.g., "000106.json"
  };
}

/**
 * Get the full filesystem path for an applicant JSON file
 */
function getApplicantPath(ttbId) {
  const { dirPath, filename } = ttbIdToShardedPath(ttbId);
  return path.join(applicantDir, dirPath, filename);
}

/**
 * Get the URL path (for documentation/comments)
 */
function getApplicantUrlPath(ttbId) {
  const { dirPath, filename } = ttbIdToShardedPath(ttbId);
  return `applicant/${dirPath.replace(/\\/g, '/')}/${filename}`;
}

// Read and parse TSV
const tsvContent = fs.readFileSync(tsvPath, 'utf8');
const lines = tsvContent.trim().split('\n');
const headers = lines[0].split('\t');

console.log(`Reading ${lines.length - 1} applications from TSV...`);

const applications = [];

for (let i = 1; i < lines.length; i++) {
  const values = lines[i].split('\t');
  const app = {};

  headers.forEach((header, idx) => {
    let val = values[idx] || '';
    // Unescape newlines
    val = val.replace(/\\n/g, '\n');
    app[header] = val;
  });

  applications.push(app);
}

// Category helper for sorting/grouping
function categoryForCode(code) {
  const n = parseInt(code, 10);
  if (isNaN(n)) return 'spirits';
  if (n >= 80 && n <= 89) return 'wine';
  if (n >= 900 && n <= 959) return 'malt';
  return 'spirits';
}

// Define featured applications (show first in their categories)
const featuredIds = [
  '24028001000106',  // Iron Ridge bourbon
  '24030001000213',  // Breezy Wave seltzer
  '24017001000212',  // Burnett Brews Winter Ale
  '24027001000310',  // Lighthouse Cellars rosé
  '24026001000309',  // TTB Imports Niagara red
];

// Sort: featured first, then by category, then by ttbId
applications.sort((a, b) => {
  const aFeatured = featuredIds.indexOf(a.ttbId);
  const bFeatured = featuredIds.indexOf(b.ttbId);

  // Featured apps come first (in their specified order)
  if (aFeatured !== -1 && bFeatured === -1) return -1;
  if (aFeatured === -1 && bFeatured !== -1) return 1;
  if (aFeatured !== -1 && bFeatured !== -1) return aFeatured - bFeatured;

  // Then sort by category
  const catOrder = { spirits: 0, malt: 1, wine: 2 };
  const aCat = catOrder[categoryForCode(a.classTypeCode)] || 0;
  const bCat = catOrder[categoryForCode(b.classTypeCode)] || 0;
  if (aCat !== bCat) return aCat - bCat;

  // Then by ttbId
  return a.ttbId.localeCompare(b.ttbId);
});

// Generate applications.js (index only)
const indexEntries = applications.map(app => {
  const comment = `${app.brandName} ${app.fancifulName}`.substring(0, 30);
  return `  { ttbId: "${app.ttbId}", classTypeCode: "${app.classTypeCode}" },  // ${comment}`;
});

const applicationsJs = `/**
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
${indexEntries.join('\n')}
];
`;

fs.writeFileSync(path.join(dataDir, 'applications.js'), applicationsJs);
console.log(`Generated applications.js with ${applications.length} entries`);

// Generate individual JSON files in sharded directories
let created = 0;
applications.forEach(app => {
  // Build the full application object
  const fullApp = {
    ttbId: app.ttbId,
    status: 'PENDING REVIEW',
    vendorCode: app.vendorCode,
    serialNumber: app.serialNumber,
    appType: app.appType,
    classTypeCode: app.classTypeCode,
    classTypeDesc: app.classTypeDesc,
    originCode: app.originCode,
    originDesc: app.originDesc,
    brandName: app.brandName,
    dbaName: app.dbaName,
    fancifulName: app.fancifulName,
    alcoholContent: app.alcoholContent,
    netContents: app.netContents,
    plantRegistry: app.plantRegistry,
    permitNumber: app.permitNumber,
    applicantName: app.applicantName,
    applicantAddress: app.applicantAddress,
    dateReceived: app.dateReceived,
    qualifications: app.qualifications,
    labelImages: {
      front: app.labelImageFront || null,
      back: app.labelImageBack || null
    }
  };

  // Add wine-specific fields if present
  if (app.wineVintage) fullApp.wineVintage = app.wineVintage;
  if (app.grapeVarietal) fullApp.grapeVarietal = app.grapeVarietal;
  if (app.wineAppellation) fullApp.wineAppellation = app.wineAppellation;

  // Add spirits-specific fields if present
  if (app.ageStatement) fullApp.ageStatement = app.ageStatement;

  // Create sharded directory structure
  const jsonPath = getApplicantPath(app.ttbId);
  const jsonDir = path.dirname(jsonPath);

  fs.mkdirSync(jsonDir, { recursive: true });
  fs.writeFileSync(jsonPath, JSON.stringify(fullApp, null, 2));
  created++;
});

console.log(`Generated ${created} JSON files in sharded applicant/ structure`);

// Generate date-based index for batch processor queries
// Groups applications by dateReceived (MM/DD/YYYY -> YYYY-MM-DD)
const byDate = {};
applications.forEach(app => {
  if (!app.dateReceived) return;
  // Convert MM/DD/YYYY to YYYY-MM-DD
  const parts = app.dateReceived.split('/');
  if (parts.length !== 3) return;
  const isoDate = `${parts[2]}-${parts[0].padStart(2, '0')}-${parts[1].padStart(2, '0')}`;
  if (!byDate[isoDate]) byDate[isoDate] = [];
  byDate[isoDate].push(app.ttbId);
});

// Write date query files: /query/received/{date}/applications.json
const dates = Object.keys(byDate).sort();
dates.forEach(date => {
  const dateDir = path.join(queryDir, 'received', date);
  fs.mkdirSync(dateDir, { recursive: true });
  const indexFile = path.join(dateDir, 'applications.json');
  fs.writeFileSync(indexFile, JSON.stringify({
    date,
    count: byDate[date].length,
    applications: byDate[date]
  }, null, 2));
});

console.log(`Generated ${dates.length} date query endpoints in query/received/`);

console.log('');
console.log('Example paths:');
applications.slice(0, 3).forEach(app => {
  console.log(`  ${app.ttbId} -> ${getApplicantUrlPath(app.ttbId)}`);
});
console.log('');
console.log('Query endpoints:');
dates.slice(0, 3).forEach(date => {
  console.log(`  /query/received/${date}/applications.json (${byDate[date].length} apps)`);
});
console.log('');
console.log('Done!');
