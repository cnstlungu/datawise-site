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

![Input data: input\_data with population and surface, five rows labelled OK or ERROR: 10000 / 60 and 7000 / 35 are OK; 20000 / 0, 25000 / null and 25000 / -1 are ERROR.](/images/raising-errors-in-bigquery/1-input.jpg)

![BigQuery results for the two OK rows: population\_density 166.6666666666... and 200.0.](/images/raising-errors-in-bigquery/1-result.jpg)

```sql
SELECT population/surface AS population_density
FROM input_data
WHERE IF(IFNULL(surface,0) > 0,
         TRUE,
         ERROR(FORMAT('Error: surface must be strictly greater than 0, but is %t', surface)));
```

The query fails with the error `Error: surface must be strictly greater than 0, but is 0`.

```sql
SELECT population / CASE WHEN IFNULL(surface,0) > 0 THEN surface
                         ELSE ERROR(FORMAT('Error: surface must be strictly greater than 0, but is %t', surface)) END AS population_density

FROM input_data
```

The query fails with the error `Error: surface must be strictly greater than 0, but is NULL`.

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
