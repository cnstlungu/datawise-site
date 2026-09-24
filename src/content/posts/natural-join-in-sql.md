---
title: "NATURAL JOIN in SQL"
seoTitle: "SQL NATURAL JOIN Explained: Auto-Join on Matching Columns"
seoDescription: "NATURAL JOIN automatically joins tables on columns sharing the same name and datatype, with no explicit condition needed."
datePublished: 2024-06-20T06:00:25.812Z
dateUpdated: 2026-03-02T10:52:31.861Z
cover: "/images/natural-join-in-sql/cover.jpg"
coverCredit:
  name: "micheile henderson"
  url: "https://unsplash.com/@micheile"
series: "practical-sql"
hashnodeCuid: "clxmus99000060ajs1dfi2y2z"
---

Another lesser known JOIN - the natural join. But maybe the NATURAL JOIN is not as obscure after all, since it has its own keyword, at least in a couple of SQL dialects - see PostgreSQL portrayed below (sorry, it's not supported in BigQuery, but it does recognize it).

So what's special about it? Well, it joins the tables based on columns that have the same name (and datatype) in the two tables. That is, we don't need to specify any join conditions.

Watch out because if there are no columns with the same name and datatype, it defaults to a Cartesian product is produced (which is what CROSS JOIN does).

```sql
WITH stores AS (
SELECT 1 AS store_id, 'Flagship store - NY' AS store_name UNION ALL
SELECT 2 AS store_id, 'Main St. - LA' AS store_name UNION ALL
SELECT 3 AS store_id, 'Michigan Ave. - Chicago' AS store_name ),

employees AS (
SELECT 1 AS employee_id, 1 AS store_id UNION ALL
SELECT 2 AS employee_id, 2 AS store_id UNION ALL
SELECT 3 AS employee_id, 3 AS store_id
)

SELECT employee_id, store_id, store_name
FROM stores
NATURAL JOIN employees
```

![Output: employee 1 with store 1 Flagship store - NY, employee 2 with store 2 Main St. - LA, and employee 3 with store 3 Michigan Ave. - Chicago.](/images/natural-join-in-sql/1-result.jpg)

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Self-joins in SQL](/self-joins-in-sql)
- [Anti-joins in SQL](/anti-joins-in-sql)
- [SEMI-JOINS in SQL](/semi-joins-in-sql)
- [NON-EQUI joins in SQL](/non-equi-joins-in-sql)
