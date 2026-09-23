---
title: "COALESCE vs IFNULL vs NULLIF in BigQuery"
seoTitle: "BigQuery COALESCE vs IFNULL vs NULLIF: When to Use Each"
seoDescription: "Learn the difference between COALESCE, IFNULL, and NULLIF in BigQuery with side-by-side examples and practical guidance on when to use each one."
datePublished: 2024-03-25T16:34:59.796Z
dateUpdated: 2026-04-28T08:37:09.024Z
cover: "/images/coalesce-vs-ifnull-vs-nullif-in-bigquery/cover.jpg"
coverCredit:
  name: "Ben Hershey"
  url: "https://unsplash.com/@benhershey"
series: "practical-sql"
hashnodeCuid: "clu7657bn000208l3ce23eyfp"
---

What are they and when to use them?

\- IFNULL tests a column for the NULL value, returning the original value if it is NOT NULL and the second value we provide otherwise. The two columns need to be coercible to the same datatype. It's works like ISNULL in SQL Server.

\- COALESCE works like IFNULL, but for multiple values. The first of them to return a non-null value is returned, otherwise resulting in a NULL.

\- NULLIF allows you to replace a given value with a NULL, essentially saying "treat this value as it is was a missing value". An empty string, for example.

See below a representative example.

![](/images/coalesce-vs-ifnull-vs-nullif-in-bigquery/1.jpg)

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [A couple of fun things about NULL in SQL](/a-couple-of-fun-things-about-null-in-sql)
- [Not all NULLS are the same](/not-all-nulls-are-the-same)
- [Null-safe comparison: IS DISTINCT/NOT DISTINCT FROM](/null-safe-comparison-is-distinctnot-distinct-from)
- [Controlling ordering of NULL values in the ORDER BY clause](/controlling-ordering-of-null-values-in-the-order-by-clause)
