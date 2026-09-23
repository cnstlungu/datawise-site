---
title: "Time Series functions in BigQuery"
seoTitle: "BigQuery DATE_BUCKET, DATETIME_BUCKET, TIMESTAMP_BUCKET"
seoDescription: "BigQuery's time series bucket functions — DATE_BUCKET, DATETIME_BUCKET, and TIMESTAMP_BUCKET — group temporal values into fixed-size intervals."
datePublished: 2024-05-07T13:24:51.561Z
dateUpdated: 2026-03-02T10:51:24.450Z
cover: "/images/time-series-functions-in-bigquery/cover.jpg"
coverCredit:
  name: "Nathan Dumlao"
  url: "https://unsplash.com/@nate_dumlao"
series: "practical-sql"
hashnodeCuid: "clvwfabc900070al205wdf0n2"
---

I've [posted some time ago](/rounding-timestamps-in-bigquery) about "rounding" timestamps and datetime values, but in the past few months BigQuery has added Time Series functions (in preview for now), making for a cleaner and simpler approach of this problem.  
  
We now have `DATE_BUCKET`, `DATETIME_BUCKET` and `TIMESTAMP_BUCKET` which will help us bucket dates, datetimes and timestamps, respectively.  
  
In the example below, we're specifying the bucket size to be 15 minutes and the function groups each of our event\_timestamps into their respective bucket.

![](/images/time-series-functions-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
