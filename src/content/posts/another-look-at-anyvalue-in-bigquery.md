---
title: "Another look at ANY_VALUE in BigQuery"
seoTitle: "BigQuery ANY_VALUE with HAVING MAX: Pick a Row Without a Subquery"
seoDescription: "Use ANY_VALUE with HAVING MAX or MIN in BigQuery to select a row by a criterion without writing a subquery. Includes practical examples and caveats."
datePublished: 2024-10-20T06:18:23.196Z
dateUpdated: 2026-04-28T08:37:10.590Z
cover: "/images/another-look-at-anyvalue-in-bigquery/cover.jpg"
coverCredit:
  name: "Aakash Dhage"
  url: "https://unsplash.com/@aakashdhage"
series: "practical-sql"
hashnodeCuid: "cm2h759wc000109l56engd67h"
---

A reminder that ANY\_VALUE is a pretty interesting aggregation function in BigQuery SQL.

It gives you a chosen row from a group. Chosen doesn't mean random, but non-deterministic.

Together with HAVING MAX | MIN you can actually control what rows get picked.

While ANY\_VALUE works both with GROUP BY and as a window function OVER (PARTITION BY...), the window variety does not yet support HAVING MIN MAX.

Otherwise, when do I use it? A couple of cases, and it's not only for the thrill of getting an item by chance from the group:  
\- line events also contain header info, so say we need to extract order header data from orderline data  
\- aggregation after pseudo-pivoting with CASE WHEN value = x, same as we used to do with MIN or MAX before  
\- other aggregations of string values based on a rule

```sql
WITH input_data AS
(
  SELECT 1 AS order_id, 'Banana' AS product_id, 7.00 AS price, '2024-01-01' AS best_before_date
  UNION ALL
  SELECT 1 AS order_id, 'Mango' AS product_id, 8.00 AS price, '2024-01-10' AS best_before_date
  UNION ALL
  SELECT 2 AS order_id, 'Pears' AS product_id, 10.00 AS price, '2024-01-05' AS best_before_date
),

processing AS (

  SELECT order_id, product_id, price, product_id = 'Banana' AS is_banana, best_before_date FROM input_data
)

SELECT
  order_id,
  ANY_VALUE(product_id HAVING MAX price ) AS most_expensive_product,
  ANY_VALUE(product_id HAVING MIN is_banana) AS any_product_except_banana,
  ANY_VALUE(product_id HAVING MIN best_before_date) AS first_expiring_product
FROM processing
GROUP BY order_id
```

![BigQuery results: order 1 gives most\_expensive\_product Mango, any\_product\_except\_banana Mango and first\_expiring\_product Banana; order 2 gives Pears in all three columns.](/images/another-look-at-anyvalue-in-bigquery/1-result.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
