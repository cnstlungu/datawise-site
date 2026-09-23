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

![BigQuery SQL selecting \* EXCEPT(table\_catalog) from learning.INFORMATION\_SCHEMA.PARTITIONS for table data\_source ORDER BY last\_modified\_time DESC; results list partition\_id, total\_rows, bytes, last\_modified\_time and storage\_tier, with partition 20221112 modified 2024-05-31 ACTIVE and older ones LONG\_TERM.](/images/the-partitions-view-in-informationschema/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
