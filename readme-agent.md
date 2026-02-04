# Agent View — Simulated Government Interface

**File:** `htdocs/agent-view.html`


## What this is

A simulated version of the TTB's internal COLA application detail page.
This is NOT the real system — it's an approximation built from publicly
visible elements of the COLAs Online public registry, inferred UI
patterns from government web applications of that era, and general
knowledge of what TTB Form 5100.31 contains.

The goal is to give demo viewers a realistic sense of what an agent's
screen looks like when they're reviewing a COLA application, so the
value of the AI verification app is immediately obvious by contrast.


## Design choices

- **Intentionally dated aesthetic:** dark muted blue header bar (#2d4a6f),
  plain table layouts, system serif fonts (Times New Roman), gray cell
  backgrounds, no rounded corners, no shadows. This evokes early-2000s
  government web applications.

- **Header bar** says "COLA Registry" with right-aligned label identifying
  this as a mockup. The sub-bar has placeholder agent nav links
  (My Queue, Review History, Guidelines) at reduced opacity.

- **Yellow-highlighted fields** (#fffde6 cells, #f5f0c8 headers) mark the
  fields an agent would manually verify against label artwork. Based
  on TTB regulations (27 CFR Parts 4, 5, 7) and COLAs Online manual:

### Always required on label (verify for all applications)

| Field | Notes |
|-------|-------|
| Brand Name | |
| Class/Type | Product designation as shown on label |
| Alcohol Content | Wine: Required (>14% must show exact %; 7-14% may use "table wine"). Spirits: Required. Malt: OPTIONAL unless product contains added flavors |
| Net Contents | OR may be blown/embossed into container. If COLA notes "embossed" in Step 3, skip label verification |
| Bottler/Producer Name | Or DBA if provided — see below |
| Bottler/Producer Address | City + state minimum |

### Verify only if declared in application

| Field | Notes |
|-------|-------|
| DBA / Trade Name | If provided, THIS is the name on label (replaces corporate name). TTB manual: "must match the label" |
| Fanciful Name | If provided, must appear on label |

### Imported products only

- **Origin (Country of Origin)** — required on label for imports only.
  Domestic products do not require origin on label. Foreign products
  must show country of origin (e.g., "Product of France").
  Yellow-highlighted only for imported products.

**TTB Origin Code ranges:**
- Domestic: 00-49 (US states), 4A (Puerto Rico), 4B (USVI), 4E (Alaska), 4K (DC)
- Foreign: 50+ (Italy=50, France=51, Germany=53, etc.)
  Letter codes except US territories (4H=Barbados, 51=France, 69=Canada, 81=Mexico, 92=UK, 99=Poland)

### Wine only

| Field | Notes |
|-------|-------|
| Vintage | Optional, but if present triggers appellation requirement |
| Grape Varietal | Optional, but if present triggers appellation requirement |
| Appellation | MANDATORY if vintage OR varietal is shown (27 CFR 4.27) |

### Distilled spirits only

| Field | Notes |
|-------|-------|
| Age Statement | MANDATORY for whiskey aged <4 years (27 CFR 5.74). MANDATORY if any age/maturity claim appears on label. Optional for whiskey ≥4 years with no age claims. Must show youngest component age if blended |

### Name/Address verification logic

```
IF dbaName provided → verify dbaName on label (NOT applicantName)
ELSE → verify applicantName on label
ALWAYS → verify applicantAddress (city, state) on label
Note: Address may be blown/embossed into container
```

### Presence check (not field-match)

- **Government Warning** — mandatory fixed text on all labels ≥0.5% ABV.
  Exact wording prescribed by 27 CFR Part 16. NOT entered in COLA
  application; TTB just checks it's present. Verify presence only.

### Not verified against label (informational only)

- **Qualifications** — administrative notes or TTB-imposed conditions.
  May contain special wording (translations, embossed info), or
  certificate restrictions ("For sale in [state] only").
  Generally NOT label verification items unless qualification
  specifically requires something to appear on label.
  Displayed in agent view for context but NOT yellow-highlighted.

### Other UI elements

- A floating circle badge ("Agent checks yellow fields against the
  label images") explains the workflow without cluttering the form.

- "Verify Label Images" button (#5d70ff blue) near the Product
  Information section, with an animated bobbing tap icon below it.
  This button triggers the AI verification in the right panel.

- Section headings and page title use navy (#00416f) to maintain the
  government institutional look.

- Data fields are based on the public TTB COLA registry and Form 5100.31:
  TTB ID, status, vendor code, serial number, class/type code, origin
  code, brand name, fanciful name, alcohol content, net contents, plant
  registry, permit number, applicant name/address, qualifications, and
  label images.


## Sample data

38 applications in `htdocs/ttb-external/data/applicant/*.json`:

| Category | Class/Type Codes | Count |
|----------|------------------|-------|
| Wine | 80-89 | ~11 applications |
| Malt Beverages | 900-959 | ~13 applications |
| Distilled Spirits | 100-799 | ~7 applications |

Category filtering by numeric class/type code prefix. Applications
include domestic and imported products across diverse categories
(table wine, sparkling, rosé, bourbon, tequila, vodka, gin, IPA,
stout, hard seltzer, mead, cider, sake, etc.).

15 applications are compliant (labels match form data).
15 have deliberate errors for testing the verification system.

4 applications (app-27 through app-30) were added specifically for
non-compliance testing with ChatGPT-generated front labels:
- Lighthouse Cellars rosé (compliant)
- Iron Ridge bourbon (ABV mismatch: label 40%/80proof vs app 45%/90proof)
- Casa Dorada tequila (origin in Spanish instead of English)
- Breezy Wave seltzer (brand name "BREEZE WAVE" vs "BREEZY WAVE")

9 additional real-bottle photos were added from actual bottles
(Cointreau, Luksusowa, Gato Negro, Ricard, Martini & Rossi, Calvados
Morin, Schofferhofer, Boddingtons, Drop of the Creator). These were
phone photos (HEIC) converted to PNG and downsampled to 800px wide.


## What's simulated vs. real

**Simulated / inferred:**
- The internal page layout and styling (the public registry shows
  similar data but the internal agent view is not publicly accessible)
- Vendor codes, plant registry numbers, and permit numbers (formatted
  to match real patterns but are fictional)
- The specific applicant names and addresses (fictional companies)
- The "Verify Label Images" button (does not exist in the real system
  — it represents the integration point with the new AI tool)

**Based on real public data patterns:**
- TTB ID format (14-digit numeric)
- Class/type code ranges (wine 80-89, malt 900-959, spirits 100-799)
- Origin code conventions (two-digit numeric + description)
- Government warning text (legally mandated, standardized)
- Field names and data structure from Form 5100.31


## Data architecture

Two separate APIs:

| Path | Purpose |
|------|---------|
| `/ttb-external/` | TTB's COLA system (simulated for demo). Applicant data, label images. Batch processor reads INPUT from here |
| `/verification/` | Our verification system. AI extraction results, cropped field images. Batch processor writes OUTPUT here |

The agent view reads from `/ttb-external/` which simulates an external
API we'd authenticate with in production. Uses sharded paths designed
to scale to TTB's production volume (~150K-180K applications/year,
3-5 million historical records).

**Sharding scheme:** TTB ID `24028001000106` becomes path `2/4/0/2/8/0/0/1/000106.json`
(first 8 digits = directory levels, remainder = filename)

```
/data/applications.tsv          Source of truth. Edit this file to add
                                or modify applications. Tab-separated.

/ttb-external/data/
  applications.js               GENERATED. Lightweight index with
                                { ttbId, classTypeCode } for filtering.

  applicant/{sharded}/*.json    GENERATED. Full application form data.
                                Fetched on demand by agent-view.html.

/ttb-external/query/
  received/{date}/              GENERATED. Date-based index for batch
  applications.json             processor to discover new submissions.

/ttb-external/images/           Label images (front/back PNGs).

/verification/
  results/{sharded}/*.json      AI verification results (JSON).
                                Created by batch processing pipeline.

  extractions/{sharded}/{id}/   Cropped field images (PNG files).
    brandName.png               One file per extracted field.
    alcoholContent.png
    ...
```

**To regenerate after editing applications.tsv:**

```bash
cd htdocs/ttb-external
make
```

Or directly: `cd htdocs/ttb-external/data && node generate_from_tsv.js`

Alternative: The Python scripts can also export applicant data:

```bash
cd scripts
make applicant
```

The agent view fetches from `/ttb-external/data/applicant/` and caches results.


## Scripts directory (batch processing pipeline)

The `/scripts` directory contains the batch processing pipeline:

```
scripts/
  config.py             Shared configuration (paths, model settings)
  paths.py              Sharding utilities for filesystem API
  Makefile              Orchestrates all workflows

  demoSetup/            Demo setup (run once per dataset)
    make_demo_db.py       Create SQLite DB from applications.tsv
    export_applicant.py   Export applicant JSON files

  batchProcessor/       AI processing (web server triggers)
    process_labels.py     Extract fields from labels via Claude API
    verify_extractions.py OCR verification of cropped images
    export_extractions.py Export verification results + extractions
    clear_processing.py   Reset processing status

  tools/                Diagnostic utilities
    make_preview.py       Generate HTML preview of extractions
```

**Workflows:**

```bash
# Agent data setup (run once after editing applications.tsv)
cd scripts && make setup

# AI processing (run to analyze labels)
ANTHROPIC_API_KEY=sk-ant-... make process

# Full pipeline
ANTHROPIC_API_KEY=sk-ant-... make all
```

The verification results and extractions are created by the AI processing
pipeline, not by the Node.js generator in `htdocs/ttb-external/data/`.

The "qualifications" field is the TTB Form 5100.31 term for all
mandatory label statements beyond the primary fields — government
warning, origin/import statements, bottler info, sulfite declarations.


## Interaction

- Responds to postMessage from parent frame:
  - `{ action: 'navigate', direction: 'prev'|'next' }`
  - `{ action: 'setCategory', category: 'wine'|'malt'|'spirits' }`
  - `{ action: 'goTo', ttbId: '...' }`

- "Verify Label Images" button posts to parent frame:
  ```json
  {
    "source": "agent-view",
    "section": "ai-check",
    "ttbId": "...",
    "dbaName": "...",
    "brandName": "...",
    "fancifulName": "...",
    "alcoholContent": "...",
    "netContents": "...",
    "classTypeCode": "...",
    "classTypeDesc": "...",
    "qualifications": "...",
    "wineVintage": "...",
    "grapeVarietal": "...",
    "wineAppellation": "...",
    "ageStatement": "...",
    "originCode": "...",
    "originDesc": "...",
    "applicantName": "...",
    "applicantAddress": "...",
    "labelImages": { "front": "...", "back": "..." }
  }
  ```

- Works standalone — opening agent-view.html directly shows the first
  wine application, though navigation requires the outer frame.


## TTB Origin Codes

Foreign country codes start at 50 (domestic US states are 00-49):

| Code | Country |
|------|---------|
| 50 | Italy |
| 51 | France |
| 53 | Germany |
| 70 | Chile |
| 92 | United Kingdom |
| 99 | Poland |

The `isImported()` function uses this to determine if origin must appear
on the label (required for imports, not required for domestic products).


## Qualifications Field

The "qualifications" field contains TTB-mandated disclosures only:

**Included:**
- Import/origin statements (PRODUCT OF FRANCE, WINE OF CHILE)
- Sulfites declarations (CONTAINS SULFITES)
- Composition disclosures (WITH NATURAL FLAVORS, 100% DE AGAVE)
- Bottler/producer info
- Required regulatory statements

**Excluded (not TTB compliance items):**
- Marketing slogans
- Historical claims (ESTD 1776, etc.)
- Technical specs (IBU, TA, pH values)
- Info already in dedicated fields (vintage, appellation)


## Workflow Guidance (Tap Icon)

A bouncing finger icon guides users through the demo workflow. Its
location is orchestrated by index.html based on processing state:

| State | Tap Icon Location |
|-------|-------------------|
| `totalProcessed = 0` | Points to batch.html ("Reprocess Now") |
| `totalProcessed > 0` | Points to agent-view.html ("Verify Label Images") |

**State transitions:**
- On page load: checks `verification/stats.json`
- After "Forget All": moves to batch.html immediately
- After batch processing completes: 10s delay, then moves to agent-view

Implementation via postMessage between index.html and iframes.


## Testbed Controls

Two buttons in index.html's right panel header for demo testing:

| Button | Action |
|--------|--------|
| FORGET 5 | Reset 5 random processed apps back to pending |
| FORGET ALL | Wipe all processing data (full reset for re-running AI) |

These buttons only appear in Batch Process mode (hidden in Agent View).
Gold styling makes them clearly visible as primary testbed actions.

"Forget 5" is useful for testing the "new apps in queue" workflow
without clearing everything. Apps are removed from Recent Completions
so they appear fresh when reprocessed.


## Operational Event Log

Performance-oriented event logging for monitoring batch processing health.
Events are stored in `htdocs/verification/events.json`.

| Event Type | Example Message |
|------------|-----------------|
| `batch_started` | "Processing started: 38 applications queued" |
| `batch_complete` | "Batch complete: 38 apps in 6m 12s (9.8s/app)" |
| `api_degraded` | "API response degraded: 8.2s avg (typical: 1.2s)" |
| `api_recovered` | "API response normalized" |
| `api_timeout` | API call timed out |
| `api_error` | API call failed |
| `cleared` | Processing data wiped |
| `apps_forgotten` | Apps reset to pending |

Design principle: NO per-application chatter. Only batch summaries,
state changes, and performance anomalies.


## Cache Management

Iframes can show stale content without proper cache handling:

- **Cache-busting:** timestamp parameters on iframe src URLs (`?t=...`)
- **No-cache meta tags** on all HTML files
- **Category toggles and pagination** reset app.html to home state
