#!/usr/bin/env python3
"""
Introduce deliberate errors into applications.tsv for testing verification.

===============================================================================
TAKE-HOME PROJECT FOR IT SPECIALIST POSITION
AI-Powered Alcohol Label Verification App
Michael Douma, February 2026
Developed with AI assistance (Claude)
===============================================================================

Description:
    Testing utility that introduces deliberate discrepancies between the
    COLA application data (applications.tsv) and what actually appears on
    the label images. This creates test cases to verify the AI verification
    system correctly detects mismatches.

    Simulates real-world errors that TTB agents encounter:
    - Alcohol content mismatches (form says 18%, label shows 21%)
    - Brand name misspellings ("CASA DORADA" vs "CASA DORADO")
    - Net contents discrepancies (750 ML vs 1 LITER)
    - Vintage year errors (2015 vs 2014)
    - Abbreviated names ("CHARD" vs "CHARDONNAY")

Inputs:
    - data/applications.tsv: Master application data file
    - ERRORS dict: Hard-coded mapping of {ttbId: {field: new_value}}

Actions:
    - Reads applications.tsv with csv.DictReader
    - Applies defined errors to matching TTB IDs
    - Prints each modification for verification
    - Writes modified data back to applications.tsv

Outputs:
    - Modified data/applications.tsv with ~35 deliberate errors
    - Console log of all changes made
    - Summary: count of errors and affected applications

Usage:
    cd scripts && python3 tools/introduce_errors.py

Note: Run make setup after this script to regenerate the database
      and exported JSON files with the new error values.

Created: February 2026
"""

import csv
import os

# Path relative to this script's location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSV_PATH = os.path.join(BASE_DIR, 'data', 'applications.tsv')

# Define errors to introduce: { ttbId: { field: new_value, ... } }
ERRORS = {
    # Spirits
    '24001001000101': {  # 12345 IMPORTS - Barbados rum
        'alcoholContent': '21% ALC./VOL.',  # Was 18%
    },
    '24002001000102': {  # ABC Distillery - Rye
        'brandName': 'A.B.C.',  # Was "ABC"
    },
    '24003001000103': {  # Polly's - Spiced Rum
        'fancifulName': 'SPICE RUM',  # Was "SPICED RUM"
        'alcoholContent': '18% ALC. BY VOL.',  # Was 20%
    },
    '24004001000104': {  # Sunnyside - Apple Vodka
        'netContents': '750 ML',  # Was "1 LITER"
    },
    '24005001000105': {  # Chimes - Gin
        'alcoholContent': '40% BY VOLUME',  # Was 43%
    },
    '24028001000106': {  # Iron Ridge - Bourbon
        'alcoholContent': '45% ALC./VOL. (90 PROOF)',  # Was 40%/80 PROOF
    },
    '24029001000107': {  # Casa Dorada - Tequila
        'brandName': 'CASA DORADO',  # Was "CASA DORADA"
    },
    '24031001000108': {  # Cointreau
        'alcoholContent': '42% alc./Vol.',  # Was 40%
    },
    '24033001000110': {  # Ricard
        'alcoholContent': '40% alc./Vol.',  # Was 45%
    },
    '24035001000112': {  # Drop of the Creator - Gin
        'netContents': '1 L',  # Was 750 ML
    },

    # Malt beverages
    '24006001000201': {  # Example Brewing - IPA
        'alcoholContent': '7.0% ALC/VOL',  # Was 6.5%
    },
    '24009001000204': {  # Example Brewing - Milo's Ale
        'brandName': 'EXAMPLE BREWING CO.',  # Was "EXAMPLE BREWING COMPANY"
    },
    '24012001000207': {  # Malt & Hop - Pale Ale
        'netContents': '1 PINT',  # Was "1 PINT 8 FL OZ"
    },
    '24013001000208': {  # Malt & Hop - Dark Ale
        'alcoholContent': '10% ALCOHOL/VOLUME',  # Was 12%
    },
    '24016001000211': {  # Tasty Collection - Cherry
        'fancifulName': 'WILD CHERRY',  # Was "CHERRY"
        'alcoholContent': '5.5% ALC/VOL',  # Was 6%
    },
    '24017001000212': {  # Burnett Brews
        'brandName': 'BURNETT BREW',  # Was "BURNETT BREWS"
    },
    '24030001000213': {  # Breeze Wave - Hard Seltzer
        'brandName': 'BREEZY WAVE',  # Was "BREEZE WAVE"
    },
    '24038001000214': {  # Schofferhofer
        'alcoholContent': '3.0% ALC. BY VOL.',  # Was 2.5%
    },
    '24039001000215': {  # Boddingtons
        'alcoholContent': '5.0% ALC./VOL.',  # Was 4.6%
    },

    # Wine
    '24018001000301': {  # ABC Winery - Red
        'brandName': 'ABC WINES',  # Was "ABC WINERY"
        'alcoholContent': 'ALC. 14% BY VOL.',  # Was 13%
    },
    '24020001000303': {  # Big Black Cat - Margarita
        'netContents': '750 ML',  # Was 375 ML
    },
    '24021001000304': {  # Wine for a Rainy Day - Albarino
        'alcoholContent': '13% ALC. BY VOL.',  # Was 12.5%
        'wineVintage': '2015',  # Was 2014
    },
    '24022001000305': {  # Chimes Vineyard - Chardonnay
        'grapeVarietal': 'CHARD',  # Was "CHARDONNAY"
    },
    '24025001000308': {  # Spare You Wines - Oregon Red
        'alcoholContent': '11.5% ALC BY VOL',  # Was 12%
        'netContents': '750 ML',  # Was "1 LITER"
    },
    '24026001000309': {  # TTB Imports - Niagara
        'wineVintage': '2012',  # Was 2011
    },
    '24027001000310': {  # Lighthouse Cellars - Rose
        'alcoholContent': '12% ALC. BY VOL.',  # Was 11.5%
        'wineVintage': '2022',  # Was 2023
    },
    '24036001000313': {  # Gato Negro - Sauvignon Blanc
        'wineVintage': '2020',  # Was 2019
        'grapeVarietal': 'SAUV BLANC',  # Was "SAUVIGNON BLANC"
    },
    '24037001000314': {  # Martini & Rossi - Vermouth
        'alcoholContent': '18% alc./vol.',  # Was 15%
    },
}

def main():
    # Read existing TSV
    with open(TSV_PATH, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        fieldnames = reader.fieldnames
        rows = list(reader)

    # Apply errors
    error_count = 0
    affected_apps = set()

    for row in rows:
        ttb_id = row['ttbId']
        if ttb_id in ERRORS:
            for field, new_value in ERRORS[ttb_id].items():
                old_value = row.get(field, '')
                row[field] = new_value
                print(f"  {ttb_id}: {field}: '{old_value}' → '{new_value}'")
                error_count += 1
            affected_apps.add(ttb_id)

    # Write back
    with open(TSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nIntroduced {error_count} errors across {len(affected_apps)} applications")
    print(f"Affected TTB IDs: {sorted(affected_apps)}")

if __name__ == '__main__':
    main()
