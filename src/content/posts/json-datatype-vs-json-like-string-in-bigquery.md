---
title: "JSON datatype vs JSON-like STRING in BigQuery"
seoTitle: "BigQuery JSON Type vs STRING: What Changes and Why It Matters"
seoDescription: "BigQuery handles native JSON and JSON-formatted STRING values differently. Learn what changes in validation, parsing, and function behavior."
datePublished: 2024-05-07T13:19:46.299Z
dateUpdated: 2026-04-28T08:37:12.106Z
cover: "/images/json-datatype-vs-json-like-string-in-bigquery/cover.jpg"
coverCredit:
  name: "Michael Dziedzic"
  url: "https://unsplash.com/@lazycreekimages"
series: "bigquery-json"
hashnodeCuid: "clvwf3rsr000b09jthofy0499"
---

In [one my previous posts](/the-json-datatype-in-bigquery), we've briefly introduced the JSON datatype in BigQuery.

But did anyone notice how most of the JSON functions have signatures for both a JSON-type input and a json-formatted string input?

What is the difference between the two?

Well, I like to call the json-formatted STRING a "json-like string" because while it might look like it, it's not necessarily valid JSON.

When you use, say, JSON\_VALUE to query such a string, it does not validate it and reads it from the start until (and if) it finds the key matching your query. It does not care that you gave it invalid JSON.

In the example below, the json-formatted/json-like string is missing a closing bracket "}", but JSON\_VALUE using it still manages to retrieve the 'key' since it never reaches the missing bracket .

```sql
DECLARE native_json DEFAULT  JSON
"""
{"key": "value"}
"""
;

DECLARE json_formatted_string STRING DEFAULT "{\"key\": \"value\"";



SELECT
  JSON_VALUE(native_json, '$.key') AS value_from_native,
  JSON_VALUE(json_formatted_string, '$.key') AS value_from_json_like_string
```

![BigQuery results: value\_from\_native and value\_from\_json\_like\_string both return value.](/images/json-datatype-vs-json-like-string-in-bigquery/1-result.jpg)

---

*Enjoyed this? Here are some related articles you might find useful:*

- [The JSON datatype in BigQuery](/the-json-datatype-in-bigquery)
- [Flattening JSON arrays in BigQuery](/flattening-json-arrays-in-bigquery)
- [Extracting keys from JSON in BigQuery](/extracting-keys-from-json-in-bigquery)
- [LAX JSON conversion functions in BigQuery](/lax-json-conversion-functions-in-bigquery)
