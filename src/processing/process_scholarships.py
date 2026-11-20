
from pathlib import Path
import shutil

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, when

import pyarrow as pa
import pyarrow.parquet as pq


# ----------------------------------
# 1. PROJECT CONFIGURATION
# ----------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CSV_PATH = PROJECT_ROOT / "data" / "processed" / "nsp_scholarships.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "scholarships_cleaned"

PARQUET_FILE = OUTPUT_PATH / "scholarships_cleaned.parquet"


# ----------------------------------
# 2. CHECK INPUT FILE
# ----------------------------------

if not CSV_PATH.exists():
    raise FileNotFoundError(f"Input CSV not found: {CSV_PATH}")


# ----------------------------------
# 3. CREATE SPARK SESSION
# ----------------------------------

spark = (
    SparkSession.builder
    .appName("ScholarshipIntelligencePipeline")
    .master("local[*]")
    .getOrCreate()
)

try:

    # ----------------------------------
    # 4. READ SCHOLARSHIP DATA
    # ----------------------------------

    print("\nREADING SCHOLARSHIP DATA")
    print("------------------------")

    df = spark.read.csv(
        str(CSV_PATH),
        header=True,
        inferSchema=False
    )

    required_columns = {
        "scheme_name",
        "source_name",
        "source_url",
        "data_status"
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    original_count = df.count()

    print("Original Records:", original_count)


    # ----------------------------------
    # 5. DATA CLEANING
    # ----------------------------------

    print("\nDATA CLEANING")
    print("-------------")

    df = df.withColumn(
        "scheme_name",
        trim(col("scheme_name"))
    )

    df = df.filter(
        col("scheme_name").isNotNull() &
        (col("scheme_name") != "")
    )

    df = df.dropDuplicates(["scheme_name"])

    cleaned_count = df.count()

    print("Cleaned Records:", cleaned_count)


    # ----------------------------------
    # 6. SCHOLARSHIP CATEGORY
    # ----------------------------------

    print("\nCREATING SCHOLARSHIP CATEGORY")
    print("-----------------------------")

    df = df.withColumn(
        "scheme_category",
        when(
            col("scheme_name").contains("(Merit Based Scheme)"),
            "Merit Based"
        ).when(
            col("scheme_name").contains("(Welfare Based Scheme)"),
            "Welfare Based"
        ).otherwise("Unknown")
    )

    df.select(
        "scheme_name",
        "scheme_category"
    ).show(10, truncate=False)


    # ----------------------------------
    # 7. FINAL DATAFRAME
    # ----------------------------------

    print("\nFINAL SCHOLARSHIP DATAFRAME")
    print("---------------------------")

    df.show(10, truncate=False)

    print("Total Records:", cleaned_count)
    print("Total Columns:", len(df.columns))
    print("Column Names:", df.columns)


    # ----------------------------------
    # 8. SAVE DATA AS PARQUET
    # ----------------------------------

    print("\nSAVING CLEANED DATA")
    print("-------------------")

    # Dataset currently contains only 31 records.
    # Collecting records for PyArrow Parquet output is
    # suitable for this small local dataset.

    rows = [
        row.asDict(recursive=True)
        for row in df.collect()
    ]

    table = pa.Table.from_pylist(rows)

    if OUTPUT_PATH.exists():
        shutil.rmtree(OUTPUT_PATH)

    OUTPUT_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    pq.write_table(
        table,
        PARQUET_FILE
    )

    print("Cleaned data saved successfully!")
    print("Output Path:", PARQUET_FILE)
    print("Total Records Saved:", table.num_rows)


finally:

    # ----------------------------------
    # 9. STOP SPARK SESSION
    # ----------------------------------

    spark.stop()

    print("\nSPARK SESSION STOPPED")


print("PROCESS COMPLETED SUCCESSFULLY!")
