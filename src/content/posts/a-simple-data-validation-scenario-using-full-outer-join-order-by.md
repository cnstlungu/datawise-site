---
title: "A simple data validation scenario using FULL OUTER JOIN & ORDER BY"
seoTitle: "Data Validation in BigQuery: FULL OUTER JOIN + ORDER BY ABS"
seoDescription: "Use FULL OUTER JOIN combined with ORDER BY ABS to surface the largest discrepancies between two source systems in BigQuery."
datePublished: 2024-05-02T21:42:55.493Z
dateUpdated: 2026-03-02T10:52:16.111Z
cover: "/images/a-simple-data-validation-scenario-using-full-outer-join-order-by/cover.jpg"
coverCredit:
  name: "Tolga Ulkan"
  url: "https://unsplash.com/@tolga__"
series: "practical-sql"
hashnodeCuid: "clvprvklh000208k30ckvhkxs"
---

Data Engineers do a lot of Data Analysis work, too.

For example: we need to understand why is there a difference between two approaches or data in two source systems.

[I've previously shown how a FULL OUTER JOIN](/comparing-tables-with-full-outer-join) in SQL with simple validation and how you [can ORDER BY an expression](/order-by-expressions-in-sql).

Let's look at a scenario where we can combine the two.

So we've got two source systems A and B, which *in theory* should provide the same sales figures, but they don't.

Understanding the difference between the two sources means identifying individual cases where the values are different, starting with the biggest discrepancies.

In the example below, we're going to order the results by the absolute value (ABS) of the difference between the figures in two systems, considering a missing value as 0.

This way, we can start our investigation from the biggest differences, regardless of which system shows 'bigger' values and also take into account missing values between the two.

![Input data: System A and System B tables with department, sales\_date and total\_sales for clothing and shoes from 2021-01-01 to 2021-01-03; they differ for clothing on 2021-01-01 (1500 vs 1400) and shoes on 2021-01-02 (1500 vs 1550), System A has no value for shoes on 2021-01-01 (B: 3000) and System B none for shoes on 2021-01-03 (A: 1400).](/images/a-simple-data-validation-scenario-using-full-outer-join-order-by/1-input.jpg)

```sql
SELECT
  department,
  sales_date,
  a.total_sales AS sales_a,
  b.total_sales AS sales_b,
  ABS(IFNULL(a.total_sales, 0) - IFNULL(b.total_sales, 0)) AS difference

FROM sales_system_a a
FULL OUTER JOIN sales_system_b b USING (department, sales_date)

ORDER BY ABS(IFNULL(sales_a, 0) - IFNULL(sales_b, 0)) DESC
```

![BigQuery results, biggest difference first: shoes 2021-01-01 (sales\_a null, sales\_b 3000, difference 3000), shoes 2021-01-03 (1400, null, 1400), clothing 2021-01-01 (1500, 1400, 100), shoes 2021-01-02 (1500, 1550, 50), then clothing 2021-01-02 and 2021-01-03 with difference 0.](/images/a-simple-data-validation-scenario-using-full-outer-join-order-by/1-result.jpg)

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Self-joins in SQL](/self-joins-in-sql)
- [Anti-joins in SQL](/anti-joins-in-sql)
- [SEMI-JOINS in SQL](/semi-joins-in-sql)
- [NON-EQUI joins in SQL](/non-equi-joins-in-sql)
