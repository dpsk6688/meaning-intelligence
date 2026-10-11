.PHONY: validate descriptives primary secondary report all

validate:
python scripts/00_validate_data.py

descriptives:
python scripts/01_descriptives.py

primary:
python scripts/02_primary_analysis.py

secondary:
python scripts/03_secondary_analysis.py

report:
python scripts/04_report.py

all: validate descriptives primary secondary report