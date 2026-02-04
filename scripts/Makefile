# ==============================================================================
# TAKE-HOME PROJECT FOR IT SPECIALIST POSITION
# AI-Powered Alcohol Label Verification App
# Michael Douma, February 2026
# ==============================================================================
#
# Batch Label Processing Pipeline - Makefile
# ==========================================
#
# Description:
#   Task automation for the label processing pipeline. Provides a simple,
#   documented interface to the Python scripts without requiring knowledge
#   of individual script locations or arguments.
#
#   Why Make? It's universal (pre-installed on Linux/macOS), requires no
#   dependencies, and is self-documenting via `make help`. For a government
#   IT environment, this pragmatic choice prioritizes reliability and
#   maintainability over trendy build tools.
#
# Inputs:
#   - Environment: ANTHROPIC_API_KEY (required for AI processing)
#   - Environment: LIMIT=N (optional, process only N apps for testing)
#   - Environment: API_PORT (optional, default 9081 for API server)
#
# Main Targets:
#   make setup     - Initialize demo data (create DB, export JSON)
#   make process   - Run full AI pipeline (extract → verify → export)
#   make all       - Complete pipeline (setup + process)
#   make clean     - Reset to initial state for fresh demo
#   make api       - Start HTTP server for web UI controls
#
# Usage Examples:
#   export ANTHROPIC_API_KEY="sk-ant-..."
#   make setup              # One-time data initialization
#   make process            # Full AI extraction run
#   LIMIT=5 make extract    # Test with 5 applications
#   make help               # Show all available targets
#
# ==============================================================================
#

.PHONY: all setup process clean install db applicant extract verify export api help

PYTHON := python3
PIP := pip3
LIMIT ?= 0

# Workaround for containerized environments without proper user
export USER ?= user
export LOGNAME ?= user

# ============================================================
# Main targets
# ============================================================

# Full pipeline: setup + AI processing
all: setup process
	@echo ""
	@echo "========================================"
	@echo "Pipeline complete!"
	@echo "========================================"

# ============================================================
# Workflow 1: Agent Data Setup (Michael runs)
# ============================================================

# Setup agent view data (DB + applicant JSON)
setup: install db applicant
	@echo "Agent data setup complete."

# Create/reset database from applications.tsv
db:
	@echo "Creating database..."
	$(PYTHON) demoSetup/make_demo_db.py
	@echo "Database ready."

# Export applicant JSON to sharded API
applicant:
	@echo "Exporting applicant data..."
	$(PYTHON) demoSetup/export_applicant.py

# ============================================================
# Workflow 2: AI Processing (web server triggers)
# ============================================================

# Full AI processing pipeline
process: install extract verify export
	@echo "AI processing complete."

# Run label extraction (Claude Vision + EasyOCR)
extract:
	@if [ -z "$$ANTHROPIC_API_KEY" ]; then \
		echo "ERROR: ANTHROPIC_API_KEY not set"; \
		echo "  export ANTHROPIC_API_KEY='sk-ant-...'"; \
		exit 1; \
	fi
	@echo "Extracting labels..."
	@SSL_CERT=$$($(PYTHON) -c "import certifi; print(certifi.where())" 2>/dev/null); \
	if [ "$(LIMIT)" -gt 0 ]; then \
		SSL_CERT_FILE=$$SSL_CERT REQUESTS_CA_BUNDLE=$$SSL_CERT $(PYTHON) batchProcessor/process_labels.py --limit $(LIMIT); \
	else \
		SSL_CERT_FILE=$$SSL_CERT REQUESTS_CA_BUNDLE=$$SSL_CERT $(PYTHON) batchProcessor/process_labels.py; \
	fi

# Run OCR verification on cropped mini-images
verify:
	@echo "Verifying extractions..."
	@SSL_CERT=$$($(PYTHON) -c "import certifi; print(certifi.where())" 2>/dev/null); \
	SSL_CERT_FILE=$$SSL_CERT REQUESTS_CA_BUNDLE=$$SSL_CERT $(PYTHON) batchProcessor/verify_extractions.py

# Export AI results to sharded API (verification/results + extractions)
export:
	@echo "Exporting AI results..."
	$(PYTHON) batchProcessor/export_extractions.py

# Clear AI processing, reset to pending
clean:
	@echo "Clearing AI processing..."
	$(PYTHON) batchProcessor/clear_processing.py
	@echo "Ready for fresh processing."

# ============================================================
# Utilities
# ============================================================

# Install Python dependencies
install:
	@echo "Installing dependencies..."
	$(PIP) install --quiet --break-system-packages anthropic Pillow pillow-heif easyocr certifi 2>/dev/null || \
	$(PIP) install --quiet anthropic Pillow pillow-heif easyocr certifi
	@echo "Dependencies installed."

# API server for batch.html buttons (PORT=8081 by default)
API_PORT ?= 9081
api:
	@echo "Starting API server on port $(API_PORT)..."
	$(PYTHON) miniServer/api_server.py --port $(API_PORT)

# Help
help:
	@echo "Batch Label Processing Pipeline"
	@echo ""
	@echo "Workflows:"
	@echo "  make setup     Agent data setup (DB + applicant JSON)"
	@echo "  make process   AI processing (extract + verify + export)"
	@echo "  make all       Full pipeline (setup + process)"
	@echo ""
	@echo "Agent Data (Michael runs):"
	@echo "  make db        Create database from applications.tsv"
	@echo "  make applicant Export applicant JSON to API"
	@echo ""
	@echo "AI Processing (web server triggers):"
	@echo "  make extract   Run label extraction (Claude + EasyOCR)"
	@echo "  make verify    Run OCR verification"
	@echo "  make export    Export verification results + extractions"
	@echo "  make clean     Clear processing, reset to pending"
	@echo ""
	@echo "Utilities:"
	@echo "  make install   Install Python dependencies"
	@echo "  make api       Start API server for batch.html buttons"
	@echo ""
	@echo "Options:"
	@echo "  LIMIT=N        Process only N applications"
	@echo ""
	@echo "Environment:"
	@echo "  ANTHROPIC_API_KEY  Required for AI processing"
