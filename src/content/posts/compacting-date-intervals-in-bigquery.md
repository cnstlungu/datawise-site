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

![BigQuery SQL compacting SCD-2 intervals in four steps: FARM\_FINGERPRINT of the flags as hash\_val, LAG over a named WINDOW to flag is\_new\_segment, a running SUM as segment\_id, then MIN(valid\_from) and MAX(valid\_to) per segment; adjacent rows with equal flags merge, e.g. into 2021-01-12 to 2021-01-25.](/images/compacting-date-intervals-in-bigquery/1.jpg)

Here's a breakdown of how it all works:

1️⃣ we're starting by computing a hash of all the column of interest, excluding the grain (in my example: flag\_a, flag\_b)  
2️⃣ then we use LAG() over grain window to detect whether the current row starts right after the previous one and if the hashes (so the 'payload' of the two rows) match  
3️⃣ we mark the start of a new "segment" when either:  
\- attributes have changed (flags differ), so hash being different  
\- intervals are not adjacent (there are gaps)

4️⃣ use a cumulative SUM() over grain window to group rows into segment IDs

5️⃣ collapse each segment using MIN(valid\_from) and MAX(valid\_to)

We can now see that in our example that several intervals were merged into bigger ones.

*Found it useful? Subscribe to my Analytics newsletter at* [***notjustsql.com***](https://www.notjustsql.com/)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Joining temporal tables in BigQuery](/practical-bigquery-joining-temporal-tables)
- [Generating a compact temporal table in BigQuery](/generating-a-compact-temporal-table-in-bigquery)
- [Aggregating Multiple SCD-2 Attribute Timelines in BigQuery](/aggregating-multiple-scd-2-attribute-timelines-in-bigquery)
- [Transforming cumulative sums into monthly values](/transforming-cumulative-sums-into-monthly-values)
