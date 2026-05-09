# Senior Living Operations Intelligence

**[Live dashboard →](https://senior-living-ops-lappjvwboq83p22mpapjdz3.streamlit.app/)**

A unified analytics layer across fragmented public data sources in senior living and skilled nursing — built to demonstrate what's possible inside an operator's own walls.

---

## Why this exists

Senior living and skilled nursing operators sit on data scattered across 8–12 systems: EHR, eMAR, PBJ, CRM, scheduling, billing, compliance, surveys, finance. Cross-system questions take weeks to answer because no one owns the seams.

The public data landscape has the same problem in miniature. CMS publishes facility data in one shape, states publish assisted living data in 50 different shapes, BLS publishes workforce data in a third shape, and none of them share a clean identifier.

This project unifies that public landscape. The pattern that makes it work is the same pattern that works on operators' internal stacks.

---

## What it does

A live dashboard that flags nursing facilities understaffed relative to their peers — same state, same bed-size cohort — combining CMS Provider Info with Payroll-Based Journal staffing data. Filter by state, bed size, and staffing percentile. Updates instantly.

**Why this question matters to operators:**

Corporate offices see their own staffing numbers. They can't easily see *peer* numbers. That comparison drives capital allocation, agency-spend decisions, acquisition targeting, and quality-improvement priorities. The dashboard answers in seconds what most operators can't answer at all.

**A few things that make the output credible:**

- Computes the industry-standard hours-per-resident-day (HRD) metric the same way CMS does
- Tracks contract-staffing percentage — the post-COVID stress signal operators care about most
- Peer cohorts are state + bed-size, not national, because comparing a 50-bed rural facility to a 250-bed urban facility is meaningless

---

## What was hard (and why it matters for your team)

The interesting work wasn't the SQL. It was:

**Identity resolution.** CMS uses CCN. States use their own license numbers. Names and addresses drift across sources. *On your stack, this is the same problem between your EHR's resident ID, your CRM's lead ID, your billing system's account ID, and your compliance system's case ID.*

**Schema drift.** CMS occasionally renames PBJ columns between quarterly refreshes. State data dictionaries change without notice. Vendor systems update without warning. *Every operator has lived this — every upgrade is a small fire.*

**Grain reconciliation.** PBJ is daily. Provider Info is monthly. Deficiencies are by survey cycle. ACS is annual. Picking a unified grain and documenting every rollup is one of the hardest unsolved problems in operator BI. *You feel this every time finance, ops, and clinical disagree on the "real" number.*

---

## How this translates to your organization

If you operate 5–500 communities, the same pattern works on your internal data:

1. **Identity layer first.** One resident, one staff member, one community — across every system.
2. **Schema contracts.** Vendor changes don't break your dashboards.
3. **A unified semantic model** that finance, ops, and clinical can all trust.
4. **Operator-grade questions, not vanity metrics** — census trends, agency-spend ROI, staffing-vs-quality early warning, market-entry workforce stress.

**Typical engagement:** 6–10 weeks to a unified operator dashboard across your top 3–5 systems. Fixed-fee scoping call, milestone-based delivery.

I work with mid-market operators who have the pain but don't want to build a 4-person internal data team.

**Next step:** [Reach out via LinkedIn →](https://www.linkedin.com/in/benbiddick/) — or email at the address in my profile.

---

## Tech stack

Python · DuckDB · Streamlit · Pandas · GitHub. The whole thing runs on a laptop and deploys to Streamlit Community Cloud. Intentionally boring, because operators hire people who use tools their internal teams can maintain.

---

## Data sources

- [CMS Provider Data Catalog](https://data.cms.gov/provider-data/topics/nursing-homes) — Provider Info, Health Deficiencies
- [CMS Payroll-Based Journal](https://data.cms.gov/quality-of-care/payroll-based-journal-daily-non-nurse-staffing) — daily staffing by job code
- State licensing databases (Wisconsin first, more states added on demand)

None of these organizations endorse this analysis. Any errors are mine.

---

## About me

Ben Biddick. Multiple years across operations, clinical, and finance roles in aging services. Now building data infrastructure for operators who need a unified view but don't want to staff an internal data team.

Based in Madison, Wisconsin. Work nationally.