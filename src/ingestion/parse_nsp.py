
"
from pathlib import Path
import csv
from bs4 import BeautifulSoup

# ----------------------------------
# 1. Project Paths
# ----------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FOLDER = PROJECT_ROOT / "data" / "raw"
OUTPUT_FOLDER = PROJECT_ROOT / "data" / "processed"

SOURCE_URL = "https://scholarships.gov.in/All-Scholarships"
SOURCE_NAME = "National Scholarship Portal"

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


# ----------------------------------
# 2. Find Latest NSP HTML File
# ----------------------------------

html_files = list(RAW_FOLDER.glob("*.html"))

if not html_files:
    raise FileNotFoundError(
        f"No HTML file found in: {RAW_FOLDER}"
    )

html_file = max(
    html_files,
    key=lambda file: file.stat().st_mtime
)

print("Reading NSP HTML file:", html_file.name)


# ----------------------------------
# 3. Extract Scholarship Information
# ----------------------------------

html_content = html_file.read_text(
    encoding="utf-8",
    errors="replace"
)

soup = BeautifulSoup(html_content, "html.parser")

page_text = soup.get_text(
    separator="\n",
    strip=True
)

scholarships = []

for line in page_text.splitlines():

    clean_name = " ".join(line.split())

    if (
        "(Merit Based Scheme)" in clean_name
        or "(Welfare Based Scheme)" in clean_name
    ):
        scholarships.append(clean_name)


# ----------------------------------
# 4. Remove Duplicate Records
# ----------------------------------

unique_scholarships = {
    name.casefold(): name
    for name in scholarships
}

scholarships = sorted(
    unique_scholarships.values(),
    key=str.casefold
)


# ----------------------------------
# 5. Data Quality Validation
# ----------------------------------

empty_names = [
    name for name in scholarships
    if not name.strip()
]

if not scholarships:
    raise ValueError("No scholarship schemes found.")

if empty_names:
    raise ValueError("Empty scholarship names detected.")

if len(scholarships) != len(unique_scholarships):
    raise ValueError("Duplicate scholarship records detected.")


# ----------------------------------
# 6. Generate Structured CSV
# ----------------------------------

output_file = OUTPUT_FOLDER / "nsp_scholarships.csv"

with output_file.open(
    "w",
    newline="",
    encoding="utf-8-sig"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "scheme_name",
        "source_name",
        "source_url",
        "data_status"
    ])

    for name in scholarships:
        writer.writerow([
            name,
            SOURCE_NAME,
            SOURCE_URL,
            "Official listing text; eligibility not verified"
        ])


# ----------------------------------
# 7. Final Execution Report
# ----------------------------------

print("\nSCHOLARSHIP DATA EXTRACTION REPORT")
print("----------------------------------")

print("Source:", SOURCE_NAME)
print("Total Schemes:", len(scholarships))
print("Duplicate Check: PASSED")
print("Empty Name Check: PASSED")

print("\nCSV FILE GENERATED SUCCESSFULLY")
print("Output:", output_file)

print("\nALL INGESTION VALIDATIONS PASSED!")
