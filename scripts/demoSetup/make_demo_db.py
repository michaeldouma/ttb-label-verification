#!/usr/bin/env python3
"""
Create processing.db SQLite database from applications.tsv.

===============================================================================
TAKE-HOME PROJECT FOR IT SPECIALIST POSITION
AI-Powered Alcohol Label Verification App
Michael Douma, February 2026
Developed with AI assistance (Claude)
===============================================================================

Description:
    Initializes the SQLite database that drives the batch processing pipeline.
    Parses the master applications.tsv file and creates the database schema
    with tables for applications, processing status, and extracted fields.

Inputs:
    - data/applications.tsv: Tab-separated values containing all COLA
      application data (TTB ID, brand name, alcohol content, label images, etc.)

Actions:
    - Parses applications.tsv using Python's csv.DictReader
    - Creates fresh SQLite database (removes existing if present)
    - Creates three tables:
        * applications: All COLA application form data
        * processing_results: Tracks processing status per application
        * extracted_fields: Stores AI-extracted text and mini-image paths
    - Inserts all applications with status='pending'

Outputs:
    - data/processing.db: SQLite database with schema ready for batch processing

Usage:
    cd scripts && python3 demoSetup/make_demo_db.py

Created: February 2026
"""

import csv
import os
import sqlite3
import sys

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PROCESSING_DB, DATA_DIR

SCRIPTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(SCRIPTS_DIR)
TSV_PATH = os.path.join(BASE_DIR, "data", "applications.tsv")


def parse_applications_tsv(path: str) -> list[dict]:
    """Parse the TSV file into a list of dicts."""
    apps = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            ttb_id = row.get("ttbId", "").strip()
            if not ttb_id:
                continue

            # Build app dict matching expected format
            app = {
                "id": ttb_id,
                "ttbId": ttb_id,
                "status": "PENDING REVIEW",
                "vendorCode": row.get("vendorCode", ""),
                "serialNumber": row.get("serialNumber", ""),
                "classTypeCode": row.get("classTypeCode", ""),
                "classTypeDesc": row.get("classTypeDesc", ""),
                "originCode": row.get("originCode", ""),
                "originDesc": row.get("originDesc", ""),
                "brandName": row.get("brandName", ""),
                "dbaName": row.get("dbaName", ""),
                "fancifulName": row.get("fancifulName", ""),
                "appType": row.get("appType", ""),
                "plantRegistry": row.get("plantRegistry", ""),
                "permitNumber": row.get("permitNumber", ""),
                "applicantName": row.get("applicantName", ""),
                "applicantAddress": row.get("applicantAddress", ""),
                "approvalDate": "",
                "expirationDate": "",
                "alcoholContent": row.get("alcoholContent", ""),
                "netContents": row.get("netContents", ""),
                "qualifications": row.get("qualifications", ""),
                "processedDate": "",
                "labelImages": {
                    "front": row.get("labelImageFront", ""),
                    "back": row.get("labelImageBack", ""),
                },
                # Wine-specific
                "wineVintage": row.get("wineVintage", ""),
                "grapeVarietal": row.get("grapeVarietal", ""),
                "wineAppellation": row.get("wineAppellation", ""),
                # Spirits-specific
                "ageStatement": row.get("ageStatement", ""),
            }
            apps.append(app)
    return apps


APP_COLUMNS = [
    "id", "ttbId", "status", "vendorCode", "serialNumber",
    "classTypeCode", "classTypeDesc", "originCode", "originDesc",
    "brandName", "dbaName", "fancifulName", "appType", "plantRegistry",
    "permitNumber", "applicantName", "applicantAddress",
    "approvalDate", "expirationDate", "alcoholContent", "netContents",
    "qualifications", "processedDate",
    "front_image_path", "back_image_path",
    "wineVintage", "grapeVarietal", "wineAppellation", "ageStatement",
]


def create_applications_db(apps: list[dict]):
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(PROCESSING_DB):
        os.remove(PROCESSING_DB)

    conn = sqlite3.connect(PROCESSING_DB)
    c = conn.cursor()

    # applications table
    c.execute("""
        CREATE TABLE applications (
            id TEXT PRIMARY KEY,
            ttbId TEXT UNIQUE NOT NULL,
            status TEXT,
            vendorCode TEXT,
            serialNumber TEXT,
            classTypeCode TEXT,
            classTypeDesc TEXT,
            originCode TEXT,
            originDesc TEXT,
            brandName TEXT,
            dbaName TEXT,
            fancifulName TEXT,
            appType TEXT,
            plantRegistry TEXT,
            permitNumber TEXT,
            applicantName TEXT,
            applicantAddress TEXT,
            approvalDate TEXT,
            expirationDate TEXT,
            alcoholContent TEXT,
            netContents TEXT,
            qualifications TEXT,
            processedDate TEXT,
            front_image_path TEXT,
            back_image_path TEXT,
            wineVintage TEXT,
            grapeVarietal TEXT,
            wineAppellation TEXT,
            ageStatement TEXT
        )
    """)

    # processing_results table
    c.execute("""
        CREATE TABLE processing_results (
            ttbId TEXT PRIMARY KEY REFERENCES applications(ttbId),
            status TEXT NOT NULL DEFAULT 'pending',
            processed_at TEXT,
            error_message TEXT
        )
    """)

    # extracted_fields table
    c.execute("""
        CREATE TABLE extracted_fields (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ttbId TEXT NOT NULL REFERENCES applications(ttbId),
            field_name TEXT NOT NULL,
            extracted_text TEXT,
            confidence REAL,
            mini_image_path TEXT,
            region_bbox TEXT,
            rotation_degrees REAL,
            ocr_text TEXT,
            ocr_match_score REAL
        )
    """)

    for app in apps:
        images = app.get("labelImages", {})
        front = images.get("front", "")
        back = images.get("back", "")

        values = []
        for col in APP_COLUMNS:
            if col == "front_image_path":
                values.append(front)
            elif col == "back_image_path":
                values.append(back)
            else:
                values.append(app.get(col))

        placeholders = ",".join(["?"] * len(APP_COLUMNS))
        cols = ",".join(APP_COLUMNS)
        c.execute(f"INSERT INTO applications ({cols}) VALUES ({placeholders})", values)

        # Set pending processing result
        c.execute(
            "INSERT INTO processing_results (ttbId, status) VALUES (?, 'pending')",
            (app["ttbId"],),
        )

    conn.commit()
    conn.close()
    print(f"Created {PROCESSING_DB} with {len(apps)} applications")


def main():
    if not os.path.exists(TSV_PATH):
        print(f"Error: applications.tsv not found at {TSV_PATH}")
        sys.exit(1)

    apps = parse_applications_tsv(TSV_PATH)
    print(f"Parsed {len(apps)} applications from applications.tsv")
    create_applications_db(apps)


if __name__ == "__main__":
    main()
