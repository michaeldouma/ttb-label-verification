# Batch Label Processing Pipeline

Extracts text fields from COLA label images using Claude Vision API
for text reading and EasyOCR for precise bounding box detection.

**Two workflows:**
1. **Demo Setup** — Create database and fake TTB API (see [readme-demoSetup.md](readme-demoSetup.md))
2. **AI Processing** — Batch extraction triggered from web UI


## TTB COLA Volume & Why We Shard

The COLA registry is massive:

| Metric | Value |
|--------|-------|
| Annual volume | ~150,000-180,000 applications/year |
| Historical total | 3-5 million COLAs (records from 1996, images from 1999) |
| Weekly additions | A few thousand new records per week |
| 2018 alone | 160,000+ records (from COLA Cloud demo dataset) |

Storing millions of JSON files in flat directories causes filesystem
and S3 performance issues. We use prefix sharding instead:

```
TTB ID "24001001000101" becomes path:
  results/2/4/0/0/1/0/0/1/000101.json

First 8 digits → 8 nested directories
Remaining digits → filename
```

**Benefits:**
- No directory exceeds thousands of files (vs millions in flat)
- Works with S3 (key distribution improves performance)
- CDN-cacheable static paths
- No database needed for lookups — purely static file serving

See `paths.py` for the shared utility functions.


## Quick Start (Makefile)

```bash
cd scripts/
export ANTHROPIC_API_KEY="sk-ant-..."

make setup        # Demo setup: create DB + export applicant JSON
make process      # AI processing: extract + verify + export
make all          # Full pipeline (setup + process)

make clean        # Clear AI processing, reset to pending
LIMIT=5 make extract   # Test extraction with 5 apps
```

**Makefile targets:**

| Category | Target | Description |
|----------|--------|-------------|
| Workflows | `make setup` | Demo data setup (see [readme-demoSetup.md](readme-demoSetup.md)) |
| | `make process` | AI processing (extract + verify + export) |
| | `make all` | Full pipeline (setup + process) |
| AI Processing | `make extract` | Run label extraction (Claude + EasyOCR) |
| | `make verify` | Run OCR verification |
| | `make export` | Export results + extraction images to verification API |
| | `make clean` | Clear processing, reset to pending |
| Utilities | `make install` | Install Python dependencies |
| | `make api` | Start API server for batch.html buttons (port 9081) |
| | `make help` | Show all targets |


## API Server for batch.html

The batch.html UI has buttons to trigger processing. These require a
simple API server running alongside the static file server:

```bash
# Terminal 1: Static file server
cd htdocs && python3 -m http.server 8080

# Terminal 2: API server (from scripts/)
cd scripts
export ANTHROPIC_API_KEY="sk-ant-..."
make api
```

**API endpoints (port 9081):**

| Method | Endpoint | Action |
|--------|----------|--------|
| POST | `/api/clear` | Run make clean, return deletion report |
| POST | `/api/forget` | Reset 5 random processed apps to pending |
| POST | `/api/process` | Start make process in background |
| POST | `/api/abort` | Stop running process (creates STOP file) |
| GET | `/api/status` | Get processing status and output |

**Stop mechanism (file-based signal):**

The batch processor checks for `data/STOP` before each label.
If the file exists, it halts gracefully after the current label.

- `POST /api/abort` creates `data/STOP`
- `POST /api/process` deletes `data/STOP` before starting
- Processor removes STOP file after stopping

Manual stop from terminal:
```bash
touch data/STOP          # Signal stop
rm data/STOP             # Allow processing to start
```

This is bulletproof — works even if API server crashes, survives
page reloads, and can be triggered manually from the command line.


## batch.html UI

The batch processing interface at `/htdocs/batch.html` provides an
operations dashboard for monitoring the label processing service.

**Header:**
- Dynamic title: "Label Processing Service — Processing/Running/Stopped"
- Dark magenta banner (#6d1a6d)
- State toggle: RUNNING (green) / STOPPED (orange-red gradient)
  Shows SERVICE state, not job state. Click inactive to switch.
  When RUNNING, service auto-processes any queued work.
  When STOPPED, service is off and won't process.

**Status Bar:**
- Uptime: "Running for 14d 3h"
- COLA Registry connection status (green dot)
- Anthropic API connection status (green dot)
- Current queue depth

**Metrics Row (current state + throughput):**

| Metric | Description |
|--------|-------------|
| Done | Current count of processed apps |
| Pending | Current count waiting to process |
| Apps/Hour | Processing throughput rate |
| Avg/App | Average time per application |
| Errors (24h) | Error rate percentage |

**Throughput Sparklines:**
- 24h Activity: hourly buckets, shows processing events
- 7d Activity: daily buckets, shows processing events
- Note: These show historical activity, not current state.
  "Done" count may differ due to forgotten/reset apps.

**Two-Column Activity (compact, max-height 160px):**
- Recent Completions: thumbnail grid with TTB IDs
  New items get a pop-in animation with green glow
  Only updates when content changes (no flicker)
  Deduplicated by TTB ID (handles race conditions)
- Recent Errors: timestamp, TTB ID, error type
  (or "No errors in last 24h")

**Activity Log (resizable):**
- Drag handle above log to resize height (80-400px)
- Performance-oriented event log (max 100 entries)
- Batch summaries, state changes, errors, recoveries
- Not per-application chatter

**Service Behavior:**
- RUNNING mode stays on even when queue empties
- Auto-detects new work via 3-second polling
- Service picks up new/forgotten apps automatically if RUNNING

**Test Controls (in index.html, outside iframe):**

| Button | Action |
|--------|--------|
| "Forget 5" | Resets 5 random processed apps to pending. Removes them from database AND from Recent Completions. Service auto-picks them up if RUNNING |
| "Forget All" | Permanently clears ALL processing data. Deletes results, extractions, resets all apps to pending. Use this to demo the AI processing from scratch |

Stats are read from `/verification/stats.json` which is updated after
each application is processed.


## Manual Execution

If you prefer running scripts directly (from scripts/ directory):

```bash
export ANTHROPIC_API_KEY="sk-ant-..."

# Demo setup (see readme-demoSetup.md for details)
python3 demoSetup/make_demo_db.py
python3 demoSetup/export_applicant.py

# AI Processing
python3 batchProcessor/process_labels.py       # Extract fields from labels
python3 batchProcessor/verify_extractions.py   # OCR verification
python3 batchProcessor/export_extractions.py   # Export results
python3 batchProcessor/clear_processing.py     # Reset to pending

# Testing options
python3 batchProcessor/process_labels.py --limit 2                    # Process only 2 apps
python3 batchProcessor/process_labels.py --ttb-id 24001001000101      # Reprocess single app
```


## Directory Structure

```
scripts/
├── Makefile              Pipeline automation
├── config.py             Shared configuration
├── paths.py              Shared path utilities
├── stats.py              Processing stats (writes to verification/stats.json)
├── events.py             Operational event log (writes to verification/events.json)
│
├── demoSetup/            Demo data setup (Michael runs)
│   ├── make_demo_db.py       Create DB from applications.tsv
│   └── export_applicant.py   Export applicant JSON to API
│
├── batchProcessor/       AI batch processing (web server triggers)
│   ├── process_labels.py     Claude Vision + EasyOCR extraction
│   ├── verify_extractions.py OCR verification pass
│   ├── export_extractions.py Export results + extraction images
│   └── clear_processing.py   Reset to pending
│
├── miniServer/           Web server controls
│   └── api_server.py         HTTP API for batch.html buttons
│
└── tools/                Testing utilities
    └── introduce_errors.py   Introduce errors for testing
```


## Two-API Architecture

There are TWO separate static APIs, representing different systems:

### 1. TTB External API (`/htdocs/ttb-external/`)

Simulates TTB's COLA system — their data, their structure.
In production, this would be TTB's actual API that we query.

```
ttb-external/
├── data/
│   ├── applicant/{sharded}/*.json   # Application form data
│   └── applications.js              # Index for agent-view
├── query/
│   └── received/{YYYY-MM-DD}/applications.json  # New apps to process
└── images/
    └── *.png                        # Label images from applicants
```

### 2. Verification API (`/htdocs/verification/`)

OUR system — AI extraction results, verification data.
Batch processor writes here, app.html reads from here.

```
verification/
├── results/{sharded}/*.json         # AI-extracted text + metadata
│   └── 000101.json                  # {status, fields: {brandName: {text, imageUrl, ...}}}
├── extractions/{sharded}/           # Cropped mini-images
│   └── 000101/
│       ├── brandName.png
│       ├── fancifulName.png
│       ├── alcoholContent.png
│       ├── netContents.png
│       ├── classTypeCode.png
│       ├── bottlerName.png
│       ├── bottlerAddress.png
│       ├── governmentWarning.png
│       ├── sulfites.png             # wine only
│       ├── countryOfOrigin.png      # imports only
│       ├── wineVintage.png          # wine only
│       ├── grapeVarietal.png        # wine only
│       ├── wineAppellation.png      # wine only
│       └── ageStatement.png         # spirits only
├── stats.json                       # Processing summary + per-app log
└── events.json                      # Operational event log (performance metrics)
```

**Why separate APIs:**
- `/ttb-external/` = "someone else's API we're faking for the demo"
- `/verification/` = "our system, our design, our output"

**Why image files (not base64 in JSON):**
- No conversion overhead (base64 adds ~33% file size)
- Directly auditable (view images in browser/finder)
- Standard image tooling works (thumbnails, preview, etc.)
- CDN/S3 can serve images with proper content-type
- Field names as filenames (brandName.png, not a.png) for clarity

**Frontend fetches:**
```
/ttb-external/data/applicant/2/4/0/0/1/0/0/1/000101.json
/verification/results/2/4/0/0/1/0/0/1/000101.json
/verification/extractions/2/4/0/0/1/0/0/1/000101/brandName.png
```


## Scripts Reference

### Shared

| File | Description |
|------|-------------|
| `config.py` | Configuration: paths, API key, model, field list. API key read from `ANTHROPIC_API_KEY` env var. Model defaults to claude-sonnet-4-20250514 |
| `paths.py` | Shared utilities for sharded file paths. TTB External API: `ttb_id_to_sharded_path()`, `ttb_id_to_url_path()`, `ensure_sharded_dir()`. Verification API: `get_verification_result_path()`, `get_extraction_image_dir()`, `get_extraction_image_url()` |
| `stats.py` | Processing statistics as JSON. Writes to `htdocs/verification/stats.json` for frontend. `log_action()` - log a processing action. `update_summary()` - update processed/pending/error counts. batch.html polls this file for live status updates |
| `events.py` | Operational event log for monitoring. Writes to `htdocs/verification/events.json` for frontend. Performance-oriented events (NOT per-application chatter): `batch_started()`, `batch_complete()`, `api_response()`, `api_timeout()`, `api_error()`, `processing_stopped()`, `cleared()`. Also tracks API state transitions: `api_degraded` (avg response > 8s), `api_recovered` (avg response normalized < 3s). Max 100 events kept in rolling log |

### Demo Setup (demoSetup/)

See [readme-demoSetup.md](readme-demoSetup.md) for documentation of `make_demo_db.py` and
`export_applicant.py` scripts.

### AI Processing (batchProcessor/)

| Script | Description |
|--------|-------------|
| `process_labels.py` | Main extraction pipeline with timing output. `--limit N` to process only N apps (for testing). For each pending app: 1) Sends front+back images to Claude Vision, 2) Runs EasyOCR on both images, 3) Fuzzy-matches Claude text → OCR bounding boxes, 4) Crops mini-images with padding and de-rotation, 5) Writes to extracted_fields table, 6) Updates processing_results. Outputs per-app timing and summary statistics |
| `verify_extractions.py` | Post-processing verification. Runs EasyOCR on each cropped mini-image and compares against Claude's extracted text. Writes ocr_text and ocr_match_score to DB |
| `export_extractions.py` | Exports AI extraction results to verification API. Output: `verification/results/{sharded}/{id}.json`, `verification/extractions/{sharded}/{id}/` |
| `clear_processing.py` | Reset script. Clears processing_results and extracted_fields, deletes mini-images, clears verification API output, resets all apps to pending |

### Tools (tools/)

| Script | Description |
|--------|-------------|
| `introduce_errors.py` | Testing utility. Introduces errors into processed data for testing error handling in the UI |


## Architecture & Key Decisions

### Two-pass extraction (the most important decision)

We tried having Claude Vision return bounding box coordinates directly.
This failed — vision LLMs are good at reading text but bad at precise
pixel coordinates. Even with percentage-based coordinates, crops were
consistently off, especially for small fields on small images.

**The solution: a two-pass approach.**

| Pass | Tool | Purpose |
|------|------|---------|
| Pass 1 | Claude Vision API | Extracts field TEXT only. (What does the label say? Which side is it on?) This is what Claude is good at |
| Pass 2 | EasyOCR | Runs locally on each image, returns precise bounding box polygons for every text region. We then fuzzy-match Claude's extracted text against OCR regions to find the exact pixel location |
| Pass 3 (verify) | EasyOCR | On the cropped mini-images themselves, compared against Claude's extraction. This gives an independent verification score |

This separation of concerns (LLM for understanding, OCR for geometry)
produces far better crops than either approach alone.


### Fuzzy matching for OCR ↔ Claude alignment

OCR text is never perfect — it reads "I8%" instead of "18%",
"ALCIVOL" instead of "ALC./VOL.", etc. The matcher:
- Strips punctuation for comparison
- Uses word-level SequenceMatcher (>0.6 threshold per word)
- Tries consecutive groups of OCR items for multi-word fields
- Falls back to checking the other image side if no match found
- Short fields (≤6 words): finds best contiguous group
- Long fields (governmentWarning): gathers all matching regions


## Extracted Fields

Up to 14 fields per application (when present on the label):

> **IMPORTANT:** Per TTB regulations (27 CFR 5.63, 7.63, 4.32), fields may appear
> on ANY label (front, back, side, neck). We search ALL images for each field.

**Core fields (all products):**

| Field | Description |
|-------|-------------|
| `brandName` | Most prominent brand text |
| `fancifulName` | Product descriptive name (not the brand) |
| `alcoholContent` | Alcohol percentage (note: "ABV" is NOT TTB-compliant) |
| `netContents` | Volume/size statement |
| `classTypeCode` | Regulatory product type |
| `bottlerName` | Bottler/producer/importer company name |
| `bottlerAddress` | Bottler location (city, state) |

**Mandatory elements (presence verification):**

| Field | Description |
|-------|-------------|
| `governmentWarning` | The GOVERNMENT WARNING statement (caps required) |
| `sulfites` | Sulfite warning: "Contains Sulfites", "Sulphites", etc. |
| `countryOfOrigin` | Country of origin (required for imports) |

**Wine-specific fields:**

| Field | Description |
|-------|-------------|
| `wineVintage` | Vintage year (e.g., "2021") |
| `grapeVarietal` | Grape variety (e.g., "CHARDONNAY") |
| `wineAppellation` | Region/appellation (required if vintage or varietal shown) |

**Spirits-specific field:**

| Field | Description |
|-------|-------------|
| `ageStatement` | Age claim (required for whiskey under 4 years) |


## Field Validation Rules

Per TTB Form 5100.31 and the COLA application manual:

### Summary of what can be verified

| Element | Verifiable? | How |
|---------|-------------|-----|
| Government Warning | ✓ Yes | Presence check — always required |
| Sulfites | ✓ Yes | Label OR COLA attachment (wine only) |
| Country of Origin | ✓ Yes | If import, must be on label |
| FD&C Yellow No. 5 | ✗ No | Agent doesn't know ingredients |
| Cochineal/Carmine | ✗ No | Agent doesn't know ingredients |
| Aspartame | ✗ No | Agent doesn't know ingredients |

### Two types of verification

**1. Field-match verification (compare application data ↔ label text):**

Always required on label:
- `brandName` — Always required
- `classTypeCode` — Always required
- `alcoholContent` — Required for wine/spirits; optional for malt beverages
- `netContents` — Required (label OR embossed in container)
- `bottlerName` — Always required (dbaName or applicantName)
- `bottlerAddress` — Always required (city, state)

Verify ONLY IF declared in application:
- `fancifulName` — If provided, must match label
- `wineVintage` — "if it is shown on the label"
- `grapeVarietal` — "if it is shown on the label"
- `wineAppellation` — "if it appears on the label"
- `ageStatement` — If claimed (spirits)

**2. Presence verification (mandatory element must exist on label):**

These elements appear on labels but are NOT typed into the COLA form.
Verification = check that required text is present on label.

| Element | Requirement |
|---------|-------------|
| `governmentWarning` | Required on ALL alcohol ≥0.5% ABV since 1989. Fixed text per 27 CFR Part 16 (see config.py). Verification: presence check only |
| `sulfites` | Required on wines with ≥10ppm sulfur dioxide. Fixed phrase: "Contains Sulfites". Verification: conditional (see below) |
| `countryOfOrigin` | Required on imports (customs requirement). Varies: "Product of France", "Imported from...", etc. Verification: if import, must be present |

### Sulfites verification logic (wine only)

```
IF wine label shows "Contains Sulfites":
    ✓ Compliant — declaration present

IF wine label has NO sulfite statement:
    Check: Does COLA have sulfite waiver (lab report) attached?
    IF yes → ✓ Compliant (lab proves <10ppm)
    IF no  → ⚠ Problem — missing required documentation
```

Note: Wine COLAs without sulfite declaration must include lab
analysis proving <10ppm. The agent can verify via COLA attachments.

### Out of scope (agent cannot verify from label alone)

- `fdcYellow5` — Required if FD&C Yellow No. 5 is used
- `cochinealCarmine` — Required if cochineal extract or carmine is used
- `aspartame` — Required if aspartame is used

These ingredient declarations are producer responsibility.
Agent doesn't know product ingredients — only visible if declared.
Violations caught by: lab testing, formula review, or complaints.

### Name/Address logic

```
IF dbaName provided:
    verify dbaName on label (this IS the bottler identity)
ELSE:
    verify applicantName on label
ALWAYS verify:
    bottlerAddress (city, state) on label
```

### Case sensitivity

- Most fields: case-insensitive matching
- GOVERNMENT WARNING: first two words must be ALL CAPS and bold
- Remainder of warning must NOT be bold


## TTB Text Format Rules

Per 27 CFR, specific text formats are required:

**Alcohol Content:**
- Acceptable: "13.5% ALC. BY VOL.", "ALC 13.5% BY VOL", "13.5% ALC/VOL"
- NOT allowed: "ABV" abbreviation (e.g., "13.5% ABV" is non-compliant)

**Government Warning:**
- "GOVERNMENT WARNING" must be in CAPITAL LETTERS and BOLD
- Remainder of text must NOT be bold
- Must be continuous paragraph (no line breaks in middle of sentences)

**Sulfites (multiple acceptable phrases):**
- "Contains Sulfites"
- "Contains Sulphites" (British spelling)
- "Contains (a) Sulfiting Agent(s)"
- "Contains Naturally Occurring Sulfites"

**Net Contents:**
- Acceptable: "mL", "ml", "ML", "L" (with or without periods)

**Bottler statements (valid prefixes):**
- "Bottled By", "Produced and Bottled By", "Imported By"
- "Packed By", "Vinted By", "Blended By", "Made By"
- "Cellared By", "Distilled By", etc.

The verification app compares applicant JSON (declared) against
verification/results JSON (AI-extracted) to flag discrepancies. Empty optional
fields are skipped entirely — nothing to review.


## Database Schema

`processing.db` (data/):

| Table | Columns |
|-------|---------|
| `applications` | All app fields from applications.tsv |
| `processing_results` | ttbId, status, processed_at, error_message |
| `extracted_fields` | ttbId, field_name, extracted_text, confidence, mini_image_path, region_bbox, rotation_degrees, ocr_text, ocr_match_score |


## Dependencies

```bash
pip install anthropic Pillow pillow-heif easyocr certifi
```

(sqlite3 and numpy come with stdlib / easyocr)
(certifi fixes macOS Python SSL certificate issues)

Or use: `make install`


## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Required. Claude API key |
| `ANTHROPIC_MODEL` | Optional. Defaults to claude-sonnet-4-20250514 |
| `LOGNAME` / `USER` | Set to any value to suppress EasyOCR warnings in containerized environments |


## Known Limitations

- Claude's self-reported confidence is unreliable (often 95%+ even when
  wrong). The OCR verify score is the real quality indicator.

- Decorative/script fonts defeat EasyOCR, so verify scores are low
  even when crops are visually correct.

- When two fields share one physical line of text, both match the same
  OCR region, producing overlapping crops.

- Government Warning OCR verify may be low — crops capture the whole
  warning block while Claude extracts only specific text.

- `classTypeCode` is the hardest field — many labels don't print product
  type as standalone text.

- Curved text on cylindrical bottles is readable by Claude Vision but
  OCR bounding boxes may be imprecise.


## Performance & Throughput

Measured on development machine (no GPU):

| Operation | Time |
|-----------|------|
| EasyOCR initialization | ~2.0s (one-time per session) |
| EasyOCR per-image | ~12-13s (800px wide bottle photos) |
| Claude Vision per-app | ~2-4s (front + back images) |
| Full extraction per app | ~25-30s (2 images × EasyOCR + 1 API call) |

With 38 applications and ~76 images:
- Total extraction time: ~20-25 minutes
- Verification pass: ~10 minutes (one OCR call per mini-image)

**Scalability notes:**
- EasyOCR is the bottleneck (12-13s/image vs 2-4s API call)
- GPU acceleration would dramatically improve OCR speed
- API calls can be parallelized; EasyOCR is CPU-bound
- For 1k apps/day target: need GPU + concurrent workers
