---
title: "Using RANGE_BUCKET in BigQuery"
seoTitle: "BigQuery: Mastering RANGE_BUCKET Usage"
seoDescription: "Learn how to use the RANGE_BUCKET function in BigQuery for effective data distribution and grouping in this concise guide"
datePublished: 2024-09-23T21:03:32.713Z
dateUpdated: 2026-03-02T10:50:23.422Z
cover: "/images/using-rangebucket-in-bigquery/cover.jpg"
coverCredit:
  name: "Wandering Indian"
  url: "https://unsplash.com/@wanderingindian"
series: "practical-sql"
hashnodeCuid: "cm1fhvlgp001a0amigdly7dbt"
---

I've recently had to perform a validation of differences between 2 data sources, so I've figured it would be interesting to see the distribution of absolute differences between the two (how big are they + how often they happen).

I've used RANGE\_BUCKET function in BigQuery SQL. So what does it do?

It takes a value and an array. The value is the one you want to find a bucket for, whereas the array are the buckets intervals you want to group the values in.

Something like value = 1, bucket bounds \[0, 5, 10, 100, 1000\]

This will get you the index of the next larger value in the array, in other words, the index of your group.

A couple of special cases:  
\- if your value is smaller than the first bound, it gets assigned to bucket 0  
\- if it's NULL, the bucket is also NULL

One can of course do the same with a CASE WHEN statement, but this way looks pretty concise. I've combined it with a COUNT / GROUP BY to assess how big where the differences in my analyzed dataset.

Check out a representative example below.

![](/images/using-rangebucket-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
