---
title: "Optimizing compute cost in BigQuery"
seoTitle: "BigQuery Compute Cost: On-Demand vs Capacity-Based Billing"
seoDescription: "Explains the difference between on-demand and capacity-based BigQuery compute billing and how to optimize for each."
datePublished: 2023-12-21T15:56:29.646Z
dateUpdated: 2026-03-02T10:51:59.202Z
cover: "/images/optimizing-compute-cost-in-bigquery/cover.jpg"
coverCredit:
  name: "Jason Leung"
  url: "https://unsplash.com/@ninjason"
series: "bigquery-performance"
hashnodeCuid: "clqfdxrgt000108ju7qne4nq6"
---

Let's talk money 💸 . Now that I've got your attention - more precisely, cost optimization as a regular user. As cloud data warehouse users, in addition to ticking off functional requirements and of course, getting the results in a timely manner, we care also about the costs.

BigQuery costs can be split into compute (what you process) and storage (what you store). Let's look at compute (I promise a post about storage, too).

So it's important to know that BigQuery has two billing models for compute: on-demand and capacity-based.

On-demand is pretty straightforward - you pay per amount of data scanned, say 7.5 $ per TB, depending on region. Imagine paying your 🍧 ice-cream by weight.

Capacity-based means your company has purchased a processing capacity, measured in slots, over a unit of time. Here you pay the reservation and not the amount of data you scan. Imagine paying your ice-cream per recipient that you fill. As long as it fits in, regardless of weight, you pay the fixed amount.

So how does optimizing for compute look like for a regular user? When trying out different approaches (especially for working with very big datasets):  
\- If your company is billed on-demand basis, aim for processing less data (see the top-right corner info BEFORE running the query). This means you will get billed less.  
\- If your company has capacity-based billing, aim for a lower slot time consumed (see execution details AFTER you've ran your query). This will ensure there is enough capacity for other workloads in your organization.

Now, they typically correlate, but there might be cases where you pick between a lower slot time or a lower amount of data processed.

![BigQuery console running a QUALIFY ROW\_NUMBER() query on bigquery-public-data.google\_trends.top\_terms for Los Angeles CA, with two metrics highlighted: the estimate of 81.57 MB to be processed and 8 sec of slot time consumed under Execution details.](/images/optimizing-compute-cost-in-bigquery/1.png)

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Why partitioning tables is not a silver bullet for BigQuery performance](/why-partitioning-tables-is-not-a-silver-bullet-for-bigquery-performance)
- [Why you should care about partition pruning in BigQuery](/why-you-should-care-about-partition-pruning-in-bigquery)
- [Optimizing SQL queries in BigQuery](/optimizing-sql-queries-in-bigquery)
- [Optimizing storage costs in BigQuery](/optimizing-storage-costs-in-bigquery)
