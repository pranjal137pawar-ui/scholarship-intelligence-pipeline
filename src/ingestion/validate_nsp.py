
from pathlib import Path
import csv

# Project location
project_root = Path(__file__).resolve().parents[2]

csv_file = (
    project_root
    / "data"
    / "processed"
    / "nsp_scholarships.csv"
)

print("\nNSP DATA QUALITY TEST")
print("---------------------")

# Check file exists
if not csv_file.exists():
    raise FileNotFoundError("CSV file not found!")

# Read CSV
with csv_file.open(
    "r",
    encoding="utf-8-sig",
    newline=""
) as file:

    reader = csv.DictReader(file)
    rows = list(reader)

# 1. Row count
print("Total records:", len(rows))

# 2. Empty name check
empty_names = [
    row for row in rows
    if not row["scheme_name"].strip()
]

print(
    "Empty names:",
    "PASSED" if not empty_names else "FAILED"
)

# 3. Duplicate check
names = [
    " ".join(row["scheme_name"].split()).casefold()
    for row in rows
]

duplicates = len(names) != len(set(names))

print(
    "Duplicate check:",
    "FAILED" if duplicates else "PASSED"
)

# 4. Navigation text check
invalid_words = [
    "apply for scholarship",
    "list of applicants processed",
    "nsp : national scholarship portal"
]

invalid_rows = [
    row for row in rows
    if any(
        word in row["scheme_name"].casefold()
        for word in invalid_words
    )
]

print(
    "Navigation text check:",
    "FAILED" if invalid_rows else "PASSED"
)

# 5. Source URL check
invalid_sources = [
    row for row in rows
    if not row["source_url"].startswith("https://")
]

print(
    "Source URL check:",
    "FAILED" if invalid_sources else "PASSED"
)

# 6. Scholarship classification check
invalid_categories = [
    row for row in rows
    if not any(
        category in row["scheme_name"]
        for category in [
            "(Merit Based Scheme)",
            "(Welfare Based Scheme)"
        ]
    )
]

print(
    "Classification check:",
    "FAILED" if invalid_categories else "PASSED"
)

# Final result
failed = (
    len(rows) == 0
    or bool(empty_names)
    or duplicates
    or bool(invalid_rows)
    or bool(invalid_sources)
    or bool(invalid_categories)
)

print("---------------------")

if failed:
    print("OVERALL RESULT: FAILED")
else:
    print("OVERALL RESULT: PASSED")

print("Validation completed!")
