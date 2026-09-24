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

![Input data: a transaction\_date column with three dates, 2021-01-01, 2021-01-03 and 2021-01-05.](/images/using-gapsfill-in-bigquery/1-input.jpg)

```sql
SELECT
  dates.transaction_date

FROM GAP_FILL (
  TABLE learning.dates_with_gaps,
  'transaction_date',
  INTERVAL 1 DAY
) dates
```

![BigQuery results of GAP\_FILL: five rows, transaction\_date 2021-01-01, 2021-01-02, 2021-01-03, 2021-01-04 and 2021-01-05.](/images/using-gapsfill-in-bigquery/1-result.jpg)

```sql
WITH bounds AS (
  SELECT
    MIN(transaction_date) AS start_date,
    MAX(transaction_date) AS end_date
  FROM `learning.dates_with_gaps`
)

SELECT filled_date AS transaction_date
FROM bounds
JOIN UNNEST(GENERATE_DATE_ARRAY(start_date, end_date, INTERVAL 1 DAY)) AS filled_date
LEFT JOIN `learning.dates_with_gaps` dates ON filled_date = dates.transaction_date
```

![BigQuery results of the GENERATE\_DATE\_ARRAY query: the same five dates, 2021-01-01 through 2021-01-05.](/images/using-gapsfill-in-bigquery/1-result-2.jpg)
