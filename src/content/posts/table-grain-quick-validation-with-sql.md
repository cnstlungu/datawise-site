---
title: "Table grain quick validation with SQL"
seoTitle: "Validate Table Grain in SQL: Find Duplicates and Bad Keys Fast"
seoDescription: "Quickly validate table grain, spot duplicate rows, and test key assumptions using SQL patterns built on TO_JSON_STRING and FARM_FINGERPRINT."
datePublished: 2025-10-04T12:22:56.146Z
dateUpdated: 2026-04-05T20:11:29.937Z
cover: "/images/table-grain-quick-validation-with-sql/cover.jpg"
coverCredit:
  name: "Lutz Wernitz"
  url: "https://unsplash.com/@luwe83"
series: "practical-sql"
hashnodeCuid: "cmgc8udua000f02kv63z0c0l9"
---

I was doing some exploratory data analysis on a number of tables I didn’t have much information about and, unfortunately, didn’t know their grain.

I needed a quick way to validate my assumptions about the table grain, identify contradicting observations (rows), and check for duplicates at the same time.

Therefore I decided to use a combination of TO\_JSON\_STRING and FARM\_FINGERPRINT. The first creates a JSON representation of the entire row (given a table alias), while the second converts the resulting string into a INT64 hash.

By comparing the total number of rows in a group against the distinct count of these fingerprints, we can determine whether the proposed grain is correct and whether there are duplicates in the data.

This was a quick exercise but use this with care. Depending on your SQL implementation, data volumes and context, results may vary.

![Input data: input\_data with order\_id, product\_name, qty, price and order\_status, 15 rows for orders 1 to 3 (Apples, Mangoes, Cucumbers, Tomatoes and Plums), each product once ORDER\_PLACED and once ORDER\_SENT, with the order 3 Plums rows repeated and one Plums row with a null order\_status.](/images/table-grain-quick-validation-with-sql/1-input.jpg)

```sql
SELECT

  order_id,
  product_name,
  COUNT(FARM_FINGERPRINT(TO_JSON_STRING(i))) AS count_duplicates,
  COUNT(DISTINCT FARM_FINGERPRINT(TO_JSON_STRING(i))) AS count_grain

FROM input_data i

GROUP BY ALL

HAVING count_duplicates > 1 OR count_grain > 1
```

```sql
SELECT

  order_id,
  product_name,
  order_status,
  COUNT(FARM_FINGERPRINT(TO_JSON_STRING(i))) AS count_duplicates,
  COUNT(DISTINCT FARM_FINGERPRINT(TO_JSON_STRING(i))) AS count_grain

FROM input_data i

GROUP BY ALL

HAVING count_duplicates > 1 OR count_grain > 1
```

![Results of the two queries. Incorrect grain (order\_id, product\_name): six groups with count\_grain 2, e.g. order 1 Apples 2/2 and order 3 Plums with count\_duplicates 4. Correct grain, but there are duplicates (adding order\_status): order 3 Plums ORDER\_PLACED and ORDER\_SENT, each count\_duplicates 2 and count\_grain 1.](/images/table-grain-quick-validation-with-sql/1-result.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [9 tips on writing cleaner SQL](/9-tips-on-writing-cleaner-sql)
- [Order of precedence in SQL: WHERE vs HAVING](/order-of-precedence-in-sql-where-vs-having)
- [Easy with that SELECT DISTINCT!](/easy-with-that-select-distinct)
- [Why you should use parentheses with AND & OR in SQL](/why-you-should-use-parentheses-with-and-or-in-sql)
