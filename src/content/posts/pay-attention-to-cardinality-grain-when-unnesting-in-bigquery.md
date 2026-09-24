---
title: "Pay attention to cardinality & grain when UNNESTING in BigQuery!"
seoTitle: "BigQuery UNNEST Multiple Arrays: Avoid Cartesian Products"
seoDescription: "UNNESTing two unrelated arrays in the same BigQuery query produces a Cartesian product, multiplying row counts unexpectedly."
datePublished: 2024-04-19T14:39:41.889Z
dateUpdated: 2026-03-02T10:51:39.138Z
cover: "/images/pay-attention-to-cardinality-grain-when-unnesting-in-bigquery/cover.jpg"
coverCredit:
  name: "Joshua Tsu"
  url: "https://unsplash.com/@joshdatsu"
series: "bigquery-arrays-and-structs"
hashnodeCuid: "clv6s183l000209l22r61bqua"
---

Whenever you're UNNESing an ARRAY, you're getting a Cartesian product between the row and the array contents. If you were to unnest another array, you'll get another Cartesian product between the output of the previous unnest and the elements in the current array.

Let's look at an example. A student has their grades stored in an ARRAY as well as their food allergies in another ARRAY.

If we are to UNNEST both array we'll end having count\_of\_grades x count\_of\_allergies rows for each student, 4x3 in this case.

Why this happens? Well the allergies and grades have no relationship between each other, they just refer to the same student row.

Take this into account when you're working with nested data.

```sql
SELECT
  'Joe Doe' AS name,
  [90, 58, 50, 100] AS grades,
  ['gluten','milk', 'eggs'] AS allergies
```

![BigQuery results: one row for Joe Doe with the grades array 90, 58, 50, 100 and the allergies array gluten, milk, eggs.](/images/pay-attention-to-cardinality-grain-when-unnesting-in-bigquery/1-result.jpg)

```sql
SELECT
  name,
  grade,
  food_allergy
FROM input_data

LEFT JOIN UNNEST(grades) AS grade
LEFT JOIN UNNEST(allergies) AS food_allergy
```

![BigQuery results: 12 rows for Joe Doe, pairing each grade (90, 58, 50, 100) with each food\_allergy (gluten, milk, eggs).](/images/pay-attention-to-cardinality-grain-when-unnesting-in-bigquery/1-result-2.jpg)

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using ARRAY_AGG in BigQuery](/using-array-agg-in-bigquery)
- [UNNESTING ARRAYS in BigQuery](/unnesting-arrays-in-bigquery)
- [Leveraging ARRAYS in BigQuery for query performance](/leveraging-arrays-in-bigquery-for-query-performance)
- [Accessing ARRAY elements in BigQuery](/accessing-array-elements-in-bigquery)
