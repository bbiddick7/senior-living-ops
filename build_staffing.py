import duckdb

con = duckdb.connect("senior_living.duckdb")

print("Building facility-level staffing summary...")

con.execute("""
CREATE OR REPLACE TABLE facility_staffing AS
SELECT 
    PROVNUM AS ccn,
    AVG(MDScensus) AS avg_daily_census,
    SUM(Hrs_RN) / NULLIF(SUM(MDScensus), 0) AS rn_hrd,
    SUM(Hrs_LPN) / NULLIF(SUM(MDScensus), 0) AS lpn_hrd,
    SUM(Hrs_CNA) / NULLIF(SUM(MDScensus), 0) AS cna_hrd,
    (SUM(Hrs_RN) + SUM(Hrs_LPN) + SUM(Hrs_CNA)) / NULLIF(SUM(MDScensus), 0) AS total_nurse_hrd,
    SUM(Hrs_RN_ctr + Hrs_LPN_ctr + Hrs_CNA_ctr) / NULLIF(SUM(Hrs_RN + Hrs_LPN + Hrs_CNA), 0) AS contract_pct,
    COUNT(DISTINCT WorkDate) AS days_reported
FROM pbj_daily
WHERE MDScensus > 0
GROUP BY PROVNUM
""")

# Sanity check — what does this look like?
result = con.execute("""
    SELECT 
        COUNT(*) AS total_facilities, 
        ROUND(AVG(total_nurse_hrd), 2) AS avg_nurse_hrd,
        ROUND(MIN(total_nurse_hrd), 2) AS min_hrd,
        ROUND(MAX(total_nurse_hrd), 2) AS max_hrd,
        ROUND(AVG(contract_pct) * 100, 1) AS avg_contract_pct
    FROM facility_staffing
""").fetchone()

print(f"\nBuilt staffing summary for {result[0]:,} facilities.")
print(f"Average total nurse HRD: {result[1]}")
print(f"Range: {result[2]} to {result[3]} HRD")
print(f"Average contract staffing: {result[4]}%")

# Show 5 example facilities
print("\nFirst 5 facilities:")
sample = con.execute("""
    SELECT 
        ccn,
        ROUND(avg_daily_census, 0) AS census,
        ROUND(rn_hrd, 2) AS rn,
        ROUND(lpn_hrd, 2) AS lpn,
        ROUND(cna_hrd, 2) AS cna,
        ROUND(total_nurse_hrd, 2) AS total,
        ROUND(contract_pct * 100, 1) AS contract_pct,
        days_reported
    FROM facility_staffing
    LIMIT 5
""").fetchdf()
print(sample.to_string())