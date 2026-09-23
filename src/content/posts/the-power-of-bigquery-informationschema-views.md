---
title: "The power of BigQuery INFORMATION_SCHEMA views"
seoTitle: "BigQuery INFORMATION_SCHEMA: 12 Useful Queries for Tables, Jobs, and Storage"
seoDescription: "Ready-to-run INFORMATION_SCHEMA queries for BigQuery tables, jobs, partitions, and storage costs. Practical examples you can copy and adapt."
datePublished: 2023-09-25T21:33:09.386Z
dateUpdated: 2026-04-28T08:33:42.053Z
cover: "/images/the-power-of-bigquery-informationschema-views/cover.jpg"
coverCredit:
  name: "Ryunosuke Kikuno"
  url: "https://unsplash.com/@ryunosuke_kikuno"
series: "practical-sql"
hashnodeCuid: "clmzenloq000008l69o4m0feh"
---

In one of the [previous posts about BigQuery labels](/using-labels-in-bigquery), I provided an example showcasing the usage of the INFORMATION\_SCHEMA JOBS view when analyzing query statistics per label.

Now what are these views? These are system-generated views that provide metadata about your datasets, tables, columns, jobs, partitions, constraints and more.

Just wanted to highlight that INFORMATION\_SCHEMA view (JOBS included) can do much, much more than that.

Look into your table storage costs, query resource consumption, build dynamic queries, and leverage partition metadata for incremental pipelines - all of this can benefit from the INFORMATION\_SCHEMA views.

Let's look at a couple of interesting use cases.

## JOBS

JOBS is one of the most powerful views when you’re interested in the queries run in that project. It can provide information about:

* slot time used
    
* runtime
    
* bytes processed and billed
    
* referenced tables
    
* errors if any and so much more!
    

```sql
SELECT 

creation_time, 
job_type, 
query, 
total_bytes_billed, 
total_bytes_processed, 
total_slot_ms, 
referenced_table.table_id AS referenced_table_name

FROM `region-eu`.INFORMATION_SCHEMA.JOBS,
UNNEST(referenced_tables) AS referenced_table
```

![](/images/the-power-of-bigquery-informationschema-views/1.png)

## **COLUMNS**

This view contains information about columns, such as:

* tables where they reside
    
* data types
    
* whether they are nullable or not
    
* default values if any
    

Need a dynamic UNPIVOT? Fetch the column names dynamically using this view.

```sql
DECLARE myunpivot STRING;
SET myunpivot = (
  SELECT CONCAT('(', STRING_AGG( column_name, ','), ')'),
From(
SELECT column_name FROM learning.INFORMATION_SCHEMA.COLUMNS
where table_name ="Customer_Data" 
and column_name not in("CustomerId")  ));

EXECUTE IMMEDIATE format("""
SELECT * FROM
(
  SELECT * FROM learning.Customer_Data
)
unpivot
(
  value 
  FOR keys in %s
)
""", myunpivot);
```

FROM:

![](/images/the-power-of-bigquery-informationschema-views/2.png)

TO:

![](/images/the-power-of-bigquery-informationschema-views/3.png)

## CONSTRAINT COLUMN USAGE

If you’re interested in column usage in constraints (newly added BigQuery feature), there is this dataset-level view, showcasing which constraints are applied to columns.

```sql
SELECT * EXCEPT(table_catalog, constraint_catalog) 

FROM testing.INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE;
```

![](/images/the-power-of-bigquery-informationschema-views/4.png)

## TABLE STORAGE

Looking to dive into table storage, including physical and logical storage, so you can estimate your costs? Use one of the table storage views (per project or region, as below).

```sql
SELECT * FROM region-eu.INFORMATION_SCHEMA.TABLE_STORAGE;
```

![](/images/the-power-of-bigquery-informationschema-views/5.png)

## But there's more!

* Building an incremental pipeline and you’d like information about the last time a Partition has been modified? There’s the PARTITIONS view.
    
* Looking to find object access grants? There’s OBJECT\_PRIVILEGES
    
* Want to see a list of Table Snapshots? There is a view for that too.
    
* Be sure to check the [BigQuery documentation](https://cloud.google.com/bigquery/docs/information-schema-table-storage) for the latest list of INFORMATION SCHEMA views you can use
    

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
