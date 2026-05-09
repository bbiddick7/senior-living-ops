import streamlit as st
import duckdb
import pandas as pd

# Page setup
st.set_page_config(
    page_title="Senior Living Operations Intelligence",
    layout="wide"
)

st.title("Senior Living Operations Intelligence")
st.caption("Peer-cohort staffing analysis using public CMS data")

# Connect to the database (read-only since we're just querying)
import os

# In production (Streamlit Cloud), use the pre-built parquet file.
# Locally, use the full DuckDB database if available.
if os.path.exists("senior_living.duckdb"):
    con = duckdb.connect("senior_living.duckdb", read_only=True)
else:
    con = duckdb.connect(":memory:")
    con.execute("""
        CREATE TABLE facility_peer_analysis AS 
        SELECT * FROM 'deploy_data/facility_peer_analysis.parquet'
    """)
# ---- SIDEBAR FILTERS ----
st.sidebar.header("Filters")

# Get list of states from the data
states = con.execute(
    "SELECT DISTINCT state FROM facility_peer_analysis WHERE state IS NOT NULL ORDER BY state"
).fetchdf()["state"].tolist()

# Default to Wisconsin if it's in the list, otherwise first state
default_state_index = states.index("WI") if "WI" in states else 0

selected_state = st.sidebar.selectbox(
    "State",
    states,
    index=default_state_index
)

bed_cohorts = ["Under 50", "50-99", "100-199", "200+"]
selected_cohorts = st.sidebar.multiselect(
    "Bed size cohorts",
    bed_cohorts,
    default=bed_cohorts
)

percentile_threshold = st.sidebar.slider(
    "Show facilities below this percentile in their cohort",
    min_value=10,
    max_value=50,
    value=25,
    step=5,
    help="25 = bottom quartile. Lower numbers = more selective."
)

# ---- TOP-LEVEL METRICS ----
state_summary = con.execute("""
    SELECT 
        COUNT(*) AS facility_count,
        ROUND(AVG(total_nurse_hrd), 2) AS avg_hrd,
        ROUND(MEDIAN(total_nurse_hrd), 2) AS median_hrd,
        ROUND(AVG(contract_pct) * 100, 1) AS avg_contract_pct
    FROM facility_peer_analysis
    WHERE state = ?
""", [selected_state]).fetchone()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Facilities in state", f"{state_summary[0]:,}")
col2.metric("Avg nurse HRD", state_summary[1])
col3.metric("Median nurse HRD", state_summary[2])
col4.metric("Avg contract %", f"{state_summary[3]}%")

# ---- MAIN TABLE ----
st.subheader(f"Bottom-percentile staffing facilities in {selected_state}")

st.write(
    f"Facilities below the {percentile_threshold}th percentile in their state-and-bed-size cohort. "
    "Lower percentile means more understaffed relative to peers."
)

# Build the query with the selected filters
if not selected_cohorts:
    st.warning("Select at least one bed cohort.")
    st.stop()

placeholders = ",".join(["?"] * len(selected_cohorts))
query = f"""
SELECT 
    provider_name AS "Facility",
    city AS "City",
    beds AS "Beds",
    bed_cohort AS "Bed Cohort",
    ROUND(total_nurse_hrd, 2) AS "Total Nurse HRD",
    ROUND(cohort_median_hrd, 2) AS "Cohort Median HRD",
    ROUND(staffing_percentile_in_cohort * 100, 0) AS "Percentile",
    ROUND(contract_pct * 100, 1) AS "Contract %",
    overall_rating AS "Overall Rating",
    staffing_rating AS "Staffing Rating",
    ownership AS "Ownership"
FROM facility_peer_analysis
WHERE state = ?
  AND bed_cohort IN ({placeholders})
  AND staffing_percentile_in_cohort < ?
ORDER BY staffing_percentile_in_cohort
"""

params = [selected_state] + selected_cohorts + [percentile_threshold / 100]
df = con.execute(query, params).fetchdf()

st.metric("Facilities flagged", len(df))

st.dataframe(df, use_container_width=True, hide_index=True)

# ---- METHODOLOGY ----
st.divider()
with st.expander("How this works"):
    st.markdown("""
    **Peer cohort** = facilities in the same state and bed-size bucket (Under 50, 50-99, 100-199, 200+).

    **Total Nurse HRD** = total nurse hours per resident per day, summed across RN + LPN + CNA categories. 
    Calculated from CMS Payroll-Based Journal (PBJ) data.

    **Percentile in Cohort** = where this facility ranks against its peers. Lower = less staffing.

    **Contract %** = percentage of nurse hours provided by agency/contract staff vs. employed staff.

    Built on [CMS Provider Data](https://data.cms.gov/provider-data/) and 
    [Payroll-Based Journal](https://data.cms.gov/quality-of-care/payroll-based-journal-daily-non-nurse-staffing) datasets.
    """)