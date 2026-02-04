# Demo Setup Guide

This guide covers running the web demo and setting up the fake TTB
external API data. The demo simulates TTB's COLA registry system
with sample applications and label images.


## Running the Web Demo

The demo requires two terminal windows:

### Terminal 1 — Static file server (serves the web app)

```bash
cd htdocs
python3 -m http.server 8080

# Output:
# Serving HTTP on :: port 8080 (http://[::]:8080/) ...
```

### Terminal 2 — API server (handles batch processing commands)

```bash
cd scripts
export ANTHROPIC_API_KEY="sk-ant-..."
make api

# Output:
# Starting API server on port 9081...
# Endpoints:
#   POST http://localhost:9081/api/clear    - Reset all apps to pending
#   POST http://localhost:9081/api/forget   - Forget 5 random apps (for testing)
#   POST http://localhost:9081/api/process  - Start batch processing
#   POST http://localhost:9081/api/abort    - Stop processing
#   GET  http://localhost:9081/api/status   - Get processing status
```

Then open http://localhost:8080/ in your browser.

> **Note:** The API server requires an Anthropic API key for batch processing.
> The static file server works without it (for viewing the UI only).


## Demo Data Overview

The demo includes 38 sample COLA applications:

| Category | Class Codes | Count |
|----------|-------------|-------|
| Wine | 80-89 | ~11 applications |
| Malt Beverages | 900-959 | ~13 applications |
| Distilled Spirits | 100-799 | ~14 applications |

**Sources:**
- ChatGPT-generated labels (fictional brands)
- Real bottle photos (Cointreau, Luksusowa, Gato Negro, etc.)
- Mix of domestic and imported products

**Test cases include 35 deliberate errors for verification testing:**
- Alcohol content mismatches (15 errors)
- Brand name variations (6 errors)
- Net contents mismatches (5 errors)
- Wine vintage errors (4 errors)
- Fanciful name / varietal variations (5 errors)

**Date range:** December 1, 2025 to February 3, 2026


## Source of Truth

All application data lives in one file:

```
data/applications.tsv
```

Tab-separated values with columns:
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

Label images are stored in:

```
htdocs/ttb-external/images/
```

Naming convention: `{category}_{brand}_{product}_{front|back}.png`


## Setting Up Demo Data

After editing `applications.tsv`, regenerate the derived files:

```bash
cd scripts
make setup
```

This runs two scripts:

### 1. demoSetup/make_demo_db.py

- Reads `applications.tsv`
- Creates `data/processing.db` (SQLite)
- Tables: `applications`, `processing_results`, `extracted_fields`
- All apps set to `status='pending'`

### 2. demoSetup/export_applicant.py

- Exports form data to sharded JSON files
- Output: `htdocs/ttb-external/data/applicant/{sharded}/*.json`
- Creates `applications.js` index for agent view

Or run directly:

```bash
python3 demoSetup/make_demo_db.py
python3 demoSetup/export_applicant.py
```


## Adding New Bottles

To add photos of real bottles (e.g., from phone camera):

1. **Convert HEIC to PNG** if needed, downsample to ~800px wide
   (`pillow-heif` package handles HEIC conversion)

2. **Copy images** to `htdocs/ttb-external/images/` with naming:
   `{category}_{brand}_{product}_{front|back}.png`

   Examples:
   ```
   wine_gato-negro_cabernet_front.png
   spirits_cointreau_liqueur_front.png
   malt_boddingtons_ale_front.png
   ```

3. **Add a row** to `data/applications.tsv` with the application data

4. **Regenerate:**
   ```bash
   cd scripts && make setup
   ```

5. **Run AI processing** to extract fields:
   ```bash
   make process
   ```


## Directory Sharding

The demo uses a sharded directory structure designed for TTB-scale
volumes (150K+ applications/year, millions historical):

```
TTB ID:     24028001000106
Path:       applicant/2/4/0/2/8/0/0/1/000106.json
```

First 8 digits become 8 nested directories. Remaining digits are filename.

**This scheme:**
- Keeps directory sizes manageable
- Works with S3/CDN for production
- Enables parallel batch processing

See [readme-ttb-external-api.md](readme-ttb-external-api.md) for full API documentation.


## Files Generated

### From applications.tsv

```
htdocs/ttb-external/data/
  applications.js              Index for agent view filtering
  applicant/{sharded}/*.json   Full application form data
```

### From AI batch processing

```
htdocs/verification/
  results/{sharded}/*.json     AI extraction results
  extractions/{sharded}/*/     Cropped field images
  stats.json                   Processing statistics
  events.json                  Operational event log

data/
  processing.db                SQLite database with all state
```
