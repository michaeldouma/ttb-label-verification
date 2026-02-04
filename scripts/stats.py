"""
Processing statistics stored as JSON.

===============================================================================
TAKE-HOME PROJECT FOR IT SPECIALIST POSITION
AI-Powered Alcohol Label Verification App
Michael Douma, February 2026
Developed with AI assistance (Claude)
===============================================================================

Description:
    Manages processing statistics as a JSON file for real-time UI updates.
    Tracks per-application processing actions and summary counts. The web
    UI (batch.html) polls this file to display live processing status.

Inputs:
    - TTB ID for each logged action
    - Action type and descriptive message
    - Summary counts (processed, pending, errors)

Actions:
    - Logs timestamped processing actions to a rolling log (max 500 entries)
    - Updates summary counts for dashboard display
    - Reads current stats for status queries
    - Clears log while preserving summary

Outputs:
    - htdocs/verification/stats.json containing:
      - summary: {date, totalProcessed, totalPending, totalErrors}
      - log: [{timestamp, ttbId, action, message}, ...]

Created: February 2026
"""

import json
import os
from datetime import datetime, timezone

# Stats file location - in verification API for frontend access
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATS_FILE = os.path.join(BASE_DIR, "htdocs", "verification", "stats.json")

# Maximum log entries to keep
MAX_LOG_ENTRIES = 500


def _load_stats() -> dict:
    """Load stats from JSON file."""
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    return {
        "summary": {
            "date": None,
            "totalProcessed": 0,
            "totalPending": 0,
            "totalErrors": 0,
        },
        "log": [],
    }


def _save_stats(data: dict):
    """Save stats to JSON file."""
    os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
    with open(STATS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def log_action(ttb_id: str | None, action: str, message: str):
    """Log a processing action."""
    data = _load_stats()

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ttbId": ttb_id,
        "action": action,
        "message": message,
    }

    # Prepend to log (newest first)
    data["log"].insert(0, entry)

    # Trim to max entries
    data["log"] = data["log"][:MAX_LOG_ENTRIES]

    _save_stats(data)


def update_summary(total_processed: int, total_pending: int, total_errors: int):
    """Update the summary counts."""
    data = _load_stats()

    data["summary"] = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "totalProcessed": total_processed,
        "totalPending": total_pending,
        "totalErrors": total_errors,
    }

    _save_stats(data)


def get_stats() -> dict:
    """Get current stats."""
    return _load_stats()


def clear_log():
    """Clear the log but keep summary."""
    data = _load_stats()
    data["log"] = []
    _save_stats(data)
