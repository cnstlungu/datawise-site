---
title: "Query parameters in BigQuery"
seoTitle: "BigQuery Query Parameters: Parameterize Your SQL Safely"
seoDescription: "Query parameters in BigQuery let you pass values into SQL safely without string concatenation, preventing injection and enabling query plan caching."
datePublished: 2024-07-06T07:00:56.989Z
dateUpdated: 2026-04-05T20:11:09.486Z
cover: "/images/query-parameters-in-bigquery/cover.jpg"
coverCredit:
  name: "Martin Woortman"
  url: "https://unsplash.com/@martfoto1"
series: "practical-sql"
hashnodeCuid: "cly9rzpr100020akweej93gdq"
---

Query parameters in BigQuery. You need to know about them if you're constructing queries based on user input. What do they do?

They can help secure your query against SQL injection and can be recognized by the @ (for named usage) and ? (for positional usage).

Unlike variables, with whom we should not confound them, one cannot use them in the console (web IDE), but only with bq command line interface, API or client libraries.

You can ✅ :  
\- use parameters for expressions  
\- provide a datatype for the query parameter or omit it with STRING as default  
\- use complex types such as ARRAY or STRUCT

But you cannot ❌ :  
\- pass parameters as column or table names  
\- use positional AND named parameters at the same time

![Terminal running bq query --use\_legacy\_sql=false with named query parameters --parameter=input\_value:INT64:1 and --parameter=input\_date:DATE:2020-12-18, used as @input\_value and @input\_date in a SELECT on learning.data\_source; the output lists six id values.](/images/query-parameters-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Parameters in BigQuery](/parameters-in-bigquery)
