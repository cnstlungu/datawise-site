---
title: "Rounding Timestamps in BigQuery"
seoTitle: "BigQuery Timestamp Rounding: TIMESTAMP_TRUNC and DATE_TRUNC"
seoDescription: "Round timestamps in BigQuery with TIMESTAMP_TRUNC and DATE_TRUNC. Covers hour, day, week, month granularity, time zone handling, and interval arithmetic."
datePublished: 2023-03-26T21:09:49.923Z
dateUpdated: 2026-03-02T10:22:43.469Z
cover: "/images/rounding-timestamps-in-bigquery/cover.jpg"
coverCredit:
  name: "Lukas Blazek"
  url: "https://unsplash.com/@goumbik"
series: "practical-sql"
hashnodeCuid: "clfpw8pur000209jy97zpe92c"
---

Have you ever encountered a situation where you would need to round a timestamp to the nearest second, 5 seconds or minute? While rounding a number is trivial, it's a little bit less straightforward when dealing with timestamps.

Let's consider the following input data.

![BigQuery input data for rounding: a single event\_time TIMESTAMP column with 10 rows between 2023-03-01 10:00:22.577 and 10:01:52.371 UTC, stored at millisecond precision.](/images/rounding-timestamps-in-bigquery/1.png)

We have our *event\_times* that are at milliseconds-level grain. To round the times to the nearest granularity we'd like, we can use a combination of *UNIX\_MILLIS* and *TIMESTAMP\_MILLIS.*

The steps are as follows:

* Transform the timestamp into milliseconds since Unix epoch (that is, number of milliseconds that have passed since January 1st, 1970) with *UNIX\_MILLIS*
    
* Divide that number by your target grain in milliseconds i.e. 1000 for 1 second or 60000 for 1 minute
    
* *CAST* that number to an INT64
    
* Multiply that number by your target grain (the number from above) i.e. 1000 for 1 second or 60000 for 1 minute
    
* Transform it back to a timestamp using *TIMESTAMP\_MILLIS*
    

```sql
SELECT 

event_time,
UNIX_MILLIS(event_time) AS epoch_milliseconds,
TIMESTAMP_MILLIS( CAST(UNIX_MILLIS(event_time) / 1000 AS INT64) * 1000) AS nearest_second,
TIMESTAMP_MILLIS( CAST(UNIX_MILLIS(event_time) / 5000 AS INT64) * 5000) AS nearest_5seconds,
TIMESTAMP_MILLIS( CAST(UNIX_MILLIS(event_time) / 60000 AS INT64) * 60000) AS nearest_1minute,
TIMESTAMP_MILLIS( CAST(UNIX_MILLIS(event_time) / 300000 AS INT64) * 300000) AS nearest_5minutes,

FROM input_data
```

Upon executing this query, the following results are produced:

![BigQuery result of rounding event\_time: columns event\_time, epoch milliseconds (header cut off), nearest\_second, nearest\_5seconds, nearest\_1minute and nearest\_5minutes; for example 10:00:34.757 rounds to 10:00:35, 10:00:35, 10:01:00 and 10:00:00 UTC respectively.](/images/rounding-timestamps-in-bigquery/2.png)

The functions presented above and others relevant to working with timestamps are presented in the [documentation](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions).

Thanks for reading and enjoy working with BigQuery!
