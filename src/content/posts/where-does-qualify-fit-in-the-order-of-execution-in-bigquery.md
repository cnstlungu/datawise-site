---
title: "Where does QUALIFY fit in the order of execution in BigQuery?"
seoTitle: "QUALIFY Clause: SQL Execution Order in BigQuery Explained"
seoDescription: "QUALIFY filters rows based on window function results in BigQuery, running after HAVING. Use it to deduplicate rows or keep only the latest record per group."
datePublished: 2024-05-07T13:35:13.732Z
dateUpdated: 2026-03-02T10:22:46.823Z
cover: "/images/where-does-qualify-fit-in-the-order-of-execution-in-bigquery/cover.jpg"
coverCredit:
  name: "Markus Spiske"
  url: "https://unsplash.com/@markusspiske"
series: "practical-sql"
hashnodeCuid: "clvwfnnes000k09jthan62zys"
---

Here's an example of how QUALIFY fits into the order of execution in SQL.  
  
In the BigQuery example below, we want to compute the second-to-last `order_updated` event for each order.  
  
To do this, we filter to keep only the rows WHERE order\_status = 'order\_updated'.  
  
We use there rows then to retrieve the event occurring second - sorting decreasingly by event\_ts and partitioning by order\_id, using QUALIFY.  
  
The output is then ORDER BY the second\_to\_last\_order\_update\_ts decreasingly.

![BigQuery SQL on order events (order\_id, event\_ts, order\_status) that filters WHERE order\_status = 'order\_updated' and then QUALIFY ROW\_NUMBER() OVER(PARTITION BY order\_id ORDER BY event\_ts DESC) = 2; results give order 2 at 13:15 and order 1 at 11:30, the highlighted second-to-last updates.](/images/where-does-qualify-fit-in-the-order-of-execution-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
