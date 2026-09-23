---
title: "Approximate Aggregate Functions in BigQuery"
seoTitle: "Approximate Aggregate Functions in BigQuery Explained"
seoDescription: "Learn when and how to use APPROX_COUNT_DISTINCT and APPROX_TOP_COUNT in BigQuery to reduce compute cost for exploratory queries on large datasets."
datePublished: 2023-12-14T08:32:46.171Z
dateUpdated: 2026-03-02T10:51:27.867Z
cover: "/images/approximate-aggregate-functions-in-bigquery/cover.jpg"
coverCredit:
  name: "gretta vosper"
  url: "https://unsplash.com/@grettav"
series: "practical-sql"
hashnodeCuid: "clq4y05zu000m08l04gal7q1p"
---

Sometimes you don't need perfect, but just good enough. Take approximate aggregate functions in BigQuery, for example.

These are a type of aggregate functions that produce approximate results instead of exact ones but have the upside of typically requiring fewer resources for the computation.

When would I use one? This would be suitable where we can live with an uncertainty or small difference, especially for huge tables, during a preliminary check or data exploration.

Let's look at a practical example. Suppose we have the following data:

![BigQuery console preview of the sample data for approximate aggregates, with columns id, value and ds\_date; the first 10 rows are all dated 2020-12-18 and have single-digit values such as 1, 8, 6, 4 and 0.](/images/approximate-aggregate-functions-in-bigquery/1.png)

`APPROX_TOP_COUNT` will compute the approx top N elements and their value counts

```sql
SELECT 
    APPROX_TOP_COUNT(value, 5) AS top_value_counts 
FROM `learning.data_source`
```

![BigQuery console result of APPROX\_TOP\_COUNT(value, 5): one row holding an array of value and count pairs, 4 with 40258, 0 with 40057, 5 with 40051, 3 with 39979 and 9 with 39944.](/images/approximate-aggregate-functions-in-bigquery/2.png)

`APPROX_COUNT_DISTINCT` will compute the approx distinct count (also can be grouped)

```sql
SELECT 
    APPROX_COUNT_DISTINCT(value) AS approx_distinct_value_count 
FROM `learning.data_source`
```

![BigQuery console result of APPROX\_COUNT\_DISTINCT(value): a single row in the approx\_distinct\_value\_count column, header truncated, with the value 11.](/images/approximate-aggregate-functions-in-bigquery/3.png)

You can discover more approximate aggregate functions in the [documentation](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions).

Thanks for reading!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Why partitioning tables is not a silver bullet for BigQuery performance](/why-partitioning-tables-is-not-a-silver-bullet-for-bigquery-performance)
- [Why you should care about partition pruning in BigQuery](/why-you-should-care-about-partition-pruning-in-bigquery)
- [Optimizing SQL queries in BigQuery](/optimizing-sql-queries-in-bigquery)
- [Optimizing compute cost in BigQuery](/optimizing-compute-cost-in-bigquery)
