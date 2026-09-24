---
title: "WITH expressions in BigQuery"
seoTitle: "BigQuery WITH Expressions Explained"
seoDescription: "Learn how WITH expressions in BigQuery can simplify complex SQL queries and reduce boilerplate code by defining scoped variables within expressions"
datePublished: 2025-09-30T05:38:06.112Z
dateUpdated: 2026-03-02T10:51:26.734Z
cover: "/images/with-expressions-in-bigquery/cover.jpg"
coverCredit:
  name: "Raphael Schaller"
  url: "https://unsplash.com/@raphaelphotoch"
series: "practical-sql"
hashnodeCuid: "cmg64mcv4000102jp2j0sb5mg"
---

So I recently discovered the WITH expression in BigQuery SQL.

Not to be confused with the WITH clause, which we use to define common table expressions (CTEs).

👉 What does a WITH expression do?  
It lets you define a series of variables, scoped to a single expression. Each variable can reference previously defined ones (and table columns), and in the end, the whole expression returns a result.

📌 Where could this be useful?  
Think back to the time before QUALIFY was supported. We often had to create an extra CTE just to filter with WHERE rn = 1 or for similar windowed calculations. When QUALIFY came, it saved us a bunch of boilerplate CTEs.  
Well, WITH expressions have the potential to help in the same way — but for non-window calculations.

When working with complex formulas, you can’t reference (within the same SELECT) a column you just defined. The usual workaround is to push it into another CTE — which works, but feels verbose. I still opted to do it since it's important that the code stayed readable and maintainable.  
Now WITH expressions give us a cleaner option and help avoid those 7-operand expressions. I, for one, plan on trying them out ASAP.

```sql
-- WITH clause
WITH input_data AS (
  SELECT 1 AS product_id, 5 AS quantity, 100 AS base_price, 0.15 AS discount_rate, 0.21 AS tax_rate
  UNION ALL
  SELECT 2 AS product_id, 3 AS quantity, 80 AS base_price, 0.12 AS discount_rate, 0.21 AS tax_rate
  UNION ALL
  SELECT 3 AS product_id, 2 AS quantity, 75 AS base_price, 0.10 AS discount_rate, 0.21 AS tax_rate
)



--WITH expression
SELECT

product_id,

WITH(
  discounted_price AS base_price * (1 - discount_rate), -- variable 1
  price_incl_tax AS discounted_price * (1 + tax_rate), -- variable 2
  quantity * price_incl_tax) AS sales_amount           -- result


FROM input_data
```

![BigQuery results: sales\_amount 514.25 for product 1, 255.552 for product 2 and 163.35 for product 3.](/images/with-expressions-in-bigquery/1-result.jpg)

Has anyone here used them already? Any thoughts? Docs [here](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators#with_expression).
