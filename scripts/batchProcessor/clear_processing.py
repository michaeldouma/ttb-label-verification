#!/usr/bin/env python3
"""
Clear all processing results and reset applications to pending status.

===============================================================================
TAKE-HOME PROJECT FOR IT SPECIALIST POSITION
AI-Powered Alcohol Label Verification App
Michael Douma, February 2026
Developed with AI assistance (Claude)
===============================================================================

Description:
    Resets the batch processing pipeline to its initial state. Use this
    to re-run AI extraction from scratch or to clean up after testing.
    Essential for the demo workflow where stakeholders want to observe
    the full processing pipeline in action.

Inputs:
    - data/processing.db: SQLite database with processing state
    - output/extracted/*.png: Temporary mini-images
    - htdocs/verification/: API output directories

Actions:
    - Resets all processing_results rows to status='pending'
    - Deletes all extracted_fields records
    - Removes temporary mini-images from output/extracted/
    - Removes verification API output (results/ and extractions/)
    - Clears and resets stats.json with zero counts
    - Clears events.json and emits a "cleared" event

Outputs:
    - Database reset: All applications pending, no extracted fields
    - Filesystem cleaned: No mini-images or verification API output
    - Stats reset: summary shows 0 processed, N pending, 0 errors
    - Events log: Fresh log with single "cleared" event

Usage:
    cd scripts && python3 batchProcessor/clear_processing.py
    cd scripts && make clean

Created: February 2026
"""

import glob
import os
import shutil
import sqlite3
import sys

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PROCESSING_DB, OUTPUT_DIR, VERIFICATION_DIR
import stats
import events


def main():
    if not os.path.exists(PROCESSING_DB):
        print("processing.db not found. Run make_demo_db.py first.")
        return

    conn = sqlite3.connect(PROCESSING_DB)
    c = conn.cursor()

    # Reset processing_results to pending
    c.execute("UPDATE processing_results SET status='pending', processed_at=NULL, error_message=NULL")
    reset_count = c.rowcount

    # Clear extracted_fields
    c.execute("DELETE FROM extracted_fields")
    fields_deleted = c.rowcount

    conn.commit()
    conn.close()

    # Delete mini-images from temp output dir
    images_deleted = 0
    if os.path.exists(OUTPUT_DIR):
        for f in glob.glob(os.path.join(OUTPUT_DIR, "*.png")):
            os.remove(f)
            images_deleted += 1

    # Clear verification API output
    verification_cleared = 0
    results_dir = os.path.join(VERIFICATION_DIR, "results")
    extractions_dir = os.path.join(VERIFICATION_DIR, "extractions")

    for dir_path in [results_dir, extractions_dir]:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            verification_cleared += 1

    # Update stats - clear the log first so counts go to 0
    stats.clear_log()
    stats.update_summary(0, reset_count, 0)
    stats.log_action(None, "clear", f"Cleared {fields_deleted} fields, {images_deleted} images, reset {reset_count} apps to pending")

    # Clear events log and emit a cleared event
    events.clear_events()
    events.cleared(reset_count, fields_deleted, images_deleted)

    print(f"Reset {reset_count} apps to pending")
    print(f"Deleted {fields_deleted} extracted fields")
    print(f"Deleted {images_deleted} mini-images from temp dir")
    if verification_cleared:
        print(f"Cleared verification API output")


if __name__ == "__main__":
    main()
