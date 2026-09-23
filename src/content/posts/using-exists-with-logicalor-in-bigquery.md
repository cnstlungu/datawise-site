---
title: "Using EXISTS with LOGICAL_OR in BigQuery"
seoTitle: "BigQuery: Working with EXISTS and LOGICAL_OR"
seoDescription: "Learn to use EXISTS with LOGICAL_OR in BigQuery for efficient flag checks across orders in SQL"
datePublished: 2025-02-08T14:03:04.685Z
dateUpdated: 2026-03-02T10:51:46.926Z
cover: "/images/using-exists-with-logicalor-in-bigquery/cover.jpg"
coverCredit:
  name: "Tekton"
  url: "https://unsplash.com/@tekton_tools"
series: "practical-sql"
hashnodeCuid: "cm6w9mfe5000009joacu13dga"
---

Long time, no see! Here's a quick SQL exercise that illustrates some important modern concepts.

So, we're given a list of updates per each order, and at each point in time we have some flags. Our goal here is to check for each order if there was any point in time when any of the flags had the value of 1.

![BigQuery SQL where input\_data holds per-order updates with an indicators ARRAY; a compute\_flags CTE uses EXISTS(SELECT indicator FROM UNNEST(indicators) WHERE indicator = 1), then LOGICAL\_OR(flag\_was\_true) with GROUP BY order\_id; results show order 1 true, order 2 false.](/images/using-exists-with-logicalor-in-bigquery/1.jpg)

We solve this by:

➡️ UNNEST the ARRAY where the indicators are stored, doing so in an inline select. Yes, you can use WHERE to filter the output of FROM UNNEST().  
➡️ leverage EXISTS to only check the existence of such an entry (we don't want to retrieve it), resulting in a TRUE/FALSE result  
➡️ use LOGICAL\_OR aggregation function, grouped by order\_id, to check if there is at least one entry where the flag from the previous step was true for that grain.

Happy querying!

*Found it useful? Subscribe to my Analytics newsletter at* [https://www.notjustsql.com](https://www.notjustsql.com/) *.*
