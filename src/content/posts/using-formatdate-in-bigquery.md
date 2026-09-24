---
title: "Using FORMAT_DATE in BigQuery"
seoTitle: "BigQuery FORMAT_DATE: Extract Weekday Name for Joins"
seoDescription: "FORMAT_DATE in BigQuery extracts formatted date parts like abbreviated weekday names using strftime-style format elements."
datePublished: 2024-04-28T21:29:54.324Z
dateUpdated: 2026-03-02T10:50:40.764Z
cover: "/images/using-formatdate-in-bigquery/cover.jpg"
coverCredit:
  name: "Towfiqu barbhuiya"
  url: "https://unsplash.com/@towfiqu999999"
series: "practical-sql"
hashnodeCuid: "clvk1nf6c000c08i671uk4kne"
---

The code we write daily as Data Engineers is not necessarily complicated.

We're solving a lot of problems like the following:

Given a schedule per day of the week (Monday hours are 10:00 - 22:00 / 10 am - 10 pm), find out what was the schedule for a list of calendar days.

Here's how a BigQuery solution could look like:  
\- using FORMAT\_DATE we can extract the abbreviated week day (%a in the list of format elements for date and time parts, attached in comments)  
\- transform that match casing of the joined column  
\- (INNER) JOIN

How would your solution to such a problem look like?

```sql
WITH schedule AS (
  SELECT 'MON' AS day, TIME '10:00:00' AS opening_time, TIME '22:00:00' AS closing_time
    UNION ALL
  SELECT 'TUE' AS day, TIME '10:00:00' AS opening_time, TIME '22:00:00' AS closing_time
    UNION ALL
  SELECT 'WED' AS day, TIME '10:00:00' AS opening_time, TIME '22:00:00' AS closing_time
    UNION ALL
  SELECT 'THU' AS day, TIME '10:00:00' AS opening_time, TIME '22:00:00' AS closing_time
    UNION ALL
  SELECT 'FRI' AS day, TIME '10:00:00' AS opening_time, TIME '22:00:00' AS closing_time
    UNION ALL
  SELECT 'SAT' AS day, TIME '11:00:00' AS opening_time, TIME '20:00:00' AS closing_time
    UNION ALL
  SELECT 'SUN' AS day, TIME '11:00:00' AS opening_time, TIME '16:00:00' AS closing_time
),
dates AS (
  SELECT calendar_date FROM UNNEST(GENERATE_DATE_ARRAY(DATE '2023-04-01', DATE '2023-04-30')) AS calendar_date
)
SELECT
  calendar_date,
  FORMAT_DATE('%a', d.calendar_date) AS day_of_week,
  s.day,
  s.opening_time,
  s.closing_time
FROM dates d
JOIN schedule s ON UPPER(FORMAT_DATE('%a', d.calendar_date)) = s.day
```

![BigQuery results: 2023-04-01 is Sat (SAT, 11:00:00 to 20:00:00), 2023-04-02 is Sun (SUN, 11:00:00 to 16:00:00), and Mon to Thu, 2023-04-03 to 2023-04-06, are 10:00:00 to 22:00:00.](/images/using-formatdate-in-bigquery/1-result.jpg)
