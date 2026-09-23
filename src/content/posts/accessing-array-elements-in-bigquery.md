---
title: "Accessing ARRAY elements in BigQuery"
seoTitle: "BigQuery Array Access: OFFSET, ORDINAL, SAFE_OFFSET, SAFE_ORDINAL"
seoDescription: "Access BigQuery arrays with OFFSET or ORDINAL, and use SAFE_OFFSET or SAFE_ORDINAL to return NULL instead of failing on out-of-bounds indexes."
datePublished: 2024-03-31T15:41:50.257Z
dateUpdated: 2026-04-28T08:37:16.914Z
cover: "/images/accessing-array-elements-in-bigquery/cover.jpg"
coverCredit:
  name: "JJ Ying"
  url: "https://unsplash.com/@jjying"
series: "bigquery-arrays-and-structs"
hashnodeCuid: "clufovy9d000108l2bzv3gn9t"
---

So here's 3 ways we can access elements in a BigQuery array.

\- by index: array\[index\], starting at 0  
\- using OFFSET(index): array\[OFFSET(index)\], also starting at 0  
\- using ORDINAL(1-based index)), starting at 1

The above will return an "index out of range" error if they are out of bounds, so to get around that you can using SAFE\_OFFSET and SAFE\_ORDINAL.

If you'd like to see what position each elements resides at in the array, check [WITH OFFSET](/enumerating-array-elements-in-bigquery-using-with-offset).

```sql
WITH input_data AS (


  SELECT ['a','b','c','d','e'] AS letters
)

SELECT

  letters[ORDINAL(2)] AS second_with_ordinal, -- 1 based

  letters[1]  second_with_index, -- 0-based

  letters[OFFSET(1)] second_with_offest, --0-based

  letters[SAFE_OFFSET(5)]  AS sixth_with_safe_offset, -- 0-based, safe: returns NULL when out of bounds

  letters[SAFE_ORDINAL(6)] AS sixth_with_safe_ordinal -- 1-based, safe: returns NULL when out of bounds

FROM input_data
```

![BigQuery results: second\_with\_ordinal, second\_with\_index and second\_with\_offest are all b; sixth\_with\_safe\_offset and sixth\_with\_safe\_ordinal are null.](/images/accessing-array-elements-in-bigquery/1-result.png)

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using ARRAY_AGG in BigQuery](/using-array-agg-in-bigquery)
- [UNNESTING ARRAYS in BigQuery](/unnesting-arrays-in-bigquery)
- [Leveraging ARRAYS in BigQuery for query performance](/leveraging-arrays-in-bigquery-for-query-performance)
- [Enumerating ARRAY elements in BigQuery using WITH OFFSET](/enumerating-array-elements-in-bigquery-using-with-offset)
