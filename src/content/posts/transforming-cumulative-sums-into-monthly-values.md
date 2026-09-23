---
title: "Transforming cumulative sums into monthly values"
seoTitle: "Monthly Values from Cumulative Sums"
seoDescription: "Reverse cumulative sums to monthly values using BigQuery, focusing on fiscal year, lag function, and grain considerations"
datePublished: 2025-03-27T07:34:24.903Z
dateUpdated: 2026-03-02T10:52:04.889Z
cover: "/images/transforming-cumulative-sums-into-monthly-values/cover.jpg"
coverCredit:
  name: "kofookoo.de"
  url: "https://unsplash.com/@kofookoo"
series: "bigquery-window-functions"
hashnodeCuid: "cm8r1fn2f000q09jy9kl73vgy"
---

Here’s a quick BigQuery SQL exercise. I often work with cumulative aggregations, but it’s not every day that I need to reverse them—converting cumulative values back into monthly figures.

Let's look at an example.

The dataset provides cumulative sales per fiscal year (July 1st - June 30th in this case). Our goal is to determine the actual sales for each month.

How do we do it?

1. Identify the fiscal year each period belongs to. We can use a UDF (as shown) or retrieve this from a date dimension table.

2. Use the LAG window function to retrieve the previous cumulative value (partitioned by our grain + fiscal year and ordered by period).

3. Subtract the previous cumulative value from the current one to derive the actual monthly sales.

• For the first month of a fiscal year, there’s no previous value, so we default to 0 in case of a NULL there.

Things to watch out for:  
➡️ Gaps in the data: How do they impact the calculation? Are we okay with that?  
➡️ Grain considerations: Do we need to do this per department? Per country? If so, adjust the PARTITION BY accordingly.

![BigQuery SQL turning cumulative fiscal-year sales into monthly values: a temp function GET\_FINANCIAL\_YEAR\_START (July to June), LAG(cumulative\_fy\_sales,1) per fiscal year, and cumulative\_fy\_sales minus IFNULL(LAG(...),0) AS current\_month\_sales; 1100 cumulative in 2021-01 becomes 300.](/images/transforming-cumulative-sums-into-monthly-values/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [***notjustsql.com***](https://www.notjustsql.com/)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Joining temporal tables in BigQuery](/practical-bigquery-joining-temporal-tables)
- [Generating a compact temporal table in BigQuery](/generating-a-compact-temporal-table-in-bigquery)
- [Aggregating Multiple SCD-2 Attribute Timelines in BigQuery](/aggregating-multiple-scd-2-attribute-timelines-in-bigquery)
- [Compacting date intervals in BigQuery](/compacting-date-intervals-in-bigquery)
