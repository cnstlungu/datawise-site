---
title: "Comparing ranking functions in BigQuery"
seoTitle: "ROW_NUMBER vs RANK vs DENSE_RANK in BigQuery"
seoDescription: "Breaks down the difference between ROW_NUMBER, RANK, and DENSE_RANK in BigQuery with a clear side-by-side example."
datePublished: 2023-11-15T21:59:31.974Z
dateUpdated: 2026-03-02T10:51:28.994Z
cover: "/images/comparing-ranking-functions-in-bigquery/cover.jpg"
coverCredit:
  name: "Martin Sanchez"
  url: "https://unsplash.com/@martinsanchez"
series: "bigquery-window-functions"
hashnodeCuid: "clp0b1yti00000ajtflzj29k1"
---

One of the most common sightings in SQL code is using ranking functions. It's simple but we must surely get it right. I use `ROW_NUMBER` very often for de-duplication, also used `DENSE_RANK` a couple of times - but I've never used `RANK`. So how are they different?

\- ROW\_NUMBER - sequential row number, regardless of equal values. If no order is provided, the results might be different every time you run it (aka non-deterministic): 1,2,3,4,5

\- DENSE\_RANK - also a sequential row number, but takes into account peer rows (with equal values). next rank is the immediate following: 1,2,2,3 (no gaps)

\- RANK - also a sequential row number, takes into account rows with equal values, but next rank is incremented: 1,2,2,4 (with gaps)

See below for an example of how it all works.

```sql
SELECT 
  store_code, 
  country, 
  sales_usd, 
  ROW_NUMBER() OVER country_sales AS row_no,
  DENSE_RANK() OVER country_sales AS dense_rnk,
  RANK() OVER country_sales       AS rnk

FROM input_data

WINDOW country_sales AS (PARTITION BY country ORDER BY sales_usd DESC)
```

![](/images/comparing-ranking-functions-in-bigquery/1.png)

Thanks for reading!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Beware of ROW_NUMBER without ORDER BY](/beware-of-rownumber-without-order-by)
- [Tidying up WINDOW functions in BigQuery with named windows](/tidying-up-window-functions-in-bigquery-with-named-windows)
- [Using RANGE in Window Functions in BigQuery](/using-range-in-window-functions-in-bigquery)
- [Computing a cumulative sum in BigQuery](/computing-a-cumulative-sum-in-bigquery)
