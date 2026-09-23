---
title: "Using GAPS_FILL in BigQuery"
seoTitle: "BigQuery GAPS_FILL: Fill Missing Rows in Time Series"
seoDescription: "BigQuery's GAPS_FILL table-valued function fills missing intervals in DATE, DATETIME, or TIMESTAMP series without needing a date dimension or..."
datePublished: 2024-05-07T13:29:13.362Z
dateUpdated: 2026-03-02T10:51:47.975Z
cover: "/images/using-gapsfill-in-bigquery/cover.jpg"
coverCredit:
  name: "Suad Kamardeen"
  url: "https://unsplash.com/@suadkamardeen"
series: "practical-sql"
hashnodeCuid: "clvwffxci000c09kz910d2sub"
---

Another new time series function in BigQuery in addition to the [ones previously presented](/time-series-functions-in-bigquery) is the `GAPS_FILL` table-valued function.

It allows us to fill in a time series (DATE, DATETIME, TIMESTAMP) with missing rows to a desired time grain.

Previously, one could have solved this by joining with a date dimension or by using GENERATE\_DATE\_ARRAY for example.

It's simpler now, you just need to provide:  
\- the table you'd like to fill in  
\- the column you'd like to fill in (for example a DATE column)  
\- the interval you'd like the filling in to happen (time grain of the table)

In the example below, it allows us to fill in the time series with 2 missing days.

Since it's a table-valued function, it acts like a table so you select FROM it.

Obligatory remark that this is in 'Preview' for now.

![BigQuery SQL filling a transaction\_date column with gaps (2021-01-01, 01-03, 01-05) two ways: the GAP\_FILL table function with TABLE learning.dates\_with\_gaps, 'transaction\_date' and INTERVAL 1 DAY, and a bounds CTE with GENERATE\_DATE\_ARRAY and LEFT JOIN; both return all five dates.](/images/using-gapsfill-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at*[*notjustsql.com*](https://www.notjustsql.com)*.*
