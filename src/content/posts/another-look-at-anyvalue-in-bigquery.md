---
title: "Another look at ANY_VALUE in BigQuery"
seoTitle: "BigQuery ANY_VALUE with HAVING MAX: Pick a Row Without a Subquery"
seoDescription: "Use ANY_VALUE with HAVING MAX or MIN in BigQuery to select a row by a criterion without writing a subquery. Includes practical examples and caveats."
datePublished: 2024-10-20T06:18:23.196Z
dateUpdated: 2026-04-28T08:37:10.590Z
cover: "/images/another-look-at-anyvalue-in-bigquery/cover.jpg"
coverCredit:
  name: "Aakash Dhage"
  url: "https://unsplash.com/@aakashdhage"
series: "practical-sql"
hashnodeCuid: "cm2h759wc000109l56engd67h"
---

A reminder that ANY\_VALUE is a pretty interesting aggregation function in BigQuery SQL.

It gives you a chosen row from a group. Chosen doesn't mean random, but non-deterministic.

Together with HAVING MAX | MIN you can actually control what rows get picked.

While ANY\_VALUE works both with GROUP BY and as a window function OVER (PARTITION BY...), the window variety does not yet support HAVING MIN MAX.

Otherwise, when do I use it? A couple of cases, and it's not only for the thrill of getting an item by chance from the group:  
\- line events also contain header info, so say we need to extract order header data from orderline data  
\- aggregation after pseudo-pivoting with CASE WHEN value = x, same as we used to do with MIN or MAX before  
\- other aggregations of string values based on a rule

![BigQuery SQL using ANY\_VALUE(product\_id HAVING MAX price), ANY\_VALUE(product\_id HAVING MIN is\_banana) and ANY\_VALUE(product\_id HAVING MIN best\_before\_date) with GROUP BY order\_id; order 1 returns Mango, Mango and Banana, order 2 returns Pears for all three.](/images/another-look-at-anyvalue-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
