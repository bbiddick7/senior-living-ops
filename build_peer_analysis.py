import duckdb

con = duckdb.connect("senior_living.duckdb")

print("Building peer cohort analysis...")

# This combines providers + staffing into one analysis table
# and computes peer-cohort percentiles for staffing
con.execute("""
CREATE OR REPLACE TABLE facility_peer_analysis AS
WITH joined AS (
    SELECT 
        p."CMS Certification Number (CCN)" AS ccn,
        p."Provider Name" AS provider_name,
        p."City/Town" AS city,
        p."State" AS state,
        p."County/Parish" AS county,
        p."Number of Certified Beds" AS beds,
        p."Ownership Type" AS ownership,
        p."Overall Rating" AS overall_rating,
        p."Staffing Rating" AS staffing_rating,
        s.total_nurse_hrd,
        s.rn_hrd,
        s.cna_hrd,
        s.contract_pct,
        CASE 
            WHEN p."Number of Certified Beds" < 50 THEN 'Under 50'
            WHEN p."Number of Certified Beds" < 100 THEN '50-99'
            WHEN p."Number of Certified Beds" < 200 THEN '100-199'
            ELSE '200+'
        END AS bed_cohort
    FROM providers p
    LEFT JOIN facility_staffing s 
        ON p."CMS Certification Number (CCN)" = s.ccn
    WHERE s.total_nurse_hrd IS NOT NULL
)
SELECT 
    *,
    PERCENT_RANK() OVER (
        PARTITION BY state, bed_cohort 
        ORDER BY total_nurse_hrd
    ) AS staffing_percentile_in_cohort,
    MEDIAN(total_nurse_hrd) OVER (
        PARTITION BY state, bed_cohort
    ) AS cohort_median_hrd,
    total_nurse_hrd - MEDIAN(total_nurse_hrd) OVER (
        PARTITION BY state, bed_cohort
    ) AS gap_vs_cohort_median
FROM joined
""")

# Sanity check
total = con.execute("SELECT COUNT(*) FROM facility_peer_analysis").fetchone()[0]
print(f"\nBuilt peer analysis for {total:,} facilities.\n")

# Show the 10 most-understaffed Wisconsin facilities relative to their bed-size peers
print("10 most understaffed Wisconsin facilities relative to their bed-size cohort:\n")
result = con.execute("""
SELECT 
    provider_name AS facility,
    city,
    beds,
    bed_cohort,
    ROUND(total_nurse_hrd, 2) AS hrd,
    ROUND(cohort_median_hrd, 2) AS cohort_median,
    ROUND(staffing_percentile_in_cohort * 100, 0) AS pct_rank,
    overall_rating AS rating
FROM facility_peer_analysis
WHERE state = 'WI' 
  AND staffing_percentile_in_cohort < 0.25
ORDER BY staffing_percentile_in_cohort
LIMIT 10
""").fetchdf()

print(result.to_string())