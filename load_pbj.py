import duckdb

# Connect to your existing DuckDB database
con = duckdb.connect("senior_living.duckdb")

pbj_path = "data/PBJ_dailynursestaffing_CY2025Q4.csv"

print("Loading PBJ data... this might take 30-90 seconds.")
print("The terminal will look frozen. It isn't. Be patient.")

con.execute(f"""
CREATE OR REPLACE TABLE pbj_daily AS 
SELECT * FROM read_csv_auto('{pbj_path}', ignore_errors=true)
""")

row_count = con.execute("SELECT COUNT(*) FROM pbj_daily").fetchone()[0]
print(f"\nLoaded {row_count:,} rows of staffing data.")

# Show the column names so we know what we're working with
print("\nFirst 10 columns in PBJ:")
columns = con.execute("DESCRIBE pbj_daily").fetchdf()
print(columns.head(50))

print(f"\nTotal columns: {len(columns)}")