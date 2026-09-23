---
title: "A closer look at STRING_AGG in BigQuery"
seoTitle: "Exploring STRING_AGG Function in BigQuery"
seoDescription: "Discover how to use BigQuery's STRING_AGG function to concat grouped values with custom separators and ordering"
datePublished: 2025-02-08T14:18:55.802Z
dateUpdated: 2026-03-02T10:50:37.353Z
cover: "/images/a-closer-look-at-stringagg-in-bigquery/cover.jpg"
coverCredit:
  name: "Kelly Sikkema"
  url: "https://unsplash.com/@kellysikkema"
series: "practical-sql"
hashnodeCuid: "cm6wa6ta2000k08l83bbpaib4"
---

Modern SQL engines have a wealth of aggregation functions.

Here's a quick example that makes use ofBigQuery STRING\_AGG.

What does it do?

It aggregates all the values in a grouping, joined by a separator of our choice, creating a string of those joined values.

We can of course choose to:

➡️ keep only distinct values, as well as  
➡️ order the values in the newly created string

so that, as in the below example, ("Card", "Cash") and ("Cash", "Card") both produce "Card~Cash", every time.

Any interesting aggregation function that you use in your SQL dialect?

![](/images/a-closer-look-at-stringagg-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [***notjustsql.com***](https://www.notjustsql.com/)*.*
