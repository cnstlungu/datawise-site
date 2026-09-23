---
title: "Enumerating ARRAY elements in BigQuery using WITH OFFSET"
seoTitle: "BigQuery WITH OFFSET: Get Array Element Index After UNNEST"
seoDescription: "WITH OFFSET pairs each array element with its 0-based index after UNNEST. Use it to preserve order, filter by position, or locate specific elements."
datePublished: 2024-03-31T08:00:26.050Z
dateUpdated: 2026-03-02T15:57:23.308Z
cover: "/images/enumerating-array-elements-in-bigquery-using-with-offset/cover.jpg"
coverCredit:
  name: "Anne Nygård"
  url: "https://unsplash.com/@polarmermaid"
series: "bigquery-arrays-and-structs"
hashnodeCuid: "cluf8ekzm000608l61vvhf85w"
---

In a [previous post](/unnesting-arrays-in-bigquery) we've covered what ARRAYS are in BigQuery, their use cases and how to flatten them with UNNEST.

Quite important to mention, ARRAYS are ordered collections (like lists in Python) - you set up that order when creating it. By UNNESTING them, the order is no longer guaranteed.

In order to retrieve the order in which an element was in an array before UNNESTING (apart from ordering again by something in the array like a timestamp) you can use `WITH OFFSET`, which will yield an additional column, showing the 0-based index of the element in the original array.

```sql
WITH input_data AS (
  SELECT 1 AS customer_id, 100 AS order_id, 'order_created' AS event_type, TIMESTAMP '2021-01-01 10:00:00' AS event_time
  UNION ALL
  SELECT 1 AS customer_id, 100 AS order_id, 'order_paid' AS event_type, '2021-01-01 10:01:05' AS event_time
  UNION ALL
  SELECT 1 AS customer_id, 100 AS order_id, 'order_shipped' AS event_type, '2021-01-01 18:30:00' AS event_time
  UNION ALL
  SELECT 2 AS customer_id, 200 AS order_id, 'order_created' AS event_type, TIMESTAMP '2021-02-01 11:01:00' AS event_time
  UNION ALL
  SELECT 2 AS customer_id, 200 AS order_id, 'order_paid' AS event_type, '2021-02-01 11:01:45' AS event_time
  UNION ALL
  SELECT 2 AS customer_id, 200 AS order_id, 'order_shipped' AS event_type, '2021-02-01 14:35:00' AS event_time
), nested_data AS (
SELECT
  customer_id,
  order_id,
  ARRAY_AGG(event_type ORDER BY event_time) AS status_updates
FROM input_data
GROUP BY customer_id, order_id)

SELECT customer_id, order_id, status_update, offset

FROM nested_data

LEFT JOIN UNNEST(status_updates) AS status_update

WITH OFFSET AS offset
```

![BigQuery results: for customer 1 / order 100 and customer 2 / order 200, status\_update order\_created, order\_paid and order\_shipped with offset 0, 1 and 2.](/images/enumerating-array-elements-in-bigquery-using-with-offset/1-result.jpg)

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using ARRAY_AGG in BigQuery](/using-array-agg-in-bigquery)
- [UNNESTING ARRAYS in BigQuery](/unnesting-arrays-in-bigquery)
- [Leveraging ARRAYS in BigQuery for query performance](/leveraging-arrays-in-bigquery-for-query-performance)
- [Accessing ARRAY elements in BigQuery](/accessing-array-elements-in-bigquery)
- [Flattening JSON arrays in BigQuery](/flattening-json-arrays-in-bigquery)
