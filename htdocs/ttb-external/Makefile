# COLA Data Generation Makefile
#
# Usage:
#   make          - Generate applicant API from applications.tsv
#   make clean    - Remove generated applicant/ directory
#   make rebuild  - Clean and regenerate
#
# Source of truth: ../../data/applications.tsv
# Generated files: data/applications.js, data/applicant/{sharded}/*.json

.PHONY: all clean rebuild help

# Default target
all: data/applications.js

# Generate applications.js and sharded applicant/ JSON files
data/applications.js: ../../data/applications.tsv data/generate_from_tsv.js
	@echo "Generating applicant API from applications.tsv..."
	@cd data && node generate_from_tsv.js
	@echo ""
	@echo "Done. Test at http://localhost:8080/index.html"

# Remove generated files
clean:
	@echo "Removing generated applicant/ directory..."
	rm -rf data/applicant
	rm -f data/applications.js
	@echo "Done."

# Clean and rebuild
rebuild: clean all

# Show help
help:
	@echo "COLA Data Generation"
	@echo ""
	@echo "Targets:"
	@echo "  make          Generate applicant API from applications.tsv"
	@echo "  make clean    Remove generated files"
	@echo "  make rebuild  Clean and regenerate"
	@echo ""
	@echo "Edit data/applications.tsv, then run 'make' to regenerate."
