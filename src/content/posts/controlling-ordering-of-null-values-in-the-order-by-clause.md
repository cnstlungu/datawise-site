---
title: "Controlling ordering of NULL values in the ORDER BY clause"
seoTitle: "BigQuery ORDER BY: NULLS FIRST vs NULLS LAST Explained"
seoDescription: "Learn how BigQuery sorts NULL values by default in ORDER BY, and how to override that behavior with NULLS FIRST and NULLS LAST."
datePublished: 2024-06-05T21:34:46.691Z
dateUpdated: 2026-04-28T08:37:18.768Z
cover: "/images/controlling-ordering-of-null-values-in-the-order-by-clause/cover.jpg"
coverCredit:
  name: "Markus Spiske"
  url: "https://unsplash.com/@markusspiske"
series: "bigquery-window-functions"
hashnodeCuid: "clx2ck23n000009jway3i06lg"
---

Here's something I found out about the ORDER BY clause in BigQuery SQL the other day.

Check out the NULLS FIRST / NULLS LAST clauses. What do they do? They control how to treat NULL values when sorting.

While these are entirely optional, they're actually already happening behind the scenes even if you don't specify them.

🔹 ORDER BY \[column\] ASC (which is the default) uses NULLS FIRST if unspecified  
🔹 ORDER BY \[column\] DESC uses NULLS LAST if unspecified

![BigQuery SQL on six orders, two with NULL order\_amount, sorted with ORDER BY order\_amount DESC NULLS FIRST; the results list orders 3 and 5 (null) first, then 100, 90, 90 and 50.](/images/controlling-ordering-of-null-values-in-the-order-by-clause/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [A couple of fun things about NULL in SQL](/a-couple-of-fun-things-about-null-in-sql)
- [Not all NULLS are the same](/not-all-nulls-are-the-same)
- [COALESCE vs IFNULL vs NULLIF in BigQuery](/coalesce-vs-ifnull-vs-nullif-in-bigquery)
- [Null-safe comparison: IS DISTINCT/NOT DISTINCT FROM](/null-safe-comparison-is-distinctnot-distinct-from)
