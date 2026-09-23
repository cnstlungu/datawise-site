---
title: "DECLARE and SET variables in BigQuery"
seoTitle: "BigQuery DECLARE and SET: Using Variables in SQL Scripts"
seoDescription: "Use DECLARE and SET in BigQuery SQL scripts to define reusable variables for incremental load watermarks, dynamic filters, and parameterized queries."
datePublished: 2024-07-03T21:27:16.452Z
dateUpdated: 2026-04-05T20:11:07.975Z
cover: "/images/declare-and-set-variables-in-bigquery/cover.jpg"
coverCredit:
  name: "s2 art"
  url: "https://unsplash.com/@s2artz"
series: "practical-sql"
hashnodeCuid: "cly6cm9d0000209l8dak6eagq"
---

Here's a part of procedural language that I use quite a lot in BigQuery.

Whether you're looking to run a query based on a multiple values of a particular parameter, finding out the watermark for incremental loading or just doing some testing, you can DECLARE and SET variables you can reuse across your query.

A couple of ways to do it:  
\- we can declare a variable with no type, but we need to provide a default, from which the time will be inferred  
\- a variable can be declared together with the type and choose to assign a value at declaration or later with SET  
\- a sub query can also provide the implicit value and table of a variable

![](/images/declare-and-set-variables-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Parameters in BigQuery](/parameters-in-bigquery)
