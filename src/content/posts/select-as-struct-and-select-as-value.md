---
title: "SELECT AS STRUCT and SELECT AS VALUE"
seoTitle: "SELECT AS STRUCT and SELECT AS VALUE in BigQuery"
seoDescription: "Explains the difference between SELECT AS STRUCT and SELECT AS VALUE in BigQuery and when to use each. Covers value tables, UNNEST scenarios, and using..."
datePublished: 2023-12-05T22:56:05.014Z
dateUpdated: 2026-03-02T10:51:41.347Z
cover: "/images/select-as-struct-and-select-as-value/cover.jpg"
coverCredit:
  name: "Greg Rosenke"
  url: "https://unsplash.com/@greg_rosenke"
series: "bigquery-arrays-and-structs"
hashnodeCuid: "clpsxvq8m000008l6bexeajyw"
---

Ever heard about value tables in BigQuery? Well, neither have I, until I've seen them mentioned in the docs. So, while in a normal table, a row is made up of columns, in a value table the row is a STRUCT.

Say you UNNEST `order_lines` AS order\_line. The 'order\_line' here is a value table.

Now, with this out of the way, let's see how it is useful, we need to introduce `SELECT AS STRUCT` and `SELECT AS VALUE`.

➡ `SELECT AS STRUCT` - produces a value table but preserves the STRUCT type i.e. you're still going to have order\_line.product\_id or order\_line.unit\_price

➡ `SELECT AS VALUE` - produces a value table by unpacking the struct values

When can these be useful?

☑ You have a STRUCT with a lot of attributes and don't want to reference them manually  
☑ You want to create a separate table out of the values in a STRUCT, without unpacking each column  
☑ Use this as input for creating an array of STRUCTS  
☑ You're using ARRAY\_AGG to de-duplicate (see example in comments).

See below for an illustration of the differences between the two.

![BigQuery SQL value tables infographic: SELECT AS VALUE order\_line and SELECT AS STRUCT order\_line FROM input\_data LEFT JOIN UNNEST(order\_lines), applied to orders with nested order lines; both yield product\_id, order\_quantity and unit\_price rows, but the STRUCT result keeps a nested column prefix.](/images/select-as-struct-and-select-as-value/1.png)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Understanding STRUCTS in BigQuery](/understanding-structs-in-bigquery)
- [Constructing STRUCTS in BigQuery](/constructing-structs-in-bigquery)
- [Using STRUCTS for quick analysis in BigQuery](/using-structs-for-quick-analysis-in-bigquery)
- [Using STRUCTS for Audit Fields in BigQuery](/using-structs-for-audit-fields-in-bigquery)
