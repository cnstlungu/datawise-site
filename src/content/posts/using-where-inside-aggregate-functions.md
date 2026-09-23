---
title: "Using WHERE inside aggregate functions"
subtitle: ""
seoTitle: "BigQuery Aggregate Functions Now Support WHERE"
seoDescription: "Filter the input rows of any BigQuery aggregate with WHERE. What it does, how it compares to HAVING MAX / HAVING MIN, and why it beats CASE WHEN."
datePublished: 2026-09-22T06:52:46.748Z
cover: "/images/using-where-inside-aggregate-functions/cover.jpg"
coverCredit:
  name: "jiteng hermanto"
  url: "https://unsplash.com/@jiteng11"
series: "practical-sql"
tags: ["bigquery", "sql", "data-engineer", "google-cloud"]
hashnodeCuid: "cmucbhi4z00020agmcydwcgd8"
---

I've [previously shared](/another-look-at-anyvalue-in-bigquery) how aggregate functions in BigQuery SQL can pick their rows with HAVING MAX / HAVING MIN.  
  
WHERE is now supported in preview (yes, I'm the tenth person posting it). It filters the input rows, so any aggregate can run on any subset of the data. The difference: HAVING MAX picks the extreme rows of the group; WHERE picks rows by conditions you know beforehand.  
  
Sure, you could solve most of this before with SUM(CASE WHEN ... END), a classic SQL interview question. To me, a WHERE like this is more intuitive and pleasing to the eye. Very BigQuery!

![Input data: a sales table with year, country, amount and category, one fruit and one vegetable amount per country and year: 2025 US 10 and 12, FR 15 and 8, NL 12 and 20; 2026 US 12 and 13, FR 16 and 9, NL 13 and 21.](/images/using-where-inside-aggregate-functions/1-input.png)

```sql
SELECT
    -- 1. No condition: include every row.
    SUM(amount) AS total_sales,

    -- 2. One condition: each aggregate selects its own category.
    SUM(amount WHERE category = 'fruit') AS fruit_all_time_sales,
    SUM(amount WHERE category = 'vegetable') AS vegetable_all_time_sales,

    -- 3. Two conditions: restrict both category and year.
    SUM(amount WHERE category = 'fruit' AND year = 2025) AS fruit_sales_2025,
    SUM(amount WHERE category = 'fruit' AND year = 2026) AS fruit_sales_2026,

    -- 4. IN selects several countries; AND also restricts the category.
    SUM(amount WHERE category = 'fruit' AND country IN ('FR', 'NL')) AS fr_nl_fruit_all_time_sales,

    -- 5. The same matching rows can feed different aggregates.
    -- These four expressions all select the amounts 20 and 21.
    SUM(amount WHERE category = 'vegetable' AND country = 'NL') AS nl_vegetable_all_time_sales,
    MAX(amount WHERE category = 'vegetable' AND country = 'NL') AS highest_yearly_nl_vegetable_sales
FROM sales;
```

![Query results as JSON: total\_sales 161, fruit\_all\_time\_sales 78, vegetable\_all\_time\_sales 83, fruit\_sales\_2025 37, fruit\_sales\_2026 41, fr\_nl\_fruit\_all\_time\_sales 56, nl\_vegetable\_all\_time\_sales 41 and highest\_yearly\_nl\_vegetable\_sales 21.](/images/using-where-inside-aggregate-functions/1-result.png)
