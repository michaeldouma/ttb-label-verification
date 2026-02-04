"""
Configuration for the batch label processing pipeline.

===============================================================================
TAKE-HOME PROJECT FOR IT SPECIALIST POSITION
AI-Powered Alcohol Label Verification App
Michael Douma, February 2026
Developed with AI assistance (Claude)
===============================================================================

Description:
    Central configuration module for the batch label processing pipeline.
    Defines paths, API settings, and the list of fields to extract from
    alcohol beverage labels.

Inputs:
    - Environment variable: ANTHROPIC_API_KEY (required for Claude API)
    - Environment variable: ANTHROPIC_MODEL (optional, defaults to claude-sonnet-4-20250514)

Actions:
    - Sets up directory paths for data, output, and API directories
    - Configures Claude API model selection
    - Defines the complete list of label fields to verify
    - Provides the prescribed Government Warning text per 27 CFR Part 16

Outputs:
    - Exports configuration constants used by all other pipeline scripts:
      BASE_DIR, DATA_DIR, OUTPUT_DIR, IMAGES_DIR, VERIFICATION_DIR,
      PROCESSING_DB, VERIFY_FIELDS, GOVERNMENT_WARNING_TEXT

Created: February 2026
"""

import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "extracted")  # Temp location for mini-images

# TTB External API (their system - simulated for demo)
TTB_EXTERNAL_DIR = os.path.join(BASE_DIR, "htdocs", "ttb-external")
APPLICATIONS_JS = os.path.join(TTB_EXTERNAL_DIR, "data", "applications.js")
IMAGES_DIR = os.path.join(TTB_EXTERNAL_DIR, "images")

# Verification API (our system - AI extraction results)
VERIFICATION_DIR = os.path.join(BASE_DIR, "htdocs", "verification")

PROCESSING_DB = os.path.join(DATA_DIR, "processing.db")

# Control file for batch processing - write "STOP" to halt, delete to allow run
STOP_FILE = os.path.join(DATA_DIR, "STOP")

# API
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")

# Processing - fields to extract and verify
# Note: Fields can appear on ANY label (front, back, side) per TTB rules
VERIFY_FIELDS = [
    # Core fields - all products
    "brandName",
    "fancifulName",
    "alcoholContent",
    "netContents",
    "classTypeCode",
    "bottlerName",        # dbaName or applicantName
    "bottlerAddress",     # City, State
    # Mandatory elements - presence verification
    "governmentWarning",  # Required on all alcohol ≥0.5% ABV
    "sulfites",           # Required on wine with ≥10ppm sulfur dioxide
    "countryOfOrigin",    # Required on imports
    # Wine-specific fields
    "wineVintage",        # Vintage year (if shown)
    "grapeVarietal",      # Grape variety (if shown)
    "wineAppellation",    # Appellation/region (required if vintage or varietal shown)
    # Spirits-specific field
    "ageStatement",       # Age claim (required for whiskey <4 years)
]

# Prescribed Government Warning text (27 CFR Part 16)
# Required on ALL alcohol beverages ≥0.5% ABV since November 18, 1989
GOVERNMENT_WARNING_TEXT = (
    "GOVERNMENT WARNING: (1) According to the Surgeon General, women should not "
    "drink alcoholic beverages during pregnancy because of the risk of birth defects. "
    "(2) Consumption of alcoholic beverages impairs your ability to drive a car or "
    "operate machinery, and may cause health problems."
)
