---
title: "Computing a hash aggregation in BigQuery"
seoTitle: "BigQuery Hash Aggregation Explained"
seoDescription: "Learn to simulate Snowflake's HASH_AGG in BigQuery to check for data changes using existing functions"
datePublished: 2024-10-21T12:33:40.393Z
dateUpdated: 2026-03-02T10:51:04.253Z
cover: "/images/computing-a-hash-aggregation-in-bigquery/cover.jpg"
coverCredit:
  name: "Tomas Sobek"
  url: "https://unsplash.com/@tomas_nz"
series: "practical-sql"
hashnodeCuid: "cm2izzqy1000009mfebxvedm3"
---

So I've seen Snowflake has an HASH\_AGG function. When would we need it?

Every time we'd like to work out if ANY value in a group (or the entire table) has changed in any way, even a single extra blank space.

While BigQuery does not have it yet, we can still simulate it using the tools at hand.

Here's how we can do it:  
\- TO\_JSON\_STRING to create a STRUCT from each entire row (or create a STRUCT containing only the columns you care about)  
\- STRING\_AGG to aggregate all the json strings into a single value per group (or the entire table)  
\- FARM\_FINGERPRINT, a hashing function that will product the same output given only the exact same input, check my comment for more info

![](/images/computing-a-hash-aggregation-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
