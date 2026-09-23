---
title: "BigQuery Primary Key & Foreign Key constraints"
seoTitle: "BigQuery Primary & Foreign Key: Do They Help Performance?"
seoDescription: "BigQuery's unenforced primary and foreign key constraints are not just metadata — this post tests their actual impact on join optimization with real query..."
datePublished: 2023-09-16T13:46:35.479Z
dateUpdated: 2026-04-05T20:11:17.868Z
cover: "/images/bigquery-primary-key-foreign-key-constraints/cover.jpg"
coverCredit:
  name: "Florian Berger"
  url: "https://unsplash.com/@bergerteam"
series: "practical-sql"
hashnodeCuid: "clmm30xg7000408mj4dot9ber"
---

Recently, BigQuery introduced Primary Key and Foreign Key constraints. However, they differ from what we're accustomed to in traditional RDBMS. For instance, these constraints aren't currently enforced, and they can only be set between tables within the same dataset. This means you can insert a *customer\_id* that doesn't match any in the customer table, even with a foreign key in place.

Since this felt somewhat watered down, I initially thought they'd serve mainly for metadata purposes. For example, defining a key's reference to values from a certain dimension or establishing the granularity of a table.

However, after some research, I found a [blog post](https://cloud.google.com/blog/products/data-analytics/join-optimizations-with-bigquery-primary-and-foreign-keys) that shed light on how these constraints can enhance join optimizations in BigQuery. Contrary to my initial belief, they're not just for documentation.

I decided to test this. Using a data\_source table (~400k rows) partitioned by date and clustered by id, I needed to look up a unique identifier from another table.

![BigQuery console Preview tabs of two tables side by side: lookup\_table with columns id and unique\_identifier (UUID strings) and data\_source with columns id, value and ds\_date, in the sample rows every id is 1.](/images/bigquery-primary-key-foreign-key-constraints/1.jpg)

```python
ALTER TABLE testing.lookup_table ADD PRIMARY KEY (id) NOT ENFORCED;
ALTER TABLE testing.data_source ADD PRIMARY KEY (id, ds_date) NOT ENFORCED,
ADD FOREIGN KEY(id) references testing.lookup_table(id) NOT ENFORCED;
```

![BigQuery console Schema tabs side by side: data\_source has id INTEGER keyed PK/FK, value INTEGER and ds\_date DATE keyed PK, while lookup\_table has id INTEGER keyed PK and unique\_identifier STRING, all NULLABLE.](/images/bigquery-primary-key-foreign-key-constraints/2.jpg)

I compared query results from two tables without constraints (learning dataset) to their replicas with constraints (testing dataset), ensuring cached results were disabled.

```sql
-- WITH CONSTRAINTS

SELECT id, MAX(ds_date), MIN(ds_date)

FROM testing.data_source d
JOIN testing.lookup_table l USING (id)


GROUP BY id
```

```sql
-- WITHOUT CONSTRAINTS

SELECT id, MAX(ds_date), MIN(ds_date)

FROM learning.data_source d
JOIN learning.lookup_table l USING (id)


GROUP BY id
```

![Execution details side by side: with constraints (left) elapsed time 212 ms, slot time consumed 91 ms, bytes shuffled 3.55 KB and 0 B spilled to disk; without constraints (right) 2 sec, 18 min 9 sec, 7.19 MB and 0 B.](/images/bigquery-primary-key-foreign-key-constraints/3-result.jpg)

From my tests, the queries using tables with constraints showed a significant efficiency boost. While they're not a one-size-fits-all solution, it's evident that Primary and Foreign Key constraints can influence performance (as showcased in the aforementioned article).

I'm optimistic about these functionalities expanding and their restrictions easing in the future.

Thanks for reading!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Cross-dataset foreign key relationships in BigQuery](/cross-dataset-foreign-key-relationships-in-bigquery)
