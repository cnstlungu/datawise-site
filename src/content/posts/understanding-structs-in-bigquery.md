---
title: "Understanding STRUCTS in BigQuery"
seoTitle: "BigQuery STRUCT vs ARRAY: Differences and When to Use Each"
seoDescription: "BigQuery STRUCTs group named fields of mixed types into one column. Learn to create them with STRUCT(), access nested fields, and UNNEST arrays of STRUCTs."
datePublished: 2024-04-19T13:56:31.766Z
dateUpdated: 2026-03-02T10:16:29.747Z
cover: "/images/understanding-structs-in-bigquery/cover.jpg"
coverCredit:
  name: "Greg Rosenke"
  url: "https://unsplash.com/@greg_rosenke"
series: "bigquery-arrays-and-structs"
hashnodeCuid: "clv6qhpjp000208mlgvmj9305"
---

I've previously did a [short intro post about ARRAYS](/unnesting-arrays-in-bigquery) in BigQuery, but I do see from time to time people that are just getting started become confused about how are they different from STRUCTS and when should we use them.

Let's clarify this.

STRUCT = a bundle of "columns" inside a single column. STRUCTS fields have a mandatory data type (inferred or declared by you) and an optional name. You're still having one instance of each field, but this field can be an ARRAY of multiple things.

ARRAY = a bundle of "rows", a list inside a single row. They NEED to be of the same type - INT64, STRING, STRUCT etc. They cannot have another ARRAY directly under them, but you can get around that with an ARRAY(STRUCT(\[array\_inside\_struct\])

You can still combine the two as you want, nest them in multiple layers, as long as you don't have an ARRAY directly under another ARRAY.

Both of them you can compare but you cannot order by or group by.  
For STRUCT, you can totally ORDER BY or GROUP BY one of the fields in the STRUCT (as long as it's not a STRUCT or ARRAY itself).

When to use each? Let's look an example.

![](/images/understanding-structs-in-bigquery/1.jpg)

STRUCT = a bundle of fields that relate to the same "thing" - say your current address - city, street name, postal\_code etc. Helps with a cleaner, more intuitive schema. `TYPE = RECORD, MODE = NULLABLE`

ARRAY = a list of things (0, 1 or more) that are related to this observation, for example a list of instruments a person plays on. `TYPE = your_data_type, MODE = REPEATED`

ARRAY of STRUCTS = you have a list of "things" that you know multiple things about and want to keep the together i.e. certifications =&gt; (name, from\_date).  
Would also be good to store all them addresses a person ever had. `TYPE = RECORD, MODE = REPEATED`

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Constructing STRUCTS in BigQuery](/constructing-structs-in-bigquery)
- [Using STRUCTS for quick analysis in BigQuery](/using-structs-for-quick-analysis-in-bigquery)
- [Using STRUCTS for Audit Fields in BigQuery](/using-structs-for-audit-fields-in-bigquery)
- [Using LAST_VALUE with STRUCTS](/using-lastvalue-with-structs)
