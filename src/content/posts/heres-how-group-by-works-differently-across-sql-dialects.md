---
title: "Here's how GROUP BY works differently across SQL dialects"
seoTitle: "Can You Use Column Aliases in GROUP BY in BigQuery?"
seoDescription: "Yes, BigQuery allows column aliases in GROUP BY. See how this differs from SQL Server and other dialects, with examples and edge cases."
datePublished: 2024-06-08T16:36:18.591Z
dateUpdated: 2026-04-28T08:33:43.573Z
cover: "/images/heres-how-group-by-works-differently-across-sql-dialects/cover.jpg"
coverCredit:
  name: "Nicolas Brulois"
  url: "https://unsplash.com/@nicod5300"
series: "practical-sql"
hashnodeCuid: "clx6c7s4f00000ala50hmfh0y"
---

It turns out I've been writing longer queries than I should.😁 Here's an interesting gotcha about GROUP BY between SQL dialects that I've just learned.

So I've started with SQL Server back in the day, where according to docs:

> a GROUP BY column expression cannot be "a column alias that is defined in the SELECT list".

Naturally, if I processed a column during aggregation, I would have the same expression in GROUP BY (minus the alias of course).

```sql
SELECT 
CASE WHEN country in ('US','USA','US of A') THEN 'USA' ELSE country END AS country, SUM (sales_amount) AS total_sales
FROM sales
GROUP BY CASE WHEN country in ('US','USA','US of A') THEN 'USA' ELSE country END
```

Where it matters: if the alias is the same as the original column name, you would be grouping not by the 'transformed' column, but by the original one, yielding things you might not expect 😁 A newly-assigned alias cannot be grouped by for the same reason.

Well, things are different with BigQuery for instance. Docs mention:

> GROUP BY clauses may also refer to aliases. If a query contains aliases in the SELECT clause, those aliases override names in the corresponding FROM clause.

So in BQ, you can reference the alias you've assigned in SELECT (overriding the one from FROM if matching) and you can reference a newly aliased column. No need to copy the unwieldy `CASE WHEN ...` to the `GROUP BY` in this case.

```sql
SELECT 
 country AS cntry,
 SUM(amount) AS total_amount
FROM input_data
GROUP BY cntry
```

Lesson learned (for now).

![](/images/heres-how-group-by-works-differently-across-sql-dialects/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
