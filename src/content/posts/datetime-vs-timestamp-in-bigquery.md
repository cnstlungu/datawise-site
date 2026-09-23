---
title: "DATETIME vs TIMESTAMP in BigQuery"
seoTitle: "BigQuery DATETIME vs TIMESTAMP: Key Differences"
seoDescription: "Clarifies the critical difference between DATETIME and TIMESTAMP types in BigQuery and why mixing them causes errors."
datePublished: 2024-01-16T10:58:21.710Z
dateUpdated: 2026-03-02T10:51:15.414Z
cover: "/images/datetime-vs-timestamp-in-bigquery/cover.jpg"
coverCredit:
  name: "Agê Barros"
  url: "https://unsplash.com/@agebarros"
series: "practical-sql"
hashnodeCuid: "clrg8qidq000m09jpeah43n6v"
---

DATETIME and TIMESTAMP in BigQuery are not the same and should not be used interchangeably!

One thing I encounter from time to time is mixing of DATETIME and TIMESTAMP types. Even casually converting TIMESTAMP(DATETIME\_COLUMN) with no timezone provided.

This should not be done and you will get a type mismatch error when you, for example, try to compare them, for a very good reason.

What's the difference?

➡ DATETIME is a local time, happening once per day across the globe, at different points in time - it's 17:00 on January 12 first in Tokyo, then Bangalore, London and finally Los Angeles.

➡ TIMESTAMP is an absolute point in time and uses the UTC as a reference.

You can of course convert between the two, but you will NEED to provide a timezone context:  
\- if starting with a DATETIME, you need to provide a source timezone for the TIMESTAMP to be computed  
\- if you have a TIMESTAMP, you need to provide a target timezone for the DATETIME to be computed.

See below an illustration of how it's done.

```sql
SELECT

CURRENT_DATETIME('Europe/Bucharest') AS local_time_bucharest,

CURRENT_DATETIME('America/New_York') AS local_time_new_york,

CURRENT_TIMESTAMP() AS utc_timestamp,

TIMESTAMP(CURRENT_DATETIME('America/New_York'),'America/New_York') AS
timestamp_converted_from_datetime,

DATETIME( CURRENT_TIMESTAMP(), 'Europe/Bucharest') AS bucharest_datetime_from_timestamp
```

![BigQuery results: local\_time\_bucharest 2024-01-12T18:09:21.870935, local\_time\_new\_york 2024-01-12T11:09:21.870935, utc\_timestamp and timestamp\_converted\_from\_datetime both 2024-01-12 16:09:21.870935 (the UTC suffix is cut off), and bucharest\_datetime\_from\_timestamp 2024-01-12T18:09:21.870935.](/images/datetime-vs-timestamp-in-bigquery/1-result.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
