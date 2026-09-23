---
title: "Search Indexes in BigQuery"
seoTitle: "BigQuery Search Indexes: Speed Up Text and JSON Queries"
seoDescription: "BigQuery search indexes accelerate SEARCH() queries on STRING and JSON columns. Learn how to create them, verify their use, and understand when they apply."
datePublished: 2024-04-06T22:29:41.003Z
dateUpdated: 2026-03-02T10:22:41.251Z
cover: "/images/search-indexes-in-bigquery/cover.jpg"
coverCredit:
  name: "Maksym Kaharlytskyi"
  url: "https://unsplash.com/@qwitka"
series: "bigquery-performance"
hashnodeCuid: "cluoo3k0b000308l3ev5zfzrh"
---

Here's something that might be interesting if you analyze large volumes of STRING or JSON data in BigQuery.

Let's look at SEARCH indexes and what you need to know to get started.

### So, what are they used for?

You have a big table (&gt;10 GB) with STRING or JSON columns which you perform text analysis on.

Search indexes can help retrieving data more efficiently from unstructured/semi-structured data - columns of type STRING, JSON, ARRAY of STRING, STRUCTS with STRING or JSON columns.

It can help optimize the usage of SEARCH funciton as well as other operators you use with string fields like 'STARTS\_WITH', 'IN', '=' or 'LIKE'.

### How to create one?

`CREATE SEARCH INDEX term_search_index ON dataset.table_name(ALL COLUMNS/1 or more columns);`

Based on what columns you've indexed, you can leverage the search index to search the entire table (columns with the compatible datatypes) or just a subset of columns of interest.

### How to know if an search index is used?

Check the 'Job Information' of your BigQuery. This will tell if you if an index was used, and if not, what was the reason.

![](/images/search-indexes-in-bigquery/1.jpg)

### Further reading

Check out [text analyzer options](https://cloud.google.com/bigquery/docs/reference/standard-sql/text-analysis) to see what different use case you can cover better. Maybe a future post about this 😁

### Words of caution

\- works best when you have a lot of distinct values (high query selectivity)  
\- if you've indexed all the columns any new compatible (STRING, JSON) column in that table will be indexed as well

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
