---
title: "Extended data type support for BigQuery search indexes"
seoTitle: "Expanded BigQuery Search Index Data Support"
seoDescription: "BigQuery's search index for INT64 and TIMESTAMP improves performance with large datasets, enhancing real-world applications"
datePublished: 2024-11-13T22:00:00.000Z
dateUpdated: 2026-03-02T10:52:26.200Z
cover: "/images/extended-data-type-support-for-bigquery-search-indexes/cover.jpg"
coverCredit:
  name: "Markus Winkler"
  url: "https://unsplash.com/@markuswinkler"
series: "bigquery-performance"
hashnodeCuid: "cm6w9gntv000f08l8ahybe642"
---

So, a couple of months ago, I posted about [BigQuery search indexes](/search-indexes-in-bigquery), interesting to those who work with large volumes of STRING or JSON data.

Recently, I came across a blog post introducing, in preview, the indexing of INT64 and TIMESTAMP columns as well.

Now, this brings interesting applications when working with big and huge tables, logs, or JSON data. You can partition only by one field and cluster by another four. You can’t partition or cluster by fields belonging to a STRUCT. Now this , using a SEARCH INDEX with integers and timestamps allows for a more efficient retrieval in such scenarios.

The referenced blog post (in comments) presents some pretty impressive improvements over not using search indexes.

I’ve played a bit with it but still haven’t managed to get the index to be used (which, last time, with STRING columns, I did). Perhaps something is wrong with the sample data (although not the size; I tried with a ~200 GB table), need to dig some more.

Does anyone use this feature in the real world?

```sql
CREATE SEARCH INDEX `test_index`

ON `auxiliary.sample_logs`(event_details, json_payload)

OPTIONS (data_types = ['STRING', 'INT64', 'TIMESTAMP'])
```

![Schema of auxiliary.sample\_logs: level STRING, source\_ip STRING, event\_details RECORD, json\_payload STRING and upsert\_timestamp TIMESTAMP, all NULLABLE.](/images/extended-data-type-support-for-bigquery-search-indexes/1-schema.jpg)

![Job information: 43.77 GB processed in 10 sec, Index Usage Mode UNUSED, because the amount of data covered by the search index on auxiliary.sample\_logs is too small for the index to be effective.](/images/extended-data-type-support-for-bigquery-search-indexes/1-result.jpg)

```sql
SELECT table_name, index_name, ddl, coverage_percentage, analyzer
FROM auxiliary.INFORMATION_SCHEMA.SEARCH_INDEXES
WHERE index_status = 'ACTIVE';
```

![BigQuery results: table sample\_logs with index test\_index, its DDL (partly visible), coverage\_percentage 0 and analyzer LOG\_ANALYZER.](/images/extended-data-type-support-for-bigquery-search-indexes/1-result-2.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [https://www.notjustsql.com](https://www.notjustsql.com/)*.*
