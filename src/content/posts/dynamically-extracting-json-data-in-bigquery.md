---
title: "Dynamically extracting JSON data in BigQuery"
seoTitle: "BigQuery Dynamic JSON Extraction: Key-Value Pairs with Regex"
seoDescription: "Extract dynamic key-value pairs from JSON in BigQuery when the schema varies per row. Uses JSON_EXTRACT and regex to handle heterogeneous JSON structures."
datePublished: 2024-08-09T09:00:08.892Z
dateUpdated: 2026-03-02T10:22:47.893Z
cover: "/images/dynamically-extracting-json-data-in-bigquery/cover.jpg"
coverCredit:
  name: "Dirk Jutzas"
  url: "https://unsplash.com/@dirk_0815"
series: "bigquery-json"
hashnodeCuid: "clzmh7yv000030ajz9k0a03na"
---

I was asked today about dynamically extracting key-value pairs from heterogeneous JSON-like strings in BigQuery SQL and I've remembered this interesting approach I've seen a while ago.

It leverages regular expressions, one of everyone's favorites, I know.

This allows extraction of key-value pairs from each JSON-like string, even if they are don't look the same.

Kudos to someone on Stack Overflow where I've first seen it.

Pretty sure the regex can be streamlined, but that's as much me feat. GPT could do today.

PS. If we're talking about JSON datatype, you can transform it to JSON-like STRING with TO\_JSON\_STRING() and do the same thing.

![BigQuery SQL turning JSON-like strings with varying keys into rows: REGEXP\_REPLACE strips braces and quotes, SPLIT plus LEFT JOIN UNNEST yields kv pairs, and REGEXP\_EXTRACT pulls key and value; results list id 1 key\_1=1, key\_3=3 and id 2 key\_99=2, key\_4=4.](/images/dynamically-extracting-json-data-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [The JSON datatype in BigQuery](/the-json-datatype-in-bigquery)
- [JSON datatype vs JSON-like STRING in BigQuery](/json-datatype-vs-json-like-string-in-bigquery)
- [Flattening JSON arrays in BigQuery](/flattening-json-arrays-in-bigquery)
- [Extracting keys from JSON in BigQuery](/extracting-keys-from-json-in-bigquery)
