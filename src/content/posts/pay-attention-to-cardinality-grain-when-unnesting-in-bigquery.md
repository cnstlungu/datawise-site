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

![BigQuery SQL for student Joe Doe with a grades ARRAY of 4 values and an allergies ARRAY of 3; unnesting both with LEFT JOIN UNNEST(grades) AS grade and LEFT JOIN UNNEST(allergies) AS food\_allergy returns 12 rows, pairing every grade with every allergy.](/images/pay-attention-to-cardinality-grain-when-unnesting-in-bigquery/1.jpg)

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using ARRAY_AGG in BigQuery](/using-array-agg-in-bigquery)
- [UNNESTING ARRAYS in BigQuery](/unnesting-arrays-in-bigquery)
- [Leveraging ARRAYS in BigQuery for query performance](/leveraging-arrays-in-bigquery-for-query-performance)
- [Accessing ARRAY elements in BigQuery](/accessing-array-elements-in-bigquery)
