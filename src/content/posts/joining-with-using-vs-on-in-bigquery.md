---
title: "Joining with USING vs ON in BigQuery"
seoTitle: "BigQuery SQL: JOIN ON vs USING Clause Differences"
seoDescription: "Understand the difference between JOIN ON and JOIN USING in BigQuery SQL — USING is syntactic sugar for equality joins on same-named columns and..."
datePublished: 2024-06-05T21:27:56.075Z
dateUpdated: 2026-03-02T10:51:34.661Z
cover: "/images/joining-with-using-vs-on-in-bigquery/cover.jpg"
coverCredit:
  name: "Lance Grandahl"
  url: "https://unsplash.com/@lg17"
series: "practical-sql"
hashnodeCuid: "clx2cb99n000f0al71yq65b1h"
---

What's the difference when joining with `ON` vs `USING` clause in BigQuery SQL flavor? I was quite surprised to see USING when moving from SQLServer.  
  
In short:  
➡ USING allows you to join tables where the columns you want to join on have the same names and you just test for equality: table1.column = table2.column. You enumerate these columns in the USING clause :  
  
`USING (columnA, columnB, etc)`  
  
➡ ON is the more general one, doing everything what USING does (but you need to spell out that equality), but also allowing you to join on inequalities, transforming on the fly in joining, filtering for a value, and pretty much any other way you'd need joining.  
  
`ON table1.columnA = table2.columnA` etc  
  
So yes, USING is pretty much syntactic sugar for a fairly common type of join, but still narrower in functionality than the good old ON.  
  
It's worth pointing out that with USING, the columns in the clause do not need an alias for disambiguation (making clear which one of the two tables we take the column from), effectively doing the same a COALESCE of the columns in the two tables would do.  
This helps you a little bit with FULL OUTER JOINS for example. Of course, for other columns, if there are clashes in the namespace, you do need to specify where do you want them sourced from.

![BigQuery SQL joining orders to products (size, color, product\_id, variant) two ways: LEFT JOIN products p USING (product\_id, variant) lets product\_id and variant be selected unqualified, while ON o.product\_id = p.product\_id AND o.variant = p.variant needs o. prefixes; both return the same rows.](/images/joining-with-using-vs-on-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Self-joins in SQL](/self-joins-in-sql)
- [Anti-joins in SQL](/anti-joins-in-sql)
- [SEMI-JOINS in SQL](/semi-joins-in-sql)
- [NON-EQUI joins in SQL](/non-equi-joins-in-sql)
