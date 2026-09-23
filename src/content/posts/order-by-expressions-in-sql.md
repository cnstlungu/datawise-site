---
title: "ORDER BY expressions in SQL"
seoTitle: "SQL ORDER BY Expressions: Sort by CASE WHEN and More"
seoDescription: "In SQL, ORDER BY accepts expressions, not just column names, letting you apply CASE WHEN logic to control sort priority."
datePublished: 2024-04-01T13:56:56.805Z
dateUpdated: 2026-03-02T10:52:01.471Z
cover: "/images/order-by-expressions-in-sql/cover.jpg"
coverCredit:
  name: "Héctor J. Rivas"
  url: "https://unsplash.com/@hjrc33"
series: "practical-sql"
hashnodeCuid: "cluh0kwv9000a08ky5fwc0y7n"
---

Friendly reminder: when you ORDER BY something in SQL, that something does not necessarily need to be a column, but could be an expression, the output of which can be ordered.

In the example below, we'd like to ORDER by sales decreasingly, but show the 'direct' sales first.

This is achieved by using a CASE WHEN that will rank direct sales above other types of sales, then sorting by the sales decreasingly.

![BigQuery SQL sorting sales rows with ORDER BY CASE WHEN channel = 'direct' THEN 1 ELSE 0 END DESC, sales DESC; results list direct sales first (FR 170, IT 150, US 100), then partners sales (FR 200, US 125, IT 100).](/images/order-by-expressions-in-sql/1.jpg)

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [9 tips on writing cleaner SQL](/9-tips-on-writing-cleaner-sql)
- [Order of precedence in SQL: WHERE vs HAVING](/order-of-precedence-in-sql-where-vs-having)
- [Easy with that SELECT DISTINCT!](/easy-with-that-select-distinct)
- [Why you should use parentheses with AND & OR in SQL](/why-you-should-use-parentheses-with-and-or-in-sql)
