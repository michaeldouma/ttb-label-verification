# TTB Label Verification Demo

Take-home project for a TTB IT Specialist position demonstrating how AI
could assist COLA (Certificate of Label Approval) review agents.

You are welcome to use or adapt any of this code for your projects.

TTB agents currently review COLA applications by manually cross-referencing
form fields (brand name, ABV, net contents, etc.) against uploaded label
artwork — often low-quality photos of curved bottles or flat scans. This
demo shows how an AI tool could automate that comparison, flagging
mismatches and surfacing cropped image regions for quick human review.

**Quick start:** See [Running the Demo](#running-the-demo) below for setup instructions.


## Development Approach

This project was developed using AI-assisted coding (Claude) to demonstrate
the human+AI workflow relevant to this position. The architecture, requirements,
and design decisions are mine; Claude helped with implementation, debugging,
and documentation. This mirrors how I would approach AI-augmented operations
work at Treasury.


## Approach

The core insight: TTB agents spend significant time on a task that's tedious
for humans but well-suited for AI — comparing declared form values against
label images. Rather than replacing agents, AI can pre-screen applications
and surface discrepancies for human review.

**Key design decisions:**

1. **Two-pass extraction** — Claude Vision reads text accurately but returns
   unreliable pixel coordinates. EasyOCR provides precise bounding boxes but
   weaker text recognition. Using each tool for what it's best at produces
   far better results than either alone.

2. **Human-in-the-loop** — AI flags potential issues; agents make final
   decisions. The verification app presents AI findings alongside cropped
   image evidence, enabling quick confirmation or override.

3. **Scalable architecture** — Sharded file paths handle millions of records.
   Static APIs mean no database bottlenecks. Designed for CDN/S3 deployment
   from the start, not retrofitted later.

4. **Portable demo** — No build step, no framework dependencies. A hiring
   manager can run this with `python3 -m http.server` and see it working.


## Tools Used

| Tool | Purpose | Why This Choice |
|------|---------|-----------------|
| **Claude Vision API** | Text extraction from label images | Superior accuracy on curved bottles, decorative fonts, multi-language text |
| **EasyOCR** | Bounding box detection | Open-source, runs locally, precise geometry where Claude fails |
| **Python / SQLite** | Batch processing pipeline | Standard government-approved stack, no exotic dependencies |
| **Static HTML/JS** | Frontend interfaces | Zero build complexity, runs anywhere, easy to audit |
| **Make** | Task automation | Universal, self-documenting, pre-installed on Linux/macOS |


## Assumptions

**Domain assumptions:**

- Agents review applications individually, not in bulk batches
- Label images vary widely in quality (phone photos, scans, digital artwork)
- The existing government system cannot be modified — new tools must work alongside it
- Speed matters: agents process thousands of applications; seconds saved per review compound

**Technical assumptions:**

- Claude Vision API will remain available and cost-effective for government use
- Label text extraction is a solved problem for ~90% of cases; the remaining
  edge cases (extreme angles, damaged labels) require human judgment anyway
- A verification tool that's right 95% of the time and flags uncertainty is
  more valuable than one that's right 99% of the time but provides no confidence signal


## Three Components

This project has three primary components:

| Component | Audience | Purpose |
|-----------|----------|---------|
| **Simulated Agent View** | Demo viewers | Mockup of TTB's internal COLA review system, showing what agents see today |
| **Batch Processing System** | Administrators | Backend pipeline that extracts text from label images using AI |
| **Label Verification App** | Human agents | New tool that displays AI analysis alongside application data for quick review |

The demo presents these as a two-panel interface: the simulated government
system on the left, and the new AI-powered tools on the right.

---

## 1. Simulated Agent View

**File:** `htdocs/agent-view.html` — [Full documentation](readme-agent.md)

A mockup of TTB's internal COLA application detail page. This simulates what
an agent's screen looks like when reviewing applications in the existing
government system.

### Design

- **Intentionally dated aesthetic** — dark blue header, plain table layouts,
  Times New Roman, gray backgrounds. Evokes early-2000s government web apps.
- **Yellow-highlighted fields** mark what agents must manually verify against
  label images: brand name, alcohol content, net contents, bottler info, etc.
- **"Verify Label Images" button** sends application data to the right panel,
  demonstrating how the new AI tool would integrate.

### Data

38 sample COLA applications across wine, malt beverages, and distilled spirits:

| Category | Class Codes | Applications |
|----------|-------------|--------------|
| Wine | 80-89 | ~11 |
| Malt Beverages | 900-959 | ~13 |
| Distilled Spirits | 100-799 | ~14 |

**Label image sources:**
- 9 real bottle photos (phone photos converted from HEIC)
- 6 ChatGPT-generated fictional labels
- 23 programmatically generated with Python/Pillow

**Test cases:** 28 applications have deliberate errors (35 total) to test
the verification system — ABV mismatches, brand name variations, wrong
vintage years, etc.

### Files

```
htdocs/
  agent-view.html              Simulated government interface
  ttb-external/
    data/applicant/{sharded}/  Application JSON files
    images/                    Label images (front/back PNGs)

data/
  applications.tsv             Source of truth for all application data
```

---

## 2. Batch Processing System

**Directory:** `scripts/` — [Full documentation](readme-batch.md)

A Python pipeline that extracts text fields from label images. Intended to
run as a backend service, triggered by administrators or scheduled jobs.

### How it works

The system uses a **two-pass extraction approach**:

1. **Claude Vision API** — Reads text from labels (what it's good at)
2. **EasyOCR** — Returns precise bounding box coordinates (what vision LLMs are bad at)

Claude identifies what text says and which image it's on. EasyOCR provides
exact pixel locations. Fuzzy matching aligns the two, producing accurate
cropped images of each field.

A third verification pass runs OCR on the cropped images and compares
against Claude's extraction for an independent quality score.

### Operations dashboard

**File:** `htdocs/batch.html`

Web interface for monitoring batch processing:
- Service state toggle (Running/Stopped)
- Queue depth and throughput metrics
- Recent completions with thumbnails
- Activity log with performance events

**Testbed controls** (in the outer frame):
- **FORGET 5** — Reset 5 random apps for re-testing
- **FORGET ALL** — Wipe all processing data for fresh demo

### Files

```
scripts/
  Makefile                     Pipeline automation
  config.py                    Shared configuration
  paths.py                     Sharding utilities
  stats.py                     Processing statistics
  events.py                    Operational event log

  demoSetup/                   One-time setup scripts
    make_demo_db.py              Create SQLite DB from TSV
    export_applicant.py          Export applicant JSON files

  batchProcessor/              AI processing pipeline
    process_labels.py            Claude Vision + EasyOCR extraction
    verify_extractions.py        OCR verification pass
    export_extractions.py        Export results to verification API
    clear_processing.py          Reset all processing

  miniServer/
    api_server.py                HTTP API for web UI controls

htdocs/
  batch.html                   Operations dashboard
  verification/
    results/{sharded}/         AI extraction results (JSON)
    extractions/{sharded}/     Cropped field images (PNG)
    stats.json                 Processing statistics
    events.json                Operational event log
```

### Quick start

```bash
cd scripts
export ANTHROPIC_API_KEY="sk-ant-..."

make setup      # Create database and export applicant JSON
make process    # Run AI extraction (Claude Vision + EasyOCR)
```

See [readme-demoSetup.md](readme-demoSetup.md) for full setup instructions.

---

## 3. Label Verification App

**File:** `htdocs/app.html` — [Full documentation](readme-app.md)

The new AI-powered tool for human agents. Receives application data when
the agent clicks "Verify Label Images" and displays a verification report
comparing declared form values against AI-extracted label content.

### What it shows

**Status banner** — Green "Label Verified" or red "Issues Identified" with
count of items needing attention.

**Mandatory element checks** (presence verification):
- Government Warning — required on all labels ≥0.5% ABV
- Contains Sulfites — wine only
- Country of Origin — imports only

**Field verification table** (declared vs. label):
- Brand Name, Class/Type, Alcohol Content, Net Contents
- Bottler/Importer Name and Address
- Wine: vintage, varietal, appellation (if declared)
- Spirits: age statement (if declared)

Each field shows:
- What the applicant declared
- What the AI extracted from the label
- Cropped image of the relevant label region
- Review toggles (?, ✓, ✗) for agent decision

**Revision notes** — Dynamic guidance text for applicant correspondence,
generated based on which fields the agent marks as issues.

### Review workflow

1. Agent selects application in left panel
2. Clicks "Verify Label Images"
3. AI report appears in right panel
4. Agent reviews each flagged item, clicking ✓ or ✗
5. When all items reviewed, Copy button appears for revision notes

Review states persist in localStorage — agents can navigate away and return.

### Files

```
htdocs/
  app.html                     Label verification tool
  index.html                   Outer frame (two-panel layout)
```

The app fetches from two APIs:
- `/ttb-external/` — Simulated TTB system (applicant data, label images)
- `/verification/` — Our system (AI extraction results, cropped images)

---

## Running the Demo

The demo requires two terminal windows:

**Terminal 1 — Static file server:**
```bash
cd htdocs
python3 -m http.server 8080
```

**Terminal 2 — API server (for batch processing controls):**
```bash
cd scripts
export ANTHROPIC_API_KEY="sk-ant-..."
make api
```

Then open http://localhost:8080/ in your browser.

> The static server works without an API key (for viewing the UI only).
> The API server requires a key for batch processing.

See [readme-demoSetup.md](readme-demoSetup.md) for complete setup instructions.


## TTB Background

### Label submission formats

TTB accepts label images in several forms:
- Digital artwork files (most common via COLAs Online)
- Scans of printed labels
- Photographs of applied labels on containers

Per 27 CFR Part 13, labels must be "legible and in sufficient detail."
There is no strict format requirement — the key is readability. This
means agents routinely deal with widely varying image quality, which is
a core pain point that AI verification could address.

### Why this matters

The COLA registry processes 150,000-180,000 applications annually with
3-5 million historical records. Manual cross-referencing of form fields
against label images is time-consuming and error-prone. An AI assistant
that pre-flags mismatches and extracts relevant image regions could
significantly accelerate the review process while maintaining accuracy.
