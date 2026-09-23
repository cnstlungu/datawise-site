---
title: "NON-EQUI joins in SQL"
seoTitle: "SQL Non-Equi Joins: Join on Range and Inequality Conditions"
seoDescription: "Non-equi joins use comparison or BETWEEN operators instead of equality to match rows across tables in SQL. A practical pattern for range-based lookups..."
datePublished: 2024-06-23T21:00:06.683Z
dateUpdated: 2026-03-02T10:51:36.882Z
cover: "/images/non-equi-joins-in-sql/cover.jpg"
coverCredit:
  name: "Julia Taubitz"
  url: "https://unsplash.com/@schwarzeweissheitenfotografie"
series: "practical-sql"
hashnodeCuid: "clxs18t5n00000albai1q38nv"
---

So here's another post about SQL joins. Based on the type of condition we use for joining we distinguish equi joins and non-equi joins.

Simply put:  
\- equi joins: we're using the equality operator:  
tab\_a.column\_x = tab\_b.column\_y  
\- non-equi joins: other operators, like comparison, inequality or BETWEEN are used

While a good portion of the time we use equi joins to, say, lookup the department the employee is part of, non-equi joins are not uncommon either.

Moreover, sometimes we might use both equality and other operators for joining the same table.

Let's look at a simple non-equi join scenario below.

![Input data: campaigns (Winter 2021, Summer 2021, Winter 2022, Summer 2022 with valid\_from/valid\_to half-year ranges), discounts (0-50 at 0.1, 50-100 at 0.15, 100-1000000 at 0.2) and orders (1 on 2021-03-01 for 100, 2 on 2022-03-01 for 45, 3 on 2022-07-01 for 151, 4 on 2022-12-01 for 80).](/images/non-equi-joins-in-sql/1-input.jpg)

```sql
SELECT
  o.order_id,
  o.order_date,
  c.name AS campaign_name,
  o.amount AS list_price_amount,
  d.discount_percentage,
  (1-discount_percentage)*amount AS paid_amount
FROM orders o
JOIN campaign c ON o.order_date BETWEEN c.valid_from AND c.valid_to
JOIN discounts d ON o.amount >= value_from AND o.amount < value_to
```

![Results: order 4 (2022-12-01, Summer 2022, 80) gets 0.15 and pays 68; order 3 (2022-07-01, Summer 2022, 151) gets 0.2 and pays 120.8; order 2 (2022-03-01, Winter 2022, 45) gets 0.1 and pays 40.5; order 1 (2021-03-01, Winter 2021, 100) gets 0.2 and pays 80.](/images/non-equi-joins-in-sql/1-result.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Self-joins in SQL](/self-joins-in-sql)
- [Anti-joins in SQL](/anti-joins-in-sql)
- [SEMI-JOINS in SQL](/semi-joins-in-sql)
- [NATURAL JOIN in SQL](/natural-join-in-sql)
