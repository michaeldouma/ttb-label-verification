#!/usr/bin/env python3
"""
Export AI extraction data to the verification API for frontend access.

===============================================================================
TAKE-HOME PROJECT FOR IT SPECIALIST POSITION
AI-Powered Alcohol Label Verification App
Michael Douma, February 2026
Developed with AI assistance (Claude)
===============================================================================

Description:
    Exports processed extraction data from the SQLite database to the
    verification API's static file structure. This enables the web frontend
    (app.html) to fetch extraction results and display verification reports.

    Creates two types of output:
    - JSON files with extraction metadata (text, confidence, OCR scores)
    - PNG mini-images for visual verification of each extracted field

    Uses the same sharding scheme as the TTB external API for consistency
    and scalability. Example:
    TTB ID "24018001000301" → results/2/4/0/1/8/0/0/1/000301.json

Inputs:
    - data/processing.db: SQLite database with processed applications
    - output/extracted/*.png: Temporary mini-images from extraction

Actions:
    - Queries database for all processed applications
    - For each application:
        * Builds JSON with field text, confidence, OCR verification scores
        * Copies mini-images to sharded extraction directory
        * Sets imageUrl paths for frontend fetch
    - Provides export_one() function for real-time single-app export

Outputs:
    - htdocs/verification/results/{sharded}/*.json
      Contains: {status, fields: {fieldName: {text, confidence, ocrText,
                 ocrScore, imageUrl}, ...}}
    - htdocs/verification/extractions/{sharded}/{ttbId}/
      Contains: brandName.png, fancifulName.png, alcoholContent.png, etc.

Usage:
    cd scripts && python3 batchProcessor/export_extractions.py

Created: February 2026
"""

import json
import os
import shutil
import sqlite3
import sys

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PROCESSING_DB
from paths import (
    get_verification_result_path,
    get_extraction_image_dir,
    get_extraction_image_url,
    VERIFICATION_BASE,
)


def export_one(ttb_id: str, conn=None) -> int:
    """Export a single application's extraction data.

    Returns number of images copied.
    """
    close_conn = False
    if conn is None:
        conn = sqlite3.connect(PROCESSING_DB)
        close_conn = True

    # Ensure row_factory is set for dict-style access
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Get extracted fields for this app
    c.execute("""
        SELECT field_name, extracted_text, confidence,
               mini_image_path, ocr_text, ocr_match_score
        FROM extracted_fields
        WHERE ttbId = ?
    """, (ttb_id,))

    fields = {}
    for r in c.fetchall():
        field_name = r["field_name"]
        field_data = {
            "text": r["extracted_text"] or "",
            "confidence": r["confidence"] or 0,
            "ocrText": r["ocr_text"] or "",
            "ocrScore": r["ocr_match_score"] if r["ocr_match_score"] is not None else None,
            "side": "front",
        }
        if r["mini_image_path"] and os.path.exists(r["mini_image_path"]):
            field_data["_src_image"] = r["mini_image_path"]
            field_data["imageUrl"] = get_extraction_image_url(ttb_id, field_name)
        fields[field_name] = field_data

    if close_conn:
        conn.close()

    if not fields:
        return 0

    # Copy mini-images
    images_count = 0
    img_dir = get_extraction_image_dir(ttb_id)
    for field_name, field_data in fields.items():
        src_path = field_data.pop("_src_image", None)
        if src_path and os.path.exists(src_path):
            dst_path = os.path.join(img_dir, f"{field_name}.png")
            shutil.copy2(src_path, dst_path)
            images_count += 1

    # Write results JSON
    json_path = get_verification_result_path(ttb_id)
    with open(json_path, "w") as f:
        json.dump({"status": "processed", "fields": fields}, f, indent=2)

    return images_count


def main():
    conn = sqlite3.connect(PROCESSING_DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Get all processed applications
    c.execute("""
        SELECT a.ttbId, p.status
        FROM applications a
        LEFT JOIN processing_results p ON a.ttbId = p.ttbId
        WHERE p.status = 'processed'
    """)
    apps = {r["ttbId"]: {"fields": {}} for r in c.fetchall()}

    # Get all extracted fields
    c.execute("""
        SELECT ttbId, field_name, extracted_text, confidence,
               mini_image_path, ocr_text, ocr_match_score
        FROM extracted_fields
    """)

    for r in c.fetchall():
        ttb_id = r["ttbId"]
        if ttb_id not in apps:
            continue

        field_name = r["field_name"]

        # Side is stored in extracted_fields table, default to front if unknown
        # Note: TTB allows fields on ANY label, so we don't enforce sides
        side = "front"  # Will be overwritten by actual data if available

        # Build field data with imageUrl instead of base64
        field_data = {
            "text": r["extracted_text"] or "",
            "confidence": r["confidence"] or 0,
            "ocrText": r["ocr_text"] or "",
            "ocrScore": r["ocr_match_score"] if r["ocr_match_score"] is not None else None,
            "side": side,
        }

        # Store mini_image_path for later copying
        if r["mini_image_path"] and os.path.exists(r["mini_image_path"]):
            field_data["_src_image"] = r["mini_image_path"]
            field_data["imageUrl"] = get_extraction_image_url(ttb_id, field_name)

        apps[ttb_id]["fields"][field_name] = field_data

    conn.close()

    # Export to verification API
    results_count = 0
    images_count = 0

    for ttb_id, data in apps.items():
        if not data["fields"]:
            continue

        # Copy mini-images to extractions directory
        img_dir = get_extraction_image_dir(ttb_id)
        for field_name, field_data in data["fields"].items():
            src_path = field_data.pop("_src_image", None)
            if src_path and os.path.exists(src_path):
                dst_path = os.path.join(img_dir, f"{field_name}.png")
                shutil.copy2(src_path, dst_path)
                images_count += 1

        # Write results JSON
        json_path = get_verification_result_path(ttb_id)
        with open(json_path, "w") as f:
            json.dump({"status": "processed", "fields": data["fields"]}, f, indent=2)
        results_count += 1

    print(f"Exported {results_count} result files to {VERIFICATION_BASE}/results/")
    print(f"Copied {images_count} extraction images to {VERIFICATION_BASE}/extractions/")


if __name__ == "__main__":
    main()
