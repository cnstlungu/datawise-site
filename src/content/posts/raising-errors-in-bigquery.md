---
title: "Raising ERRORS in BigQuery"
seoTitle: "BigQuery ERROR(): Raise Custom Errors in SQL Queries"
seoDescription: "BigQuery's ERROR() raises a custom message when a SQL condition fails. Use it for data quality assertions and catching unexpected values in pipelines."
datePublished: 2024-04-24T21:30:45.558Z
dateUpdated: 2026-03-02T10:22:40.125Z
cover: "/images/raising-errors-in-bigquery/cover.jpg"
coverCredit:
  name: "Etienne Girardet"
  url: "https://unsplash.com/@etiennegirardet"
series: "practical-sql"
hashnodeCuid: "clvebx41i00020am7dovafq4t"
---

Does anyone have interesting use cases for the ERROR function in BigQuery?

If you like BQ errors so much that you've decided to create your own, or if you're debugging with dirty data, maybe check it out.

If will raise an error that you specify whenever executed. Plus you can also combine it with FORMAT to see what was the value that generated the issue.

![BigQuery SQL using ERROR(FORMAT('Error: surface must be strictly greater than 0, but is %t', surface)) inside WHERE IF(IFNULL(surface,0) \> 0, TRUE, ...) and in a CASE WHEN divisor to guard population/surface; the queries fail reporting surface 0 and NULL for the bad rows.](/images/raising-errors-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
