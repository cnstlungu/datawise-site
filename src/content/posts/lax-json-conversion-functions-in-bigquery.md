---
title: "LAX JSON conversion functions in BigQuery"
seoTitle: "BigQuery LAX JSON Functions: Safe Type Conversion"
seoDescription: "LAX_STRING, LAX_BOOL, LAX_FLOAT64, and LAX_INT64 convert JSON values to SQL types without throwing errors on failure."
datePublished: 2024-06-22T21:00:44.306Z
dateUpdated: 2026-03-02T10:51:35.743Z
cover: "/images/lax-json-conversion-functions-in-bigquery/cover.jpg"
coverCredit:
  name: "David Hunter"
  url: "https://unsplash.com/@fla5h904"
series: "bigquery-json"
hashnodeCuid: "clxqltriq00000aky9esd4z9w"
---

So if you're looking to decompress after a long week and relax, check out the LAX conversion functions for handling JSON conversions in BigQuery.

There are 4 separate functions: `LAX_STRING`, `LAX_BOOL`, `LAX_FLOAT64`, `LAX_INT64` - with each one of them attempting to convert a JSON value into the respective datatype.

This is a bit like using SAFE\_CAST - you won't get an error if the casting fails, just a NULL (so watch out, check the comments for an example when this can come to back to bite you).

Just note that even JSON-like string won't work as an input, it only works for the native JSON type.

As usual, watch out because these conversion functions might work differently as how you'd expect. SAFE\_CAST('1' AS BOOL) =&gt; NULL but SAFE\_CAST(1 AS BOOL) =&gt; TRUE.

![BigQuery SQL declaring an ARRAY\<JSON\> of fruits with loosely typed fields and reading them via UNNEST with LAX\_STRING, LAX\_BOOL, LAX\_FLOAT64 and LAX\_INT64; string "7.1" becomes 7.1, 1/0 and "TRUE"/"false" become booleans, and an empty string is\_local gives null.](/images/lax-json-conversion-functions-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [The JSON datatype in BigQuery](/the-json-datatype-in-bigquery)
- [JSON datatype vs JSON-like STRING in BigQuery](/json-datatype-vs-json-like-string-in-bigquery)
- [Flattening JSON arrays in BigQuery](/flattening-json-arrays-in-bigquery)
- [Extracting keys from JSON in BigQuery](/extracting-keys-from-json-in-bigquery)
