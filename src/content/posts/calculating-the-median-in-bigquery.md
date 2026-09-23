---
title: "Calculating the Median in BigQuery"
seoTitle: "BigQuery Median: PERCENTILE_CONT vs APPROX_QUANTILES"
seoDescription: "BigQuery has no native MEDIAN(). Use PERCENTILE_CONT(0.5) for exact results or APPROX_QUANTILES for large datasets. Includes GROUP BY and window examples."
datePublished: 2024-08-09T15:00:51.085Z
dateUpdated: 2026-03-02T10:16:33.213Z
cover: "/images/calculating-the-median-in-bigquery/cover.jpg"
coverCredit:
  name: "Jesse Collins"
  url: "https://unsplash.com/@jtc"
series: "practical-sql"
hashnodeCuid: "clzmu3u3100030ams8f76fylo"
---

One of these days, I had to handle missing value imputation and stumbled upon the need to calculate a median in BigQuery SQL. Since there is no built-in function for this, I looked for what other people used as workarounds—see sources in comments.

First, we have `PERCENTILE_CONT` and `PERCENTILE_DISC` (from continuous and discrete, respectively). The difference between them lies in whether interpolation is used:  
\- `PERCENTILE_CONT` uses linear interpolation. In the case of an even number of values, it returns their average.  
\- `PERCENTILE_DISC` selects the closest value without any interpolation.  
Both of these are window functions, so if you want to simulate grouping, you need to ensure that a single value is kept per group. Also, note the option of IGNORE | RESPECT NULLS (ignore is the default).

Additionally, we can use the approximate aggregation function `APPROX_QUANTILES`, which allows grouping. This function splits the values into quantiles, from which we can select the 50th percentile to retrieve the median. Check out the comments for a quick into intro approximate aggregate functions.

![](/images/calculating-the-median-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
