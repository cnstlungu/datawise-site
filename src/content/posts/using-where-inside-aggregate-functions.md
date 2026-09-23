---
title: "Using WHERE inside aggregate functions"
subtitle: ""
seoTitle: "BigQuery Aggregate Functions Now Support WHERE"
seoDescription: "Filter the input rows of any BigQuery aggregate with WHERE. What it does, how it compares to HAVING MAX / HAVING MIN, and why it beats CASE WHEN."
datePublished: 2026-09-22T06:52:46.748Z
cover: "/images/using-where-inside-aggregate-functions/cover.jpg"
coverCredit:
  name: "jiteng hermanto"
  url: "https://unsplash.com/@jiteng11"
series: "practical-sql"
tags: ["bigquery", "sql", "data-engineer", "google-cloud"]
hashnodeCuid: "cmucbhi4z00020agmcydwcgd8"
---

I've [previously shared](/another-look-at-anyvalue-in-bigquery) how aggregate functions in BigQuery SQL can pick their rows with HAVING MAX / HAVING MIN.  
  
WHERE is now supported in preview (yes, I'm the tenth person posting it). It filters the input rows, so any aggregate can run on any subset of the data. The difference: HAVING MAX picks the extreme rows of the group; WHERE picks rows by conditions you know beforehand.  
  
Sure, you could solve most of this before with SUM(CASE WHEN ... END), a classic SQL interview question. To me, a WHERE like this is more intuitive and pleasing to the eye. Very BigQuery!

![](/images/using-where-inside-aggregate-functions/1.png)
