---
title: "Not all NULLS are the same"
seoTitle: "Understanding Different Types of NULLs"
seoDescription: "Understanding how different NULLs behave in BigQuery SQL and their impact on data types"
datePublished: 2024-10-27T12:25:21.145Z
dateUpdated: 2026-03-02T10:52:32.958Z
cover: "/images/not-all-nulls-are-the-same/cover.jpg"
coverCredit:
  name: "Pierre Bamin"
  url: "https://unsplash.com/@bamin"
series: "practical-sql"
hashnodeCuid: "cm2rkc5q0000309jxhjpu7tby"
---

So NULLs are definitely beasts of their own and as Data Engineers we come to learn to take them into account.

That is because not knowing their quirks can lead to unexpected results or errors. Let's look at how not all NULLS are the same in BigQuery SQL.

First, sure, the NULL means the absence of a value, but it is bound to a particular data type (so it's like "i'm a missing an INT64 here"). It can be found in columns with the NULLABLE mode, therefore a DATETIME NULL and a NUMERIC NULL cannot be compared as they are different types.

I've also seen that if we specify just the NULL literal, it defaults to INTEGER.

![BigQuery SQL showing typed NULLs: CAST(NULL AS INT64) \<\> CAST(NULL AS STRING) fails with no matching signature for operator !=, while CREATE OR REPLACE TABLE learning.my\_table AS SELECT NULL AS my\_column gives an INTEGER NULLABLE column, and comparing it to CAST(NULL AS INT64) returns null.](/images/not-all-nulls-are-the-same/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [https://www.notjustsql.com](https://www.notjustsql.com/)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [A couple of fun things about NULL in SQL](/a-couple-of-fun-things-about-null-in-sql)
- [COALESCE vs IFNULL vs NULLIF in BigQuery](/coalesce-vs-ifnull-vs-nullif-in-bigquery)
- [Null-safe comparison: IS DISTINCT/NOT DISTINCT FROM](/null-safe-comparison-is-distinctnot-distinct-from)
- [Controlling ordering of NULL values in the ORDER BY clause](/controlling-ordering-of-null-values-in-the-order-by-clause)
