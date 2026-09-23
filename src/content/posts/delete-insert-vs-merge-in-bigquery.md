---
title: "DELETE + INSERT vs MERGE in BigQuery"
seoTitle: "BigQuery DELETE + INSERT vs MERGE: Which Costs Less?"
seoDescription: "Comparing DELETE+INSERT and MERGE strategies for updating BigQuery partitioned tables. Free partition deletion makes DELETE+INSERT a cost-effective..."
datePublished: 2024-03-18T21:58:44.677Z
dateUpdated: 2026-03-02T10:50:54.310Z
cover: "/images/delete-insert-vs-merge-in-bigquery/cover.jpg"
coverCredit:
  name: "Sam Pak"
  url: "https://unsplash.com/@sampakpak"
series: "practical-sql"
hashnodeCuid: "cltxhmkzp000208l587nigamf"
---

How do you merge changes from staging tables into target tables in BigQuery?

I've previously covered [swapping out partitions using bq command](/swapping-partitions-in-bigquery) and [using constant false predicate "MERGE on FALSE"](/merge-on-false-in-bigquery), but I've learned that you can [now DELETE entire partitions for free](https://docs.cloud.google.com/bigquery/docs/release-notes#February_27_2024) (provided a filter on the partitioned column is used) from tables.

That means that instead of merging your changes the old-fashioned way, it might be well worth DELETING the days you would like to update and INSERTING the entire days data back sourced from the staging table.

Here's a comparison of the two approaches for the same source and destination tables. As you can see the amount of processed data can be wildly different between the two.

![BigQuery SQL comparing two ways to load staging data: DELETE FROM learning.data\_source WHERE ds\_date \>= 2023-09-02 then INSERT INTO ... SELECT \* FROM learning.data\_source\_staging, estimated at 67.97 KB, versus a MERGE ON id and ds\_date with WHEN NOT MATCHED THEN INSERT and WHEN MATCHED THEN UPDATE SET, estimated at 9.15 MB.](/images/delete-insert-vs-merge-in-bigquery/1.png)

Happy querying!

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
