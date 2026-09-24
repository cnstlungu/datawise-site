---
title: "Comments in SQL"
seoTitle: "SQL Comments in BigQuery: --, #, and /* */ Syntax"
seoDescription: "BigQuery supports single-line comments with -- or #, and multi-line block comments with /* */. Learn the differences between inline and block comments to..."
datePublished: 2024-06-26T22:17:04.171Z
dateUpdated: 2026-03-02T10:52:19.487Z
cover: "/images/comments-in-sql/cover.jpg"
coverCredit:
  name: "Raphael Schaller"
  url: "https://unsplash.com/@raphaelphotoch"
series: "practical-sql"
hashnodeCuid: "clxwebc17000009jx954kh53g"
---

Let's look at the available options in terms of SQL comments in BigQuery.

If you ever need to pass on a note to the future you or a fellow developers about the reasoning behind a particular approach or something to watch out for in a query, you can write a comment.

Based on where we put them, we can distinguish between:  
\- single line, taking the entire line  
\- in-line, comments intertwined with code  
\- multi-line, comments spanning across lines

With regards to the notation, we have:  
\- the '--' will turn everything after it on the same line into a comment  
\- the '#' which you might recognize from say Python, and works like '--'  
\- the '/\* \*/' block which clearly marks it start and end, making possible the insertions of a comment inside a code line and multi-line comments

How much are you using comments in your SQL code and in what situations?

```sql
WITH orderline_updates AS (

  SELECT 1 AS order_id, 'Apples' AS product, 10 AS quantity, '2021-01-01 12:00:12' AS last_updated UNION ALL
  SELECT 1 AS order_id, 'Grapes' AS product, 3 AS quantity, '2021-01-01 12:00:12' AS last_updated UNION ALL
  SELECT 2 AS order_id, 'Mangoes' AS product, 1 AS quantity, '2021-01-02 10:00:19' AS last_updated UNION ALL
  SELECT 2 AS order_id, 'Kiwi' AS product, 6 AS quantity, '2021-01-03 12:24:33' AS last_updated
)
-- single line comment, taking the entire line

SELECT
  order_id, -- inline comment
  product, # also an inline comment
  quantity /* also an inline comment, but you can write code after it */ AS total_quantity,
  last_updated
/*
comment spanning multiple lines:
a multi-line comment
*/
FROM orderline_updates
```

![BigQuery results: four order lines, order 1 Apples 10 and Grapes 3 (2021-01-01 12:00:12), order 2 Mangoes 1 (2021-01-02 10:00:19) and Kiwi 6 (2021-01-03 12:24:33), with the quantity column named total\_quantity.](/images/comments-in-sql/1-result.jpg)
