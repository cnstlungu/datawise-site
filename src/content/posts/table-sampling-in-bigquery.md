---
title: "Table Sampling in BigQuery"
seoTitle: "BigQuery Table Sampling: Explore Big Tables Cost-Efficiently"
seoDescription: "Three ways to explore large BigQuery tables without full scan costs: the Preview button, partition filtering, and TABLESAMPLE SYSTEM — with guidance on..."
datePublished: 2023-10-26T12:18:48.709Z
dateUpdated: 2026-03-02T10:51:43.515Z
cover: "/images/table-sampling-in-bigquery/cover.jpg"
coverCredit:
  name: "Louis Reed"
  url: "https://unsplash.com/@_louisreed"
series: "bigquery-performance"
hashnodeCuid: "clo75i491000509mj221s3n2x"
---

It should be no surprise that understanding your data is very important when working with it. The initial step in my approach to a new dataset always involves examining the data closely. Although the `Schema Tab` reveals the data schema, to grasp the contents, identify missing data, spot potential issues, and review the cardinality of values, taking a look at the data is unavoidable.

![Schema tab for a table in BigQuery](/images/table-sampling-in-bigquery/1.png)

Then comes the issue of cost.

In BigQuery, when working with big tables, you should know that a `LIMIT` clause does not reduce the amount of data processed (and thus the cost), but merely truncates the output.

There are a couple of ways around that.

### Preview

The simplest is the `PREVIEW` button, which allows us to see a subset of rows from this particular table. This does not incur any charges.

![Preview Tab](/images/table-sampling-in-bigquery/2.png)

### Partitioning

Another way would be leveraging partitions in a partitioned table. By selecting one particular partition in such a table we will achieve partition elimination - BigQuery will ignore all other partitions (dates) and process only the one we are providing, achieving a cost saving for us.

![Reading one partition from a partitioned table](/images/table-sampling-in-bigquery/3.png)

### Sampling

A relatively new way would be using [Table Sampling](https://cloud.google.com/bigquery/docs/table-sampling). While this is still in Pre-GA (so not fit for production yet), it is still handy when doing exploratory work with data.

How does it work? Using the TABLESAMPLE SYSTEM command, you provide a percentage of rows that you'd like sampled and returned to you.

The SQL command would look like as follows:

```sql
SELECT * 
FROM `learning.data_source` 
TABLESAMPLE SYSTEM (1 PERCENT)
```

Using this, from my table of ~400k rows the query returned 4k rows.

![](/images/table-sampling-in-bigquery/4.png)

![](/images/table-sampling-in-bigquery/5.png)

To summarize, employing these three strategies — Preview, Partition Filtering, and Sampling — together, significantly saves time, computational resources, and consequently, money during the exploratory stage, especially when handling big tables.

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
