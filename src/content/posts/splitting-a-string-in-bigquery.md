---
title: "Splitting a STRING in BigQuery"
seoTitle: "BigQuery SPLIT: Split a String by Delimiter into an Array"
seoDescription: "SPLIT(string, delimiter) returns an array of substrings in BigQuery. Access elements with OFFSET, expand rows with UNNEST, or recombine with STRING_AGG."
datePublished: 2024-04-11T21:15:36.997Z
dateUpdated: 2026-03-02T10:16:21.866Z
cover: "/images/splitting-a-string-in-bigquery/cover.jpg"
coverCredit:
  name: "Bon Vivant"
  url: "https://unsplash.com/@bonvivant"
series: "practical-sql"
hashnodeCuid: "cluvqnkbp000208lc0smg3it8"
---

Splitting a string in BigQuery works pretty much the same as in Excel.

`SPLIT` works in a similar way as its Excel cousin `TEXTSPLIT` - taking a string to be split and a delimiter (can be multiple characters), and returns an array of elements.

You can access them using the 0-based index or check out [my previous post](/accessing-array-elements-in-bigquery) on more options for accessing array elements in BigQuery.

![](/images/splitting-a-string-in-bigquery/1.jpg)

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
