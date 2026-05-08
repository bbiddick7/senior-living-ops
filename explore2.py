import duckdb

# Point to the CSV file you downloaded
csv_path = "data/NH_HealthCitations_Apr2026.csv"

# Replace "Mmm2026" above with whatever your actual filename says

# Connect to DuckDB (creates a new database file in your folder)
con = duckdb.connect("senior_living.duckdb")

# Load the CSV into a table called "providers"
con.execute(f"CREATE OR REPLACE TABLE providers AS SELECT * FROM read_csv_auto('{csv_path}')")

# Count the rows
result = con.execute("SELECT COUNT(*) FROM providers").fetchone()
print(f"Loaded {result[0]} nursing homes.")

# Show the first 5 rows
print(con.execute("SELECT * FROM providers LIMIT 5").fetchdf())
