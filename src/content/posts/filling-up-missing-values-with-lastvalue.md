---
title: "Filling up missing values with LAST_VALUE"
seoTitle: "Fill Missing Values in BigQuery with LAST_VALUE IGNORE NULLS"
seoDescription: "Learn how to forward-fill missing sensor readings in BigQuery using LAST_VALUE with IGNORE NULLS and an unbounded window frame."
datePublished: 2023-12-03T16:35:13.788Z
dateUpdated: 2026-03-02T15:57:29.362Z
cover: "/images/filling-up-missing-values-with-lastvalue/cover.jpg"
coverCredit:
  name: "Pierre Bamin"
  url: "https://unsplash.com/@bamin"
series: "bigquery-window-functions"
hashnodeCuid: "clpppe8sc000809jw9jrven3d"
---

Window functions are powerful. But they can also help us fill in missing data in BigQuery.

Let's say you have a sensor that records temperature and humidity. Unfortunately, it is quite unreliable, so sometimes it might not send one or both readings. You'd like to retain the last known reading for a measurement.

![](/images/filling-up-missing-values-with-lastvalue/1.png)

Here's how we can solve it:

\- Leverage the LAST\_VALUE window function.  
\- Specify the IGNORE NULLS clause  
\- Partition by `sensor_id` so only we consider data from the same sensor  
\- Order the window by the timestamp column  
\- Define a ROWS condition to consider rows from the beginning of time up to and including the current row - this way, if we do have a current reading for this timestamp, we keep it.

Here's how it would look in SQL:

```sql
  SELECT


  sensor_id,
  temperature,
  humidity_percentage,
  at_timestamp,

  LAST_VALUE(temperature IGNORE NULLS) OVER (PARTITION BY sensor_id ORDER BY at_timestamp ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS tr_temperature,

  LAST_VALUE(humidity_percentage IGNORE NULLS) OVER (PARTITION BY sensor_id ORDER BY at_timestamp ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS tr_humidity,

FROM input_data

ORDER BY at_timestamp
```

![](/images/filling-up-missing-values-with-lastvalue/2.png)

Previously, I've written [another blog post solving a similar problem](/practical-bigquery-filling-in-missing-data) by leveraging `NTH_VALUE` .

P.S. This would not work if you're trying to fill in a STRUCT for example. IGNORE NULLS does not regard STRUCT(NULL AS a, NULL AS b) the same as NULL, so you might need to unpack the STRUCT.

Happy querying!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using LAST_VALUE with STRUCTS](/using-lastvalue-with-structs)
