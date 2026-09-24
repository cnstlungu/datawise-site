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

AND [has a higher order of precedence](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators#operator_precedence) than OR, therefore, in the example below:

`is_paid AND is_shipped OR customer_is_on_contract AND is_first_time_buyer`

is equivalent to

`( is_paid AND is_shipped) OR (customer_is_on_contract AND is_first_time_buyer)`.

It should also be noted that for comparison operators parentheses are required in order to resolve ambiguity since they are not associative like NOT/AND/OR.

```sql
WITH input_data AS (
  SELECT 1 AS order_id, TRUE AS is_paid, FALSE AS is_shipped, TRUE AS customer_is_on_contract, TRUE AS is_first_time_buyer
  UNION ALL
  SELECT 2 AS order_id, FALSE AS is_paid, TRUE AS is_shipped, TRUE AS customer_is_on_contract, TRUE AS is_first_time_buyer
  UNION ALL
  SELECT 3 AS order_id, FALSE AS is_paid, FALSE AS is_shipped, TRUE AS customer_is_on_contract, FALSE AS is_first_time_buyer
)

SELECT *

FROM input_data

WHERE
      --is_paid AND is_shipped OR customer_is_on_contract AND is_first_time_buyer
      --resolved as:
     (is_paid AND is_shipped) OR (customer_is_on_contract AND is_first_time_buyer)
```

![BigQuery results: orders 1 and 2 are returned; order 1 has is\_paid true and is\_shipped false, order 2 has is\_paid false and is\_shipped true, and both have customer\_is\_on\_contract and is\_first\_time\_buyer true.](/images/why-you-should-use-parentheses-with-and-or-in-sql/1-result.jpg)

---

*Enjoyed this? Here are some related articles you might find useful:*

- [9 tips on writing cleaner SQL](/9-tips-on-writing-cleaner-sql)
- [Order of precedence in SQL: WHERE vs HAVING](/order-of-precedence-in-sql-where-vs-having)
- [Easy with that SELECT DISTINCT!](/easy-with-that-select-distinct)
- [ORDER BY expressions in SQL](/order-by-expressions-in-sql)
