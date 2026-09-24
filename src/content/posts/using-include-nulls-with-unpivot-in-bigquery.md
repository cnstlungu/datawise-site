---
title: "Using INCLUDE NULLS with UNPIVOT in BigQuery"
seoTitle: "UNPIVOT INCLUDE NULLS in BigQuery to Keep NULL Rows"
seoDescription: "Learn how UNPIVOT in BigQuery drops NULL rows by default and how to retain them using the INCLUDE NULLS modifier."
datePublished: 2024-02-17T13:51:00.099Z
dateUpdated: 2026-03-02T10:50:35.137Z
cover: "/images/using-include-nulls-with-unpivot-in-bigquery/cover.jpg"
coverCredit:
  name: "Pierre Bamin"
  url: "https://unsplash.com/@bamin"
series: "practical-sql"
hashnodeCuid: "clsq4zsaq000009l586a1d366"
---

While solving a bug I was reminded *again* that, when UNPIVOTing, rows with NULL values are excluded. Fine.

But it turns out we have the option to specify the INCLUDE NULLS with UNPIVOT, thus allowing us to keep those rows in the result set.

Let's look at an example.

![BigQuery console result showing the wide input table for UNPIVOT, with columns measurement\_date, water\_level, temperature and pressure for 2021-01-01 to 2021-01-03, a null water\_level on 2021-01-01 and a null temperature on 2021-01-02.](/images/using-include-nulls-with-unpivot-in-bigquery/1.png)

This is how it would look if UNPIVOTed as usual:

```sql
SELECT 
    measurement_date, 
    value, 
    measurement 
FROM input
UNPIVOT INCLUDE NULLS (value FOR measurement IN (water_level, temperature, pressure))
```

![BigQuery console result of a regular UNPIVOT into columns measurement\_date, value and measurement: only 7 rows, because the null water\_level for 2021-01-01 and the null temperature for 2021-01-02 are dropped.](/images/using-include-nulls-with-unpivot-in-bigquery/2.png)

As you notice, we don't have the rows where the measurement values are NULL.

How can we fix it? Let's use UNPIVOT in conjunction with `INCLUDE NULLS`.

```sql
SELECT 
    measurement_date, 
    value, 
    measurement 
FROM input
UNPIVOT INCLUDE NULLS (value FOR measurement IN (water_level, temperature, pressure))
```

![BigQuery console result of UNPIVOT INCLUDE NULLS with columns measurement\_date, value and measurement: all 9 rows appear, including null values for water\_level on 2021-01-01 and temperature on 2021-01-02.](/images/using-include-nulls-with-unpivot-in-bigquery/3.png)

Voila! The NULL entries are here now.
