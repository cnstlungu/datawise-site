---
title: "Flattening JSON arrays in BigQuery"
seoTitle: "Simplify JSON Arrays in BigQuery"
seoDescription: "Learn how to use BigQuery's JSON_FLATTEN to handle complex JSON arrays efficiently without losing data context when hierarchy isn't important"
datePublished: 2025-12-07T12:57:58.463Z
dateUpdated: 2026-03-02T10:52:51.711Z
cover: "/images/flattening-json-arrays-in-bigquery/cover.jpg"
coverCredit:
  name: "Jean-Luc Crucifix"
  url: "https://unsplash.com/@jlcrcfx"
series: "bigquery-arrays-and-structs"
hashnodeCuid: "cmivq9ynz000002ihgu7shw4o"
---

I've noticed that a new JSON function has been added (in Preview) in BigQuery SQL - JSON\_FLATTEN().

It allows us to flatten JSON arrays and return a single flat ARRAY, no matter how many nested levels there are.

So where is this actually useful?  
➡️ Handling heterogeneous JSON where the nesting depth isn’t consistent  
➡️ Cleaning up malformed or jagged arrays  
➡️ Normalizing data before UNNEST so you don’t get arrays of arrays

Where I would not use it?

👉 Don’t use it when the hierarchy matters. Flattening removes structural context, so you lose information about where an element came from.

```sql
SELECT JSON_FLATTEN(JSON '[1, [2,3,4],[[5,6],[7,8]]]' )
```

![BigQuery results: a single row whose f0\_ value is the flat array 1, 2, 3, 4, 5, 6, 7, 8.](/images/flattening-json-arrays-in-bigquery/1-result.jpg)

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [The JSON datatype in BigQuery](/the-json-datatype-in-bigquery)
- [JSON datatype vs JSON-like STRING in BigQuery](/json-datatype-vs-json-like-string-in-bigquery)
- [Extracting keys from JSON in BigQuery](/extracting-keys-from-json-in-bigquery)
- [LAX JSON conversion functions in BigQuery](/lax-json-conversion-functions-in-bigquery)
