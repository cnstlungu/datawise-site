---
title: "Using INSTR in BigQuery"
seoTitle: "BigQuery INSTR: Find Substring Position in a String"
seoDescription: "BigQuery's INSTR function returns the 1-based index of a substring within a string, returning 0 if not found. You can also specify a start position and..."
datePublished: 2024-04-22T20:50:42.666Z
dateUpdated: 2026-03-02T10:52:45.087Z
cover: "/images/using-instr-in-bigquery/cover.jpg"
coverCredit:
  name: "Sven Brandsma"
  url: "https://unsplash.com/@seffen99"
series: "practical-sql"
hashnodeCuid: "clvbflwmi00010al94mb9dnro"
---

If you ever need to do something different based on the existence of a particular substring in BigQuery, take a look at the INSTR function.

It returns the 1-based index of the first occurrence of a substring (1 or more characters) in another STRING. The function returns 0 if the substring was not found.

There's also a possibility to specify at what position to start the search (like in good old Excel) and which occurrence to get.

```sql
WITH input_data AS (
  SELECT 1 AS user_id, 'apple,grapes,melon' AS fruits
  UNION ALL
  SELECT 2 AS user_id, 'pear;mango;kiwi'
  UNION ALL
  SELECT 3 AS user_id, 'banana'
)

SELECT

  user_id,
  fruits,
  INSTR(fruits,',') AS comma_first_position,
  INSTR(fruits,';') AS semicolon_first_position,

  CASE WHEN INSTR(fruits,';') > 0 THEN SPLIT(fruits,',')
       ELSE SPLIT(fruits,',') END AS fruits_array,

FROM input_data
```

![BigQuery results: apple,grapes,melon has comma\_first\_position 6 and semicolon\_first\_position 0 and splits into apple, grapes and melon; pear;mango;kiwi has 0 and 5 and stays one item; banana has 0 and 0.](/images/using-instr-in-bigquery/1-result.png)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
