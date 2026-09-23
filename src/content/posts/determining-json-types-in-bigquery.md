---
title: "Determining JSON types in BigQuery"
seoTitle: "BigQuery JSON_TYPE Function: Detect JSON Value Types"
seoDescription: "JSON_TYPE in BigQuery returns the type of a JSON value — object, array, string, number, boolean, or null — as a STRING."
datePublished: 2024-06-22T09:00:46.803Z
dateUpdated: 2026-03-02T10:52:21.729Z
cover: "/images/determining-json-types-in-bigquery/cover.jpg"
coverCredit:
  name: "Pankaj Patel"
  url: "https://unsplash.com/@pankajpatel"
series: "bigquery-json"
hashnodeCuid: "clxpw3w43000f08l9dovqakvv"
---

Here's a mildly interesting function if you're working with JSON in BigQuery.

JSON\_TYPE takes in a JSON value and returns the name of the respective JSON type (object, array, string, number, boolean, null) as a STRING.

See below an illustration of it in action.

Also, given we use the native JSON datatype, notice how we can just access the first (\[0\]) element in an ARRAY or a field directly by dot notation.  
This you cannot do with a JSON-like STRING (not without parsing). Check out my [previous post about JSON vs JSON-like string](/json-datatype-vs-json-like-string-in-bigquery).

```sql
DECLARE json_data  DEFAULT JSON
"""
[
 {"city": "New York", "age": 25,"name": "John Doe", "registered_footballer": true },
 {"city": "London", "age": 21, "name": "Jane Dew", "registered_footballer": false},
 {"city": "Berlin", "age": 30, "name": "Joanna Dow", "registered_footballer": true},
 {"city": "Prague", "age": 28, "name": "Johann Duw", "registered_footballer": false}
]
""";

SELECT

  JSON_TYPE(json_data), -- array,
  JSON_TYPE(json_data[0]), -- object,
  JSON_TYPE(json_data[0].name), -- string,
  JSON_TYPE(json_data[0].age), -- number,
  JSON_TYPE(json_data[0].registered_footballer) --boolean
```

![BigQuery results: one row with f0\_ array, f1\_ object, f2\_ string, f3\_ number and f4\_ boolean.](/images/determining-json-types-in-bigquery/1-result.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [The JSON datatype in BigQuery](/the-json-datatype-in-bigquery)
- [JSON datatype vs JSON-like STRING in BigQuery](/json-datatype-vs-json-like-string-in-bigquery)
- [Flattening JSON arrays in BigQuery](/flattening-json-arrays-in-bigquery)
- [Extracting keys from JSON in BigQuery](/extracting-keys-from-json-in-bigquery)
