# COLA Data Directory

This directory contains application data for the TTB Label Verification demo.
Uses a filesystem-based API pattern that scales to production volumes.


## TTB COLA Volume Context

The sharded directory structure is designed for real-world TTB scale:

| Metric | Value |
|--------|-------|
| Annual volume | ~150,000-180,000 applications per year |
| Weekly additions | ~3,000+ new records |
| Historical total | Estimated 3-5 million COLAs (records since 1996) |
| Peak year data | 160,000 records from 2018 alone |

The craft beverage boom has driven exponential growth. Wine is the largest
volume, distilled spirits is fastest growing. COVID-19 caused a temporary
dip in FY 2020, with submissions rebounding to pre-pandemic levels by FY 2021.

*Source: TTB Public COLA Registry, OIG audit reports*


## Directory Sharding Scheme

To handle millions of records without filesystem performance issues:

```
TTB ID:     24028001000106
Path:       applicant/2/4/0/2/8/0/0/1/000106.json
```

First 8 digits become 8 directory levels. Remaining 6 digits are the filename.

**Benefits:**
- No directory exceeds reasonable file counts
- S3/cloud storage: fast prefix-based retrieval
- CDN-friendly: immutable paths, long cache TTLs
- Git-friendly: changes are localized (for demo purposes)
- Natural sharding for parallel batch processing

The same scheme applies to all three API endpoints:
- `applicant/2/4/0/2/8/0/0/1/000106.json` (form data)
- `verification/results/2/4/0/2/8/0/0/1/000106.json` (AI extraction results)
- `extractions/2/4/0/2/8/0/0/1/000106.json` (cropped images)


## Source of Truth

```
/data/applications.tsv
```

Tab-separated values file containing all application data.
Edit this file to add/modify applications.
Located at workspace root, not in this directory.

**Columns:**
- `ttbId`, `vendorCode`, `serialNumber`, `appType`
- `classTypeCode`, `classTypeDesc`
- `originCode`, `originDesc`
- `brandName`, `dbaName`, `fancifulName`
- `alcoholContent`, `netContents`
- `plantRegistry`, `permitNumber`
- `applicantName`, `applicantAddress`
- `qualifications`
- `labelImageFront`, `labelImageBack`
- `wineVintage`, `grapeVarietal`, `wineAppellation` (wine only)
- `ageStatement` (spirits only)


## Generated Files

| File | Description |
|------|-------------|
| `applications.js` | Lightweight index for the agent view. Contains only `{ ttbId, classTypeCode }` for each application. Used for category filtering (wine/malt/spirits) |
| `applicant/{d1}/.../` | Sharded directory tree of JSON files. One file per application with full form data. Fetched by agent-view.html on demand |


## Regenerating

After editing `data/applications.tsv`, regenerate the derived files:

```bash
cd scripts
make setup
```

This runs `demoSetup/make_demo_db.py` and `demoSetup/export_applicant.py` to:
1. Create/update the SQLite database
2. Generate `applications.js` (index)
3. Generate sharded `applicant/` JSON files

See [readme-demoSetup.md](readme-demoSetup.md) for full setup instructions.


## Verification API (separate from TTB External)

AI verification results are stored in `htdocs/verification/`, NOT in
`ttb-external/`. This separation reflects that:

| Path | System |
|------|--------|
| `/ttb-external/` | TTB's system (simulated for demo) |
| `/verification/` | Our AI system's output |

```
verification/
  results/{sharded}/*.json     AI extraction results
  extractions/{sharded}/*/     Cropped field images (PNG files)
  stats.json                   Processing statistics
  events.json                  Operational event log
```


## Category Codes

| Category | Code Range |
|----------|------------|
| Wine | 80-89 (includes 80A for rosé) |
| Malt Beverages | 900-959 |
| Distilled Spirits | 100-799, 943 (agave) |


## Featured Applications

The following applications appear first in the agent view (good for demos):

| TTB ID | Description |
|--------|-------------|
| 24028001000106 | Iron Ridge bourbon (ABV mismatch test case) |
| 24030001000213 | Breezy Wave seltzer (brand name mismatch test case) |
| 24017001000212 | Burnett Brews Winter Ale |
| 24027001000310 | Lighthouse Cellars rosé |
| 24026001000309 | TTB Imports Niagara red (import test case) |


## Note on Version Control

For the demo, the sharded data IS committed to git for portability.
In production, this data would live in S3/cloud storage or a database,
not in version control.
