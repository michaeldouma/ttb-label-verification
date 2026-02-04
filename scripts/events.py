"""
Operational event log for batch processing pipeline.

===============================================================================
TAKE-HOME PROJECT FOR IT SPECIALIST POSITION
AI-Powered Alcohol Label Verification App
Michael Douma, February 2026
Developed with AI assistance (Claude)
===============================================================================

Description:
    Tracks performance-oriented operational events for system monitoring.
    Unlike stats.py which logs per-application actions, this module captures
    system-level events: batch timing, API health, errors, and recoveries.

    Events tracked:
    - Batch start/complete with timing summaries
    - API performance issues (slow responses, timeouts, recoveries)
    - System errors and recoveries
    - Processing stopped/cleared events

Inputs:
    - Batch processing counts and durations
    - API response times for performance tracking
    - Error messages and context information

Actions:
    - Emits timestamped events to a rolling log (max 100 entries)
    - Tracks API response time trends with rolling averages
    - Detects API degradation (avg > 8s) and recovery (avg < 3s)
    - Manages state transitions for meaningful alerts

Outputs:
    - htdocs/verification/events.json containing:
      - events: [{timestamp, type, message, details}, ...]
    - Event types: batch_started, batch_complete, api_degraded,
      api_recovered, api_timeout, api_error, processing_stopped, cleared

Created: February 2026
"""

import json
import os
from datetime import datetime, timezone
from typing import Optional

# Events file location - in verification API for frontend access
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS_FILE = os.path.join(BASE_DIR, "htdocs", "verification", "events.json")

# Maximum events to keep
MAX_EVENTS = 100

# API performance thresholds (in seconds)
API_BASELINE_RESPONSE = 1.2  # Typical response time
API_SLOW_THRESHOLD = 3.0     # Warn if response > this
API_VERY_SLOW_THRESHOLD = 8.0  # Degraded if response > this

# Track API performance state for detecting changes
_api_state = {
    "is_degraded": False,
    "last_response_times": [],  # Rolling window of last 5 responses
}


def _load_events() -> dict:
    """Load events from JSON file."""
    if os.path.exists(EVENTS_FILE):
        try:
            with open(EVENTS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"events": []}


def _save_events(data: dict):
    """Save events to JSON file."""
    os.makedirs(os.path.dirname(EVENTS_FILE), exist_ok=True)
    with open(EVENTS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _emit(event_type: str, message: str, details: Optional[dict] = None):
    """Emit an event to the log."""
    data = _load_events()

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": event_type,
        "message": message,
    }
    if details:
        event["details"] = details

    # Prepend (newest first)
    data["events"].insert(0, event)

    # Trim to max
    data["events"] = data["events"][:MAX_EVENTS]

    _save_events(data)


def _format_duration(seconds: float) -> str:
    """Format duration as human-readable string."""
    if seconds < 60:
        return f"{seconds:.0f}s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}m {secs}s"


# ── Public event emitters ──

def batch_started(app_count: int):
    """Emit when batch processing begins."""
    _emit(
        "batch_started",
        f"Processing started: {app_count} applications queued",
        {"app_count": app_count}
    )


def batch_complete(app_count: int, duration_seconds: float, errors: int = 0):
    """Emit when batch processing completes."""
    if app_count == 0:
        _emit("batch_complete", "Batch complete: no applications to process")
        return

    avg = duration_seconds / app_count
    dur = _format_duration(duration_seconds)

    if errors > 0:
        msg = f"Batch complete: {app_count} apps in {dur} ({avg:.1f}s/app), {errors} errors"
    else:
        msg = f"Batch complete: {app_count} apps in {dur} ({avg:.1f}s/app)"

    _emit(
        "batch_complete",
        msg,
        {
            "app_count": app_count,
            "duration_seconds": round(duration_seconds, 1),
            "avg_seconds_per_app": round(avg, 1),
            "errors": errors,
        }
    )


def api_response(response_time: float):
    """Track API response time and emit events on state changes.

    Call this after each API call to track performance trends.
    Only emits events when there's a meaningful state change.
    """
    global _api_state

    # Add to rolling window
    _api_state["last_response_times"].append(response_time)
    if len(_api_state["last_response_times"]) > 5:
        _api_state["last_response_times"] = _api_state["last_response_times"][-5:]

    # Calculate rolling average
    avg = sum(_api_state["last_response_times"]) / len(_api_state["last_response_times"])

    was_degraded = _api_state["is_degraded"]

    # Check for state transitions
    if avg > API_VERY_SLOW_THRESHOLD and not was_degraded:
        # Transition to degraded
        _api_state["is_degraded"] = True
        _emit(
            "api_degraded",
            f"API response degraded: {avg:.1f}s avg (typical: {API_BASELINE_RESPONSE}s)",
            {
                "avg_response_seconds": round(avg, 1),
                "typical_response_seconds": API_BASELINE_RESPONSE,
            }
        )
    elif avg < API_SLOW_THRESHOLD and was_degraded:
        # Recovered
        _api_state["is_degraded"] = False
        _emit(
            "api_recovered",
            f"API response normalized: {avg:.1f}s avg",
            {"avg_response_seconds": round(avg, 1)}
        )
    elif response_time > API_VERY_SLOW_THRESHOLD * 2 and not was_degraded:
        # Single very slow response (potential timeout)
        _emit(
            "api_slow",
            f"API response slow: {response_time:.1f}s (typical: {API_BASELINE_RESPONSE}s)",
            {
                "response_seconds": round(response_time, 1),
                "typical_response_seconds": API_BASELINE_RESPONSE,
            }
        )


def api_timeout(error_message: str):
    """Emit when API call times out."""
    _emit(
        "api_timeout",
        f"API timeout: {error_message}",
        {"error": error_message}
    )


def api_error(error_message: str):
    """Emit when API call fails with an error."""
    _emit(
        "api_error",
        f"API error: {error_message}",
        {"error": error_message}
    )


def processing_stopped(apps_completed: int, apps_remaining: int):
    """Emit when processing is stopped by STOP file."""
    _emit(
        "processing_stopped",
        f"Processing stopped: {apps_completed} completed, {apps_remaining} remaining",
        {
            "apps_completed": apps_completed,
            "apps_remaining": apps_remaining,
        }
    )


def cleared(apps_reset: int, fields_cleared: int, images_deleted: int):
    """Emit when all processing data is cleared."""
    _emit(
        "cleared",
        f"Cleared: {apps_reset} apps reset, {fields_cleared} fields, {images_deleted} images",
        {
            "apps_reset": apps_reset,
            "fields_cleared": fields_cleared,
            "images_deleted": images_deleted,
        }
    )


def system_error(error_message: str, context: Optional[str] = None):
    """Emit when a system error occurs."""
    msg = f"System error: {error_message}"
    if context:
        msg = f"System error in {context}: {error_message}"
    _emit(
        "system_error",
        msg,
        {"error": error_message, "context": context}
    )


def service_started():
    """Emit when the processing service starts."""
    _emit("service_started", "Processing service started")


def service_stopped():
    """Emit when the processing service stops."""
    _emit("service_stopped", "Processing service stopped")


def queue_status(pending: int, processing: int = 0):
    """Emit queue depth status (for periodic monitoring)."""
    if pending == 0 and processing == 0:
        _emit("queue_idle", "Queue idle: no pending applications")
    elif pending > 50:
        _emit(
            "queue_backlog",
            f"Queue backlog: {pending} applications pending",
            {"pending": pending, "processing": processing}
        )


def get_events() -> list:
    """Get all events."""
    return _load_events().get("events", [])


def clear_events():
    """Clear all events."""
    _save_events({"events": []})


def reset_api_state():
    """Reset API performance tracking state."""
    global _api_state
    _api_state = {
        "is_degraded": False,
        "last_response_times": [],
    }
