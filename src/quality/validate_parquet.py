
from pathlib import Path
import sys
import pyarrow.parquet as pq


# ----------------------------------
# 1. PROJECT CONFIGURATION
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
# 2. CHECK PARQUET FILE
# ----------------------------------

print("\nSCHOLARSHIP DATA QUALITY TEST")
print("-----------------------------")

if not PARQUET_PATH.exists():
    raise FileNotFoundError(
        f"Parquet file not found: {PARQUET_PATH}"
    )


# ----------------------------------
# 3. READ PARQUET DATA
# ----------------------------------

table = pq.read_table(PARQUET_PATH)
df = table.to_pandas()

required_columns = {
    "scheme_name",
    "source_url",
    "scheme_category"
}

missing_columns = required_columns - set(df.columns)

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )


# ----------------------------------
# 4. DATA QUALITY CHECKS
# ----------------------------------

total_records = len(df)

empty_names = (
    df["scheme_name"].isna()
    | df["scheme_name"].fillna("").str.strip().eq("")
).sum()

duplicate_names = df["scheme_name"].duplicated().sum()

invalid_categories = (
    ~df["scheme_category"].isin(
        ["Merit Based", "Welfare Based"]
    )
).sum()

empty_urls = (
    df["source_url"].isna()
    | df["source_url"].fillna("").str.strip().eq("")
).sum()


# ----------------------------------
# 5. DISPLAY VALIDATION RESULTS
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
# 6. OVERALL VALIDATION RESULT
# ----------------------------------

all_checks_passed = (
    total_records > 0
    and empty_names == 0
    and duplicate_names == 0
    and invalid_categories == 0
    and empty_urls == 0
)

if all_checks_passed:
    print("\nOVERALL RESULT: PASSED")
    print("All data quality checks completed successfully!")
else:
    print("\nOVERALL RESULT: FAILED")
    print("Please review the data quality issues.")
    sys.exit(1)

print("Validation completed!")
