---
title: "Why you should care about partition pruning in BigQuery"
seoTitle: "BigQuery Partition Pruning: MERGE and _PARTITIONTIME Gotchas"
seoDescription: "Filtering on DATE(_PARTITIONTIME) or inside a MERGE ON clause can silently disable partition pruning in BigQuery. See which filter patterns keep scans cheap."
datePublished: 2024-02-22T10:05:10.891Z
dateUpdated: 2026-04-28T08:37:15.243Z
cover: "/images/why-you-should-care-about-partition-pruning-in-bigquery/cover.jpg"
coverCredit:
  name: "Ivan Bandura"
  url: "https://unsplash.com/@unstable_affliction"
series: "bigquery-performance"
hashnodeCuid: "clsx24mzv000208l2anfg1qpb"
---

When it comes to performance improvements and cost savings, handling only as much data as we need is very important. And partitioning is a cornerstone here.

Now, when working with tables that are partitioned, BigQuery tries to exclude the partitions it does not need (akin to pruning a tree) based on filters (WHERE clause) and JOINS, thus saving you time and processing power (and money).

But it's not always that simple. If you perform operations on the partitioned field (say the date field in a date-partitioned table), Big Q might not be able to prune the table accordingly. So you'll end up processing the entire massive table, even though you were only after one single day.

There's an example below with this happening when converting the date to a different timezone, but I've seen it happen with other operations. Pruning would not work in MERGE statement sourced from two UNIONed partitioned tables.

Check the number of rows read from the table in the examples below.

![BigQuery console execution graphs for two queries on learning.data\_source: filtering WHERE ds\_date = 2022-02-21 reads 100 records, while wrapping the partition column as DATE(TIMESTAMP(ds\_date, 'Asia/Tokyo')) = 2022-02-20 reads 399,803 records. Records read is highlighted in both.](/images/why-you-should-care-about-partition-pruning-in-bigquery/1.jpg)

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Why partitioning tables is not a silver bullet for BigQuery performance](/why-partitioning-tables-is-not-a-silver-bullet-for-bigquery-performance)
- [Optimizing SQL queries in BigQuery](/optimizing-sql-queries-in-bigquery)
- [Optimizing compute cost in BigQuery](/optimizing-compute-cost-in-bigquery)
- [Optimizing storage costs in BigQuery](/optimizing-storage-costs-in-bigquery)
