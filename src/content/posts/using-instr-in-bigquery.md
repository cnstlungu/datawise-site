---
title: "Using INSTR in BigQuery"
seoTitle: "BigQuery INSTR: Find Substring Position in a String"
seoDescription: "BigQuery's INSTR function returns the 1-based index of a substring within a string, returning 0 if not found. You can also specify a start position and..."
datePublished: 2024-04-22T20:50:42.666Z
dateUpdated: 2026-03-02T10:52:45.087Z
cover: "/images/using-instr-in-bigquery/cover.jpg"
coverCredit:
  name: "Sven Brandsma"
  url: "https://unsplash.com/@seffen99"
series: "practical-sql"
hashnodeCuid: "clvbflwmi00010al94mb9dnro"
---

If you ever need to do something different based on the existence of a particular substring in BigQuery, take a look at the INSTR function.

It returns the 1-based index of the first occurrence of a substring (1 or more characters) in another STRING. The function returns 0 if the substring was not found.

There's also a possibility to specify at what position to start the search (like in good old Excel) and which occurrence to get.

![BigQuery SQL using INSTR(fruits,',') and INSTR(fruits,';') to find the first comma and semicolon positions in fruit lists, feeding a CASE WHEN with SPLIT into fruits\_array; apple,grapes,melon gives 6 and 0 and splits into three items, while banana returns 0 for both.](/images/using-instr-in-bigquery/1.png)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
