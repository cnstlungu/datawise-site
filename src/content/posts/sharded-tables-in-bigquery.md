---
title: "Sharded tables in BigQuery"
seoTitle: "BigQuery Sharded Tables: What They Are and When to Avoid"
seoDescription: "Sharded tables in BigQuery use a name suffix pattern like table_YYYYMMDD and support wildcard queries, but carry schema and metadata overhead."
datePublished: 2024-04-15T21:46:36.200Z
dateUpdated: 2026-03-02T10:50:50.851Z
cover: "/images/sharded-tables-in-bigquery/cover.jpg"
coverCredit:
  name: "Jisun Han"
  url: "https://unsplash.com/@hanzlog"
series: "practical-sql"
hashnodeCuid: "clv1hitk8000708l8gb5260it"
---

Have you ever worked with sharded tables in BigQuery?

I've encountered them in a project long time ago and haven't seen them much around since.

Does the name not ring a bell?

Well, think of it as pseudo-partitioning, a way to store data split between different tables, each having a different suffix in the name `dataset.table_name_{your_suffix}`.

We'll be getting different tables, but they can be queried as one by using a wildcard \*, retrieving data from all the tables matching the wildcard, like having an invisible UNION ALL behind the scenes.

In practice, I've seen these suffixes most of the time being dates like YYYYMMDD. So, in this case, BigQuery docs discourage this usage of sharding, citing the overhead in terms of storing a separate schema and metadata + permission checks as compared to just using a date-partitioned table.

So you're just better off to use a partitioned table in this case.

They even offer a quick way to convert a group of date-sharded tables to a regular date-partitioned table.

Have you ever encountered any interesting use cases for sharding?

![BigQuery console screenshot of date-sharded tables: the explorer groups them as sharded\_table\_ (2), the sharded\_table\_20240102 page has a shard picker listing 2024 01-01 and 01-02, and SELECT \* FROM learning.sharded\_table\_\* returns rows from both shards.](/images/sharded-tables-in-bigquery/1.jpg)
