---
title: "The relationship between ARRAY_AGG and UNNEST"
seoTitle: "BigQuery ARRAY_AGG and UNNEST Explained with Simple Examples"
seoDescription: "ARRAY_AGG turns rows into arrays, and UNNEST turns arrays back into rows. Learn how they work together in BigQuery with clear examples."
datePublished: 2024-06-08T18:26:00.141Z
dateUpdated: 2026-04-28T08:33:46.606Z
cover: "/images/the-relationship-between-arrayagg-and-unnest/cover.jpg"
coverCredit:
  name: "Pawel Czerwinski"
  url: "https://unsplash.com/@pawel_czerwinski"
series: "bigquery-arrays-and-structs"
hashnodeCuid: "clx6g4uh900000ajm1u87d5dg"
---

If you're working with nested data in BigQuery, you've might've seen UNNEST, which helps 'unpack' arrays into individual rows.

But there's also ARRAY\_AGG, which, if you haven't encountered it before, which takes all rows for your GROUP BY bucket and creates an ARRAY out of them.

So, in essence, ARRAY\_AGG and UNNEST are doing the exact opposite of each other.

Check my previous posts on the topic:

* [Unnesting ARRAYS in BigQuery](/unnesting-arrays-in-bigquery)
    
* [Using ARRAY\_AGG in BigQuery](/using-array-agg-in-bigquery)
    
    ![](/images/the-relationship-between-arrayagg-and-unnest/1.jpg)
    
    *Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Flattening JSON arrays in BigQuery](/flattening-json-arrays-in-bigquery)
