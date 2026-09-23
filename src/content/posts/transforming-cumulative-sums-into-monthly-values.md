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

![Input data: month\_start\_date from 2020-12-01 to 2022-01-01 with cumulative\_fy\_sales 800, 1100, 1200, 1350, 1700, 1900, 2100, then 100, 400, 800, 1100, 1400, 1800 and 2100 after the July reset.](/images/transforming-cumulative-sums-into-monthly-values/1-input.jpg)

```sql
-- computes the start of the respective financial year
-- (July 1st -> June 30th), given a date
CREATE TEMP FUNCTION GET_FINANCIAL_YEAR_START(input_date DATE)
RETURNS DATE
AS (
DATE(IF(EXTRACT(MONTH FROM input_date) >= 7,
     EXTRACT(YEAR FROM input_date),
     EXTRACT(YEAR FROM input_date) - 1), 7, 1)
);

SELECT

  month_start_date,

  -- computes the first day of the fiscal year
  GET_FINANCIAL_YEAR_START(month_start_date) AS fiscal_year_start,

  cumulative_fy_sales,


  -- retrieves the previous month's cumulative sales
  LAG(cumulative_fy_sales,1) OVER (PARTITION BY GET_FINANCIAL_YEAR_START(month_start_date)
                                   ORDER BY month_start_date) AS previous_cumulative_sales,

  -- calculates the sales for this particular month
  cumulative_fy_sales - IFNULL(LAG(cumulative_fy_sales,1) OVER (PARTITION BY GET_FINANCIAL_YEAR_START(month_start_date)
                                                                ORDER BY month_start_date),0) AS current_month_sales

FROM input_data
```

![BigQuery results: fiscal\_year\_start 2020-07-01 through 2021-06, then 2021-07-01; current\_month\_sales 800, 300, 100, 150, 350, 200, 200, then 100, 300, 400, 300, 300, 400 and 300, with previous\_cumulative\_sales null at the start of each fiscal year.](/images/transforming-cumulative-sums-into-monthly-values/1-result.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [***notjustsql.com***](https://www.notjustsql.com/)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Joining temporal tables in BigQuery](/practical-bigquery-joining-temporal-tables)
- [Generating a compact temporal table in BigQuery](/generating-a-compact-temporal-table-in-bigquery)
- [Aggregating Multiple SCD-2 Attribute Timelines in BigQuery](/aggregating-multiple-scd-2-attribute-timelines-in-bigquery)
- [Compacting date intervals in BigQuery](/compacting-date-intervals-in-bigquery)
