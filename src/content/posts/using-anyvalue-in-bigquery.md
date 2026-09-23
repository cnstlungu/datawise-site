---
title: "Using ANY_VALUE()  in BigQUERY"
seoTitle: "ANY_VALUE() in BigQuery: Non-Deterministic Aggregation"
seoDescription: "Learn how to use ANY_VALUE in BigQuery, including with HAVING MAX and HAVING MIN to find top or bottom values within a group."
datePublished: 2023-12-11T23:48:53.027Z
dateUpdated: 2026-03-02T10:52:06.109Z
cover: "/images/using-anyvalue-in-bigquery/cover.jpg"
coverCredit:
  name: "Edge2Edge Media"
  url: "https://unsplash.com/@edge2edgemedia"
series: "practical-sql"
hashnodeCuid: "clq1keqoz000008jx1mikd9h4"
---

Have you ever used ANY\_VALUE in BigQuery?

It's an aggregate function like SUM or AVG, but it returns a non-deterministic (not random) row from the group. I've been using it in scenarios where there's one value anyway, such as when PIVOTing.

![](/images/using-anyvalue-in-bigquery/1.png)

```sql
WITH input_data AS (
  SELECT 'Europe' AS Region, 'Q1' AS quarter, 250000 AS sales
  UNION ALL
  SELECT 'Europe' AS Region, 'Q2' AS quarter, 225000 AS sales
  UNION ALL
  SELECT 'Europe' AS Region, 'Q3' AS quarter, 275000 AS sales
  UNION ALL
  SELECT 'Europe' AS Region, 'Q4' AS quarter, 290000 AS sales
  UNION ALL
  SELECT 'MEA' AS Region, 'Q1' AS quarter, 190000 AS sales
  UNION ALL
  SELECT 'MEA' AS Region, 'Q2' AS quarter, 210000 AS sales
  UNION ALL
  SELECT 'MEA' AS Region, 'Q3' AS quarter, 300000 AS sales
  UNION ALL
  SELECT 'MEA' AS Region, 'Q4' AS quarter, 220000 AS sales
)

SELECT * FROM input_data

PIVOT(ANY_VALUE(sales) as sales FOR quarter IN ('Q1', 'Q2', 'Q3', 'Q4'));
```

![](/images/using-anyvalue-in-bigquery/2.png)

Upon documenting myself for this post, I found an interesting thing - it supports the HAVING clause, allowing us to restrict the rows this function is aggregating, either by a MIN or MAX of a given expression.

Let's look at how it works. Say we have the following data:

![](/images/using-anyvalue-in-bigquery/3.png)

We're going to compute the product that has sold the highest by value and the product that has sold the least by quantity in each of the countries.

```sql
WITH input_data AS (
  SELECT 'Germany' AS country, 'productA' AS product_id, 200 AS quantity, 5.00 AS price
  UNION ALL
    SELECT 'Germany' AS country, 'productB' AS product_id, 75 AS quantity, 100.00 AS price
  UNION ALL
    SELECT 'Germany' AS country, 'productC' AS product_id, 100 AS quantity, 120.00 AS price
  UNION ALL
    SELECT 'Spain' AS country, 'productA' AS product_id, 300 AS quantity, 5.00 AS price
  UNION ALL
    SELECT 'Spain' AS country, 'productD' AS product_id, 250 AS quantity, 20.00 AS price
  UNION ALL
    SELECT 'Spain' AS country, 'productE' AS product_id, 100 AS quantity, 15.00 AS price
)

SELECT 
    country, 
    ANY_VALUE(product_id HAVING MAX quantity*price) AS highest_selling_by_value,
    ANY_VALUE(product_id HAVING MIN quantity) AS lowest_selling_by_quantity,
FROM input_data
GROUP BY country
```

Here's what the results would look like:

![](/images/using-anyvalue-in-bigquery/4.png)

Thanks for reading!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
