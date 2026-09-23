---
title: "BigQuery BigLake Tables Explained: What They Are and When to Use Them"
subtitle: "Query your data lake with warehouse-grade security and performance — without moving a single file."
seoTitle: "BigLake Tables: Faster, Safer BigQuery External Data"
seoDescription: "BigQuery BigLake tables improve on classic external tables with access delegation, row-level security, and metadata caching. Includes a SQL example."
datePublished: 2026-04-26T21:13:46.927Z
cover: "/images/bigquery-biglake-tables-explained-what-they-are-and-when-to-use-them/cover.jpg"
series: "bigquery-performance"
tags: ["bigquery", "gcp", "data-engineering", "google-cloud", "sql"]
hashnodeCuid: "cmog9mu2500a01qjp1lln6h5e"
---

If you've worked with BigQuery [external tables](https://docs.cloud.google.com/bigquery/docs/external-tables) before, you know the basic idea: a thin wrapper around data that resides somewhere else, but queryable from BigQuery. Sources include Cloud Storage, [Google Sheets](/importing-google-sheets-into-bigquery), or Google Drive.

Today I'd like to talk about a special variety of external table: the **BigLake table**. It's built to bridge data lakes and data warehouses.

### BigQuery External Tables: Limitations and Pain Points

With a regular external table, users need access both to the BigQuery table *and* to the underlying external data source.

If the data is in Cloud Storage, a user needs BigQuery permissions, but also permissions on the bucket and objects. This might be fine for a quick exercise, but the pain points are real:

*   you manage permissions in multiple places, for different types of resources
    
*   bucket-level access can be too broad
    
*   it's harder to apply table-like governance on files
    

### How BigLake Tables Work: Access Delegation Explained

BigLake tables use a BigQuery Connection that accesses the files on behalf of the users. Users don't need direct access to the underlying buckets.

This enables table-level security on external data, including:

*   row-level security
    
*   column-level security
    
*   dynamic data masking (for Cloud Storage BigLake tables)
    

BigLake also enables — powered by BQ Omni — reading data from Amazon S3 and Azure Blob Storage.

### Metadata Caching in BigLake Tables: Faster Queries, Better Plans

When querying external data, BigQuery needs to inspect the files first: what files exist, how they are partitioned, and what metadata they contain. With classic external tables, every query triggers a listing operation against the underlying storage.

If you have a small number of files, this is barely noticeable. If you have thousands or millions of files, especially Hive-partitioned data, it becomes painful.

BigLake tables unlock metadata caching. With it enabled, BigQuery skips the listing on every query and prunes files and partitions faster — avoiding reading unneeded files altogether.

For Parquet BigLake tables, metadata caching also collects table statistics, which helps the optimizer produce better query plans.

The cache has a staleness window you control, and you choose between automatic or manual refreshes (the manual option runs a stored procedure, useful if you want to make it event-driven).

### Creating a BigLake Table: Step-by-Step SQL Example

Say we have some sales data in Google Cloud Storage as follows

![Preview of an orders CSV file from the order\_date=2026-04-01, country=DE partition, with columns order\_id, customer\_id, channel, amount, discount\_amount and created\_at, and web, marketplace and store orders such as O20260401DE0000 at 156.71.](/images/bigquery-biglake-tables-explained-what-they-are-and-when-to-use-them/1.png)

It is Hive partitioned Date -> Country.

![Google Cloud Storage console screenshot of the datawise-biglake-hive-demo bucket with a Hive-partitioned layout: orders/order\_date=2026-04-01 through 2026-04-10, each with country=DE, GB, RO and US folders; the country=DE folder holds a single 1.6 KB orders.csv.](/images/bigquery-biglake-tables-explained-what-they-are-and-when-to-use-them/2.png)

In order to create a BigLake table we need to do the following:

Create a BQ Connection

![BigQuery console screenshot of the Connections page, with Connections highlighted in the left explorer panel, listing demo-biglake-connection and test-bigquery-connection, both in the eu location.](/images/bigquery-biglake-tables-explained-what-they-are-and-when-to-use-them/3.png)

![BigQuery console screenshot of the External data source form for a new connection: type Vertex AI remote models, remote functions, Lakehouse and Spanner (Cloud Resource), Connection ID demo-biglake-connection, EU multi-region, description Connection for BigLake Table.](/images/bigquery-biglake-tables-explained-what-they-are-and-when-to-use-them/4.png)

![BigQuery console screenshot of the Connection info page for demo-biglake-connection: data location eu, Cloud Resource connection type, description Connection for BigLake Table, and a service account id ending in gcp-sa-bigquery-condel.iam.gserviceaccount.com, with project details hidden.](/images/bigquery-biglake-tables-explained-what-they-are-and-when-to-use-them/5.png)

Now, we need to grant this service account access to the GCS bucket

![Google Cloud Storage console screenshot of the Edit access dialog for the datawise-biglake-hive-demo bucket, granting the connection's bqc service account at gcp-sa-bigquery-condel.iam.gserviceaccount.com the Storage Object Viewer role.](/images/bigquery-biglake-tables-explained-what-they-are-and-when-to-use-them/6.png)

We can now create the BigLake table:

```sql
CREATE EXTERNAL TABLE `learning.orders_biglake`
(
  order_id STRING,
  customer_id INT64,
  channel STRING,
  amount NUMERIC,
  discount_amount NUMERIC,
  created_at TIMESTAMP
)
WITH PARTITION COLUMNS
(
  order_date DATE,
  country STRING
)
WITH CONNECTION `projects/your-gcp-project/locations/eu/connections/demo-biglake-connection`
OPTIONS (
  format = 'CSV',
  skip_leading_rows = 1,
  field_delimiter = ',',
  hive_partition_uri_prefix = 'gs://datawise-biglake-hive-demo-bucket/orders',
  uris = ['gs://datawise-biglake-hive-demo-bucket/orders/*'],
  max_staleness = INTERVAL 1 DAY,
  metadata_cache_mode = 'AUTOMATIC'
);
```

A few things to note:

*   max\_staleness — how old the cache can be before BigQuery goes back to storage. Minimum is 15 minutes
    
*   metadata\_cache\_mode — AUTOMATIC refreshes on its own; MANUAL lets you trigger it via stored procedure, useful for event-driven pipelines
    
*   consider adding require\_partition\_filter to force callers to filter on a partition key and avoid full file scans
    

The table is now created and can be queried like any other BigQuery table.

![BigQuery console screenshot: SELECT \* FROM learning.orders\_biglake returns orders plus partition columns order\_date and country, and the Details tab shows a partitioned Lakehouse table over CSV files at gs://datawise-biglake-hive-demo/orders/\* with Hive partitioning mode CUSTOM.](/images/bigquery-biglake-tables-explained-what-they-are-and-when-to-use-them/7.png)

### **Before you go**

A couple of things worth knowing:

*   an existing classic external table can be upgraded to a BigLake table without recreating it from scratch
    
*   metadata cache refreshes incur processing costs — worth keeping in mind if you're dealing with a large number of files
