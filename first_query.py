import duckdb

con = duckdb.connect("senior_living.duckdb")

# How many facilities are there per state, with their average rating?
query = """
SELECT 
    "State" AS state,
    COUNT(*) AS facility_count,
    ROUND(AVG(CAST("Overall Rating" AS DOUBLE)), 2) AS avg_rating
FROM providers
WHERE "Overall Rating" IS NOT NULL
GROUP BY "State"
ORDER BY facility_count DESC
LIMIT 10
"""

result = con.execute(query).fetchdf()
print(result)