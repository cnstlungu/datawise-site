---
title: "Cleaning up STRINGS in BigQuery"
seoTitle: "BigQuery String Cleaning: TRIM, REPLACE, UPPER, SUBSTR"
seoDescription: "Clean messy string data in BigQuery using TRIM, REPLACE, UPPER, LOWER, SUBSTR, and NORMALIZE before analysis. The goal is a common denominator so matching..."
datePublished: 2024-04-24T21:27:43.142Z
dateUpdated: 2026-03-02T10:50:53.125Z
cover: "/images/cleaning-up-strings-in-bigquery/cover.jpg"
coverCredit:
  name: "JESHOOTS.COM"
  url: "https://unsplash.com/@jeshoots"
series: "practical-sql"
hashnodeCuid: "clvebt7ae00020amef47t9blm"
---

Data is collected and processed in a number of ways, and it should come as no surprise that it's not always perfect.

Perhaps the most important thing you need to do before analyzing data is have a look at how it's presented and check for irregularities.

Before any sound analysis a great deal of attention needs to be paid to cleaning the data.

Take string columns for instance. In BigQuery, as with other engines, there is a wealth of functions helping you to process strings, including:

\- TRIM/RTRIM/LTRIM for getting rid of the whitespace  
\- REPLACE to replace a substring with another one  
\- UPPER/LOWER/NORMALIZE etc to control casing  
\- SUBSTR/SUBSTRING to cut strings and so on.

The main goal here is to bring everything to a common denominator, being able to tell which observations belong together and which data can be considered "missing".

```sql
SELECT '' AS city --empty string
UNION ALL
SELECT ' ' AS city --whitespace
UNION ALL
SELECT 'New York' AS city
UNION ALL
SELECT 'Athens' AS city
UNION ALL
SELECT ' New York' AS city --whitespace before
UNION ALL
SELECT 'New York ' AS city -- whitespace after
UNION ALL
SELECT NULL AS city       -- NULL value
```

```sql
SELECT DISTINCT city FROM input_data
```

```sql
SELECT DISTINCT NULLIF(TRIM(city),'') AS city FROM input_data
```

![BigQuery results: SELECT DISTINCT city returns 7 rows (two that look blank, New York, Athens, New York with a leading space, New York again, and null), while the NULLIF(TRIM(city),'') query returns 3 rows: null, New York and Athens.](/images/cleaning-up-strings-in-bigquery/1-result.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
