---
title: "Optimizing storage costs in BigQuery"
seoTitle: "Reduce BigQuery Storage Costs: Practical Tips for FinOps"
seoDescription: "Covers actionable strategies to lower BigQuery storage costs including logical vs physical billing, long-term storage tiers, table clones, expiration..."
datePublished: 2023-12-22T23:53:23.896Z
dateUpdated: 2026-03-02T10:51:19.990Z
cover: "/images/optimizing-storage-costs-in-bigquery/cover.jpg"
coverCredit:
  name: "Josh Appel"
  url: "https://unsplash.com/@joshappel"
series: "bigquery-performance"
hashnodeCuid: "clqhaex14000008jrcxjbeax5"
---

As promised on a previous post about [optimizing costs for compute](/optimizing-compute-cost-in-bigquery), I've promised a post about storage as well, so let's dive in.

So how does BigQuery charge for storage?

Two billing models - set at dataset level: logical and physical.

Logical table size is the default option, representing uncompressed size. It is cheaper per Gib (roughly half of physical) and you get time travel storage for free.

Physical storage represents compressed, actual size of physical bytes stored on disk. It's twice as expensive as logical and you need to pay for the time travel storage as well BUT if you have data that compresses well (for example by using arrays), you might be able to save storage costs.

Now, we can further split these down into:  
\- active storage: any table or partition (for partitioned tables) modified in the last 90 days  
\- long-term storage: a table or partition (for partitioned tables) that hasn't changed in the last 90 days, and is 50% cheaper than the active storage.

Here's what you can do to help bring these costs down:

\- Identify what is taking up storage space: Look at information schema views such as INFORMATION\_SCHEMA.TABLE\_STORAGE to find out what is taking up the space that you pay for.

\- Cleanup: Clean up unneeded data or archive in cheap long-term storage. Think about storing aggregated version of historical data and save on storage.

\- Leverage table clones and snapshots in BigQuery to save on storing redundant data

\- Shorten time travel window (which is 7 days by default) - if you would not need to restore this data or not for the entire 7 days, you can reduce this (dataset level) and store less data. A staging table that is recreated every time, for example, might not need the 7 days. Read more in the [post about BigQuery time travel](/using-bigquery-time-travel).

\- Leverage long-term vs short-term data: any table or partition that you don't modify for 90 days becomes 50% cheaper to store, so maybe don't rebuild massive historical tables every time you run the process.

\- Use the table and partition expiration settings: you can set particular tables or partitions to expire after a given time, so you don't store data that you don't need

Hope these tips are useful!

![BigQuery console Storage info panel for a table with 399,803 rows and 4,000 partitions: 9.15 MB total logical bytes, 9.08 MB of it long-term, versus 6.42 MB total physical bytes, 6.37 MB of it long-term, and 0 B time travel.](/images/optimizing-storage-costs-in-bigquery/1.jpg)

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Why partitioning tables is not a silver bullet for BigQuery performance](/why-partitioning-tables-is-not-a-silver-bullet-for-bigquery-performance)
- [Why you should care about partition pruning in BigQuery](/why-you-should-care-about-partition-pruning-in-bigquery)
- [Optimizing SQL queries in BigQuery](/optimizing-sql-queries-in-bigquery)
- [Optimizing compute cost in BigQuery](/optimizing-compute-cost-in-bigquery)
