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

```sql
DELETE FROM learning.data_source WHERE ds_date >= "2023-09-02";
INSERT INTO learning.data_source
SELECT * FROM learning.data_source_staging;
```

![BigQuery query validator: This script will process 67.97 KB when run.](/images/delete-insert-vs-merge-in-bigquery/1-result.png)

```sql
MERGE `learning.data_source` AS t
USING `learning.data_source_staging` AS s ON t.id = s.id AND t.ds_date = s.ds_date
WHEN NOT MATCHED THEN INSERT (id,value,ds_date) VALUES(id,value,ds_date)
WHEN MATCHED THEN UPDATE SET t.value = s.value
```

![BigQuery query validator: This query will process 9.15 MB when run.](/images/delete-insert-vs-merge-in-bigquery/1-result-2.png)

Happy querying!
