---
title: "A couple of fun things about NULL in SQL"
seoTitle: "SQL NULL Behavior: Key Rules Every Data Engineer Must Know"
seoDescription: "NULL is not zero or empty string — it behaves differently in comparisons, aggregations, joins, and ORDER BY in SQL."
datePublished: 2024-06-08T18:06:34.933Z
dateUpdated: 2026-03-02T10:52:13.884Z
cover: "/images/a-couple-of-fun-things-about-null-in-sql/cover.jpg"
coverCredit:
  name: "Pierre Bamin"
  url: "https://unsplash.com/@bamin"
series: "practical-sql"
hashnodeCuid: "clx6ffved000409lcaibc6imr"
---

If you ever worked with SQL, even a tiny bit, you know NULL is very special value. Like no other. It's very different than an empty string '' or 0, rather representing the absence of a value.

A couple fun things about it:  
🔹 you cannot test if NULL is in a list of values: NULL IN (NULL) returns a NULL  
🔹 both (NULL = NULL) and (NULL &lt;&gt; / != NULL) are not allowed  
🔹 COUNT(column) counts non-null occurrences in a column, whereas  
COUNT(\*) or COUNT(1) counts all rows, including those with NULLS  
🔹 main aggregate functions ignore such SUM, COUNT, MIN, MAX, AVG ignore rows with NULLS; NULL is not the smallest value, it's just NULL, but  
🔹 ORDER by shows NULLS first by default when sorting ascending  
🔹 since a NULL not equal (not even comparable) to another NULL, upon joining, NULL values are not going to be matched

You can handle NULLS with:  
🔹 x IS NULL/ IS NOT NULL : checks if something is or is not a NULL  
🔹 COALESCE: take first non-null value in a list of values  
🔹 IFNULL/ISNULL: if null, use a backup value  
🔹 NULLIF: replace this value with a NULL

```sql
WITH source_a AS (

  SELECT 1 AS order_id, 'UK' AS country
  UNION ALL
  SELECT 2 AS order_id, 'US' AS country
  UNION ALL
  SELECT NULL AS order_id, 'FR' AS country
),
source_b AS (

  SELECT 1 AS order_id, 'apples' AS product
  UNION ALL
  SELECT 2 AS order_id, 'peaches' AS product
  UNION ALL
  SELECT NULL AS order_id, 'grapes' AS products

)
SELECT
order_id, country, product

FROM source_a
FULL OUTER JOIN source_b USING(order_id)
```

![BigQuery results: order\_id 1 is UK with apples and 2 is US with peaches; the NULL keys don't match, so row 3 is FR with a null product and row 4 is grapes with a null order\_id and country.](/images/a-couple-of-fun-things-about-null-in-sql/1-result.jpg)

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Not all NULLS are the same](/not-all-nulls-are-the-same)
- [COALESCE vs IFNULL vs NULLIF in BigQuery](/coalesce-vs-ifnull-vs-nullif-in-bigquery)
- [Null-safe comparison: IS DISTINCT/NOT DISTINCT FROM](/null-safe-comparison-is-distinctnot-distinct-from)
- [Controlling ordering of NULL values in the ORDER BY clause](/controlling-ordering-of-null-values-in-the-order-by-clause)
