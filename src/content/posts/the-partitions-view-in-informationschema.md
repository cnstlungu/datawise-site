---
title: "The PARTITIONS view in INFORMATION_SCHEMA"
seoTitle: "BigQuery INFORMATION_SCHEMA PARTITIONS View Explained"
seoDescription: "The PARTITIONS view in BigQuery INFORMATION_SCHEMA exposes partition row counts, bytes, storage tier, and last modified time."
datePublished: 2024-06-08T17:00:38.147Z
dateUpdated: 2026-03-02T10:51:44.652Z
cover: "/images/the-partitions-view-in-informationschema/cover.jpg"
coverCredit:
  name: "Waldemar"
  url: "https://unsplash.com/@waldemarbrandt67w"
series: "bigquery-performance"
hashnodeCuid: "clx6d32bn000207kwe6lp42tf"
---

Riding on the back of recent news that BigQuery table partition limit has just increased from 4k to 10k partitions, I wanted to talk a bit about the `PARTITIONS` view in `INFORMATION_SCHEMA`.

I've [previously posted about information schema views](/the-power-of-bigquery-informationschema-views), but this particular view allows us to get information about partitions in our partitioned tables.

Here's what we can find there:  
\- total rows in that partition  
\- logical & billable bytes for that partition  
\- storage tier (ACTIVE if modified in the last 90 days, LONG\_TERM otherwise which is 50% cheaper)  
\- last modified time

Now, let's focus this `last modified time` as it is quite useful when building incremental SQL pipelines. Looking at this field could tell you if data in one of your many partitions was changed since your last run and needs to be reprocessed.

Such a feature should help you in cases when you don't have a reliable watermark column to determine what changed since your last run.

```sql
SELECT * EXCEPT(table_catalog)
FROM `learning.INFORMATION_SCHEMA.PARTITIONS`

WHERE table_name = 'data_source'

ORDER BY last_modified_time DESC
```

![BigQuery results: 10 partitions of data\_source with partition\_id, total\_rows, total\_logical\_bytes, total\_billable\_bytes, last\_modified\_time and storage\_tier; 20221112 (modified 2024-05-31 10:14:06) and \_\_NULL\_\_ (0 rows, modified 2024-05-31 09:47:52) are ACTIVE, the other eight, about 100 rows and 2400 bytes each, last modified in 2023 or 2022, are LONG\_TERM.](/images/the-partitions-view-in-informationschema/1-result.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
