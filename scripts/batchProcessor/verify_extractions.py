#!/usr/bin/env python3
"""
Run OCR verification on cropped mini-images to validate extraction accuracy.

===============================================================================
TAKE-HOME PROJECT FOR IT SPECIALIST POSITION
AI-Powered Alcohol Label Verification App
Michael Douma, February 2026
Developed with AI assistance (Claude)
===============================================================================

Description:
    Third-pass quality verification for the extraction pipeline. Runs EasyOCR
    on each cropped mini-image and compares the result against Claude's
    extracted text. This provides an independent accuracy score since
    Claude's self-reported confidence is unreliable (often 95%+ even when wrong).

    The verification score indicates whether the mini-image crop actually
    contains the expected text, catching cases where:
    - OCR bounding box matching found the wrong region
    - The text was misread by Claude
    - The crop captured adjacent text instead

Inputs:
    - data/processing.db: Database with extracted_fields records
    - output/extracted/*.png: Cropped mini-images from extraction pass

Actions:
    - Adds ocr_text and ocr_match_score columns if missing (idempotent)
    - For each extracted field:
        * Runs EasyOCR on the mini-image
        * Normalizes both Claude and OCR text (strip punctuation, uppercase)
        * Computes fuzzy match score using SequenceMatcher
    - Flags low-match fields (< 50%) with detailed comparison output
    - Prints summary statistics

Outputs:
    - Database updates: ocr_text and ocr_match_score in extracted_fields
    - Console output: Per-field scores and summary statistics

Usage:
    cd scripts && python3 batchProcessor/verify_extractions.py

Created: February 2026
"""

import os
import re
import sqlite3
import sys
from difflib import SequenceMatcher

import easyocr

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PROCESSING_DB

_reader = None

def get_reader():
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(["en"], gpu=False, verbose=False)
    return _reader


def normalize(s: str) -> str:
    s = s.upper()
    s = re.sub(r"[./,;:_|!'\-\"\(\)]", "", s)
    return " ".join(s.split())


def ocr_mini_image(path: str) -> str:
    """OCR a mini-image and return combined text."""
    if not path or not os.path.exists(path):
        return ""
    reader = get_reader()
    results = reader.readtext(path)
    return " ".join(text for _, text, _ in results)


def match_score(extracted: str, ocr_text: str) -> float:
    """Fuzzy match score between Claude's extraction and OCR of the crop."""
    if not extracted and not ocr_text:
        return 1.0
    if not extracted or not ocr_text:
        return 0.0
    a = normalize(extracted)
    b = normalize(ocr_text)
    return SequenceMatcher(None, a, b).ratio()


def main():
    conn = sqlite3.connect(PROCESSING_DB)
    c = conn.cursor()

    # Add columns if they don't exist
    try:
        c.execute("ALTER TABLE extracted_fields ADD COLUMN ocr_text TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        c.execute("ALTER TABLE extracted_fields ADD COLUMN ocr_match_score REAL")
    except sqlite3.OperationalError:
        pass
    conn.commit()

    c.execute("SELECT id, ttbId, field_name, extracted_text, mini_image_path FROM extracted_fields")
    rows = c.fetchall()

    print(f"Verifying {len(rows)} extracted fields...")

    for row_id, ttb_id, field_name, extracted_text, mini_path in rows:
        ocr_text = ocr_mini_image(mini_path)
        score = match_score(extracted_text or "", ocr_text)

        c.execute(
            "UPDATE extracted_fields SET ocr_text=?, ocr_match_score=? WHERE id=?",
            (ocr_text, score, row_id),
        )

        flag = "" if score >= 0.5 else " *** LOW MATCH"
        print(f"  {ttb_id} {field_name}: {score:.0%}{flag}")
        if score < 0.5:
            print(f"    Claude: {(extracted_text or '')[:80]}")
            print(f"    OCR:    {ocr_text[:80]}")

    conn.commit()
    conn.close()

    # Summary
    conn = sqlite3.connect(PROCESSING_DB)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM extracted_fields WHERE ocr_match_score IS NOT NULL")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM extracted_fields WHERE ocr_match_score >= 0.5")
    good = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM extracted_fields WHERE mini_image_path IS NULL")
    no_crop = c.fetchone()[0]
    conn.close()

    print(f"\nSummary: {good}/{total} fields matched ({good/total:.0%}), {no_crop} had no crop")


if __name__ == "__main__":
    main()
