---
title: "Order of precedence in SQL: WHERE vs HAVING"
seoTitle: "SQL WHERE vs HAVING: Order of Execution Explained"
seoDescription: "Understand the difference between WHERE and HAVING in SQL and why execution order matters when reusing column aliases."
datePublished: 2024-05-09T20:59:25.978Z
dateUpdated: 2026-03-02T10:52:02.549Z
cover: "/images/order-of-precedence-in-sql-where-vs-having/cover.jpg"
coverCredit:
  name: "Kyle Glenn"
  url: "https://unsplash.com/@kylejglenn"
series: "practical-sql"
hashnodeCuid: "clvzqelqy000208jkb0mj1yjh"
---

If you're just getting started with SQL, this post is for you. So, it's worth looking at the order of precedence of SQL operators.

One particular case is WHERE vs HAVING, especially if you bind the aggregated column to the same column alias as in the input table.

This can save you from some unexpected results 😁

In short:  
\- WHERE = filter before aggregation  
\- HAVING = filter after aggregation

In the example below, the 'quantity' filtered in the HAVING clause is no longer the same 'quantity' in the original table, rather the SUM of quantities per each country bucket.

In practice, I'd rename the aggregated column to something like total\_quantity to make it more readable.

Depending what we need, we pick which approach we take, filtering out records before or after aggregation.

![Input data: quantity and country rows 10 UK, 15 UK, 15 US, -5 US, -10 FR and -5 FR.](/images/order-of-precedence-in-sql-where-vs-having/1-input.jpg)

```sql
SELECT
  country,
  SUM(quantity) AS quantity

FROM input_data

GROUP BY country

HAVING quantity > 0
```

```sql
SELECT
  country,
  SUM(quantity) AS quantity

FROM input_data

WHERE quantity > 0

GROUP BY country
```

![BigQuery results side by side: the HAVING query (left) returns UK 25 and US 10, the WHERE query (right) returns UK 25 and US 15.](/images/order-of-precedence-in-sql-where-vs-having/1-result.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [9 tips on writing cleaner SQL](/9-tips-on-writing-cleaner-sql)
- [Easy with that SELECT DISTINCT!](/easy-with-that-select-distinct)
- [Why you should use parentheses with AND & OR in SQL](/why-you-should-use-parentheses-with-and-or-in-sql)
- [ORDER BY expressions in SQL](/order-by-expressions-in-sql)
