---
title: "Why you should use parentheses with AND & OR in SQL"
seoTitle: "SQL AND vs OR Precedence: Why You Need Parentheses"
seoDescription: "AND has higher operator precedence than OR in SQL, meaning mixed conditions without parentheses can produce unexpected results."
datePublished: 2024-05-24T04:44:38.210Z
dateUpdated: 2026-03-02T10:50:28.334Z
cover: "/images/why-you-should-use-parentheses-with-and-or-in-sql/cover.jpg"
coverCredit:
  name: "Markus Spiske"
  url: "https://unsplash.com/@markusspiske"
series: "practical-sql"
hashnodeCuid: "clwk76saq000909mlak529uv8"
---

If you filter the data in SQL with WHERE using multiple logical conditions tied with AND & OR, PLEASE use the parentheses them accordingly.

Because if you don't, your fellow team members are going to have a harder time understanding your intent.

You might also get unintended results based on how they are resolved:

`... operators with the same precedence are left associative. This means that those operators are grouped together starting from the left and moving right.`

AND [has a higher order of precedence](https://cloud.google.com/bigquery/docs/reference/standard-sql/operators#operator_precedence) than OR, therefore, in the example below:

`is_paid AND is_shipped OR customer_is_on_contract AND is_first_time_buyer`

is equivalent to

`( is_paid AND is_shipped) OR (customer_is_on_contract AND is_first_time_buyer)`.

It should also be noted that for comparison operators parentheses are required in order to resolve ambiguity since they are not associative like NOT/AND/OR.

![](/images/why-you-should-use-parentheses-with-and-or-in-sql/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [9 tips on writing cleaner SQL](/9-tips-on-writing-cleaner-sql)
- [Order of precedence in SQL: WHERE vs HAVING](/order-of-precedence-in-sql-where-vs-having)
- [Easy with that SELECT DISTINCT!](/easy-with-that-select-distinct)
- [ORDER BY expressions in SQL](/order-by-expressions-in-sql)
