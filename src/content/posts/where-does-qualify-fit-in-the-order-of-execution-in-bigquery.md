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

![Input data: order events with order\_id, event\_ts and order\_status for orders 1 and 2 on 2021-01-01; the order\_updated rows are boxed and the second-to-last update of each order (11:30 for order 1, 13:15 for order 2) is highlighted.](/images/where-does-qualify-fit-in-the-order-of-execution-in-bigquery/1-input.jpg)

```sql
SELECT
  order_id,
  event_ts AS second_to_last_order_update_ts,
  order_status

FROM input_data

WHERE order_status = 'order_updated'

QUALIFY ROW_NUMBER() OVER(PARTITION BY order_id ORDER BY event_ts DESC) = 2

ORDER BY second_to_last_order_update_ts DESC
```

![BigQuery results: order 2 with second\_to\_last\_order\_update\_ts 2021-01-01 13:15:00 UTC and order 1 with 2021-01-01 11:30:00 UTC, both order\_updated.](/images/where-does-qualify-fit-in-the-order-of-execution-in-bigquery/1-result.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
