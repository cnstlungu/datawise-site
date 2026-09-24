---
title: "Using GROUP BY ALL in BigQuery"
seoTitle: "BigQuery GROUP BY ALL: Skip Listing Non-Aggregated Cols"
seoDescription: "BigQuery's GROUP BY ALL automatically groups by all non-aggregated columns in your SELECT, eliminating the need to list them manually."
datePublished: 2024-03-05T16:13:09.054Z
dateUpdated: 2026-03-02T10:50:41.902Z
cover: "/images/using-group-by-all-in-bigquery/cover.jpg"
coverCredit:
  name: "Monika Borys"
  url: "https://unsplash.com/@fotoinshadows"
series: "practical-sql"
hashnodeCuid: "cltekk2m6000209ld6pj044br"
---

Featured in other database systems, the `GROUP BY ALL` has been [announced in preview](https://docs.cloud.google.com/bigquery/docs/release-notes#February_26_2024) for BigQuery as well.

This will allow us to **not** enumerate all the non-aggregated columns when performing aggregates.

It's definitely better than `GROUP BY 1,2,3` which would fail once we'd change the list of columns we'd like to group by. Overall, I find it a useful shorthand when exploring or debugging.

Here's an example of how it looks.

```sql

SELECT country, sell_date, SUM(sales) AS total_sales

FROM input_data

-- new
GROUP BY ALL

-- instead of
-- GROUP BY country, sell_date
```

![BigQuery console Results tab for the GROUP BY ALL query, with columns country, sell\_date and total\_sales and one row per country and date: UK 150 and 195, US 200 and 260 for 2021-01-01 and 2021-01-02.](/images/using-group-by-all-in-bigquery/1.png)
