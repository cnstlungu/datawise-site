---
title: "Expressing multiple repeated joins as a correlated subquery"
seoTitle: "Optimize Joins with Correlated Subqueries"
seoDescription: "Discover how to use correlated subqueries in SQL to optimize multiple joins and improve query efficiency"
datePublished: 2025-02-23T15:13:22.421Z
dateUpdated: 2026-03-02T10:53:02.999Z
cover: "/images/expressing-multiple-repeated-joins-as-a-correlated-subquery/cover.jpg"
coverCredit:
  name: "X Y"
  url: "https://unsplash.com/@sandworm"
series: "practical-sql"
hashnodeCuid: "cm7hrqlth000009jza1ni9im9"
---

In [yesterday’s post](/revisiting-group-by-rollup-with-a-more-realistic-example), we looked at retrieving information from a table by joining it multiple times—each with different join criteria. This raises a natural question: are there better alternatives to this approach?

I initially experimented with a CASE WHEN in the join condition, hoping it would short-circuit, picking the first matching condition—just like in a SELECT clause. However, in a join, it evaluates all scenarios, so that didn’t work as expected.

But remember correlated subqueries? A correlated subquery runs once per row and can be embedded in the SELECT or WHERE clause. Essentially, it lets you create a dynamic query within a single data cell, based on the current row’s context. Check out [this quick intro](/using-correlated-subqueries-in-bigquery).

To avoid multiple joins, you can use a correlated subquery to fetch all possible combinations (previously handled by join conditions) and apply the same logic with ORDER BY and LIMIT to return exactly one value.

A word of caution: correlated subqueries execute once per row, which can impact performance, especially with large datasets. However, they’re a valuable tool in your SQL tool belt, particularly when other elegant solutions aren’t available.

![BigQuery SQL rewrite: four LEFT JOINs to calculated\_averages (per product, subcategory, category and all products) merged with COALESCE become one correlated subquery with OR conditions, ORDER BY CASE WHEN priorities 1 to 4 and LIMIT 1, returning average\_ordered\_quantity.](/images/expressing-multiple-repeated-joins-as-a-correlated-subquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [***notjustsql.com***](https://www.notjustsql.com/)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Self-joins in SQL](/self-joins-in-sql)
- [Anti-joins in SQL](/anti-joins-in-sql)
- [SEMI-JOINS in SQL](/semi-joins-in-sql)
- [NON-EQUI joins in SQL](/non-equi-joins-in-sql)
