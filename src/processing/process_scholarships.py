
from pathlib import Path
import shutil

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, when

import pyarrow as pa
import pyarrow.parquet as pq


# ----------------------------------
# 1. Project Paths
# ----------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CSV_PATH = PROJECT_ROOT / "data" / "processed" / "nsp_scholarships.csv"

OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "scholarships_cleaned"


# ----------------------------------
# 2. Create Spark Session
# ----------------------------------

spark = SparkSession.builder \
    .appName("ScholarshipIntelligencePipeline") \
    .master("local[*]") \
    .getOrCreate()


# ----------------------------------
# 3. Read Scholarship CSV
# ----------------------------------

print("\nREADING SCHOLARSHIP DATA")
print("------------------------")

df = spark.read.csv(
    str(CSV_PATH),
    header=True,
    inferSchema=True
)

print("Original Records:", df.count())


# ----------------------------------
# 4. Data Cleaning
# ----------------------------------

print("\nDATA CLEANING")
print("-------------")

# Remove extra spaces
df = df.withColumn(
    "scheme_name",
    trim(col("scheme_name"))
)

# Remove null and empty scholarship names
df = df.filter(
    col("scheme_name").isNotNull() &
    (col("scheme_name") != "")
)

# Remove duplicate scholarship names
df = df.dropDuplicates(["scheme_name"])

print("Cleaned Records:", df.count())


# ----------------------------------
# 5. Create Scholarship Category
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
# 6. Display Final DataFrame
# ----------------------------------

print("\nFINAL SCHOLARSHIP DATAFRAME")
print("---------------------------")

df.show(10, truncate=False)

print("Total Records:", df.count())
print("Total Columns:", len(df.columns))
print("Column Names:", df.columns)


# ----------------------------------
# 7. Save Cleaned Data in Parquet
# ----------------------------------

print("\nSAVING CLEANED DATA")
print("-------------------")

# Convert Spark DataFrame into Python records
rows = [
    row.asDict(recursive=True)
    for row in df.collect()
]

# Create PyArrow Table
table = pa.Table.from_pylist(rows)

# Remove old output folder if it exists
if OUTPUT_PATH.exists():
    shutil.rmtree(OUTPUT_PATH)

# Create output folder
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# Save Parquet file
PARQUET_FILE = OUTPUT_PATH / "scholarships_cleaned.parquet"

pq.write_table(
    table,
    PARQUET_FILE
)

print("Cleaned data saved successfully!")
print("Output Path:", PARQUET_FILE)
print("Total Records Saved:", table.num_rows)


# ----------------------------------
# 8. Stop Spark Session
# ----------------------------------

spark.stop()

print("\nSPARK SESSION STOPPED")
print("PROCESS COMPLETED SUCCESSFULLY!")
