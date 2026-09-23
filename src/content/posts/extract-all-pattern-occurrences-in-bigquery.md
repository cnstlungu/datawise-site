---
title: "Extract all pattern occurrences in BigQuery"
seoTitle: "BigQuery REGEXP_EXTRACT_ALL: Extract All Pattern Matches"
seoDescription: "REGEXP_EXTRACT_ALL in BigQuery returns an array of all substrings matching a regular expression pattern. It supports a single capture group and pairs well..."
datePublished: 2024-04-04T20:08:12.196Z
dateUpdated: 2026-03-02T10:50:31.789Z
cover: "/images/extract-all-pattern-occurrences-in-bigquery/cover.jpg"
coverCredit:
  name: "James McDonald"
  url: "https://unsplash.com/@jamesm"
series: "practical-sql"
hashnodeCuid: "clulo5wo4000h08lbd2h38wd2"
---

If you ever need to extract information based on a pattern in a BigQuery string, check out the `REGEXP_EXTRACT_ALL` function.

This will return an array of all the occurrences matching the specified regular expression.

With regards to the pattern itself, I typically use a representative example with a regex debugger like [regex101](https://regex101.com/).

Worth noting that it has a limitation - it would only work with a single regex capture group, so you can't match multiple patterns at the same time.

![](/images/extract-all-pattern-occurrences-in-bigquery/1.jpg)

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
