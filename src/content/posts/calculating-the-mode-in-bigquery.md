---
title: "Calculating the MODE in BigQuery"
seoTitle: "Calculate MODE in BigQuery Without a Built-in Function"
seoDescription: "No native MODE() in BigQuery. Compute the most frequent value with COUNT, GROUP BY, and QUALIFY. Covers ties, multiple modes, and window function approaches."
datePublished: 2024-02-21T22:15:27.754Z
dateUpdated: 2026-03-02T10:22:31.120Z
cover: "/images/calculating-the-mode-in-bigquery/cover.jpg"
coverCredit:
  name: "Chris Liverani"
  url: "https://unsplash.com/@chrisliverani"
series: "practical-sql"
hashnodeCuid: "clswcrxmy000008l801rbgyb5"
---

How do you compute the MODE (most frequent value) in BigQuery?

For the other measures of central tendency like MEAN and MEDIAN, there are straightforward ways to compute results - functions AVG and PERCENTILE\_CONT/PERCENTILE\_DIST respectively, but there's no dedicated function for MODE.

By the way, if you have a huge dataset and can bear some lack of precision, take a look at APPROX\_TOP\_COUNT.

Say we have the following input data:

![](/images/calculating-the-mode-in-bigquery/1.png)

Now here's how we can compute them otherwise:  
\- filter out NULLS (if we want to ignore them) or do nothing if we want to keep them  
\- compute value counts for our desired grain  
\- take the most frequent one per our grain using QUALIFY + RANK

![](/images/calculating-the-mode-in-bigquery/2.png)

Here's how the output would look with NULLS excluded.

![](/images/calculating-the-mode-in-bigquery/3.png)

And with them included:

![](/images/calculating-the-mode-in-bigquery/4.png)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
