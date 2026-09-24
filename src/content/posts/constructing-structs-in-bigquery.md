---
title: "Constructing STRUCTS in BigQuery"
subtitle: ""
seoTitle: "Constructing BigQuery STRUCTs: Tuple, Untyped, and Typed"
seoDescription: "BigQuery has three STRUCT syntax forms: tuple, untyped STRUCT(), and typed STRUCT<T>. Learn when to use each and why field order matters in comparisons."
datePublished: 2024-04-19T14:36:26.114Z
dateUpdated: 2026-03-02T10:22:32.244Z
cover: "/images/constructing-structs-in-bigquery/cover.jpg"
coverCredit:
  name: "Ben Allan"
  url: "https://unsplash.com/@ballonandon"
series: "bigquery-arrays-and-structs"
hashnodeCuid: "clv6rx11e001309mk01dz154q"
---

After my previous [STRUCTS in BigQuery post](/understanding-structs-in-bigquery), I could not have skipped to mention number of options when it comes to construct one.

You can choose whether to provide field type, field name or both.

There's 3 main ways:  
\- via tuple `('a', 1)` - BQ creates a STRUCT and infers the field types from provided values  
\- untyped `STRUCT('a', 1)` - untyped here means you'd don't declare the type, but it is rather inferred from the value literal or the column provided as input  
\- typed `STRUCT<STRING, INT64) ('a',1)` - you declare the types of the fields in the structs

There's a couple of things to be kept in mind.

➡ If you don't provide a field name it would be an anonymous field, meaning you won't be able to access it by field name  
➡ If you want explicit types + field names you need to declare the field names together with the types

⚠ Watch out: ordering of fields matters in a STRUCT, so for example

```sql
SELECT STRUCT(1 AS a, 2 AS b)
UNION ALL
SELECT STRUCT (2 as b, 1 as a)
```

won't match fields according to names!

<!-- missing image, source no longer available: https://media.licdn.com/dms/image/v2/D4D22AQGuwPsLsBbj-w/feedshare-shrink_2048_1536/feedshare-shrink_2048_1536/0/1713343102449?e=1742428800&v=beta&t=SYAdTDN081i7i8TTHFdSQGW0akSoegTMxz79F9NEQiY -->

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Understanding STRUCTS in BigQuery](/understanding-structs-in-bigquery)
- [Using STRUCTS for quick analysis in BigQuery](/using-structs-for-quick-analysis-in-bigquery)
- [Using STRUCTS for Audit Fields in BigQuery](/using-structs-for-audit-fields-in-bigquery)
- [Using LAST_VALUE with STRUCTS](/using-lastvalue-with-structs)
