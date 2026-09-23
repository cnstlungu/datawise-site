---
title: "Computing a hash aggregation in BigQuery"
seoTitle: "BigQuery Hash Aggregation Explained"
seoDescription: "Learn to simulate Snowflake's HASH_AGG in BigQuery to check for data changes using existing functions"
datePublished: 2024-10-21T12:33:40.393Z
dateUpdated: 2026-03-02T10:51:04.253Z
cover: "/images/computing-a-hash-aggregation-in-bigquery/cover.jpg"
coverCredit:
  name: "Tomas Sobek"
  url: "https://unsplash.com/@tomas_nz"
series: "practical-sql"
hashnodeCuid: "cm2izzqy1000009mfebxvedm3"
---

So I've seen Snowflake has an HASH\_AGG function. When would we need it?

Every time we'd like to work out if ANY value in a group (or the entire table) has changed in any way, even a single extra blank space.

While BigQuery does not have it yet, we can still simulate it using the tools at hand.

Here's how we can do it:  
\- TO\_JSON\_STRING to create a STRUCT from each entire row (or create a STRUCT containing only the columns you care about)  
\- STRING\_AGG to aggregate all the json strings into a single value per group (or the entire table)  
\- FARM\_FINGERPRINT, a hashing function that will product the same output given only the exact same input, check my comment for more info

```sql
WITH input_data AS (
  SELECT 1 AS id , DATE '2021-01-01' AS event_date, 10 AS number_value, NULL AS text_value UNION ALL
  SELECT 1 AS id, DATE '2021-01-02' AS event_date, 11 AS number_value, 'def' AS text_value UNION ALL
  SELECT 1 AS id, DATE '2021-01-03' AS event_date, 12 AS number_value, 'fgh' AS text_value UNION ALL
  SELECT 2 AS id , DATE '2021-01-03' AS event_date, 8 AS number_value, 'lmn' AS text_value UNION ALL
  SELECT 2 AS id, DATE '2021-01-04' AS event_date, 8 AS number_value, 'opq' AS text_value UNION ALL
  SELECT 2 AS id, DATE '2021-01-05' AS event_date, NULL AS number_value, 'rst' AS text_value
)
SELECT

  id,
  FARM_FINGERPRINT(STRING_AGG(TO_JSON_STRING(t))) AS group_hash

FROM input_data t

GROUP BY id
```

![BigQuery results: group\_hash 2171288142330… for id 1 and 7271343146336… for id 2 (both truncated in the grid).](/images/computing-a-hash-aggregation-in-bigquery/1-result.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
