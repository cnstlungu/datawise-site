---
title: "The first thing I do when analyzing a SQL table"
seoTitle: "SQL Data Quality Check: First Steps When Analyzing a Table"
seoDescription: "Run quick COUNT-based checks on NULL values and key columns to assess data quality before building a pipeline. A fast, repeatable SQL pattern for..."
datePublished: 2024-06-05T21:12:04.489Z
dateUpdated: 2026-04-05T20:11:13.451Z
cover: "/images/the-first-thing-i-do-when-analyzing-a-sql-table/cover.jpg"
coverCredit:
  name: "Markus Winkler"
  url: "https://unsplash.com/@markuswinkler"
series: "practical-sql"
hashnodeCuid: "clx2bqv0p000409l53q4he6fr"
---

Here's one of the first things I do with SQL when I want to quickly assess the data quality in a table.

I would run a series of quick COUNTs, testing key attributes of the data, such as key columns being NULL, which can display the distribution of problematic data so it can be processed accordingly.

A good way to ensure data quality in a data pipeline is to have a good look at it in the first place.

![Input data: input\_data with order\_id, is\_paid and product\_id, six rows; order 1 has a NULL product\_id and order 6 a NULL is\_paid.](/images/the-first-thing-i-do-when-analyzing-a-sql-table/1-input.jpg)

```sql
SELECT
  is_paid IS NULL AS is_paid_null,
  product_id IS NULL AS product_id_null,
  COUNT(1) AS occurences
FROM input_data
GROUP BY ALL
```

![Query results: is\_paid\_null false with product\_id\_null true occurs 1 time, both false 4 times, and is\_paid\_null true with product\_id\_null false 1 time.](/images/the-first-thing-i-do-when-analyzing-a-sql-table/1-result.jpg)

*Found it useful? Subscribe to my Analytics newsletter at*[*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Table grain quick validation with SQL](/table-grain-quick-validation-with-sql)
