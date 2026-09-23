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

![](/images/table-grain-quick-validation-with-sql/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [9 tips on writing cleaner SQL](/9-tips-on-writing-cleaner-sql)
- [Order of precedence in SQL: WHERE vs HAVING](/order-of-precedence-in-sql-where-vs-having)
- [Easy with that SELECT DISTINCT!](/easy-with-that-select-distinct)
- [Why you should use parentheses with AND & OR in SQL](/why-you-should-use-parentheses-with-and-or-in-sql)
