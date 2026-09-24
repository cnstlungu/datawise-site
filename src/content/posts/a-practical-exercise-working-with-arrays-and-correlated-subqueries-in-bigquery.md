---
title: "A practical exercise working with ARRAYS and correlated subqueries in BigQuery"
seoTitle: "BigQuery ARRAYS and Correlated Subqueries: Worked Example"
seoDescription: "A practical BigQuery exercise combining ARRAYS, UNNEST, and correlated subqueries to compute per-customer product diversity scores from order history data."
datePublished: 2024-07-06T21:00:29.677Z
dateUpdated: 2026-03-02T10:51:13.028Z
cover: "/images/a-practical-exercise-working-with-arrays-and-correlated-subqueries-in-bigquery/cover.jpg"
coverCredit:
  name: "Devin Berko"
  url: "https://unsplash.com/@devinnn_b"
series: "bigquery-arrays-and-structs"
hashnodeCuid: "clyalzdkd000409jo0q03efvn"
---

Here's an interesting SQL problem, similar to one I had to solve the other day. It involves some of our favourite BigQuery ARRAYS, but also correlated subqueries.

Say we have a table events that represents some events, together with the city and the date they have occurred.

We'd like to look up some meteorological information in a separate table, holding information about weather alerts (type and their duration). We would want to compute a variety of metrics with that.

![Input data: a weather\_alerts table (city\_id, alert\_name, valid\_from, valid\_to) with Heatwave Alert twice and Heavy Snow Alert for city 1, and Heavy Rain Alert, Hale Alert and Strong Wind Alert for city 2; and an events table (city\_id, event\_name, event\_date) with Pop Concert and Football Game in city 1 and Rock Concert and Basketball Game in city 2.](/images/a-practical-exercise-working-with-arrays-and-correlated-subqueries-in-bigquery/1-input.jpg)

```sql
WITH alerts_aggregated AS (

  SELECT city_id, ARRAY_AGG(STRUCT(alert_name, valid_from, valid_to)) AS alerts

  FROM weather_alerts

  GROUP BY city_id
),

compute_event_weather_flags AS (

SELECT

  event_name,
  event_date,

  (
  SELECT

    STRUCT(
      COUNTIF( ABS(DATE_DIFF(event_date, alert.valid_to, DAY)) <= 7 ) AS had_alert_before_or_after,
      COUNTIF(alert.alert_name = 'Heatwave Alert' AND
              alert.valid_to BETWEEN  DATE_SUB(event_date, INTERVAL 7 DAY) AND event_date) > 0 AS had_heatwave_prior,
      COUNT(DISTINCT CASE WHEN alert.valid_to BETWEEN  DATE_SUB(event_date, INTERVAL 365 DAY) AND event_date THEN alert_name END) AS count_alert_type_year_prior
    )
  FROM UNNEST(aa.alerts) AS alert
  ) AS event_weather_flags

FROM events e
FULL OUTER JOIN alerts_aggregated aa USING (city_id)
)

SELECT
  event_name,
  event_date,
  event_weather_flags.had_alert_before_or_after,
  event_weather_flags.had_heatwave_prior,
  event_weather_flags.count_alert_type_year_prior

FROM compute_event_weather_flags
```

![Intermediate result of alerts\_aggregated: one row per city\_id, each with an alerts array of alert\_name, valid\_from and valid\_to (three alerts for city 1, three for city 2).](/images/a-practical-exercise-working-with-arrays-and-correlated-subqueries-in-bigquery/1-result.jpg)

![BigQuery results: Pop Concert (2021-01-01) has had\_alert\_before\_or\_after 2, had\_heatwave\_prior true and count\_alert\_type\_year\_prior 1; Football Game (2021-07-03) 1, false, 2; Rock Concert (2021-01-01) 2, false, 1; Basketball Game (2021-03-03) 1, false, 3.](/images/a-practical-exercise-working-with-arrays-and-correlated-subqueries-in-bigquery/1-result-2.jpg)

Simply joining the two won't cut it - each metric can have a complex calculation logic. Maybe join the weather\_alerts table multiple times? But what if we have 10 different metrics?

Then, there is the problem of the grain. Joining the two solely on the city would multiply the number of event rows by the number of weather alerts in that city.

So how can we calculate weather alert metrics at the event level?

Here's how I would tackle the problem.

Step 1: Aggregate `weather_alerts` with `ARRAY_AGG`. This way, we'll have a single row per city, with all the alerts in an ARRAY we can analyse. This was we can join with the `events` table at the right grain (city).

Step 2: Use a correlated subquery and `UNNEST` the array of weather alerts for each event. We will compute the metrics we care about inside it.

We'd like to compute:  
\- count of alert in the event city in the 7 days prior or the 7 days after the event date  
\- whether a heatwave alert has been issued in the week prior to the event  
\- the number of weather alert types that occured in the rolling year prior to the event

Since the subquery needs to return a scalar (aka one single 'thing'), we wrap it all under a `STRUCT` to get around this limitation.

Step 3: We extract the flags from the above `STRUCT` .

➕ The query is relatively simple, involves a single join, allows for very flexible computations of different attributes using the

➖ Correlated subqueries can lead to performance problems as data volumes increase, given they are executed once per each row.

Are there any other ways you would approach this problem?

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using ARRAY_AGG in BigQuery](/using-array-agg-in-bigquery)
- [UNNESTING ARRAYS in BigQuery](/unnesting-arrays-in-bigquery)
- [Leveraging ARRAYS in BigQuery for query performance](/leveraging-arrays-in-bigquery-for-query-performance)
- [Accessing ARRAY elements in BigQuery](/accessing-array-elements-in-bigquery)
