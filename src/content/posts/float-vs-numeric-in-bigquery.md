---
title: "FLOAT vs NUMERIC in BigQuery"
seoTitle: "BigQuery FLOAT64 vs NUMERIC: When Precision Matters"
seoDescription: "FLOAT64 is fast but approximate; NUMERIC is exact at the cost of more storage. Learn when each matters in BigQuery and when rounding errors silently creep in."
datePublished: 2024-06-08T17:54:47.112Z
dateUpdated: 2026-03-02T10:22:39.015Z
cover: "/images/float-vs-numeric-in-bigquery/cover.jpg"
coverCredit:
  name: "Nick Hillier"
  url: "https://unsplash.com/@nhillier"
series: "practical-sql"
hashnodeCuid: "clx6f0p8o00060aifbkul4elu"
---

What are the differences between FLOAT (FLOAT64) vs NUMERIC data types in BigQuery SQL and when to use each?

While they both can express decimals, they have some important differences in terms of precision and performance.

🔷 FLOAT (FLOAT64): a double-precision floating-point number.

Pros:  
\- can express a large array of values, both large and very very small.  
\- uses 8 logical bytes (half as compared to NUMERIC)  
\- calculations can be faster  
\- we have literals for not-a-number `NaN`, minus/plus infinity

Cons:  
\- it's an approximate data type, yielding potential rounding errors

Use cases  
\- queries that can tolerate small differences i.e. how many kg of chocolate we eat per capita per year  
\- scientific calculations with very large numbers

🔷 NUMERIC: a fixed-point decimal type for up to 38 digits, 9 decimal places, alias for DECIMAL

Pros:  
\- exact storage avoiding rounding errors, no loss of precision

Cons:  
\- uses 16 logical bytes  
\- calculations can be slower

When to use it:  
\- anywhere every single decimal digit matters, like finance or sending a spaceship to another planet

P.S. There's also BIGNUMERIC (alias for BIGDECIMAL) if you need even larger range, but that takes 32 logical bytes.

![BigQuery SQL adding CAST(0.1 AS FLOAT64) and CAST(0.2 AS FLOAT64) and casting 'NaN', '-inf' and 'inf' to FLOAT64; the JSON result shows float\_sum 0.30000000000000004 plus NaN, -Infinity and Infinity values.](/images/float-vs-numeric-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
