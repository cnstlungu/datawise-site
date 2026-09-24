---
title: "Aggregating Multiple SCD-2 Attribute Timelines in BigQuery"
seoTitle: "BigQuery: Aggregating SCD-2 Attribute Timelines"
seoDescription: "Learn how to aggregate SCD-2 attribute timelines in BigQuery using SQL techniques to preserve temporal context efficiently"
datePublished: 2025-06-11T19:22:01.519Z
dateUpdated: 2026-03-02T10:52:56.234Z
cover: "/images/aggregating-multiple-scd-2-attribute-timelines-in-bigquery/cover.jpg"
coverCredit:
  name: "𝓴𝓘𝓡𝓚 𝕝𝔸𝕀"
  url: "https://unsplash.com/@kirklai"
series: "practical-sql"
hashnodeCuid: "cmbsc6dgv000202jrcn3p5zee"
---

Here’s another practical BigQuery SQL exercise 💡

Say you have an input SCD2-style table with \[valid\_from, valid\_to) and key-value attributes. Now you want to determine which attributes were valid at the same time for a given grain (e.g. id).

To do this, we:

1️⃣ Build an anchor table of all change points (start and end dates), grouped by id.

2️⃣ Generate date ranges using LEAD() over the change points, so we know the next boundary.

3️⃣ Join back to the original table to find which rows were active within each \[valid\_from, valid\_to) segment.

4️⃣ Aggregate the key-value pairs as ARRAY&lt;STRUCT&lt;key, value&gt;&gt; to preserve temporal context.

We can now see that, for example, for the period between \[2023-01-05, 2023-01-08), for id = 2, B was true and A was false.

![Input data: an ASCII table with valid\_from, valid\_to, id, key and value, five rows: id 1 has A true from 2021-01-01 to 2021-01-10 and B true from 2021-01-05 to 2021-01-15; id 2 has B true from 2022-01-05 to 2022-01-15, B true from 2023-01-05 to 2023-01-15 and A false from 2023-01-03 to 2023-01-08.](/images/aggregating-multiple-scd-2-attribute-timelines-in-bigquery/1-input.jpg)

```sql
WITH anchor_dates AS (

SELECT id, valid_from AS valid_date FROM input_data
UNION DISTINCT
SELECT id, valid_to AS valid_date FROM input_data),

date_ranges AS (
SELECT
  id,
  valid_date AS valid_from,
  LEAD(valid_date) OVER (PARTITION BY id ORDER BY valid_date) AS valid_to
FROM anchor_dates
)

SELECT
  dr.id,
  dr.valid_from,
  dr.valid_to,
  ARRAY_AGG(STRUCT(dt.key, dt.value)) AS attributes

FROM date_ranges dr
LEFT JOIN input_data dt ON dr.id = dt.id  AND dr.valid_from < dt.valid_to AND dr.valid_to > dt.valid_from

WHERE dr.valid_to IS NOT NULL

GROUP BY dr.id,  dr.valid_from, dr.valid_to

ORDER BY id,  valid_from
```

![BigQuery results: one row per id and date range with an attributes array of key/value pairs; for example id 1 from 2021-01-05 to 2021-01-10 has A true and B true, id 2 from 2022-01-15 to 2023-01-03 has null, and id 2 from 2023-01-05 to 2023-01-08 has B true and A false.](/images/aggregating-multiple-scd-2-attribute-timelines-in-bigquery/1-result.jpg)

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Joining temporal tables in BigQuery](/practical-bigquery-joining-temporal-tables)
- [Generating a compact temporal table in BigQuery](/generating-a-compact-temporal-table-in-bigquery)
- [Compacting date intervals in BigQuery](/compacting-date-intervals-in-bigquery)
- [Transforming cumulative sums into monthly values](/transforming-cumulative-sums-into-monthly-values)
