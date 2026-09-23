---
title: "Extracting keys from JSON in BigQuery"
seoTitle: "BigQuery JSON_KEYS: Extract Keys from JSON Dynamically"
seoDescription: "JSON_KEYS() in BigQuery returns an array of field names from a JSON string. Control depth and key inclusion with the mode and max_depth arguments."
datePublished: 2024-10-27T12:20:49.351Z
dateUpdated: 2026-03-02T10:22:29.978Z
cover: "/images/extracting-keys-from-json-in-bigquery/cover.jpg"
coverCredit:
  name: "Aaron Burden"
  url: "https://unsplash.com/@aaronburden"
series: "bigquery-json"
hashnodeCuid: "cm2rk6c07000409l7dvpral40"
---

[A couple of months ago](/dynamically-extracting-json-data-in-bigquery), I've posted about dynamically extracting key-value pairs from JSON in BigQuery SQL which leveraged regex (check comments).

Shortly after that post, we've gotten a new built-in function to dynamically extract the keys occurring in a JSON. It allows us to retrieve all the keys occurring in a JSON value, with a few controls on how this is done.

The function is JSON\_KEYS. Apart from the json input, we can tweak:  
\- max\_depth: for many levels of nesting we should go through to extract keys  
\- mode: strict/lax/lax recursive - controls if we extract keys from arrays.

The usual note - still in preview.

![](/images/extracting-keys-from-json-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [https://www.notjustsql.com](https://www.notjustsql.com/)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [The JSON datatype in BigQuery](/the-json-datatype-in-bigquery)
- [JSON datatype vs JSON-like STRING in BigQuery](/json-datatype-vs-json-like-string-in-bigquery)
- [Flattening JSON arrays in BigQuery](/flattening-json-arrays-in-bigquery)
- [LAX JSON conversion functions in BigQuery](/lax-json-conversion-functions-in-bigquery)
