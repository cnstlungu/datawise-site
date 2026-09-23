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

![BigQuery SQL comparing daily total\_sales per department in System A and System B with FULL OUTER JOIN USING (department, sales\_date) and ORDER BY ABS(IFNULL(sales\_a, 0) - IFNULL(sales\_b, 0)) DESC; shoes on 2021-01-01, missing in A, tops the list with a difference of 3000.](/images/a-simple-data-validation-scenario-using-full-outer-join-order-by/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Self-joins in SQL](/self-joins-in-sql)
- [Anti-joins in SQL](/anti-joins-in-sql)
- [SEMI-JOINS in SQL](/semi-joins-in-sql)
- [NON-EQUI joins in SQL](/non-equi-joins-in-sql)
