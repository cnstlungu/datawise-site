---
title: "Self-joins in SQL"
seoTitle: "SQL Self-Joins: Use Cases and BigQuery Performance Gotchas"
seoDescription: "Self-joins let you join a table with itself to retrieve related rows, such as resolving manager names from an employee table."
datePublished: 2024-06-16T20:57:20.709Z
dateUpdated: 2026-03-02T10:52:37.418Z
cover: "/images/self-joins-in-sql/cover.jpg"
coverCredit:
  name: "Ashley Batz"
  url: "https://unsplash.com/@ashleybatz"
series: "practical-sql"
hashnodeCuid: "clxi12af9000009ktezez2st6"
---

Let's talk about self-joins in SQL. It's one of the join types that don't have their own keyword, but is more of a concept.

It essentially means you are joining a table with itself to retrieve some result from another row.

Prior to the introduction of window functions, self-joins were much more prevalent - you would, for example, join the table to itself to retrieve the value for the previous day.

When considering using a self-join, be mindful of the performance implications. BigQuery, for example, [explicitly lists self-joins as an anti-pattern](https://cloud.google.com/bigquery/docs/best-practices-performance-compute#avoid_self_joins). That is not to say that the need for self-tables has disappeared, there are still cases where we'd need it.

Let's look at an example. We have a table containing all the employee data, including the id of their manager.

If order to retrieve their manager's name, we'd need to perform a self join, using manager\_id in the join condition.

By the way, this particular case can also be solved with a [recursive common-table expression](/recursive-ctes-in-bigquery).

![](/images/self-joins-in-sql/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Anti-joins in SQL](/anti-joins-in-sql)
- [SEMI-JOINS in SQL](/semi-joins-in-sql)
- [NON-EQUI joins in SQL](/non-equi-joins-in-sql)
- [NATURAL JOIN in SQL](/natural-join-in-sql)
