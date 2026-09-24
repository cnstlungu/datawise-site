---
title: "Generating date intervals in BigQuery"
seoTitle: "Generate Date Sequences in BigQuery with GENERATE_DATE_ARRAY"
seoDescription: "Learn how to use GENERATE_DATE_ARRAY and GENERATE_TIMESTAMP_ARRAY in BigQuery to create date or timestamp sequences at any interval."
datePublished: 2024-01-16T11:01:59.203Z
dateUpdated: 2026-03-02T10:51:16.521Z
cover: "/images/generating-date-intervals-in-bigquery/cover.jpg"
coverCredit:
  name: "Kyrie kim"
  url: "https://unsplash.com/@kyrie3"
series: "practical-sql"
hashnodeCuid: "clrg8v677000b09jrd2doaq22"
---

Ever had to generate a date interval in BigQuery?

Take a look at the GENERATE\_DATE\_ARRAY function.

Needs 3 arguments:  
\- start\_date  
\- end\_date  
\- interval step (DAY, WEEK, MONTH, QUARTER, YEAR)

Since it generates an ARRAY, we would need to UNNEST it to get one date per row.

If you need something more granular, there is the very similar GENERATE\_TIMESTAMP\_ARRAY, which can generate in increments between MICROSECOND and DAY.

Friendly reminder to not mix and match DATETIME and TIMESTAMP without properly converting between them beforehand - see [my previous post](/datetime-vs-timestamp-in-bigquery).

```sql
SELECT

  valid_date

FROM UNNEST(GENERATE_DATE_ARRAY('2021-01-01', '2021-01-31', INTERVAL 1 DAY)) AS valid_date
```

![BigQuery results: 31 rows of valid\_date, one per day from 2021-01-01 to 2021-01-31.](/images/generating-date-intervals-in-bigquery/1-result.jpg)
