---
title: "Ingestion-time partitioning in BigQuery"
seoTitle: "Ingestion-Time Partitioning in BigQuery: How It Works"
seoDescription: "Ingestion-time partitioning in BigQuery automatically assigns rows to date-based partitions as they arrive. Learn how to use _PARTITIONTIME and..."
datePublished: 2024-07-04T07:00:32.630Z
dateUpdated: 2026-03-02T10:51:06.435Z
cover: "/images/ingestion-time-partitioning-in-bigquery/cover.jpg"
coverCredit:
  name: "Nikolai Chernichenko"
  url: "https://unsplash.com/@perfectcoding"
series: "bigquery-performance"
hashnodeCuid: "cly6x3hme000209jlcr2gd6oy"
---

Have you ever used ingestion-time partitioning in BigQuery?

It's a separate type of partitioning that distributes rows into partitions based on the time they land in BQ.

Once such a table is defined, you can query the pseudocolumns *PARTITIONDATE and* PARTITIONTIME.

As with other partition types, you can set up OPTIONS such as :  
\- partition\_expiration\_days = drops a partition after a given period of time  
\- require\_partition\_filter = forces a user to use a partition filter when querying

Reminder that if you're ingesting data via a BigQuery job (say using the bq CLI utility), you can also control which partition in this table you want to write to using a decorator e.g. `my_table$20240621`

![](/images/ingestion-time-partitioning-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
