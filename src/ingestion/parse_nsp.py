
""" from pathlib import Path
from bs4 import BeautifulSoup

# Find project folder
project_root = Path(__file__).resolve().parents[2]

raw_folder = project_root / "data" / "raw"

# Find downloaded HTML file
html_files = list(raw_folder.glob("*.html"))

if not html_files:
    print("Error: No HTML file found!")
    raise SystemExit(1)

html_file = max(html_files, key=lambda file: file.stat().st_mtime)

print("Reading file:", html_file.name)

# Read HTML
html_content = html_file.read_text(
    encoding="utf-8",
    errors="replace"
)

soup = BeautifulSoup(html_content, "html.parser")

# Extract visible text
page_text = soup.get_text(separator="\n", strip=True)

# Search scholarship-related lines
keywords = ["AICTE", "Scholarship", "Merit Based"]

matches = []

for line in page_text.splitlines():
    if any(word.lower() in line.lower() for word in keywords):
        matches.append(line)

print("\nScholarship-related information:\n")

for item in matches[:30]:
    print("-", item)

print("\nTotal matching lines:", len(matches))
"""



from pathlib import Path
import csv
from bs4 import BeautifulSoup

project_root = Path(__file__).resolve().parents[2]

raw_folder = project_root / "data" / "raw"
output_folder = project_root / "data" / "processed"

output_folder.mkdir(parents=True, exist_ok=True)

# Find latest downloaded HTML
html_files = list(raw_folder.glob("*.html"))

if not html_files:
    raise FileNotFoundError("No NSP HTML file found")

html_file = max(
    html_files,
    key=lambda file: file.stat().st_mtime
)

# Read HTML
html_content = html_file.read_text(
    encoding="utf-8",
    errors="replace"
)

soup = BeautifulSoup(html_content, "html.parser")
page_text = soup.get_text(separator="\n", strip=True)

# Keep only lines with scheme classification
scholarships = []

for line in page_text.splitlines():

    clean_name = " ".join(line.split())

    is_merit = "(Merit Based Scheme)" in clean_name
    is_welfare = "(Welfare Based Scheme)" in clean_name

    if is_merit or is_welfare:
        scholarships.append(clean_name)

# Remove duplicates
scholarships = list({
    name.casefold(): name
    for name in scholarships
}.values())

# Sort names
scholarships.sort(key=str.casefold)

# Create CSV
output_file = output_folder / "nsp_scholarships.csv"

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
            "National Scholarship Portal",
            "https://scholarships.gov.in/All-Scholarships",
            "Official listing text; eligibility not verified"
        ])

# Validation
print("\nDATA QUALITY REPORT")
print("-------------------")

print("Total schemes:", len(scholarships))
print("Duplicate check:", "PASSED")

empty_names = [name for name in scholarships if not name.strip()]

print("Empty name check:", "PASSED" if not empty_names else "FAILED")

if not scholarships or empty_names:
    raise ValueError("Data quality validation failed")

print("CSV created:", output_file)
print("All basic validation checks passed!")
