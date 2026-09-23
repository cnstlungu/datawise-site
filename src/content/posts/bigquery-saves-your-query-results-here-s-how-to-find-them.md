---
title: "BigQuery Saves Your Query Results — Here's How to Find Them"
subtitle: ""
seoTitle: "Where BigQuery Saves Query Results: Temporary Tables Explained"
seoDescription: "BigQuery writes query results to temporary tables unless you choose a destination. Learn where to find them, how long they persist, and what changes when you save results explicitly."
datePublished: 2026-03-05T07:34:36.444Z
dateUpdated: 2026-04-05T20:11:28.403Z
cover: "/images/bigquery-saves-your-query-results-here-s-how-to-find-them/cover.jpg"
series: "practical-sql"
hashnodeCuid: "cmmd5h2n000sk2cnq4mai4mkc"
---

Ever run a heavy BigQuery SQL query, processed gigabytes of data — and then accidentally closed the tab or forgot to save the results? 😬

**Don't re-run it. Your results are still there.**

BigQuery automatically saves query results to an anonymous temporary table for **24 hours**. You can find it under **Job Information → Temporary Table**.

This is also the engine behind BigQuery's caching behavior: if you run the exact same query again within that window — with no changes — BigQuery serves results directly from cache, **at no charge**.

**One caveat worth knowing:** if your result set exceeds **10 GB** (that's the output, not the data scanned), it won't be cached. So for very large result sets, you'll want to write results to a permanent table explicitly.

![BigQuery console screenshot: a GROUP BY ALL query on learning\_us.trends\_us\_prod lists Destination table as Temporary table under Job information, and an arrow leads to querying that anonymous \_a85a60... dataset table, which processes 0 B and returns the same dma\_name results.](/images/bigquery-saves-your-query-results-here-s-how-to-find-them/1.png)
