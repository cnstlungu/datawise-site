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

![SQL non-equi joins from orders to campaign ON o.order\_date BETWEEN c.valid\_from AND c.valid\_to and to discounts ON o.amount \>= value\_from AND o.amount \< value\_to, computing (1-discount\_percentage)\*amount AS paid\_amount; e.g. order 3 (151, Summer 2022) gets 0.2 off and pays 120.8.](/images/non-equi-joins-in-sql/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Self-joins in SQL](/self-joins-in-sql)
- [Anti-joins in SQL](/anti-joins-in-sql)
- [SEMI-JOINS in SQL](/semi-joins-in-sql)
- [NATURAL JOIN in SQL](/natural-join-in-sql)
