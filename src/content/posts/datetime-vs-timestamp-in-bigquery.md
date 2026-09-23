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

![BigQuery SQL converting between DATETIME and TIMESTAMP: CURRENT\_DATETIME for Europe/Bucharest and America/New\_York, CURRENT\_TIMESTAMP(), TIMESTAMP(datetime, 'America/New\_York') and DATETIME(CURRENT\_TIMESTAMP(), 'Europe/Bucharest'); results show 18:09 Bucharest, 11:09 New York and 16:09 UTC.](/images/datetime-vs-timestamp-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
