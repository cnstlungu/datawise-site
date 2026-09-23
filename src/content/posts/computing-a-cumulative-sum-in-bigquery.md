---
title: "Computing a cumulative sum in BigQuery"
seoTitle: "Cumulative SUM in BigQuery Using Window Functions"
seoDescription: "Learn how to compute a running cumulative sum in BigQuery using SUM with ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW in a window function."
datePublished: 2024-01-11T10:24:33.312Z
dateUpdated: 2026-03-02T10:50:45.251Z
cover: "/images/computing-a-cumulative-sum-in-bigquery/cover.jpg"
coverCredit:
  name: "Antoine Dautry"
  url: "https://unsplash.com/@antoine1003"
series: "bigquery-window-functions"
hashnodeCuid: "clr92brxc000308jx0t1pbdr3"
---

How do you compute a cumulative SUM in BigQuery?

Today we're going to look at how to compute a cumulative sum in BigQuery, a scenario that pops up now and then and is quite easy to solve using window functions.

In the below example, we have a dataset representing customer orders. We'd like to find out the cumulative sum of each individual customer.

For this we'll need :  
\- SUM function combined with a WINDOW function call  
\- PARTITION BY customer ID to perform calculation at customer level  
\- ORDER BY order\_date (ascending by default) so that the values are summed up chronologically  
\- a window frame clause: ROWS BETWEEN UNBOUNDED (starting with the first entry) AND CURRENT ROW (until and including this row)

See below for an illustration of how it all works. Happy querying!

![BigQuery SQL cumulative sum on an orders table: SUM(order\_total) OVER (PARTITION BY customer\_id ORDER BY order\_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative\_sum; the highlighted result runs 100, 175, 265 for Customer-1 and 80, 200, 250 for Customer-2.](/images/computing-a-cumulative-sum-in-bigquery/1.jpg)

Bonus point: You can also use a [named window declaration](/tidying-up-window-functions-in-bigquery-with-named-windows) for cleaner code.

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Beware of ROW_NUMBER without ORDER BY](/beware-of-rownumber-without-order-by)
- [Tidying up WINDOW functions in BigQuery with named windows](/tidying-up-window-functions-in-bigquery-with-named-windows)
- [Using RANGE in Window Functions in BigQuery](/using-range-in-window-functions-in-bigquery)
- [Rolling period calculation in BigQuery](/rolling-period-calculation-in-bigquery)
