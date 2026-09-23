---
title: "GREATEST  & LEAST in BigQuery"
seoTitle: "BigQuery GREATEST and LEAST: Compare Values Across Columns"
seoDescription: "GREATEST and LEAST compare values across multiple columns in one expression. They skip NULLs by default — learn the exact behavior and edge case handling."
datePublished: 2024-03-25T16:26:45.889Z
dateUpdated: 2026-03-02T10:16:30.950Z
cover: "/images/greatest-least-in-bigquery/cover.jpg"
coverCredit:
  name: "NordWood Themes"
  url: "https://unsplash.com/@nordwood"
series: "practical-sql"
hashnodeCuid: "clu75um81000408jybt4k836b"
---

Have you ever had to compute the biggest or smallest value across multiple columns?

If so, note that in addition to using CASE WHEN or IF, we have GREATEST and LEAST, which will do exactly that.

I've also though they reminded me of how MIN / MAX in Excel works.

They also come with the advantage that you can compare multiple values at once.

As usual, pay attention to the NULLs - if one of values is NULL, the result would be as well.

![BigQuery SQL on val\_a 10, val\_b 20 and val\_c 30 comparing GREATEST(val\_a, val\_b) and LEAST(val\_a, val\_b) with equivalent IF expressions, plus GREATEST across all three; results are highest 20, also\_highest 20, lowest 10, also\_lowest 10 and greatest\_of\_all 30.](/images/greatest-least-in-bigquery/1.jpg)

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
