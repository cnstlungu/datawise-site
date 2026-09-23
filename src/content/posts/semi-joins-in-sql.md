---
title: "SEMI-JOINS in SQL"
seoTitle: "SQL Semi-Join with WHERE EXISTS: Filter Without Duplicates"
seoDescription: "A semi-join filters the left table to rows whose keys exist in the right table, without duplicating rows on multiple matches."
datePublished: 2024-06-19T06:00:29.837Z
dateUpdated: 2026-03-02T10:52:03.699Z
cover: "/images/semi-joins-in-sql/cover.jpg"
coverCredit:
  name: "davisuko"
  url: "https://unsplash.com/@davisuko"
series: "practical-sql"
hashnodeCuid: "clxlfchot000209mj8iydd401"
---

Continuing our series about lesser-know types of SQL joins, let's look at the SEMI-JOIN today.

What does it do?

Well, we filter the entries in the left table to only the keys found in the right table, but unlike an INNER JOIN, we:  
\- we only get the columns in the left table  
\- even if there's multiple matching rows in the right table, we're not duplicating rows in the left one.

How are we going to implement it? We're going to use WHERE + EXISTS + a correlated sub-query (notice the WHERE clause in the subquery).

In the example below, we're using a semi-join to see which of the products have been previously ordered.

```sql
WITH products AS (
  SELECT 1 AS product_id, 'Cherries' AS product_name UNION ALL
  SELECT 2 AS product_id, 'Tomatoes' AS product_name UNION ALL
  SELECT 3 AS product_id, 'Squash' AS product_name
),

orders AS (
  SELECT 1001 AS order_id, 1 AS product_id, 3 AS quantity UNION ALL
  SELECT 1001 AS order_id, 2 AS product_id, 4 AS quantity UNION ALL

  SELECT 1002 AS order_id, 1 AS product_id, 4 AS quantity UNION ALL
  SELECT 1002 AS order_id, 2 AS product_id, 1 AS quantity)


SELECT * FROM products p

WHERE EXISTS (

SELECT 1
    FROM orders o
    WHERE p.product_id = o.product_id

)
```

![BigQuery results: two rows, product 1 Cherries and product 2 Tomatoes.](/images/semi-joins-in-sql/1-result.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Self-joins in SQL](/self-joins-in-sql)
- [Anti-joins in SQL](/anti-joins-in-sql)
- [NON-EQUI joins in SQL](/non-equi-joins-in-sql)
- [NATURAL JOIN in SQL](/natural-join-in-sql)
