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

![BigQuery console screenshot of the Schema tab for the partitioned table data\_source, listing three NULLABLE fields: id INTEGER, value INTEGER and ds\_date DATE, next to the Details, Preview, Lineage, Data Profile and Data Quality tabs.](/images/table-sampling-in-bigquery/1.png)

Then comes the issue of cost.

In BigQuery, when working with big tables, you should know that a `LIMIT` clause does not reduce the amount of data processed (and thus the cost), but merely truncates the output.

There are a couple of ways around that.

### Preview

The simplest is the `PREVIEW` button, which allows us to see a subset of rows from this particular table. This does not incur any charges.

![BigQuery console screenshot of the Preview tab for the partitioned data\_source table, showing a free, scrollable subset of rows (rows 67 to 88 visible) with columns id, value and ds\_date, all dated 2020-12-18.](/images/table-sampling-in-bigquery/2.png)

### Partitioning

Another way would be leveraging partitions in a partitioned table. By selecting one particular partition in such a table we will achieve partition elimination - BigQuery will ignore all other partitions (dates) and process only the one we are providing, achieving a cost saving for us.

```sql
SELECT *
FROM `learning.data_source`
WHERE ds_date = "2022-01-01"
```

![BigQuery results: 10 rows of id, value and ds\_date, all with ds\_date 2022-01-01.](/images/table-sampling-in-bigquery/3-result.png)

### Sampling

A relatively new way would be using [Table Sampling](https://docs.cloud.google.com/bigquery/docs/table-sampling). While this is still in Pre-GA (so not fit for production yet), it is still handy when doing exploratory work with data.

How does it work? Using the TABLESAMPLE SYSTEM command, you provide a percentage of rows that you'd like sampled and returned to you.

The SQL command would look like as follows:

```sql
SELECT * 
FROM `learning.data_source` 
TABLESAMPLE SYSTEM (1 PERCENT)
```

Using this, from my table of ~400k rows the query returned 4k rows.

![BigQuery console Storage info panel for the table, showing Number of rows 399,803, the roughly 400k-row table used to test table sampling.](/images/table-sampling-in-bigquery/4.png)

![BigQuery console results pager showing Results per page 50 and 1 to 50 of 4000, meaning the TABLESAMPLE SYSTEM (1 PERCENT) query returned 4,000 rows from the roughly 400k-row table.](/images/table-sampling-in-bigquery/5.png)

To summarize, employing these three strategies — Preview, Partition Filtering, and Sampling — together, significantly saves time, computational resources, and consequently, money during the exploratory stage, especially when handling big tables.
