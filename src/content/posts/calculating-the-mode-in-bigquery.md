---
title: "Calculating the MODE in BigQuery"
seoTitle: "Calculate MODE in BigQuery Without a Built-in Function"
seoDescription: "No native MODE() in BigQuery. Compute the most frequent value with COUNT, GROUP BY, and QUALIFY. Covers ties, multiple modes, and window function approaches."
datePublished: 2024-02-21T22:15:27.754Z
dateUpdated: 2026-03-02T10:22:31.120Z
cover: "/images/calculating-the-mode-in-bigquery/cover.jpg"
coverCredit:
  name: "Chris Liverani"
  url: "https://unsplash.com/@chrisliverani"
series: "practical-sql"
hashnodeCuid: "clswcrxmy000008l801rbgyb5"
---

How do you compute the MODE (most frequent value) in BigQuery?

For the other measures of central tendency like MEAN and MEDIAN, there are straightforward ways to compute results - functions AVG and PERCENTILE\_CONT/PERCENTILE\_DIST respectively, but there's no dedicated function for MODE.

By the way, if you have a huge dataset and can bear some lack of precision, take a look at APPROX\_TOP\_COUNT.

Say we have the following input data:

![Input table for calculating the mode, with columns country, value and value\_date: US and UK rows twice a month from 2023-01-01 to 2023-03-15 with values 1 or 2, and empty NULL values on 2023-02-15 and 2023-03-15.](/images/calculating-the-mode-in-bigquery/1.png)

Now here's how we can compute them otherwise:  
\- filter out NULLS (if we want to ignore them) or do nothing if we want to keep them  
\- compute value counts for our desired grain  
\- take the most frequent one per our grain using QUALIFY + RANK

```sql
SELECT country, value, COUNT(1) AS times_seen

FROM input_data

-- comment this if you want to include NULLS
WHERE value IS NOT NULL

GROUP BY country, value

QUALIFY RANK() OVER(PARTITION BY country
                    ORDER BY times_seen DESC) = 1
```

Here's how the output would look with NULLS excluded.

![Mode query output with NULLs excluded, columns country, value and times\_seen: UK has mode 1 and US has mode 2, each seen 2 times.](/images/calculating-the-mode-in-bigquery/3.png)

And with them included:

![Mode query output with NULLs included, columns country, value and times\_seen: UK returns 1 and NULL, US returns 2 and NULL, all tied at 2 occurrences, so RANK keeps two rows per country.](/images/calculating-the-mode-in-bigquery/4.png)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
