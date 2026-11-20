#  Scholarship Intelligence & Data Platform

# Project Description

This project extracts scholarship scheme information from the official National Scholarship Portal (NSP), processes and cleans data using Python and PySpark, validates data quality, stores structured data in Snowflake, and visualizes scholarship category insights using Power BI.
# Technologies Used

- Python
- SQL
- PySpark
- Snowflake
- Power BI
- GitHub

# Key Features

- Extract scholarship scheme names from the official NSP website.
- Generate structured CSV data using Python.
- Clean and transform records using PySpark.
- Store processed data in Parquet format.
- Load 31 records into Snowflake.
- Perform data quality validation.
- Create scholarship category summaries using SQL.
- Visualize insights using Power BI.
# Project Workflow

1. Extract scholarship scheme names from the official NSP website.
2. Save the raw HTML snapshot for source traceability.
3. Generate structured CSV data using Python.
4. Clean and transform data using PySpark.
5. Store processed data in Parquet format in the local Silver layer.
6. Load processed records into Snowflake Silver schema.
7. Create category summary in Snowflake Gold schema.
8. Validate data quality using Python and SQL.
9. Connect Snowflake Gold data to Power BI for visualization.
# Data Sources

- National Scholarship Portal (NSP)
Currently, the project uses the official National Scholarship Portal (NSP) listing as its data source.
Note: The current dataset contains scholarship scheme names from the official NSP listing. Detailed eligibility information has not been verified.
# Power BI Dashboard
[View / Download Power BI Dashboard](report/Scholarship_Intelligence_Dashboard.pbix)

# Cloud Technology (Future Scope)

- Azure Data Lake Storage Gen2
- Planned cloud integration for future pipeline enhancement

# Architecture Diagram

![Project Architecture](report/Scholarship%20Intelligence%20Data%20Platform%20Architecture.png)
