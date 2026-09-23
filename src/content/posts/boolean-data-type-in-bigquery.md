---
title: "Boolean data type in BigQuery"
seoTitle: "BigQuery BOOL Data Type: Write Cleaner SQL Conditions"
seoDescription: "BigQuery's BOOL type stores TRUE, FALSE, or NULL. Write boolean flags from comparisons, use them in WHERE clauses, and cast from INT64 or strings as needed."
datePublished: 2024-03-27T16:32:03.613Z
dateUpdated: 2026-03-02T10:16:32.110Z
cover: "/images/boolean-data-type-in-bigquery/cover.jpg"
coverCredit:
  name: "Gemma Evans"
  url: "https://unsplash.com/@stayandroam"
series: "practical-sql"
hashnodeCuid: "clua0x4pp000408jt91l8hnnu"
---

I remember that one of the things that struck me some years ago when switching from SQL Server to BigQuery was the existence of the bool data type in the latter, which I didn't have before.

I still see from time to time BigQuery code that does not leverage it to the fullest.

For example, this means you can just say `val_b > val_a AS is_val_b_higher` for a boolean flag instead of comparing and determining TRUE/FALSE. Also, just `WHERE is_val_b_higher` instead of `WHERE is_val_b_higher IS/= TRUE`.

This, in my opinion, makes the query much more readable when working with boolean flags.

If you properly name the flags, reading the query feels much closer to natural language.

![BigQuery SQL defining val\_b \> val\_a AS is\_val\_b\_higher and filtering with just WHERE is\_val\_b\_higher, which returns true, beside a SQL Server version that needs CAST(IIF(val\_b \> val\_a, 1, 0) AS BIT) and WHERE is\_val\_b\_higher = 1, with comments marking the plain boolean forms as errors there.](/images/boolean-data-type-in-bigquery/1.jpg)

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
