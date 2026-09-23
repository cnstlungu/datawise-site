---
title: "Using COUNTIF() in BigQuery"
seoTitle: "COUNTIF in BigQuery: Count Rows Matching a Condition"
seoDescription: "Learn how to use COUNTIF in BigQuery to count rows matching a specific condition, as a cleaner alternative to COUNT combined with CASE WHEN."
datePublished: 2023-12-18T10:33:00.111Z
dateUpdated: 2026-03-02T10:50:48.647Z
cover: "/images/using-countif-in-bigquery/cover.jpg"
coverCredit:
  name: "Crissy Jarvis"
  url: "https://unsplash.com/@crissyjarvis"
series: "practical-sql"
hashnodeCuid: "clqas26z3000s08l37fv21xpw"
---

Happy weekend! Do you remember the good old COUNTIF from Excel?  
When I was just starting out in Analytics and was working with spreadsheets, I would make heavy use of it.

Well, turns out we have something similar in BigQuery as well.

It's an aggregate function, counting only rows that fulfill a given condition, for example `COUNTIF( a > 10 and b = 'text')`

Of course, this would be pretty much the same as combining COUNT + CASE WHEN.

See a quick example below.

![BigQuery SQL using COUNTIF(Salary \> 80000) AS count\_salaries\_over\_80k on learning.Customers with GROUP BY country; the console results show CA 1, IT 0, UK 1 and FR 0.](/images/using-countif-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
