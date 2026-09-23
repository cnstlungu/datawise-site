---
title: "Using LAST_VALUE with STRUCTS"
seoTitle: "Mastering LAST_VALUE Function with STRUCTS"
seoDescription: "Learn how to correctly use LAST_VALUE with STRUCTs in SQL and handle non-null structures with practical examples and solutions"
datePublished: 2025-10-05T16:27:43.240Z
dateUpdated: 2026-03-02T10:52:52.854Z
cover: "/images/using-lastvalue-with-structs/cover.jpg"
coverCredit:
  name: "Tanja Tepavac"
  url: "https://unsplash.com/@ttepavac"
series: "bigquery-window-functions"
hashnodeCuid: "cmgdx1154000002l962hqaixy"
---

Even an “empty” STRUCT is still technically something. Not the same as a standalone NULL value.

This is why, if you work with STRUCTs in SQL and try to find the latest non-empty struct using LAST\_VALUE(...) IGNORE NULLS, you’ll notice it doesn’t help — because the struct, even when all fields are null, is still considered non-null.

LAST\_VALUE only skips rows where the entire expression itself is NULL.

To fix this, we can adjust the logic in one of the following ways:  
➡️ Setting the value to NULL when all fields are NULL  
➡️ Using TO\_JSON\_STRING + NULLIF to treat such entries as “null”  
➡️ Using REGEXP\_CONTAINS (thanks ChatGPT) for more dynamic checks

Alternatively, we can just apply LAST\_VALUE separately to each individual field in the struct.

If you're new to STRUCTs, see [one of my previous posts](/understanding-structs-in-bigquery).

![BigQuery SQL where LAST\_VALUE(event IGNORE NULLS) on a STRUCT fails, since an all-NULL struct is not NULL and 2025-01-10 gets null fields, then three fixes: CASE WHEN event.a IS NULL AND event.b IS NULL THEN NULL, NULLIF(TO\_JSON\_STRING(event), ...) and REGEXP\_CONTAINS, all carrying 123 and 235 forward.](/images/using-lastvalue-with-structs/1.jpg)

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Beware of ROW_NUMBER without ORDER BY](/beware-of-rownumber-without-order-by)
- [Tidying up WINDOW functions in BigQuery with named windows](/tidying-up-window-functions-in-bigquery-with-named-windows)
- [Using RANGE in Window Functions in BigQuery](/using-range-in-window-functions-in-bigquery)
- [Computing a cumulative sum in BigQuery](/computing-a-cumulative-sum-in-bigquery)
