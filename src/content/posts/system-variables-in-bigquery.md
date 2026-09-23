---
title: "System variables in BigQuery"
seoTitle: "BigQuery System Variables: @@project_id and More"
seoDescription: "BigQuery system variables like @@project_id and @@time_zone expose runtime context in SQL scripts and procedures."
datePublished: 2024-07-05T07:00:37.170Z
dateUpdated: 2026-03-02T10:50:47.510Z
cover: "/images/system-variables-in-bigquery/cover.jpg"
coverCredit:
  name: "Alison Ivansek"
  url: "https://unsplash.com/@aliivan"
series: "practical-sql"
hashnodeCuid: "cly8cjfsi000909mk3jnudary"
---

Today's quick post is about system variables in BigQuery. What are they?

They are a special type of variables, available in scripts (multi-statement queries). You can use them to read (and sometimes write) query metadata during query execution.

Here's a couple of examples:  
\- `@@query_label` - read/write query labels, making easier for you to group your queries based on they are used for  
\- `@@time_zone` - read/write default time zone to use  
\- `@@script.job_id` - the job id of the current job

Check out below an example with slot\_ms (returns slot time in millis), bytes\_billed and creation\_date.

![BigQuery SQL script that runs a COUNT(DISTINCT value) GROUP BY ds\_date query on learning.data\_source, then selects system variables @@project\_id, @@script.slot\_ms, @@script.bytes\_billed and @@script.creation\_time; results show 636839 slot ms and 10485760 bytes billed.](/images/system-variables-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
