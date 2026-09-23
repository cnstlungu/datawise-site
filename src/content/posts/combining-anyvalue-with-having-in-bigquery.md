---
title: "Combining ANY_VALUE with HAVING in BigQuery"
seoTitle: "BigQuery ANY_VALUE with HAVING to Filter Single-Item Orders"
seoDescription: "Combine ANY_VALUE with HAVING in BigQuery to filter aggregated groups based on the single value in a group. A practical pattern for finding orders with..."
datePublished: 2024-05-29T21:47:37.891Z
dateUpdated: 2026-03-02T10:52:18.269Z
cover: "/images/combining-anyvalue-with-having-in-bigquery/cover.jpg"
coverCredit:
  name: "Volodymyr Hryshchenko"
  url: "https://unsplash.com/@lunarts"
series: "practical-sql"
hashnodeCuid: "clwscxmhv000109lj96xn2kps"
---

Here's another rather rare instance where I've used ANY\_VALUE in  
BigQuery. It's basically an aggregation function like SUM or COUNT except it retrieves a arbitrary value from the grouping.

I've posted [about ANY\_VALUE before](/using-anyvalue-in-bigquery), but today's query was a bit different.

In the example below, my goal is to find orders that contain a single value, belonging to a particular list of values.

In other words, which order consisted of exactly one item, with that being grapes or oranges?

We aggregate using COUNT to count the number of order lines in an order and ANY\_VALUE to pick a random value from the list of order lines.

We then filter the aggregate results using HAVING, keeping only order that have exactly one order line and that order line being a grape or orange.

With ANY\_VALUE of a single value being always that value, we can filter the result sets to what we need. It's entirely true that the same can be said of MIN or MAX for instance, but I think it would have been a little less obvious of why it was chosen like that.

As almost always with SQL, there are of course plenty of other ways to achieve the same result.

```sql
WITH input_data AS (

  SELECT 1 AS order_id, 'apples' AS order_line
  UNION ALL
  SELECT 1 AS order_id, 'pears' AS order_line
  UNION ALL
  SELECT 1 AS order_id, 'grapes' AS order_line
  UNION ALL
  SELECT 2 AS order_id, 'grapes' AS order_line
  UNION ALL
  SELECT 3 AS order_id, 'oranges' AS order_line
  UNION ALL
  SELECT 4 AS order_id, 'kiwi' AS order_line
)

SELECT
  order_id,
  COUNT(order_line) AS count_order_lines,
  ANY_VALUE(order_line) AS product_name

FROM input_data

GROUP BY order_id

HAVING COUNT(order_line) = 1 AND
       ANY_VALUE(order_line) IN ('grapes', 'oranges')
```

![BigQuery results: order\_id 2 with count\_order\_lines 1 and product\_name grapes, and order\_id 3 with count\_order\_lines 1 and product\_name oranges.](/images/combining-anyvalue-with-having-in-bigquery/1-result.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
