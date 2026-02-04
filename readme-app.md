# Label Verification App (Agent View Mode)

**File:** `htdocs/app.html`


## Current state

AI-powered label verification tool. Receives application data via postMessage
when the agent clicks "Verify Label Images" in the agent view. Fetches real
extraction data from pre-processed JSON files and displays a verification
report comparing application fields against OCR-extracted text from labels.


## How it works

1. **Initial state:** waiting screen prompting user to click "Verify Label
   Images" in the agent view.

2. **On receiving postMessage** (source: 'agent-view', section: 'ai-check'):
   - Fetches data from two APIs:
     - `ttb-external/data/applicant/{sharded}.json` (declared form data)
     - `verification/results/{sharded}.json` (AI extraction results)
   - Builds image URLs for cropped fields from `verification/extractions/`
   - If verification results not found: shows "Not Yet Processed" message
   - If found: displays verification report comparing declared vs extracted

3. **The report includes:**
   - Large fanciful/brand name header with product type pill (Wine, Malt,
     Spirits) and origin pill (Domestic/Imported)
   - TTB ID displayed in top right
   - Overall status banner: green "Label Verified" or yellow "Potential
     Issues Detected" with count of issues to review
   - Two verification sections:

     **A. MANDATORY ELEMENTS (presence checks)**
     - Government Warning — always required
     - Contains Sulfites — wine only
     - Country of Origin — imports only
     - Shows green ✓ if detected, red ✗ if missing.

     **B. FIELD VERIFICATION (declared vs label)**
     - Brand Name, Class/Type, Alcohol %, Net Contents, etc.
     - Three-column table: Field | Declared | On Label
     - Review toggles (?, ✓, ✗) for each field

   - Revision notes box (when corrections needed) with dynamic text and Copy button
   - Full label images (front + back) at bottom
   - Lightbox for zooming cropped field images


## Review workflow

Fields are shown with three toggle buttons: ?, ✓, ✗

The meaning of each button depends on whether AI auto-detected OK or flagged
an issue:

### Scenario 1: AI auto-detected OK

AI found the requirement / values match. Default state: ✓ (trust AI's pass).

| Button | Label | Color | Meaning |
|--------|-------|-------|---------|
| ✓ (default) | "✓ Auto-detected" | Green | Agent confirms AI was right |
| ? | "Requirement auto-detected ok" | Grey | Agent wants to review |
| ✗ | "✗ Override: Agent found issue" | Red | Agent overrides AI's pass |

### Scenario 2: AI flagged an issue

AI didn't find it / values don't match. Default state: ? (needs agent review).

| Button | Label | Color | Meaning |
|--------|-------|-------|---------|
| ? (default) | "⚠ Agent verification needed" | Bold orange | Agent still reviewing |
| ✓ | "✓ Agent verified" | Green | Agent overrides AI's flag (it's fine) |
| ✗ | "✗ Agent confirmed issue" | Red | Agent confirms issue is real |

### Revision notes

The revision notes box appears when any field is marked ✗. The Copy button
only appears after all fields have been reviewed (no ? remaining). This
ensures the agent has manually verified each AI suggestion before copying
the revision guidance.

Review states are persisted in localStorage per TTB ID + field, so agents
can navigate away and return without losing their work.


## Verification types

The app performs TWO types of verification:

### 1. Mandatory presence checks

These elements must appear on label but are NOT in the COLA form.
We just check if they're present — no field matching.

| Element | When Required | If Not Detected |
|---------|---------------|-----------------|
| Government Warning | All beverages ≥0.5% ABV | Reject |
| Contains Sulfites | Wine only | Check for waiver |
| Country of Origin | Imports only | Reject |

**Sulfites logic:**
- Required if ≥10ppm sulfur dioxide (27 CFR 4.32, 5.63, 7.63)
- Applies to ALL categories, but wine is most common (sulfites are
  routine in winemaking; rare in spirits/malt)
- Currently checked for wine only in the app
- Acceptable patterns detected:
  - "Contains Sulfites" / "Contains Sulphites"
  - "Contains (a) Sulfiting Agent"
  - "Naturally Occurring Sulfites"
- If detected on label → ✓ Compliant
- If NOT detected → Agent alert to verify visually and check for
  sulfite waiver attachment (lab report proving <10ppm)

**Alcohol content format:**
- TTB requires "alc/vol" or "alc. by vol." format
- "ABV" is NOT TTB-compliant — flagged with warning if detected

**Country of origin logic:**
- Detect import status from originCode using TTB reference list:
  - Domestic: 00 (American), 01-49 (states), 4A (Puerto Rico),
    4B (Virgin Islands US), 4E (Alaska), 4K (DC)
  - Everything else = foreign/imported → verify
- Reference: `work/reference/ttb-origin-codes.txt`
- For imports: extract country name from originDesc (e.g., "Italy"
  from "50 - ITALY") and verify it appears on label
- Common formats: "Product of Italy", "Imported from Scotland",
  "Made in Mexico", or just "France"

**Note:** Other ingredient declarations (FD&C Yellow #5, cochineal,
aspartame, etc.) are NOT verifiable from label review alone. The agent
doesn't know the actual product composition — that requires formula
review or lab testing.

### 2. Field verification (declared vs label)

Compare what applicant entered in COLA form against what's on label.

**Always verified:**
- Brand Name
- Class/Type Description
- Alcohol Content (optional for malt)
- Net Contents
- Bottler/Producer Name
- Bottler/Producer Address (city, state)

**Wine only (codes 80-89):**
- wineVintage (if declared)
- grapeVarietal (if declared)
- wineAppellation (if declared)
- Note: If vintage OR varietal is declared, appellation becomes REQUIRED

**Distilled spirits only (codes 100-799):**
- ageStatement (if declared)

**Malt beverages only (codes 900-999):**
- Alcohol Content — optional (may not appear)


## Bottler/Importer name logic

Per TTB rules, the COLA applicant for imports IS the US importer (not the
foreign producer). The label must show "Imported by [importer]" for imports.

**For imports:**
- Verify applicantName on label (this is the US importer)
- dbaName on imports often contains foreign producer (optional label info)
- Field label shows "Importer" instead of "Bottler/Producer"

**For domestic:**
- IF dbaName provided → verify dbaName on label
- ELSE → verify applicantName on label
- Field label shows "Bottler/Producer"

**Always:**
- Verify applicantAddress (city, state)

**Prefix stripping:**
Labels often include prefixes like "Imported by", "Bottled by", etc.
These are stripped before comparison. Supported prefixes:
- Imported by, Imported and bottled by
- Bottled by, Produced and bottled by, Distilled and bottled by
- Produced by, Distilled by, Blended by, Made by
- Vinted by, Cellared by, Cellared and bottled by, Packed by
- Sole Agent, Sole U.S. Agent

**Partial matching:**
Bottler names use substring matching to handle variations like:
"ADAMBA IMPORTS" matches "ADAMBA IMPORTS INTERNATIONAL, INC."


## Optional field behavior

Optional fields are hidden if the applicant didn't declare them.
If omitted from the application, there's nothing to verify — even
if the AI detects it on the label.


## NOT verified

- Qualifications: TTB-imposed conditions, not applicant input
- Ingredient declarations (FD&C Yellow #5, etc.): conditional,
  would require knowing which ingredients are used


## Smart image display

The "On Label (AI)" column adapts based on extraction quality:

| OCR Score | Display |
|-----------|---------|
| ≥95% | Cropped image only (high confidence) |
| 50-94% | Cropped image + text (verify text against image) |
| <50% | Text + verify link with thumbnail (bounding box suspect) |
| Missing | Text + verify link with thumbnail |

The 50% threshold catches cases where the bounding box captured the
wrong region entirely (e.g., OCR reads "PIRITS" from the crop but
Claude extracted "DROP OF THE CREATOR"). Minor OCR variations still
show the cropped image since the bounding box is likely correct.

The verify link includes a small thumbnail of the full label and opens
the lightbox when clicked. The link text reflects the agent's review state:
- "⚠ Verify" (amber) — agent hasn't reviewed yet
- "✓ Verified" (green) — agent marked OK
- "✗ Issue found" (red) — agent confirmed issue

All cropped images are also clickable to open in the lightbox.


## Comparison rules

| Field | Case Sensitivity |
|-------|------------------|
| Government Warning | Case-SENSITIVE (legal text must match exactly) |
| All other fields | Case-insensitive, ignores special characters |

The government warning has strict case requirements because it's
legally mandated text. Other fields like brand name, fanciful name,
alcohol content, etc. are fuzzy-matched since labels may use different
capitalization styles (e.g., "Chardonnay" vs "CHARDONNAY").

**Normalization for alcohol content and net contents:**
- Case-insensitive
- Strips punctuation (periods, commas)
- Adds spaces between digits and letters: "750ML" → "750 ML"
- Adds space after %: "15%ALC" → "15% ALC"
- Word-order independent: "ALC. 12% BY VOL." = "12% ALC. BY VOL."
- This allows matching variations like:
  - "750 ML" = "750ml" = "750ML"
  - "15% alc./vol." = "15%alc./vol."
  - "ALC. 12% BY VOL." = "12% ALC. BY VOL."

**Bottler/Importer name comparison:**
- Strips bottler prefixes ("Imported by", "Bottled by", etc.)
- Uses substring matching (declared ⊂ extracted OR extracted ⊂ declared)
- This handles: "IMPORTED BY ABC IMPORTS" matching "ABC IMPORTS"


## Two-API Architecture

The app fetches from TWO separate APIs, reflecting the real-world split:

| API | Purpose |
|-----|---------|
| `/ttb-external/` | TTB's COLA system (simulated). Applicant-declared form data, label images |
| `/verification/` | Our system. AI extraction results (JSON), cropped field images (PNG files) |

**Sharded path format:**
TTB ID "24018001000301" → "2/4/0/1/8/0/0/1/000301"

First 8 digits become directory levels, remainder is the filename.

**Why sharding?**
TTB label volume is substantial:
- 150,000-180,000 applications processed annually
- A few thousand new records added weekly
- 25+ years of electronic records (images since 1999, data since 1996)
- Public COLA Registry contains an estimated 3-5 million records
- COLA Cloud's demo dataset has 160K records from 2018 alone

Sharding keeps directories small (~10K files max) while supporting
billions of records. Works well with S3/Azure Blob or local filesystems.


## TTB External API (ttb-external/)

Simulates TTB's COLA system. We authenticate and pull from it but have
no control over its structure.

**Applicant data:**
`ttb-external/data/applicant/2/4/0/1/8/0/0/1/000301.json`

```json
{
  "ttbId": "24018001000301",
  "brandName": "GOLDEN HILLS",
  "fancifulName": "RESERVE CHARDONNAY",
  "classTypeDesc": "TABLE WINE",
  "alcoholContent": "13.5% ALC. BY VOL.",
  "netContents": "750ML",
  "qualifications": "GOVERNMENT WARNING: ...",
  "labelImages": { "front": "wine_golden-hills_front.png", "back": "..." }
}
```

**Label images:**
`ttb-external/images/*.png`


## Our Verification API (verification/)

Our system. Batch processor writes here, app.html reads from here.

**Results JSON:**
`verification/results/2/4/0/1/8/0/0/1/000301.json`

```json
{
  "ttbId": "24018001000301",
  "status": "processed",
  "processedAt": "2026-02-03T14:30:00Z",
  "fields": {
    "brandName": {
      "text": "GOLDEN HILLS",
      "confidence": 0.95,
      "ocrScore": 0.92,
      "side": "front"
    }
  }
}
```

**Cropped field images (PNG files, not base64):**

```
verification/extractions/2/4/0/1/8/0/0/1/000301/
├── governmentWarning.png   # MANDATORY - back label
├── sulfites.png            # MANDATORY - wine only, back label
├── countryOfOrigin.png     # MANDATORY - imports only
├── brandName.png
├── fancifulName.png
├── alcoholContent.png
├── netContents.png
├── classTypeDesc.png
├── bottlerName.png
├── bottlerAddress.png
├── wineVintage.png         # WINE ONLY - if declared
├── grapeVarietal.png       # WINE ONLY - if declared
├── wineAppellation.png     # WINE ONLY - if declared (required if vintage/varietal)
└── ageStatement.png        # SPIRITS ONLY - if declared
```

**Why PNG files instead of base64?**
- No 33% size overhead from base64 encoding
- Directly auditable (view in browser/finder)
- Standard image tooling works
- CDN/S3 serves with proper content-type
- Field names as filenames for clarity


## Revision guidance

When a field is marked for correction (✎), the revision notes include
helpful, professional guidance for the applicant:

| Field | Guidance |
|-------|----------|
| Brand Name | "The brand name on the label ("[X]") does not match the application ("[Y]"). Please ensure the label and application match exactly." |
| Alcohol Content | "The alcohol content on the label ("[X]") does not match the application ("[Y]"). Please correct the label or application so they match." |
| Net Contents | "The net contents on the label ("[X]") does not match the application ("[Y]"). If net contents are embossed on the container, please note this in Step 3..." |

Tone is professional and helpful — focused on what the applicant needs
to fix to get approved, not punitive or bureaucratic. These are designed
to be copied directly into applicant correspondence.


## Integration

Listens for postMessage events with:
```json
{ "source": "agent-view", "section": "ai-check", "ttbId": "...", "brandName": "...", ... }
```

The postMessage includes applicant-declared data which is used as a
fallback when the applicant API file doesn't exist. This allows the
demo to work even before applicant JSON files are created.

The outer frame (index.html) handles panel switching: if the right panel
shows batch.html when the agent clicks "Verify Label Images", it switches
to app.html and forwards the message after load.


## Script organization

Scripts are split into two workflows:

```
scripts/
├── demoSetup/              # Setup for agent view (run once per dataset)
│   ├── make_demo_db.py         # creates processing.db from TSV
│   └── export_applicant.py     # exports declared form data → applicant API
│
├── batchProcessor/         # AI verification pipeline (web server triggers)
│   ├── process_labels.py       # Claude Vision + EasyOCR extraction
│   ├── verify_extractions.py   # OCR verification pass
│   ├── export_extractions.py   # exports → verification/results + extractions
│   └── clear_processing.py     # reset to pending
│
├── paths.py                # shared sharding utilities
└── config.py               # shared config
```

**Makefile targets:**

| Target | Action |
|--------|--------|
| `make setup` | Runs demoSetup/ scripts (one-time setup) |
| `make process` | Runs batchProcessor/ scripts (batch processing) |
| `make clean` | Clears AI processing results only |


## To regenerate data

**Applicant data (declared form values):**
```bash
make setup
# or: python3 scripts/demoSetup/export_applicant.py
```

**AI extraction data (verification/results + extractions):**
```bash
make process
# or: python3 scripts/batchProcessor/export_extractions.py
```


## Batch processor requirements

The following extraction requirements ensure app.html can properly verify:

**Mandatory fields (must extract for all labels):**
- `governmentWarning`: Full text starting with "GOVERNMENT WARNING:"
- `sulfites`: For wine only, detect "Contains Sulfites" or variants
- `countryOfOrigin`: For imports only, extract country statement

**Field extraction rules:**
- `alcoholContent`: Extract just the value (e.g., "12.5% ALC. BY VOL.")
  Do NOT include the word "Alcohol" as a prefix
- `netContents`: Extract just the value (e.g., "750 ML")
  Do NOT include equivalent measures (e.g., avoid "1 Liter 33.8 oz.")
- `bottlerName`: Extract company name only
  Do NOT include prefix ("Imported by", "Bottled by", etc.)
  Do NOT include address (city, state)
- `bottlerAddress`: Extract city and state only
- `fancifulName`: Extract the COMPLETE fanciful name
  e.g., "L'UNIQUE LIQUEUR" not just "LIQUEUR"
  e.g., "EXTRA DRY VERMOUTH" not just "EXTRA DRY"

**Field locations:**
- Don't assume front/back — search ALL label images for each field
- Brand name, class/type, alcohol content must be in "same field of vision"
  but can appear on front, back, or side
- Government warning, sulfites, name/address can be on ANY label

**Sulfite patterns to detect:**
- "Contains Sulfites" / "Contains Sulphites"
- "Contains (a) Sulfiting Agent(s)"
- "Contains Naturally Occurring Sulfites"


## Design notes

- Uses Inter font for clean, modern appearance
- Product type pills: uniform cool grey (#e5e7eb) for all types
- Dark saturated status banners:
  - Pass: Dark emerald green (#064e3b) with light text
  - Verification in Progress: Bright orange (#c2410c) with light text
  - Issues Identified: Dark red (#7f1d1d) with light text
- Row highlighting: red tint for issues (✗), yellow tint for reviewing (?)
- Toggle buttons: red for issues, amber for reviewing, green for OK
- Cropped field images shown above OCR text in the "On Label" column
- Lightbox with dark overlay for image zoom (80vw x 30vh max)
- Revision notes box: sidebar layout with label/button on left, content on right
- Max width 40vw for revision notes content box
- OS native scrollbar (no custom styling)


## UI states

**Home state ("Ready to Review"):**
Shows when no application selected. Prompts user to select an
application in Agent View and click "Verify Label Images".

**Not Yet Processed ("One More Step"):**
Shows when application selected but not batch-processed yet.
Includes button to switch to Batch Process tab.

**Verification Report:**
Shows after clicking "Verify Label Images" on a processed application.
Displays mandatory element checks, field verification table, and
revision notes box when issues are identified.

**Status banner states (header + counter text):**

| Banner | Counter | Meaning |
|--------|---------|---------|
| "Label Verified" | "Ready to approve" | All checks pass, no issues found |
| "Verification in Progress" | "X potential issues for agent to verify" | Agent hasn't reviewed any items yet (all showing ?) |
| "Verification in Progress" | "X for applicant; Y for agent" | Mixed state: some confirmed (✗), some still need review (?) |
| "Issues Identified" | "X items for applicant" | All reviewed, issues confirmed for applicant to fix |


## Mandatory element status text

When a mandatory element is NOT detected, the status text is dynamic
based on agent review state:

**For elements with alertIfMissing (Sulfites):**

| State | Display |
|-------|---------|
| ? | "⚠ Verify" (amber) |
| ✓ | "✓ Verified" (green) |
| ✗ | "✗ Missing from label" (red) |

**For elements without alertIfMissing (Government Warning, Country of Origin):**

| State | Display |
|-------|---------|
| ? | "⚠ Agent verification needed" (amber) |
| ✓ | "✓ Verified" (green) |
| ✗ | "✗ Not on label" (red) |

All undetected mandatory elements include a clickable thumbnail link to
the back label (with fallback to front if no back exists). Clicking opens
the lightbox for manual verification.


## Verify link thumbnails

When OCR confidence is low and a "⚠ Verify" link is shown, the link
includes label thumbnails for manual verification:

**Back-label fields (bottlerName, bottlerAddress / Importer):**
- Primary thumbnail: back label
- Secondary thumbnail: front label (if both exist)

**Front-label fields (brandName, fancifulName, alcoholContent, etc.):**
- Primary thumbnail: front label
- Secondary thumbnail: back label (if both exist)

When both labels exist, both thumbnails appear side by side. Each
thumbnail is independently clickable to open that label in the lightbox.

The verify link text changes based on agent review state:
- "⚠ Verify" (amber) — agent hasn't reviewed yet
- "✓ Verified" (green) — agent marked OK
- "✗ Issue found" (red) — agent confirmed issue
