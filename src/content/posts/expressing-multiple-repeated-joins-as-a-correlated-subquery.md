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

```sql
SELECT
  nd.product_id,
  nd.subcategory,
  nd.category,
  COALESCE(cap.average_qty,
           cas.average_qty,
           cac.average_qty,
           ct.average_qty) AS average_qty

FROM new_data nd
LEFT JOIN calculated_averages cap ON nd.product_id = cap.product_id --per product
LEFT JOIN calculated_averages cas ON nd.subcategory = cas.subcategory AND
                                     cas.product_id IS NULL --per subcategory
LEFT JOIN calculated_averages cac ON nd.category = cac.category AND
                                     cac.subcategory IS NULL --per category
LEFT JOIN calculated_averages ct ON ct.category IS NULL --for all products
```

```sql
SELECT
  nd.product_id,
  (SELECT ca.average_ordered_quantity
   FROM calculated_averages ca
   WHERE
      (nd.product_id = ca.product_id)
      OR (nd.subcategory = ca.subcategory AND ca.product_id IS NULL)
      OR (nd.category = ca.category AND ca.subcategory IS NULL)
      OR (ca.category IS NULL)
   ORDER BY
      CASE
        WHEN nd.product_id = ca.product_id THEN 1
        WHEN nd.subcategory = ca.subcategory AND ca.product_id IS NULL THEN 2
        WHEN nd.category = ca.category AND ca.subcategory IS NULL THEN 3
        ELSE 4
      END
   LIMIT 1) AS average_ordered_quantity

FROM new_data nd
```

*Found it useful? Subscribe to my Analytics newsletter at* [***notjustsql.com***](https://www.notjustsql.com/)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Self-joins in SQL](/self-joins-in-sql)
- [Anti-joins in SQL](/anti-joins-in-sql)
- [SEMI-JOINS in SQL](/semi-joins-in-sql)
- [NON-EQUI joins in SQL](/non-equi-joins-in-sql)
