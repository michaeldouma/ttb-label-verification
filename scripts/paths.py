"""
Shared path utilities for the batch processing pipeline.

===============================================================================
TAKE-HOME PROJECT FOR IT SPECIALIST POSITION
AI-Powered Alcohol Label Verification App
Michael Douma, February 2026
Developed with AI assistance (Claude)
===============================================================================

Description:
    Utility module providing sharded directory structure for scalable static
    file APIs. Converts TTB IDs to sharded filesystem paths suitable for
    production-scale deployment (3-5M+ records).

    Example: TTB ID "24001001000101" becomes path "2/4/0/0/1/0/0/1/000101.json"

    This sharding scheme:
    - Handles millions of records without filesystem performance issues
    - Works with S3, CDN, or local filesystem
    - Keeps APIs purely static (no database queries for lookups)

    Two separate APIs:
    - TTB External (/ttb-external/): Simulates TTB's COLA registry system
    - Verification (/verification/): Our AI extraction results

Inputs:
    - TTB ID strings (14-character alphanumeric identifiers)
    - API type specifiers ("applicant", "results", "extractions")

Actions:
    - Converts TTB IDs to sharded filesystem paths
    - Converts TTB IDs to URL paths for frontend fetch
    - Creates directory structures as needed
    - Retrieves all files from sharded structures

Outputs:
    - Filesystem paths for JSON files and image directories
    - URL paths for frontend API calls
    - Lists of (ttb_id, file_path) tuples for bulk operations

Created: February 2026
"""

import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# TTB External API (their system - we're faking it for the demo)
TTB_EXTERNAL_BASE = os.path.join(BASE_DIR, "htdocs", "ttb-external", "data")
API_BASE = TTB_EXTERNAL_BASE  # Legacy alias

# Verification API (our system - AI extraction results)
VERIFICATION_BASE = os.path.join(BASE_DIR, "htdocs", "verification")

# API types for TTB External
API_TYPES = ["applicant"]

# Verification API subdirectories
VERIFICATION_TYPES = ["results", "extractions"]


def ttb_id_to_sharded_path(ttb_id: str, api_type: str, base_dir: str = None) -> str:
    """Convert a TTB ID to a sharded filesystem path.

    Args:
        ttb_id: 14-character TTB ID (e.g., "24001001000101")
        api_type: One of "applicant"
        base_dir: Base directory (defaults to htdocs/ttb-external/data)

    Returns:
        Full path like: /base/applicant/2/4/0/0/1/0/0/1/000101.json

    Example:
        >>> ttb_id_to_sharded_path("24001001000101", "applicant")
        '.../htdocs/ttb-external/data/applicant/2/4/0/0/1/0/0/1/000101.json'
    """
    if base_dir is None:
        base_dir = API_BASE

    if api_type not in API_TYPES:
        raise ValueError(f"api_type must be one of {API_TYPES}, got: {api_type}")

    # Validate TTB ID format (should be 14 alphanumeric characters)
    ttb_id = str(ttb_id).strip()
    if len(ttb_id) < 9:
        raise ValueError(f"TTB ID too short: {ttb_id}")

    # Split first 8 characters into individual directories
    prefix = ttb_id[:8]
    suffix = ttb_id[8:]

    # Build path: api_type/p/r/e/f/i/x/0/1/suffix.json
    shard_dirs = list(prefix)  # ['2', '4', '0', '0', '1', '0', '0', '1']

    return os.path.join(base_dir, api_type, *shard_dirs, f"{suffix}.json")


def ttb_id_to_url_path(ttb_id: str, api_type: str) -> str:
    """Convert a TTB ID to a URL path for frontend fetch.

    Args:
        ttb_id: 14-character TTB ID
        api_type: One of "applicant"

    Returns:
        URL path like: /ttb-external/data/applicant/2/4/0/0/1/0/0/1/000101.json
    """
    ttb_id = str(ttb_id).strip()
    if len(ttb_id) < 9:
        raise ValueError(f"TTB ID too short: {ttb_id}")

    prefix = ttb_id[:8]
    suffix = ttb_id[8:]
    shard_path = "/".join(list(prefix))

    return f"/ttb-external/data/{api_type}/{shard_path}/{suffix}.json"


def ensure_sharded_dir(ttb_id: str, api_type: str, base_dir: str = None) -> str:
    """Create the sharded directory structure for a TTB ID and return the file path.

    Args:
        ttb_id: 14-character TTB ID
        api_type: One of "applicant"
        base_dir: Base directory (defaults to htdocs/ttb-external/data)

    Returns:
        Full file path (directory is created if it doesn't exist)
    """
    file_path = ttb_id_to_sharded_path(ttb_id, api_type, base_dir)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    return file_path


def get_verification_result_path(ttb_id: str) -> str:
    """Get filesystem path for verification result JSON.

    Args:
        ttb_id: 14-character TTB ID

    Returns:
        Path like: /htdocs/verification/results/2/4/0/0/1/0/0/1/000101.json
    """
    ttb_id = str(ttb_id).strip()
    if len(ttb_id) < 9:
        raise ValueError(f"TTB ID too short: {ttb_id}")

    prefix = ttb_id[:8]
    suffix = ttb_id[8:]
    shard_dirs = list(prefix)

    path = os.path.join(VERIFICATION_BASE, "results", *shard_dirs, f"{suffix}.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def get_extraction_image_dir(ttb_id: str) -> str:
    """Get filesystem directory for extraction images.

    Args:
        ttb_id: 14-character TTB ID

    Returns:
        Directory path like: /htdocs/verification/extractions/2/4/0/0/1/0/0/1/000101/
    """
    ttb_id = str(ttb_id).strip()
    if len(ttb_id) < 9:
        raise ValueError(f"TTB ID too short: {ttb_id}")

    prefix = ttb_id[:8]
    suffix = ttb_id[8:]
    shard_dirs = list(prefix)

    path = os.path.join(VERIFICATION_BASE, "extractions", *shard_dirs, suffix)
    os.makedirs(path, exist_ok=True)
    return path


def get_extraction_image_url(ttb_id: str, field_name: str) -> str:
    """Get URL path for an extraction image (for frontend fetch).

    Args:
        ttb_id: 14-character TTB ID
        field_name: Field name (e.g., "brandName")

    Returns:
        URL path like: /verification/extractions/2/4/0/0/1/0/0/1/000101/brandName.png
    """
    ttb_id = str(ttb_id).strip()
    if len(ttb_id) < 9:
        raise ValueError(f"TTB ID too short: {ttb_id}")

    prefix = ttb_id[:8]
    suffix = ttb_id[8:]
    shard_path = "/".join(list(prefix))

    return f"/verification/extractions/{shard_path}/{suffix}/{field_name}.png"


def get_all_sharded_files(api_type: str, base_dir: str = None) -> list:
    """Get all JSON files for an API type from the sharded structure.

    Returns list of (ttb_id, file_path) tuples.
    """
    if base_dir is None:
        base_dir = API_BASE

    api_dir = os.path.join(base_dir, api_type)
    if not os.path.exists(api_dir):
        return []

    results = []
    for root, dirs, files in os.walk(api_dir):
        for f in files:
            if f.endswith(".json"):
                file_path = os.path.join(root, f)
                # Reconstruct TTB ID from path
                rel_path = os.path.relpath(file_path, api_dir)
                parts = rel_path.replace("\\", "/").split("/")
                if len(parts) >= 9:  # 8 shard dirs + filename
                    prefix = "".join(parts[:8])
                    suffix = parts[8].replace(".json", "")
                    ttb_id = prefix + suffix
                    results.append((ttb_id, file_path))

    return results


if __name__ == "__main__":
    # Quick test
    test_id = "24001001000101"
    print(f"TTB ID: {test_id}")
    print(f"Sharded path: {ttb_id_to_sharded_path(test_id, 'applicant')}")
    print(f"URL path: {ttb_id_to_url_path(test_id, 'applicant')}")
