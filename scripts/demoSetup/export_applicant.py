#!/usr/bin/env python3
"""
Export applicant data (declared form values) to sharded JSON files.

===============================================================================
TAKE-HOME PROJECT FOR IT SPECIALIST POSITION
AI-Powered Alcohol Label Verification App
Michael Douma, February 2026
Developed with AI assistance (Claude)
===============================================================================

Description:
    Exports COLA application form data to a sharded static API structure.
    This creates the "ground truth" data representing what the applicant
    declared on their COLA form, which the verification system compares
    against AI-extracted label text.

    Example: TTB ID "24001001000101" creates:
    htdocs/ttb-external/data/applicant/2/4/0/0/1/0/0/1/000101.json

Inputs:
    - data/applications.tsv: Master data file with all COLA applications

Actions:
    - Reads applications.tsv using csv.DictReader
    - For each application, builds a JSON object with all form fields
    - Creates sharded directory structure (8 levels deep + filename)
    - Writes individual JSON files for each TTB ID

Outputs:
    - htdocs/ttb-external/data/applicant/{sharded}/*.json
      One JSON file per application containing:
      - Core fields: ttbId, brandName, fancifulName, alcoholContent, etc.
      - Label images: {front, back} paths
      - Wine-specific: wineVintage, grapeVarietal, wineAppellation
      - Spirits-specific: ageStatement

Usage:
    cd scripts && python3 demoSetup/export_applicant.py

Created: February 2026
"""

import csv
import json
import os
import sys

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ensure_sharded_dir, API_BASE

SCRIPTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(SCRIPTS_DIR)
TSV_PATH = os.path.join(BASE_DIR, "data", "applications.tsv")


def main():
    if not os.path.exists(TSV_PATH):
        print(f"applications.tsv not found at {TSV_PATH}")
        return

    count = 0
    with open(TSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            ttb_id = row.get("ttbId", "").strip()
            if not ttb_id:
                continue

            # Build applicant data object (declared form values)
            applicant_data = {
                "ttbId": ttb_id,
                "vendorCode": row.get("vendorCode", ""),
                "serialNumber": row.get("serialNumber", ""),
                "appType": row.get("appType", ""),
                "classTypeCode": row.get("classTypeCode", ""),
                "classTypeDesc": row.get("classTypeDesc", ""),
                "originCode": row.get("originCode", ""),
                "originDesc": row.get("originDesc", ""),
                "brandName": row.get("brandName", ""),
                "dbaName": row.get("dbaName", ""),
                "fancifulName": row.get("fancifulName", ""),
                "alcoholContent": row.get("alcoholContent", ""),
                "netContents": row.get("netContents", ""),
                "plantRegistry": row.get("plantRegistry", ""),
                "permitNumber": row.get("permitNumber", ""),
                "applicantName": row.get("applicantName", ""),
                "applicantAddress": row.get("applicantAddress", ""),
                "qualifications": row.get("qualifications", ""),
                # Label images as nested object (matches agent-view.html expectations)
                "labelImages": {
                    "front": row.get("labelImageFront", ""),
                    "back": row.get("labelImageBack", ""),
                },
                # Wine-specific fields
                "wineVintage": row.get("wineVintage", ""),
                "grapeVarietal": row.get("grapeVarietal", ""),
                "wineAppellation": row.get("wineAppellation", ""),
                "ageStatement": row.get("ageStatement", ""),
            }

            # Write to sharded path
            json_path = ensure_sharded_dir(ttb_id, "applicant")
            with open(json_path, "w") as out:
                json.dump(applicant_data, out, indent=2)
            count += 1

    print(f"Exported {count} applicant files to htdocs/ttb-external/data/applicant/")


if __name__ == "__main__":
    main()
