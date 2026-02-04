#!/usr/bin/env python3
"""
HTTP API server for batch processing control from the web UI.

===============================================================================
TAKE-HOME PROJECT FOR IT SPECIALIST POSITION
AI-Powered Alcohol Label Verification App
Michael Douma, February 2026
Developed with AI assistance (Claude)
===============================================================================

Description:
    Lightweight HTTP server providing REST endpoints for the batch.html
    operations dashboard. Enables the web UI to control the processing
    pipeline without direct command-line access.

    Runs alongside the static file server (port 8080) on port 9081.
    Uses file-based signaling (STOP file) for reliable process control
    that survives page reloads and works even if the server crashes.

Inputs:
    - HTTP requests from batch.html UI
    - Environment: ANTHROPIC_API_KEY for processing operations
    - data/processing.db: SQLite database for status queries

Actions:
    - POST /api/clear:   Reset all apps to pending, delete outputs
    - POST /api/forget:  Reset 5 random processed apps (demo workflow)
    - POST /api/process: Start batch processing in background thread
    - POST /api/abort:   Create STOP file to halt processing gracefully
    - GET  /api/status:  Return processing state and recent output

Outputs:
    - JSON responses with operation results and status
    - Background processing via subprocess (make process)
    - File-based stop signal (data/STOP)
    - CORS headers for cross-origin requests from localhost:8080

Usage:
    cd scripts && python3 miniServer/api_server.py
    cd scripts && make api
    cd scripts && make api PORT=8082  # Custom port

Created: February 2026
"""

import http.server
import json
import os
import random
import signal
import shutil
import sqlite3
import subprocess
import threading
import time
from pathlib import Path

import argparse
import socket

DEFAULT_PORT = 9081
# Path from miniServer/api_server.py -> scripts/ -> repository/
BASE_DIR = Path(__file__).parent.parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
DATA_DIR = BASE_DIR / "data"
HTDOCS_DIR = BASE_DIR / "htdocs"
VERIFICATION_DIR = HTDOCS_DIR / "verification"
OUTPUT_DIR = BASE_DIR / "output" / "extracted"
STOP_FILE = DATA_DIR / "STOP"  # Touch this file to stop processing

# Track background process
process_thread = None
process_running = False
process_output = []
process_handle = None  # subprocess.Popen handle for killing


def get_dir_stats(path: Path) -> dict:
    """Get file count and total size for a directory."""
    if not path.exists():
        return {"exists": False, "files": 0, "size": 0, "size_human": "0 B"}

    files = list(path.rglob("*"))
    file_count = len([f for f in files if f.is_file()])
    total_size = sum(f.stat().st_size for f in files if f.is_file())

    # Human readable size
    if total_size < 1024:
        size_human = f"{total_size} B"
    elif total_size < 1024 * 1024:
        size_human = f"{total_size / 1024:.1f} KB"
    else:
        size_human = f"{total_size / (1024 * 1024):.1f} MB"

    return {
        "exists": True,
        "files": file_count,
        "size": total_size,
        "size_human": size_human
    }


def get_pre_clear_report() -> dict:
    """Get report of what will be deleted."""
    return {
        "processing_db": {
            "path": str(DATA_DIR / "processing.db"),
            "exists": (DATA_DIR / "processing.db").exists(),
            "size_human": f"{(DATA_DIR / 'processing.db').stat().st_size / 1024:.1f} KB"
                if (DATA_DIR / "processing.db").exists() else "0 B"
        },
        "verification_results": get_dir_stats(VERIFICATION_DIR / "results"),
        "verification_extractions": get_dir_stats(VERIFICATION_DIR / "extractions"),
        "output_extracted": get_dir_stats(OUTPUT_DIR),
        "stats_json": {
            "path": str(VERIFICATION_DIR / "stats.json"),
            "exists": (VERIFICATION_DIR / "stats.json").exists()
        }
    }


def run_clear() -> dict:
    """Run make clean and return report."""
    # Get pre-clear stats
    pre_report = get_pre_clear_report()

    # Run make clean
    result = subprocess.run(
        ["make", "clean"],
        cwd=SCRIPTS_DIR,
        capture_output=True,
        text=True
    )

    # Get post-clear stats
    post_report = get_pre_clear_report()

    # Build deletion log
    deletions = []

    if pre_report["processing_db"]["exists"] and not post_report["processing_db"]["exists"]:
        deletions.append(f"Deleted processing.db ({pre_report['processing_db']['size_human']})")
    elif pre_report["processing_db"]["exists"]:
        deletions.append("Reset processing.db (cleared extracted_fields, reset status to pending)")

    if pre_report["verification_results"]["files"] > 0:
        deletions.append(f"Deleted {pre_report['verification_results']['files']} result JSON files ({pre_report['verification_results']['size_human']})")

    if pre_report["verification_extractions"]["files"] > 0:
        deletions.append(f"Deleted {pre_report['verification_extractions']['files']} extraction images ({pre_report['verification_extractions']['size_human']})")

    if pre_report["output_extracted"]["files"] > 0:
        deletions.append(f"Deleted {pre_report['output_extracted']['files']} temp output files ({pre_report['output_extracted']['size_human']})")

    if pre_report["stats_json"]["exists"] and not post_report["stats_json"]["exists"]:
        deletions.append("Deleted stats.json")
    elif pre_report["stats_json"]["exists"]:
        deletions.append("Reset stats.json")

    if not deletions:
        deletions.append("Nothing to clear - already clean")

    return {
        "success": result.returncode == 0,
        "deletions": deletions,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "post_check": {
            "processing_db_exists": post_report["processing_db"]["exists"],
            "results_files": post_report["verification_results"]["files"],
            "extraction_files": post_report["verification_extractions"]["files"],
            "output_files": post_report["output_extracted"]["files"]
        }
    }


def run_forget(count: int = 5) -> dict:
    """Forget N processed applications - reset them to pending for reprocessing.

    This lets you test the 'new apps in queue' workflow without clearing everything.
    """
    db_path = DATA_DIR / "processing.db"
    if not db_path.exists():
        return {"success": False, "message": "Database not found", "forgotten": []}

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Find processed applications
    c.execute("SELECT ttbId FROM processing_results WHERE status = 'processed' ORDER BY processed_at DESC")
    processed = [row[0] for row in c.fetchall()]

    if not processed:
        conn.close()
        return {"success": True, "message": "No processed applications to forget", "forgotten": []}

    # Pick random ones to forget (or all if fewer than count)
    to_forget = random.sample(processed, min(count, len(processed)))

    # Reset their status to pending
    for ttb_id in to_forget:
        c.execute(
            "UPDATE processing_results SET status = 'pending', processed_at = NULL, error_message = NULL WHERE ttbId = ?",
            (ttb_id,)
        )
        # Delete their extracted fields
        c.execute("DELETE FROM extracted_fields WHERE ttbId = ?", (ttb_id,))

        # Delete their verification output files
        # Sharded path: TTB ID 24028001000106 -> 2/4/0/2/8/0/0/1/000106
        sharded = "/".join(ttb_id[:8]) + "/" + ttb_id[8:] + ".json"
        result_path = VERIFICATION_DIR / "results" / sharded
        extraction_dir = VERIFICATION_DIR / "extractions" / "/".join(ttb_id[:8]) / ttb_id[8:]

        if result_path.exists():
            result_path.unlink()
        if extraction_dir.exists():
            shutil.rmtree(extraction_dir)

        # Delete temp output images
        for img in OUTPUT_DIR.glob(f"{ttb_id}_*.png"):
            img.unlink()

    conn.commit()

    # Update stats.json counts
    c.execute("SELECT status, COUNT(*) FROM processing_results GROUP BY status")
    counts = dict(c.fetchall())
    conn.close()

    # Update stats file - both summary AND remove forgotten apps from log
    stats_file = VERIFICATION_DIR / "stats.json"
    if stats_file.exists():
        with open(stats_file) as f:
            stats = json.load(f)
        stats["summary"]["totalProcessed"] = counts.get("processed", 0)
        stats["summary"]["totalPending"] = counts.get("pending", 0)
        stats["summary"]["totalErrors"] = counts.get("error", 0)
        # Remove log entries for forgotten apps so they disappear from RECENT COMPLETIONS
        forgotten_set = set(to_forget)
        stats["log"] = [entry for entry in stats.get("log", []) if entry.get("ttbId") not in forgotten_set]
        with open(stats_file, "w") as f:
            json.dump(stats, f, indent=2)

    # Emit event
    try:
        import sys
        sys.path.insert(0, str(SCRIPTS_DIR))
        import events
        events._emit(
            "apps_forgotten",
            f"Forgot {len(to_forget)} apps: ready for reprocessing",
            {"count": len(to_forget), "ttb_ids": to_forget}
        )
    except Exception:
        pass  # Don't fail if events module not available

    return {
        "success": True,
        "message": f"Forgot {len(to_forget)} applications",
        "forgotten": to_forget,
        "remaining_processed": counts.get("processed", 0),
        "now_pending": counts.get("pending", 0)
    }


def run_process_background():
    """Run make process in background thread."""
    global process_running, process_output, process_handle
    process_running = True
    process_output = ["Starting batch processing..."]

    try:
        # Check for API key
        if not os.environ.get("ANTHROPIC_API_KEY"):
            process_output.append("ERROR: ANTHROPIC_API_KEY not set")
            process_running = False
            return

        process_handle = subprocess.Popen(
            ["make", "process"],
            cwd=SCRIPTS_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env={**os.environ, "USER": os.environ.get("USER", "user")},
            start_new_session=True  # Create new process group for clean termination
        )

        for line in process_handle.stdout:
            process_output.append(line.rstrip())
            # Keep last 100 lines
            if len(process_output) > 100:
                process_output = process_output[-100:]

        process_handle.wait()
        process_output.append(f"Process finished with code {process_handle.returncode}")

    except Exception as e:
        process_output.append(f"ERROR: {e}")
    finally:
        process_running = False
        process_handle = None


def abort_process() -> dict:
    """Abort the running process by creating STOP file."""
    global process_running, process_output

    try:
        # Always create STOP file - works even if server lost track of process
        STOP_FILE.parent.mkdir(parents=True, exist_ok=True)
        STOP_FILE.touch()
        process_output.append("Stop signal sent (STOP file created)")
        process_running = False  # Update server state
        return {"success": True, "message": "Stop signal sent - processing will halt after current label"}
    except Exception as e:
        return {"success": False, "message": f"Failed to create stop file: {e}"}


def start_process() -> dict:
    """Start make process in background."""
    global process_thread, process_running

    if process_running:
        return {"success": False, "message": "Processing already in progress"}

    if not os.environ.get("ANTHROPIC_API_KEY"):
        return {
            "success": False,
            "message": "ANTHROPIC_API_KEY not set. Run: export ANTHROPIC_API_KEY='sk-ant-...'"
        }

    # Clear any existing STOP file
    if STOP_FILE.exists():
        STOP_FILE.unlink()

    process_thread = threading.Thread(target=run_process_background, daemon=True)
    process_thread.start()

    return {"success": True, "message": "Processing started in background"}


class APIHandler(http.server.BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/status":
            self.send_json({
                "processing": process_running,
                "output": process_output[-20:] if process_output else []
            })
        else:
            self.send_json({"error": "Not found"}, 404)

    def do_POST(self):
        if self.path == "/api/clear":
            result = run_clear()
            self.send_json(result)
        elif self.path == "/api/process":
            result = start_process()
            self.send_json(result)
        elif self.path == "/api/abort":
            result = abort_process()
            self.send_json(result)
        elif self.path == "/api/forget":
            result = run_forget(5)
            self.send_json(result)
        else:
            self.send_json({"error": "Not found"}, 404)

    def log_message(self, format, *args):
        print(f"[API] {args[0]}")


def main():
    parser = argparse.ArgumentParser(description="API server for batch processing")
    parser.add_argument("--port", "-p", type=int, default=DEFAULT_PORT, help=f"Port to listen on (default: {DEFAULT_PORT})")
    args = parser.parse_args()

    port = args.port

    print(f"Starting API server on port {port}...")
    print(f"Endpoints:")
    print(f"  POST http://localhost:{port}/api/clear    - Reset all apps to pending")
    print(f"  POST http://localhost:{port}/api/forget   - Forget 5 random apps (for testing)")
    print(f"  POST http://localhost:{port}/api/process  - Start batch processing")
    print(f"  POST http://localhost:{port}/api/abort    - Stop processing")
    print(f"  GET  http://localhost:{port}/api/status   - Get processing status")
    print()

    # Allow socket reuse to avoid "Address already in use" after restart
    class ReuseHTTPServer(http.server.HTTPServer):
        allow_reuse_address = True

    try:
        server = ReuseHTTPServer(("", port), APIHandler)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"ERROR: Port {port} is already in use.")
            print(f"  Kill the existing process: lsof -ti:{port} | xargs kill")
            print(f"  Or use a different port: make api PORT=8082")
            return
        raise

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
