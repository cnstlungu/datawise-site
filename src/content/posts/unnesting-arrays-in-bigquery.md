---
title: "UNNESTING ARRAYS in BigQuery"
seoTitle: "How to UNNEST Arrays in BigQuery: A Practical Guide"
seoDescription: "UNNEST in BigQuery expands array columns into individual rows, enabling aggregations and filtering on nested data."
datePublished: 2024-03-30T22:29:05.866Z
dateUpdated: 2026-03-02T15:57:24.935Z
cover: "/images/unnesting-arrays-in-bigquery/cover.jpg"
coverCredit:
  name: "Kelli McClintock"
  url: "https://unsplash.com/@kelli_mcclintock"
series: "bigquery-arrays-and-structs"
hashnodeCuid: "cluenzu8a000208l53m9v5y04"
---

Here's perhaps my favorite feature in BigQuery and another one I discovered when switching from SQL Server. It's one of its most powerful features - the support for ARRAYS.

Although a bit intimidating when seeing them for the first time, they allow for efficient storing and modelling one-to-many relationships, and have deep performance implications.

In other database systems that don't support arrays, you'd have to store them in a separate table or resort to workarounds like storing in list-like strings or JSON.

Working with them is quite straightforward once you get the hang of it. Probably the most common operation to do with them is to UNNEST them.

The ARRAY is basically a set of rows inside one of the columns. In the example below each of the members have a list of activities they're signed up for, together with the date they enrolled.

While we only have 4 members (and consequentially 4 rows) , each member can have 0, 1 or multiple activities they're subscribed to.

If we want to perform operations (say find out what was the earliest enrollment date, or count the distinct activities that the members are enrolled in), we'd need to unpack these rows by UNNESTing the ARRAY where **activities** are stored it.

This will bring us from 1 (table) row per member to 1 row per each activity a member is enrolled in.

Pay attention here to how we're joining the UNNEST - this will determine if we keep or not the members that don't have any activities.

`LEFT JOIN = keep them`  
`CROSS JOIN / , (also a cross join) / INNER JOIN = exclude them`

Do remember to give the UNNESTed items a proper logical name i.e. if you're UNNESTING activities, call it activity for better readability.

![Input data: four members with a nested activities array of name and registered\_on: Jeremy (tennis, basketball), Jane (volleyball, cycling, snooker), Joseph (football, chess) and Joanna with null.](/images/unnesting-arrays-in-bigquery/1-input.jpg)

```sql
SELECT
  member,
  activity.name AS activity_name,
  activity.registered_on AS activity_registered_on

FROM input_data
LEFT JOIN UNNEST(activities) AS activity
```

![BigQuery results: eight rows, one per activity: Jeremy tennis 2023-01-06, Jeremy basketball 2022-11-01, Jane volleyball 2021-01-01, Jane cycling 2022-01-15, Jane snooker 2021-10-01, Joseph football 2022-01-01, Joseph chess 2022-06-01, and Joanna with null activity\_name and activity\_registered\_on.](/images/unnesting-arrays-in-bigquery/1-result.jpg)

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using ARRAY_AGG in BigQuery](/using-array-agg-in-bigquery)
- [Leveraging ARRAYS in BigQuery for query performance](/leveraging-arrays-in-bigquery-for-query-performance)
- [Accessing ARRAY elements in BigQuery](/accessing-array-elements-in-bigquery)
- [Enumerating ARRAY elements in BigQuery using WITH OFFSET](/enumerating-array-elements-in-bigquery-using-with-offset)
- [Flattening JSON arrays in BigQuery](/flattening-json-arrays-in-bigquery)
