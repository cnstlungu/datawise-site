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

```bash
bq query --use_legacy_sql=false \
--parameter=input_value:INT64:1 \
--parameter=input_date:DATE:2020-12-18 \
'SELECT id FROM learning.data_source WHERE value=@input_value AND ds_date=@input_date'
```

![Terminal output: an id column with six rows: 37, 94, 67, 60, 25 and 72.](/images/query-parameters-in-bigquery/1-output.jpg)

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Parameters in BigQuery](/parameters-in-bigquery)
