---
title: "Compacting date intervals in BigQuery"
seoTitle: "Merge Adjacent Date Intervals in BigQuery"
seoDescription: "Compact adjacent date intervals in BigQuery by hashing payload columns, detecting boundaries with LAG, and grouping contiguous segments step by step."
datePublished: 2025-06-09T20:38:02.282Z
dateUpdated: 2026-04-05T20:11:31.554Z
cover: "/images/compacting-date-intervals-in-bigquery/cover.jpg"
coverCredit:
  name: "Ray Shrewsberry"
  url: "https://unsplash.com/@ray12119"
series: "practical-sql"
hashnodeCuid: "cmbpk0f8q000202l89rg7hgly"
---

Here's a practical BigQuery SQL exercise that highlights some important concepts as well is an interesting algorithm imho. I've pair programmed this with LLMs, if that's a thing 😎

Problem statement: compacting a SCD-2 table, essentially finding intervals that can be safely merged, turning two adjacent intervals with the same data into a single, bigger interval.

This particular input data guarantees these intervals cannot overlap (at the same grain), but there can be gaps. We're also talking about \[left-inclusive, right-exclusive) intervals.

![Input data: input\_data with valid\_from, valid\_to, product\_id, country\_name, flag\_a and flag\_b, eleven intervals for product 1 (US), 2 (CA) and 3 (US); three pairs of adjacent rows with the same flags are boxed as MERGED: product 1 from 2021-01-12 to 2021-01-25, product 2 from 2021-01-01 to 2021-01-25 and product 3 from 2021-01-01 to 2021-01-20.](/images/compacting-date-intervals-in-bigquery/1-input.jpg)

```sql
WITH prepare_output AS (
  SELECT
    product_id,
    country_name,
    valid_from,
    valid_to,
    flag_a,
    flag_b,
    FARM_FINGERPRINT(CONCAT(TO_JSON_STRING(flag_a),
                            TO_JSON_STRING(flag_b))) AS hash_val
  FROM input_data
),
prepare_segments AS (
  SELECT
    product_id,
    country_name,
    valid_from,
    valid_to,
    flag_a,
    flag_b,
    CASE WHEN LAG(hash_val) OVER country_item = hash_val AND
              valid_from = LAG(valid_to) OVER country_item
         THEN 0 ELSE 1  END AS is_new_segment
  FROM prepare_output
  WINDOW country_item AS (PARTITION BY product_id, country_name
                          ORDER BY valid_from)
),
define_segments AS (
  SELECT
    product_id,
    country_name,
    valid_from,
    valid_to,
    flag_a,
    flag_b,
    SUM(is_new_segment) OVER (PARTITION BY product_id, country_name
                              ORDER BY valid_from
                              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                              ) AS segment_id
  FROM prepare_segments
)
SELECT
  product_id,
  country_name,
  MIN(valid_from) AS valid_from,
  MAX(valid_to) AS valid_to,
  ANY_VALUE(flag_a) AS flag_a,
  ANY_VALUE(flag_b) AS flag_b
FROM define_segments
GROUP BY product_id, country_name, segment_id
```

![BigQuery results: seven compacted intervals, with the merged ones boxed: product 1 US 2021-01-01 to 2021-01-10, 2021-01-12 to 2021-01-25, 2021-01-25 to 2021-02-04 (False, False) and 2021-02-04 to 2021-02-08; product 2 CA 2021-01-01 to 2021-01-25; product 3 US 2021-01-01 to 2021-01-20 and 2021-01-20 to 2021-01-30.](/images/compacting-date-intervals-in-bigquery/1-result.jpg)

Here's a breakdown of how it all works:

1️⃣ we're starting by computing a hash of all the column of interest, excluding the grain (in my example: flag\_a, flag\_b)  
2️⃣ then we use LAG() over grain window to detect whether the current row starts right after the previous one and if the hashes (so the 'payload' of the two rows) match  
3️⃣ we mark the start of a new "segment" when either:  
\- attributes have changed (flags differ), so hash being different  
\- intervals are not adjacent (there are gaps)

4️⃣ use a cumulative SUM() over grain window to group rows into segment IDs

5️⃣ collapse each segment using MIN(valid\_from) and MAX(valid\_to)

We can now see that in our example that several intervals were merged into bigger ones.

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Joining temporal tables in BigQuery](/practical-bigquery-joining-temporal-tables)
- [Generating a compact temporal table in BigQuery](/generating-a-compact-temporal-table-in-bigquery)
- [Aggregating Multiple SCD-2 Attribute Timelines in BigQuery](/aggregating-multiple-scd-2-attribute-timelines-in-bigquery)
- [Transforming cumulative sums into monthly values](/transforming-cumulative-sums-into-monthly-values)
