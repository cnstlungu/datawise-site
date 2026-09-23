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

![](/images/a-practical-exercise-working-with-arrays-and-correlated-subqueries-in-bigquery/1.jpg)

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

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using ARRAY_AGG in BigQuery](/using-array-agg-in-bigquery)
- [UNNESTING ARRAYS in BigQuery](/unnesting-arrays-in-bigquery)
- [Leveraging ARRAYS in BigQuery for query performance](/leveraging-arrays-in-bigquery-for-query-performance)
- [Accessing ARRAY elements in BigQuery](/accessing-array-elements-in-bigquery)
