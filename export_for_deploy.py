import duckdb
import os

con = duckdb.connect("senior_living.duckdb", read_only=True)

# Make sure the output directory exists
os.makedirs("deploy_data", exist_ok=True)

print("Exporting facility_peer_analysis...")
con.execute("""
    COPY facility_peer_analysis 
    TO 'deploy_data/facility_peer_analysis.parquet' 
    (FORMAT PARQUET, COMPRESSION ZSTD)
""")

# Verify the file size
size_mb = os.path.getsize("deploy_data/facility_peer_analysis.parquet") / (1024 * 1024)
row_count = con.execute("SELECT COUNT(*) FROM facility_peer_analysis").fetchone()[0]

print(f"Exported {row_count:,} rows to facility_peer_analysis.parquet ({size_mb:.2f} MB)")
print("\nReady to deploy.")