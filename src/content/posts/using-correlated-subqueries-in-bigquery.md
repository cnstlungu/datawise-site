---
title: "Using Correlated Subqueries in BigQuery"
seoTitle: "BigQuery 'Correlated Subqueries Not Supported' - How to Fix"
seoDescription: "Fix BigQuery's 'correlated subqueries that reference other tables are not supported' error by rewriting them as joins, window functions or LEFT JOIN UNNEST."
datePublished: 2023-11-06T13:25:35.390Z
dateUpdated: 2026-04-28T08:37:13.609Z
cover: "/images/using-correlated-subqueries-in-bigquery/cover.jpg"
coverCredit:
  name: "James Wainscoat"
  url: "https://unsplash.com/@tumbao1949"
series: "practical-sql"
hashnodeCuid: "clomxqd5q000609k1b0za12gd"
---

There are several interesting concepts in BigQuery once you get past the basics.

One such concept is a correlated subquery. In this short walkthrough, we're going to look at what they are and where are they used, as well as things to pay attention to.

## What are subqueries?

When working with SQL, you might have encountered a construct like that:

```sql
SELECT store_id, total_sales

FROM (

SELECT store_id, SUM(sales_amount) AS total_sales

FROM sales

WHERE store_country = 'US'

GROUP BY store_id

) us_sales
```

In the above query, the outermost `FROM` clause does not read from a table, but rather from the results of another query - which is called a `subquery`.

In practice, while such an approach is possible, we would prefer to use a common table expression (CTE). This would make the query more readable (especially with a more complex sub-query) and allows us to reuse the logic in the same context, leading to a more modularized code.

```sql
WITH us_sales AS (

SELECT store_id, SUM(sales_amount) AS total_sales

FROM sales

WHERE store_country = 'US'

GROUP BY store_id

)

SELECT 
    store_id, 
    total_sales
FROM us_sales
```

## What makes a subquery correlated?

There are several scenarios for correlated subqueries, but what they have in common is the fact that it's a subquery typically executed once per row. The query optimizer can, in theory, optimize some aspects, but it remains problematic in terms of performance.

### Scalar correlated subquery

Here's a **scalar correlated subquery** i.e. one that should produce one single scalar (value) since it's used in the SELECT clause.

```sql
SELECT CustomerId, Salary,
(SELECT AVG(Salary) 
 FROM `learning.Customers` ) as AverageSalary 
FROM `learning.Customers`
```

This is the same that we could achieve with a WINDOW function.

```sql
SELECT CustomerId, Salary,
AVG(Salary) OVER() as AverageSalary 
FROM `learning.Customers`
```

Both produce the same result:

![BigQuery result grid with columns CustomerId, Salary and AverageSalary: four customers with salaries 75000, 88000, 78000 and 150000, each row showing the same AverageSalary of 97750.0 computed across all customers.](/images/using-correlated-subqueries-in-bigquery/1.png)

### Filter using a correlated subquery

Another example would be using a correlated subquery to filter out the result set.

In the example below, we use a correlated subquery to keep only the orders that are above the particular customer's average order value.

```sql
WITH orders AS (
  SELECT 1 as customer_id, 1001 AS order_id, 50 AS order_total
  UNION ALL 
  SELECT 1 as customer_id, 1002 AS order_id, 75 AS order_total
  UNION ALL
  SELECT 1 as customer_id, 1003 AS order_id, 150 as order_total
)

SELECT customer_id, order_id, order_total
FROM orders o
WHERE o.order_total > (
  SELECT AVG(order_total)
  FROM orders oavg
  WHERE o.customer_id = oavg.customer_id)
```

Yet again, this could be achieved differently, using AVG window function + QUALIFY

```sql

WITH orders AS (
  SELECT 1 as customer_id, 1001 AS order_id, 50 AS order_total
  UNION ALL 
  SELECT 1 as customer_id, 1002 AS order_id, 75 AS order_total
  UNION ALL
  SELECT 1 as customer_id, 1003 AS order_id, 150 as order_total
)

SELECT customer_id, order_id, order_total
FROM orders o
QUALIFY order_total > AVG(order_total) OVER(PARTITION BY customer_id)
```

![BigQuery result grid with a single row, customer\_id 1, order\_id 1003 and order\_total 150: the only order above that customer's average order value, as kept by the filtering query.](/images/using-correlated-subqueries-in-bigquery/2.png)

## Things to pay attention to

Since a correlated subquery is typically executed once per every row, they are typically resource-intensive and slower, so should be used with great caution and only when no other more suitable alternative exists.

Let's compare the two following approaches. They are both looking to create a binary flag to see whether an offer was valid when an order for a particular product was placed.

They work with the same input data and produce the same result below.

![BigQuery result grid with columns product\_id, order\_date and has\_had\_offer (header cut off): product 1 ordered on 2021-01-01 is true, product 1 on 2021-03-01 is false and product 2 on 2022-01-01 is false.](/images/using-correlated-subqueries-in-bigquery/3.png)

The first approach uses a correlated subquery to unnest the `offer_validity` on the fly.

```sql
WITH orders AS 

(
  SELECT 1 AS product_id, '2021-01-01' AS order_date
  UNION ALL
  SELECT 1 AS product_id, '2021-03-01' AS order_date
  UNION ALL
  SELECT 2 AS product_id, '2022-01-01' AS order_date
),

offers AS (

SELECT 

1 AS product_id, 
[ STRUCT('2021-01-01' as offer_start, '2021-01-10' AS offer_end) ,
  STRUCT('2022-02-01' as offer_start, '2022-02-10' AS offer_end)   
] AS offer_validity

)

SELECT product_id, order_date,
EXISTS(SELECT 1 FROM UNNEST(offer_validity) AS offer WHERE order_date BETWEEN offer.offer_start and offer.offer_end) AS had_offer
FROM orders
LEFT JOIN offers USING (product_id)
```

The second approach UNNESTS the offer\_validity in the result

```sql
WITH orders AS 

(
  SELECT 1 AS product_id, '2021-01-01' AS order_date
  UNION ALL
  SELECT 1 AS product_id, '2021-03-01' AS order_date
  UNION ALL
  SELECT 2 AS product_id, '2022-01-01' AS order_date
),

offers AS (

SELECT 

1 AS product_id, 
[ STRUCT('2021-01-01' as offer_start, '2021-01-10' AS offer_end) ,
  STRUCT('2022-02-01' as offer_start, '2022-02-10' AS offer_end)   
] AS offer_validity

)

SELECT product_id, order_date, IFNULL(LOGICAL_OR(order_date BETWEEN offer_start AND offer_end),FALSE) AS has_had_offer

FROM orders

LEFT JOIN offers USING (product_id)

LEFT JOIN UNNEST(offer_validity) AS offer

GROUP BY product_id, order_date
```

Here's how their performance compares:

Correlated Subquery:

![BigQuery Execution Details panel for the correlated subquery version: elapsed time 296 ms, slot time consumed 219 ms, bytes shuffled 231 B and bytes spilled to disk 0 B.](/images/using-correlated-subqueries-in-bigquery/4.png)

Without correlated subquery.

![BigQuery Execution Details panel for the version without a correlated subquery: elapsed time 273 ms, slot time consumed 210 ms, bytes shuffled 231 B and bytes spilled to disk 0 B, nearly identical at this small scale.](/images/using-correlated-subqueries-in-bigquery/5.png)

While the results with this scale might look similar, the benchmark when working with a significant amount of data might be very different, hence the need to compare multiple approaches and their performance.

It's also worth pointing out that using correlated subqueries, especially complex ones, makes the query less readable and harder to understand for other team members.

## Conclusion

In conclusion, keep correlated subqueries as part of your toolbox but use them sparingly, based on the situation and compare them with other approaches to pick the best way to go forward.
