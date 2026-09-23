---
title: "Watch out when using SAFE_CAST in BigQuery"
seoTitle: "BigQuery SAFE_CAST Silent NULL: Nanosecond Timestamp Bug"
seoDescription: "Explains a subtle BigQuery SAFE_CAST pitfall where nanosecond-precision timestamps silently return NULL instead of raising an error."
datePublished: 2024-02-16T14:59:06.975Z
dateUpdated: 2026-03-02T10:51:01.025Z
cover: "/images/watch-out-when-using-safecast-in-bigquery/cover.jpg"
coverCredit:
  name: "Jarrod Erbe"
  url: "https://unsplash.com/@erbephoto"
series: "practical-sql"
hashnodeCuid: "clsorzj3300030akzcwr68rbj"
---

Here's an interesting situation I've seen with BigQuery.

Say a source system provides JSON events with timestamps at microsecond grain (6 decimals, so something like `2024-01-01 14:00:00.123456`).

This is cast using SAFE\_CAST into a proper TIMESTAMP. All works just fine.

Until one day the source system sends the JSON with timestamps at NANOsecond grain.  
Since timestamp has only MICROsecond precision, the cast quietly fails (no error), a null is returned from a seemingly correct looking timestamp.

Without proper monitoring this issue can go unnoticed quite a bit. So watch out 🤔

It just drives the point home on how important is to have proper monitoring in place and enforcing a robust data contract with data sources.

![](/images/watch-out-when-using-safecast-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
