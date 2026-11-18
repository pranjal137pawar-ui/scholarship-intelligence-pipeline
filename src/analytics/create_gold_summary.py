
from pathlib import Path
import pyarrow.parquet as pq
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

SILVER_PATH = (
    PROJECT_ROOT / "data" / "lake" / "silver"
    / "scholarships_cleaned.parquet"
)

GOLD_PATH = PROJECT_ROOT / "data" / "lake" / "gold"

# Read Silver data
df = pq.read_table(SILVER_PATH).to_pandas()

# Create scholarship category summary
total_scholarships = len(df)

category_counts = df["scheme_category"].value_counts()

summary = pd.DataFrame({
    "metric": [
        "Total Scholarships",
        "Merit Based Scholarships",
        "Welfare Based Scholarships"
    ],
    "scholarship_count": [
        total_scholarships,
        category_counts.get("Merit Based", 0),
        category_counts.get("Welfare Based", 0)
    ]
})

# Save Gold data
GOLD_PATH.mkdir(parents=True, exist_ok=True)

output_path = GOLD_PATH / "scholarship_summary.parquet"

summary.to_parquet(output_path, index=False)

# Display result
print("\nGOLD LAYER - SCHOLARSHIP SUMMARY")
print("--------------------------------")
print(summary.to_string(index=False))
print("--------------------------------")
print("Total Scholarships:", total_scholarships)
print("Gold data saved successfully!")
print("Output:", output_path)
