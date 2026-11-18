from pathlib import Path
import pyarrow.parquet as pq

# ----------------------------------
# 1. Project Paths
# ----------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PARQUET_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "scholarships_cleaned"
    / "scholarships_cleaned.parquet"
)

# ----------------------------------
# 2. Read Parquet File
# ----------------------------------

print("\nSCHOLARSHIP DATA QUALITY TEST")
print("-----------------------------")

table = pq.read_table(PARQUET_PATH)
df = table.to_pandas()

# ----------------------------------
# 3. Data Quality Checks
# ----------------------------------

total_records = len(df)

empty_names = df["scheme_name"].isna().sum() + (
    df["scheme_name"].str.strip() == ""
).sum()

duplicate_names = df["scheme_name"].duplicated().sum()

invalid_categories = (
    ~df["scheme_category"].isin(["Merit Based", "Welfare Based"])
).sum()

empty_urls = df["source_url"].isna().sum() + (
    df["source_url"].str.strip() == ""
).sum()

# ----------------------------------
# 4. Display Results
# ----------------------------------

print("Total Records:", total_records)

print(
    "Empty Scholarship Names:",
    "PASSED" if empty_names == 0 else "FAILED",
    "| Count:", empty_names
)

print(
    "Duplicate Scholarship Names:",
    "PASSED" if duplicate_names == 0 else "FAILED",
    "| Count:", duplicate_names
)

print(
    "Invalid Categories:",
    "PASSED" if invalid_categories == 0 else "FAILED",
    "| Count:", invalid_categories
)

print(
    "Empty Source URLs:",
    "PASSED" if empty_urls == 0 else "FAILED",
    "| Count:", empty_urls
)

# ----------------------------------
# 5. Overall Result
# ----------------------------------

if (
    empty_names == 0
    and duplicate_names == 0
    and invalid_categories == 0
    and empty_urls == 0
):
    print("\nOVERALL RESULT: PASSED")
else:
    print("\nOVERALL RESULT: FAILED")

print("Validation completed!")