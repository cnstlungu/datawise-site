---
title: "The order in which you ROUND matters in SQL"
seoTitle: "SQL Rounding Errors: ROUND Before or After Aggregate"
seoDescription: "Rounding before vs after aggregation in SQL produces different results — learn when each approach is correct. Covers ROUND, FLOOR, and CEILING with..."
datePublished: 2024-05-09T21:03:06.495Z
dateUpdated: 2026-03-02T10:52:41.782Z
cover: "/images/the-order-in-which-you-round-matters-in-sql/cover.jpg"
coverCredit:
  name: "Chaitanya Tatikonda"
  url: "https://unsplash.com/@tvschaitanya"
series: "practical-sql"
hashnodeCuid: "clvzqjbwf000209jx62bvcq6i"
---

Rounding numbers in SQL is one of the simplest operation, but it's important to we pay attention to how we apply it.

1. Consider the sequence in which you apply rounding and aggregation functions.
    

When you ROUND a value and then aggregate it using functions like SUM or AVG, the outcome may differ significantly compared to first aggregating the values and then rounding the result.

![BigQuery SQL grouping quantities by country and comparing SUM(ROUND(quantity,0)) AS sum\_rounded\_quantities with ROUND(SUM(quantity),0) AS round\_sum\_of\_quantities; UK gives 4.0 vs 5.0 and US 7.0 vs 6.0, so rounding before or after summing changes the result.](/images/the-order-in-which-you-round-matters-in-sql/1.jpg)

As with all things, take into consideration your context and business problem you're trying to solve.

2. Be sure to use the proper rounding function for the job:  
    \- `ROUND` - nearest integer or decimal place (if specified) 1.4 =1 but 1.5 =&gt;2  
    \- `FLOOR` - largest integer that is not greater than our value 1.7 =&gt; 1  
    \- `CEIL`/`CEILING` - smallest integer than is not smaller than our value 1.4 =&gt; 2
    

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
