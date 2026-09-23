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

![](/images/aggregating-multiple-scd-2-attribute-timelines-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [***notjustsql.com***](https://www.notjustsql.com/)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Joining temporal tables in BigQuery](/practical-bigquery-joining-temporal-tables)
- [Generating a compact temporal table in BigQuery](/generating-a-compact-temporal-table-in-bigquery)
- [Compacting date intervals in BigQuery](/compacting-date-intervals-in-bigquery)
- [Transforming cumulative sums into monthly values](/transforming-cumulative-sums-into-monthly-values)
