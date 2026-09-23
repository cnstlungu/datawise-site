---
title: "The JSON datatype in BigQuery"
seoTitle: "BigQuery JSON Data Type: How to Create and Store JSON"
seoDescription: "BigQuery's native JSON data type is not just a string — it enables structured access via JSON functions and stores heterogeneous data in one column."
datePublished: 2024-05-02T21:30:28.484Z
dateUpdated: 2026-03-02T10:52:40.705Z
cover: "/images/the-json-datatype-in-bigquery/cover.jpg"
coverCredit:
  name: "Alexander Sinn"
  url: "https://unsplash.com/@swimstaralex"
series: "bigquery-json"
hashnodeCuid: "clvprfk77000008l3fc117zlk"
---

The JSON datatype in BigQuery. This topic has been sitting in my Notion list of post ideas for some time.

So in our beloved BQ it is a native, standalone data type, not just another STRING 😁, although strings can of course hold json-like strings.

As data engineers we typically consume them in our pipelines, but let's first understand how to create them.

There are a couple of ways to express a JSON value:  
\- using the JSON literal  
\- by parsing a json-like STRING with JSON\_PARSE()  
\- from SQL objects (including an entire row) with TO\_JSON()  
\- creating a json\_object from key-value pairs with JSON\_OBJECT()  
\- creating a JSON\_ARRAY() from BQ ARRAY

Note that, for some of the above options, since JSON also have quotes, use multi-line strings """ """ or escape quotes with \\.

Defining our JSON objects as such will allow us to use JSON functions with them and, of course, store heterogeneous data in the same column.

Stay tuned for the next posts on this topic.

```sql
WITH input_data AS (

SELECT

  JSON """
      {"name": "John Doe",
      "city": "New York",
      "sports": ["football", "snooker", "tennis"]}
  """
  AS json_native,

  "{\"name\": \"John Doe\", \"city\": \"New York\", \"sports\": [\"football\", \"snooker\", \"tennis\"]}" AS json_string,

  "John Doe" AS name,
  "New York" AS city,
  ["football", "snooker", "tennis"] AS sports
)

SELECT
  json_native,
  PARSE_JSON(json_string) AS parsed_json_from_string,
  TO_JSON(STRUCT(name, city, sports)) AS json_from_key_values,
  JSON_OBJECT('name', name, 'city', city, 'sports', sports) AS json_object_from_key_value_pairs,
  JSON_ARRAY(sports) AS json_array_from_array

FROM  input_data
```

![BigQuery results: json\_native, parsed\_json\_from\_string, json\_from\_key\_values and json\_object\_from\_key\_value\_pairs all hold {"city":"New York","name":"John Doe","sports":\["football","snooker","tennis"\]}, and json\_array\_from\_array is \[\["football","snooker","tennis"\]\].](/images/the-json-datatype-in-bigquery/1-result.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [JSON datatype vs JSON-like STRING in BigQuery](/json-datatype-vs-json-like-string-in-bigquery)
- [Flattening JSON arrays in BigQuery](/flattening-json-arrays-in-bigquery)
- [Extracting keys from JSON in BigQuery](/extracting-keys-from-json-in-bigquery)
- [LAX JSON conversion functions in BigQuery](/lax-json-conversion-functions-in-bigquery)
