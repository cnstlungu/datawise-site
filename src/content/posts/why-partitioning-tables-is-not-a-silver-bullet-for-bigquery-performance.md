---
title: "Why partitioning tables is not a silver bullet for BigQuery performance"
seoTitle: "BigQuery Partitioning vs Clustering: When Each Helps"
seoDescription: "Partitioning helps only when queries filter on the partition column. Learn when clustering outperforms partitioning and when both strategies make sense."
datePublished: 2024-10-15T10:35:28.425Z
dateUpdated: 2026-03-02T10:22:42.383Z
cover: "/images/why-partitioning-tables-is-not-a-silver-bullet-for-bigquery-performance/cover.jpg"
coverCredit:
  name: "Raymond Rasmusson"
  url: "https://unsplash.com/@raymondrasmusson"
series: "bigquery-performance"
hashnodeCuid: "cm2ab4mqx000b09l63g6hhatl"
---

I recently encountered an interesting case that reminded me of a couple of things and taught me a few lessons.

When working with BigQuery tables, partitioning and clustering are often go-to operations. Typically, we would partition by a meaningful date (which helps with joins and watermarking in incremental loads) and cluster by columns that form part of the grain, common filters or are commonly used in joins (or within MERGE statements).

While working on a recent task, I had a hypothesis that didn’t quite pan out as expected. Here’s the scenario:

Let's say have two tables:  
\- orders\_per\_store, containing fields like order\_id, order\_date, and store\_id.  
\- order\_amounts\_unpartitioned, which holds order amounts but is unpartitioned and clustered only on order\_id. It doesn’t have any date field.

Since order\_id is a unique identifier, it's sufficient for joining. However, I hypothesized that transforming the order\_amounts\_unpartitioned table to a partitioned one using order\_date could improve performance. The idea was to leverage the same order\_date field for partitioning in both tables to optimize the join.

To test this, I ran an experiment in my sandbox project with ~5M orders. The results surprised me.

Results:  
\- The join with the original unpartitioned table (order\_amounts\_unpartitioned), clustered by order\_id, actually performed best in terms of cost and efficiency when joined on just order\_id.  
\- Contrary to my assumption, the option I thought would be more efficient—joining by both order\_date (the partitioning field) and order\_id—was significantly more costly.  
\- Lastly, joining with the partitioned table but using only order\_id — proved to be least efficient.

Key Takeaway: This served as a great reminder: clustering alone is often enough (and the best solution) to optimize query performance, especially when partitioning results in small partitions (the docs recommend at least 10 GB per partition!).

Partitioning by default isn’t always the best approach—particularly for smaller tables— so consider clustering carefully, including the order of clustered fields.

Ultimately, this reinforced the importance of validating assumptions through real-world testing.

The resource consumption varied significantly across runs (so avoid thinking in terms of precise percentages), but the relative performance rankings remained consistent. It should be also noted that these results might be different based on the querying patterns and needs.

![Schemas of the three tables: order\_amounts\_unpartitioned (order\_id, order\_amount; clustered by order\_id), orders\_per\_store (order\_id, order\_date, store\_id; partitioned on order\_date, clustered by order\_id) and order\_amounts (order\_id, order\_date, order\_amount; partitioned on order\_date, clustered by order\_id).](/images/why-partitioning-tables-is-not-a-silver-bullet-for-bigquery-performance/1-schema.png)

```sql
SELECT *
FROM `learning.orders_per_store` s
JOIN `learning.order_amounts_unpartitioned` a
USING (order_id)
```

```sql
SELECT *
FROM `learning.orders_per_store` s
JOIN `learning.order_amounts` a
USING (order_date, order_id)
```

```sql
SELECT *
FROM `learning.orders_per_store` s
JOIN `learning.order_amounts` a
USING (order_id)
```

![Execution details, left to right for the three queries: 7 sec elapsed and 10 min 13 sec slot time (unpartitioned order\_amounts\_unpartitioned), 7 sec and 27 min 13 sec (order\_amounts USING order\_date, order\_id), 9 sec and 41 min 47 sec (order\_amounts USING order\_id).](/images/why-partitioning-tables-is-not-a-silver-bullet-for-bigquery-performance/1-result.png)

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Why you should care about partition pruning in BigQuery](/why-you-should-care-about-partition-pruning-in-bigquery)
- [Optimizing SQL queries in BigQuery](/optimizing-sql-queries-in-bigquery)
- [Optimizing compute cost in BigQuery](/optimizing-compute-cost-in-bigquery)
- [Optimizing storage costs in BigQuery](/optimizing-storage-costs-in-bigquery)
