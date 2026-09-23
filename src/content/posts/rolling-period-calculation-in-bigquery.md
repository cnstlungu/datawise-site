---
title: "Rolling period calculation in BigQuery"
seoTitle: "Rolling Period SUM in BigQuery Using RANGE Window Frame"
seoDescription: "Compute a rolling period sum in BigQuery using RANGE BETWEEN with UNIX_DATE. Correctly handles duplicate dates and gaps where ROWS would produce wrong results."
datePublished: 2024-01-17T14:23:23.847Z
dateUpdated: 2026-03-02T10:22:36.763Z
cover: "/images/rolling-period-calculation-in-bigquery/cover.jpg"
coverCredit:
  name: "Markus Spiske"
  url: "https://unsplash.com/@markusspiske"
series: "bigquery-window-functions"
hashnodeCuid: "clrhvi1fr000309l2hsg9apg5"
---

How to compute a rolling period calculation in BigQuery?

In [one of my previous posts](/computing-a-cumulative-sum-in-bigquery), I've showcased using RANGE inside window function declarations in the context of computing a cumulative sum.

Today we're going to look at another example often found in the wild - computing a rolling period calculation. Let's look at an example.

We have customer order information and would like to compute a per customer rolling sum of the previous 60 days' worth of purchases.

How this would look in terms of SQL?

SUM(order\_total) OVER (PARTITION BY customer\_id ORDER BY UNIX\_DATE(order\_date) RANGE BETWEEN 59 PRECEDING AND CURRENT ROW) AS rolling\_60\_days\_sum

Let's explain it:

We will start by taking a SUM of order\_total with a window declaration  
and partitioning by customer\_id.

Next is ordering by our order\_date, but since RANGE only accepts a single integer field, we'll need to transform it using UNIX\_DATE. This will transform '2021-01-01' into 18628.

We can now use RANGE, setting the range between the 59 previous days and the current row. This way, if we have any gaps or duplicates in our order data (which is very likely), the calculation would still work, as opposed to the approach of using ROWS.

See below an illustration of how it all works.

```sql
SELECT 

customer_id, 
order_id, 
order_total, 
order_date, 
SUM(order_total) OVER (PARTITION BY customer_id
                       ORDER BY UNIX_DATE(order_date)
                       RANGE BETWEEN 59 PRECEDING AND CURRENT ROW) 
                 AS rolling_60_days_sum

FROM input_data


+-------------+----------+-------------+------------+---------------------+
| customer_id | order_id | order_total | order_date | rolling_60_days_sum |
+-------------+----------+-------------+------------+---------------------+
| Customer-1  | 10001    | 100         | 2021-01-01 | 100                 |
| Customer-1  | 10003    | 75          | 2021-02-15 | 175                 |
| Customer-1  | 10005    | 90          | 2021-03-12 | 165                 |
| Customer-1  | 10001    | 100         | 2021-04-21 | 190                 |
| Customer-1  | 10003    | 75          | 2021-05-12 | 175                 |
| Customer-1  | 10005    | 90          | 2021-06-23 | 165                 |
| Customer-2  | 10002    | 80          | 2021-01-01 | 80                  |
| Customer-2  | 10004    | 120         | 2021-02-04 | 200                 |
| Customer-2  | 10006    | 50          | 2021-03-05 | 170                 |
| Customer-2  | 10002    | 80          | 2021-04-11 | 130                 |
| Customer-2  | 10004    | 120         | 2021-05-12 | 200                 |
| Customer-2  | 10006    | 50          | 2021-06-30 | 170                 |
+-------------+----------+-------------+------------+---------------------+
```

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Beware of ROW_NUMBER without ORDER BY](/beware-of-rownumber-without-order-by)
- [Tidying up WINDOW functions in BigQuery with named windows](/tidying-up-window-functions-in-bigquery-with-named-windows)
- [Using RANGE in Window Functions in BigQuery](/using-range-in-window-functions-in-bigquery)
- [Computing a cumulative sum in BigQuery](/computing-a-cumulative-sum-in-bigquery)
