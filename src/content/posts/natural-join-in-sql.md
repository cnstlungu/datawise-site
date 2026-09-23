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

![SQL with stores (store\_id, store\_name) and employees (employee\_id, store\_id) CTEs joined via NATURAL JOIN with no ON clause, matching on the shared store\_id column; the result pairs employees 1, 2, 3 with Flagship store - NY, Main St. - LA and Michigan Ave. - Chicago.](/images/natural-join-in-sql/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Self-joins in SQL](/self-joins-in-sql)
- [Anti-joins in SQL](/anti-joins-in-sql)
- [SEMI-JOINS in SQL](/semi-joins-in-sql)
- [NON-EQUI joins in SQL](/non-equi-joins-in-sql)
