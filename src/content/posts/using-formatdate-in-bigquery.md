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

![](/images/using-formatdate-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
