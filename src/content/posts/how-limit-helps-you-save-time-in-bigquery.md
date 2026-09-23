---
title: "How LIMIT helps you save time in BigQuery"
seoTitle: "BigQuery LIMIT: When It Saves Time But Not Cost"
seoDescription: "LIMIT in BigQuery reduces query execution time during data validation even though it doesn't reduce bytes billed."
datePublished: 2024-06-05T21:03:41.131Z
dateUpdated: 2026-03-02T10:51:18.714Z
cover: "/images/how-limit-helps-you-save-time-in-bigquery/cover.jpg"
coverCredit:
  name: "Joshua Hoehne"
  url: "https://unsplash.com/@joshua_hoehne"
series: "practical-sql"
hashnodeCuid: "clx2bg2mj00030alee4ek8r27"
---

Here's a basic thing that can save you a bit of time when analyzing data or validating data transformations.

So I've [previously posted](/table-sampling-in-bigquery) about how in BigQuery using LIMIT for query output does not yield any cost saving as it has no effect on amount on data being processed - just how many results are returned to you.

But there are still cases where I use LIMIT.

```sql
SELECT
    order_id,
    COUNT(1) AS times_seen
FROM input_data

GROUP BY order_id

HAVING COUNT(1) > 1

LIMIT 10;
```

![BigQuery results: one row, order\_id 1 with times\_seen 2.](/images/how-limit-helps-you-save-time-in-bigquery/1-result.jpg)

Say I'm validating some data and I want to check an assumption I have about the data. For instance, knowing that even a few duplicate records exist indicates me that the problem exists and provides an example to investigate.

I do not need to know all the possible duplicates in the table, therefore I use LIMIT to get at least one observation that will contradict what I'm expecting.

And even with LIMIT, if I don't get anything back, it means that the query hasn't found any matching rows which validates my initial hypothesis.

On a big enough table, one could notice the query execution time difference between using LIMIT and not using it. Again, there is no cost difference, but your time also costs 😁.

P.S. This is not to say that LIMIT is completely irrelevant to performance in BigQuery. Check out [this post](/de-duplicating-with-rownumber-vs-arrayagg) for a case where LIMIT does make a difference!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Why partitioning tables is not a silver bullet for BigQuery performance](/why-partitioning-tables-is-not-a-silver-bullet-for-bigquery-performance)
- [Why you should care about partition pruning in BigQuery](/why-you-should-care-about-partition-pruning-in-bigquery)
- [Optimizing SQL queries in BigQuery](/optimizing-sql-queries-in-bigquery)
- [Optimizing compute cost in BigQuery](/optimizing-compute-cost-in-bigquery)
