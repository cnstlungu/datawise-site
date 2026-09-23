---
title: "Concatenation operator in BigQuery"
seoTitle: "BigQuery || Concatenation Operator for Strings and Arrays"
seoDescription: "The || operator in BigQuery is the ANSI SQL standard concatenation operator, equivalent to CONCAT() for strings and ARRAY_CONCAT() for arrays."
datePublished: 2024-04-28T21:43:07.053Z
dateUpdated: 2026-03-02T10:51:31.300Z
cover: "/images/concatenation-operator-in-bigquery/cover.jpg"
coverCredit:
  name: "Belinda Fewings"
  url: "https://unsplash.com/@bel2000a"
series: "practical-sql"
hashnodeCuid: "clvk24eul000c0aifc0j911h6"
---

You might have encountered the slightly odd-looking `||` in SQL before, whether in BigQuery or your other database system.

If not yet, it's called the 'concatenation operator' and well, it concatenates things.

In fact, it's the ANSI SQL standard concatenation operator so in theory it should work across database engines (but it doesn't - for example SQL Server uses `+` instead for concatenating strings).

In BigQuery, it does the same thing as `CONCAT()` for STRINGs and `ARRAY_CONCAT()` for ARRAYs .

![](/images/concatenation-operator-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
