---
title: "Anti-joins in SQL"
seoTitle: "SQL Anti-Join Pattern: Find Rows Missing in Another Table"
seoDescription: "An anti-join uses LEFT JOIN with a WHERE IS NULL check to return rows from one table not found in another. Learn how it differs from EXCEPT and when to..."
datePublished: 2024-06-17T21:10:22.251Z
dateUpdated: 2026-03-02T10:50:43.032Z
cover: "/images/anti-joins-in-sql/cover.jpg"
coverCredit:
  name: "Max van den Oetelaar"
  url: "https://unsplash.com/@maxvdo"
series: "practical-sql"
hashnodeCuid: "clxjgyw4r000409m9fihy3hl9"
---

Here's the SQL Anti-Join, another type of join that doesn't have its own keyword but it's very much a thing. You might have used it a lot of times before 😁

So, what does it do?

The anti-join retains all the rows in one table that are not also found in another table. So A \\ B.

We achieve this with a LEFT JOIN + WHERE \[key in right table\] IS NULL for the LEFT ANTI JOIN and RIGHT JOIN + WHERE \[key in left table) IS NULL for the RIGHT ANTI JOIN (although I know right joins don't get much love here 😁).

An anti-join is a bit similar to the [EXCEPT set operation](https://www.linkedin.com/feed/update/urn:li:activity:7124727873818509312/), with the difference that:  
\- in the EXCEPT if at least one column is different between the two tables, the row is considered a difference (so is kept)  
\- in the ANTI JOIN we typically look at just whether the join keys are present in the other table or not (but you check as many columns as you want, of course)

In the example below, we're illustrating a LEFT ANTI JOIN which finds all the products we have details for (like product name) but for which we don't have a row in the pricing table.

![](/images/anti-joins-in-sql/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Self-joins in SQL](/self-joins-in-sql)
- [SEMI-JOINS in SQL](/semi-joins-in-sql)
- [NON-EQUI joins in SQL](/non-equi-joins-in-sql)
- [NATURAL JOIN in SQL](/natural-join-in-sql)
