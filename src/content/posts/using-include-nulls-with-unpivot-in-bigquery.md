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

![](/images/using-include-nulls-with-unpivot-in-bigquery/1.png)

This is how it would look if UNPIVOTed as usual:

```sql
SELECT 
    measurement_date, 
    value, 
    measurement 
FROM input
UNPIVOT INCLUDE NULLS (value FOR measurement IN (water_level, temperature, pressure))
```

![](/images/using-include-nulls-with-unpivot-in-bigquery/2.png)

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

![](/images/using-include-nulls-with-unpivot-in-bigquery/3.png)

Voila! The NULL entries are here now.

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
