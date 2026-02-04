#!/usr/bin/env python3
"""
Process pending COLA label images via Claude Vision API + EasyOCR.

===============================================================================
TAKE-HOME PROJECT FOR IT SPECIALIST POSITION
AI-Powered Alcohol Label Verification App
Michael Douma, February 2026
Developed with AI assistance (Claude)
===============================================================================

Description:
    Core extraction pipeline implementing a two-pass approach for accurate
    label text extraction and cropping:

    Pass 1 - Claude Vision API: Extracts field TEXT with high accuracy.
             Claude excels at reading text from curved bottles, decorative
             fonts, and challenging label designs.

    Pass 2 - EasyOCR: Provides precise bounding box coordinates for each
             text region. Vision LLMs are unreliable for pixel coordinates,
             so we use traditional OCR for geometry.

    The script fuzzy-matches Claude's extracted text against OCR regions
    to locate the exact pixel coordinates, then crops mini-images with
    rotation correction for visual verification.

Inputs:
    - data/processing.db: SQLite database with pending applications
    - htdocs/ttb-external/images/*.png: Label images (front and back)
    - Environment: ANTHROPIC_API_KEY for Claude API access

Actions:
    - Queries database for pending applications
    - Sends front+back label images to Claude Vision for text extraction
    - Runs EasyOCR on both images for bounding box detection
    - Fuzzy-matches Claude text to OCR regions (handles OCR errors like I→1)
    - Crops mini-images with padding and rotation correction
    - Updates database with extracted fields and mini-image paths
    - Exports results immediately for real-time UI updates
    - Supports graceful stop via STOP file signal

Outputs:
    - Database updates: extracted_fields table with text, confidence, bbox
    - output/extracted/{ttbId}_{fieldName}.png: Cropped mini-images
    - htdocs/verification/stats.json: Real-time processing statistics
    - htdocs/verification/events.json: Operational event log

Usage:
    cd scripts && python3 batchProcessor/process_labels.py
    cd scripts && python3 batchProcessor/process_labels.py --limit 5
    cd scripts && python3 batchProcessor/process_labels.py --ttb-id 24001001000101

Created: February 2026
"""

import argparse
import base64
import json
import math
import os
import sqlite3
import sys
from datetime import datetime, timezone
from difflib import SequenceMatcher

import anthropic
import easyocr
import numpy as np
from PIL import Image, ImageOps

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    ANTHROPIC_MODEL,
    PROCESSING_DB,
    IMAGES_DIR,
    OUTPUT_DIR,
    VERIFY_FIELDS,
    STOP_FILE,
)
import stats
import events
from batchProcessor.export_extractions import export_one

# ── Vision prompt: text extraction only, no bboxes ──

VISION_PROMPT = """You are analyzing alcohol beverage label images for a U.S. TTB (Alcohol and Tobacco Tax and Trade Bureau) COLA application.

Extract the following fields with EXACT case-accurate text as printed on the label.

IMPORTANT: Fields may appear on ANY label (front, back, side, neck). Search ALL images thoroughly for each field.

CORE FIELDS (all products):

1. **brandName** — The brand name. Usually the most prominent text.

2. **fancifulName** — The product's COMPLETE fanciful/descriptive name (NOT the brand).
   - Include the FULL name: "L'UNIQUE LIQUEUR" not just "LIQUEUR"
   - Include modifiers: "EXTRA DRY VERMOUTH" not just "EXTRA DRY"
   - Include full product descriptors: "SÉLECTION APPLE BRANDY" not just "SÉLECTION"

3. **alcoholContent** — The alcohol percentage statement AS PRINTED, but:
   - DO NOT include the word "Alcohol" if it appears as a prefix
   - Examples: "12.5% ALC. BY VOL.", "ALC 40% BY VOL", "14% BY VOLUME"
   - Note: "ABV" abbreviation is not TTB-compliant

4. **netContents** — The PRIMARY volume/size only:
   - Extract: "750 ML", "1 LITER", "750ml"
   - DO NOT include equivalent measures in parentheses like "(25.4 FL OZ)" or "33.8 oz."

5. **classTypeCode** — The product class/type (e.g. "CHARDONNAY", "STRAIGHT RYE WHISKY", "ALE").

6. **governmentWarning** — The COMPLETE health warning text starting with "GOVERNMENT WARNING:" (must be present in capitals). Extract the full warning including both pregnancy and machinery statements.

7. **bottlerName** — The company name ONLY:
   - DO NOT include prefixes like "Imported by", "Bottled by", "Produced by", "Distributed by"
   - DO NOT include the address (city, state, country)
   - Example: Extract "SHAW-ROSS INTERNATIONAL IMPORTERS" not "Imported by Shaw-Ross International Importers, Miramar, FL"

8. **bottlerAddress** — The bottler's city and state ONLY (e.g. "NAPA, CA", "MIRAMAR, FL").

9. **sulfites** — Sulfite declaration if present. Look for these patterns:
   - "Contains Sulfites"
   - "Contains Sulphites" (British spelling)
   - "Contains (a) Sulfiting Agent(s)"
   - "Naturally Occurring Sulfites"
   - Often appears in small text near the government warning or alcohol content

10. **countryOfOrigin** — Country of origin statement. LOOK CAREFULLY for:
    - "Product of [COUNTRY]" or "Produce of [COUNTRY]"
    - "Wine of [COUNTRY]"
    - "Made in [COUNTRY]"
    - "Imported from [COUNTRY]"
    - "[PRODUCT] of [COUNTRY]" (e.g. "Beer of Mexico")
    - Often in small text on back label

WINE-SPECIFIC FIELDS (if wine):
11. **wineVintage** — The vintage year if present (e.g. "2019", "2021").
12. **grapeVarietal** — The grape variety if present (e.g. "CHARDONNAY", "CABERNET SAUVIGNON").
13. **wineAppellation** — The appellation/region if present (e.g. "NAPA VALLEY", "BORDEAUX").

SPIRITS-SPECIFIC FIELD (if spirits):
14. **ageStatement** — Age statement if present (e.g. "AGED 12 YEARS", "4 YEARS OLD").

For EACH field found, return:
- "field_name": the field key from above
- "extracted_text": exact text as printed, preserving case and punctuation
- "image_side": "front" or "back" (which image you found it on)
- "confidence": 0.0 to 1.0

Return ONLY a JSON array. Include only fields that are visible on the labels."""


# ── EasyOCR reader (lazy singleton) ──

_ocr_reader = None


def get_ocr_reader() -> easyocr.Reader:
    global _ocr_reader
    if _ocr_reader is None:
        _ocr_reader = easyocr.Reader(["en"], gpu=False, verbose=False)
    return _ocr_reader


# ── OCR the image and get word-level bounding boxes ──

def ocr_image(image_path: str) -> list[dict]:
    """Run EasyOCR on an image and return list of {text, bbox_polygon, confidence}.

    bbox_polygon is [[x1,y1], [x2,y2], [x3,y3], [x4,y4]] — four corners.
    """
    if not image_path or not os.path.exists(image_path):
        return []

    reader = get_ocr_reader()
    results = reader.readtext(image_path)

    ocr_items = []
    for bbox_polygon, text, conf in results:
        coords = [[int(p) for p in pt] for pt in bbox_polygon]
        ocr_items.append({"text": text, "bbox_polygon": coords, "confidence": conf})

    return ocr_items


# ── Match extracted field text to OCR regions ──

def normalize(s: str) -> str:
    """Normalize text for fuzzy matching — strip punctuation and collapse whitespace."""
    import re
    s = s.upper()
    # Replace common OCR confusions and punctuation with canonical forms
    s = re.sub(r"[./,;:_|!']", "", s)
    return " ".join(s.split())


def find_ocr_regions_for_field(field_text: str, ocr_items: list[dict], min_similarity: float = 0.3) -> list[dict]:
    """Find OCR regions that match the extracted field text.

    For short fields (brand, alc content), we look for the best matching single
    or consecutive group of OCR items.
    For long fields (qualifications), we gather all matching items.

    Returns list of matching OCR items.
    """
    if not field_text or not ocr_items:
        return []

    field_norm = normalize(field_text)
    field_words = field_norm.split()

    # Score each OCR item by how much of its text appears in the field text
    scored_items = []
    for i, item in enumerate(ocr_items):
        item_norm = normalize(item["text"])
        if not item_norm:
            continue

        # Check if OCR text appears in the field text
        if item_norm in field_norm:
            score = len(item_norm) / max(len(field_norm), 1)
            scored_items.append((i, score, item))
        else:
            # Fuzzy match at string level
            ratio = SequenceMatcher(None, item_norm, field_norm).ratio()

            # Word-level fuzzy matching (handles OCR char errors like I8→18)
            item_words = item_norm.split()
            fuzzy_word_matches = 0
            for iw in item_words:
                for fw in field_words:
                    if SequenceMatcher(None, iw, fw).ratio() > 0.6:
                        fuzzy_word_matches += 1
                        break
            word_score = fuzzy_word_matches / max(len(item_words), 1)

            score = max(ratio * 0.6, word_score * 0.8)
            if score >= min_similarity:
                scored_items.append((i, score, item))

    if not scored_items:
        return []

    # Sort by position in the image (top-to-bottom, left-to-right)
    scored_items.sort(key=lambda x: (x[2]["bbox_polygon"][0][1], x[2]["bbox_polygon"][0][0]))

    # For short fields, try to find the best contiguous group
    if len(field_words) <= 6:
        # Find best single item or pair
        best_score = 0
        best_items = []
        for idx, score, item in scored_items:
            if score > best_score:
                best_score = score
                best_items = [item]

        # Also try consecutive pairs/triples from the scored items
        for i in range(len(scored_items)):
            for j in range(i + 1, min(i + 4, len(scored_items) + 1)):
                group = [s[2] for s in scored_items[i:j]]
                combined = " ".join(normalize(it["text"]) for it in group)
                ratio = SequenceMatcher(None, combined, field_norm).ratio()
                if ratio > best_score:
                    best_score = ratio
                    best_items = group

        return best_items

    # For long fields (qualifications), return all matching items
    return [item for _, _, item in scored_items]


def compute_text_angle(polygon: list) -> float:
    """Compute the rotation angle of text from its EasyOCR polygon.

    EasyOCR returns 4 points: [top-left, top-right, bottom-right, bottom-left].
    The angle of the top edge tells us the text rotation.

    Returns angle in degrees (0 = horizontal, 90 = vertical reading bottom-to-top).
    """
    # Top-left and top-right points define the text baseline direction
    tl, tr = polygon[0], polygon[1]
    dx = tr[0] - tl[0]
    dy = tr[1] - tl[1]

    # atan2 gives angle from horizontal: 0° = right, 90° = down, -90° = up
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)

    return angle_deg


def merge_bboxes(ocr_items: list[dict]) -> dict:
    """Merge multiple OCR bounding boxes into one enclosing bbox.

    Returns {x, y, w, h, rotation_degrees}.

    Rotation detection: compute average text angle from individual OCR items.
    If the average angle is significantly non-zero (~90° or ~-90°), rotate.
    """
    if not ocr_items:
        return None

    all_points = []
    angles = []

    for item in ocr_items:
        for pt in item["bbox_polygon"]:
            all_points.append(pt)
        # Compute text angle for each OCR item
        angle = compute_text_angle(item["bbox_polygon"])
        angles.append(angle)

    all_points = np.array(all_points)
    x_min = int(all_points[:, 0].min())
    y_min = int(all_points[:, 1].min())
    x_max = int(all_points[:, 0].max())
    y_max = int(all_points[:, 1].max())

    w = x_max - x_min
    h = y_max - y_min

    # Compute average angle across all OCR items
    avg_angle = sum(angles) / len(angles) if angles else 0.0

    # Determine rotation needed to make text horizontal
    # Angles near 90° or -90° indicate vertical text
    rotation = 0.0
    if abs(avg_angle) > 45:
        # Text is more vertical than horizontal
        # Round to nearest 90° for clean rotation
        rotation = 90.0 if avg_angle > 0 else -90.0

    return {
        "x": x_min,
        "y": y_min,
        "w": w,
        "h": h,
        "rotation_degrees": rotation,
    }


# ── Image cropping with rotation handling ──

def crop_region(image_path: str, bbox: dict, output_path: str, padding_px: int = 8):
    """Crop a region from the image with padding, de-rotate if needed."""
    if not os.path.exists(image_path):
        return False

    img = Image.open(image_path)
    img_w, img_h = img.size

    x, y, w, h = bbox["x"], bbox["y"], bbox["w"], bbox["h"]
    rotation = bbox.get("rotation_degrees", 0)

    # Add fixed pixel padding
    pad = padding_px
    if rotation and abs(rotation) > 1:
        # Extra padding for rotated text
        pad += int(max(w, h) * abs(math.sin(math.radians(rotation))) * 0.3)

    x1 = max(0, x - pad)
    y1 = max(0, y - pad)
    x2 = min(img_w, x + w + pad)
    y2 = min(img_h, y + h + pad)

    if x2 - x1 <= 0 or y2 - y1 <= 0:
        return False

    cropped = img.crop((x1, y1, x2, y2))

    # De-rotate if text is significantly rotated
    if rotation and abs(rotation) > 0.5:
        if cropped.mode != "RGBA":
            cropped = cropped.convert("RGBA")
        rotated = cropped.rotate(-rotation, expand=True, resample=Image.BICUBIC)
        bg = Image.new("RGB", rotated.size, (255, 255, 255))
        bg.paste(rotated, mask=rotated.split()[3])
        cropped = bg

    # Ensure RGB
    if cropped.mode == "RGBA":
        bg = Image.new("RGB", cropped.size, (255, 255, 255))
        bg.paste(cropped, mask=cropped.split()[3])
        cropped = bg

    # Apply auto-contrast (blend 50% with original to avoid over-processing)
    try:
        enhanced = ImageOps.autocontrast(cropped, cutoff=1)
        cropped = Image.blend(cropped, enhanced, alpha=0.5)
    except Exception:
        pass  # Skip if auto-contrast fails (e.g., single-color image)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cropped.save(output_path)
    return True


# ── Claude Vision API ──

def encode_image(path: str) -> tuple[str, str]:
    ext = os.path.splitext(path)[1].lower()
    media_types = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
    media_type = media_types.get(ext, "image/png")
    with open(path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("ascii")
    return data, media_type


def call_vision_api(client: anthropic.Anthropic, front_path: str | None, back_path: str | None) -> list[dict]:
    """Send label images to Claude Vision for text extraction only."""
    content = []

    for label, path in [("FRONT LABEL", front_path), ("BACK LABEL", back_path)]:
        if path and os.path.exists(path):
            data, media_type = encode_image(path)
            content.append({"type": "text", "text": f"{label}:"})
            content.append({
                "type": "image",
                "source": {"type": "base64", "media_type": media_type, "data": data},
            })

    if not content:
        return []

    content.append({"type": "text", "text": VISION_PROMPT})

    import time as _time
    api_start = _time.time()
    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": content}],
    )
    api_elapsed = _time.time() - api_start
    events.api_response(api_elapsed)

    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

    return json.loads(text)


# ── Main processing ──

def process_one(client: anthropic.Anthropic, conn: sqlite3.Connection, ttb_id: str, front_img: str, back_img: str):
    """Process a single application: Claude Vision → EasyOCR → crop."""
    c = conn.cursor()
    c.execute("UPDATE processing_results SET status='processing' WHERE ttbId=?", (ttb_id,))
    conn.commit()

    front_path = os.path.join(IMAGES_DIR, front_img) if front_img else None
    back_path = os.path.join(IMAGES_DIR, back_img) if back_img else None

    # Step 1: Claude Vision extracts field text
    try:
        fields = call_vision_api(client, front_path, back_path)
    except anthropic.APITimeoutError as e:
        c.execute(
            "UPDATE processing_results SET status='error', processed_at=?, error_message=? WHERE ttbId=?",
            (datetime.now(timezone.utc).isoformat(), str(e), ttb_id),
        )
        conn.commit()
        events.api_timeout(str(e))
        log_to_stats(ttb_id, "error", str(e))
        print(f"  ERROR (timeout): {e}")
        return
    except Exception as e:
        c.execute(
            "UPDATE processing_results SET status='error', processed_at=?, error_message=? WHERE ttbId=?",
            (datetime.now(timezone.utc).isoformat(), str(e), ttb_id),
        )
        conn.commit()
        events.api_error(str(e))
        log_to_stats(ttb_id, "error", str(e))
        print(f"  ERROR (vision): {e}")
        return

    # Step 2: OCR both images for precise bounding boxes
    print("  Running OCR...")
    front_ocr = ocr_image(front_path)
    back_ocr = ocr_image(back_path)

    # Step 3: For each field, match text to OCR regions and crop
    extracted_count = 0
    for field in fields:
        field_name = field.get("field_name", "")
        if field_name not in VERIFY_FIELDS:
            continue

        extracted_text = field.get("extracted_text", "")

        # Don't enforce field locations — TTB allows fields on ANY label
        # Use the side Claude detected, but fall back to other side if no OCR match
        image_side = field.get("image_side", "front")

        if image_side == "back" and back_path:
            source_path = back_path
            ocr_items = back_ocr
        else:
            source_path = front_path
            ocr_items = front_ocr

        # Try to find OCR match on detected side
        matching_regions = find_ocr_regions_for_field(extracted_text, ocr_items)

        # If no match, try the other image
        if not matching_regions:
            alt_ocr = front_ocr if image_side == "back" else back_ocr
            alt_path = front_path if image_side == "back" else back_path
            if alt_path and alt_ocr:
                alt_regions = find_ocr_regions_for_field(extracted_text, alt_ocr)
                if alt_regions:
                    matching_regions = alt_regions
                    source_path = alt_path
                    image_side = "front" if image_side == "back" else "back"

        merged_bbox = merge_bboxes(matching_regions) if matching_regions else None
        rotation = merged_bbox["rotation_degrees"] if merged_bbox else 0

        mini_path = os.path.join(OUTPUT_DIR, f"{ttb_id}_{field_name}.png")
        saved = False

        if merged_bbox and source_path and os.path.exists(source_path):
            try:
                saved = crop_region(source_path, merged_bbox, mini_path)
            except Exception as e:
                print(f"  Crop error for {field_name}: {e}")

        bbox_json = json.dumps([merged_bbox["x"], merged_bbox["y"], merged_bbox["w"], merged_bbox["h"]]) if merged_bbox else None

        c.execute(
            """INSERT INTO extracted_fields
               (ttbId, field_name, extracted_text, confidence, mini_image_path, region_bbox, rotation_degrees)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                ttb_id,
                field_name,
                extracted_text,
                field.get("confidence", 0),
                mini_path if saved else None,
                bbox_json,
                rotation,
            ),
        )
        extracted_count += 1
        match_status = f"matched {len(matching_regions)} OCR regions" if matching_regions else "NO OCR MATCH"
        print(f"  {field_name}: \"{extracted_text[:50]}\" ({match_status}, side={image_side})")

    now = datetime.now(timezone.utc).isoformat()
    c.execute(
        "UPDATE processing_results SET status='processed', processed_at=? WHERE ttbId=?",
        (now, ttb_id),
    )
    conn.commit()
    log_to_stats(ttb_id, "processed", f"Extracted {extracted_count} fields")


def log_to_stats(ttb_id: str, action: str, message: str):
    """Log action to stats.json."""
    stats.log_action(ttb_id, action, message)


def update_stats_summary():
    """Update summary counts in stats.json."""
    if not os.path.exists(PROCESSING_DB):
        return

    conn = sqlite3.connect(PROCESSING_DB)
    c = conn.cursor()
    c.execute("SELECT status, COUNT(*) FROM processing_results GROUP BY status")
    counts = dict(c.fetchall())
    conn.close()

    stats.update_summary(
        counts.get("processed", 0),
        counts.get("pending", 0),
        counts.get("error", 0),
    )


def main():
    import time

    parser = argparse.ArgumentParser(description="Process pending COLA label images")
    parser.add_argument("--limit", type=int, default=0, help="Max apps to process (0=all)")
    parser.add_argument("--ttb-id", type=str, help="Process single TTB ID (reprocess even if already done)")
    args = parser.parse_args()

    if not os.path.exists(PROCESSING_DB):
        print("processing.db not found. Run make_demo_db.py first.")
        return

    total_start = time.time()

    client = anthropic.Anthropic()

    conn = sqlite3.connect(PROCESSING_DB)
    c = conn.cursor()

    if args.ttb_id:
        # Process single application (reprocess even if already done)
        c.execute(
            "SELECT ttbId, front_image_path, back_image_path FROM applications WHERE ttbId = ?",
            (args.ttb_id,)
        )
        row = c.fetchone()
        if not row:
            print(f"TTB ID {args.ttb_id} not found in database")
            return
        # Reset status to pending so it gets reprocessed
        c.execute("UPDATE processing_results SET status = 'pending' WHERE ttbId = ?", (args.ttb_id,))
        # Clear existing extracted fields
        c.execute("DELETE FROM extracted_fields WHERE ttbId = ?", (args.ttb_id,))
        conn.commit()
        pending = [row]
    else:
        query = """
            SELECT a.ttbId, a.front_image_path, a.back_image_path
            FROM applications a
            JOIN processing_results p ON a.ttbId = p.ttbId
            WHERE p.status = 'pending'
        """
        if args.limit > 0:
            query += f" LIMIT {args.limit}"

        c.execute(query)
        pending = c.fetchall()

    print(f"Found {len(pending)} pending applications")

    # Emit batch_started event (only if there's work to do)
    if pending:
        events.batch_started(len(pending))
        events.reset_api_state()

    app_times = []
    error_count = 0
    stopped_early = False

    for i, (ttb_id, front_img, back_img) in enumerate(pending, 1):
        # Check for stop signal before each label
        if os.path.exists(STOP_FILE):
            print(f"\n*** STOP file detected - halting after {i-1} applications ***")
            events.processing_stopped(i - 1, len(pending) - (i - 1))
            stopped_early = True
            break

        app_start = time.time()
        print(f"[{i}/{len(pending)}] Processing {ttb_id}...")
        process_one(client, conn, ttb_id, front_img or "", back_img or "")

        # Export this app's data immediately so it's available in the UI
        export_one(ttb_id, conn)

        app_elapsed = time.time() - app_start
        app_times.append(app_elapsed)
        print(f"  ⏱ {app_elapsed:.1f}s for this app")

        # Update stats after each app for real-time UI feedback
        update_stats_summary()

    # Count errors from this batch
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM processing_results WHERE status='error'")
    error_count = c.fetchone()[0]
    conn.close()

    # Clean up stop file if we created it
    if stopped_early and os.path.exists(STOP_FILE):
        os.remove(STOP_FILE)

    total_elapsed = time.time() - total_start

    # Emit batch_complete event (only if we processed something)
    if app_times and not stopped_early:
        events.batch_complete(len(app_times), total_elapsed, error_count)

    print(f"\n{'='*50}")
    print(f"TIMING SUMMARY")
    print(f"{'='*50}")
    print(f"Total applications: {len(pending)}")
    print(f"Total time: {total_elapsed:.1f}s ({total_elapsed/60:.1f} min)")
    if app_times:
        print(f"Average per app: {sum(app_times)/len(app_times):.1f}s")
        print(f"Min/Max: {min(app_times):.1f}s / {max(app_times):.1f}s")
    print("Done.")


if __name__ == "__main__":
    main()
