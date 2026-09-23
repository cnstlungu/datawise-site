---
title: "Using ARRAY_AGG in BigQuery"
seoTitle: "BigQuery ARRAY_AGG: Collapse Rows into Nested Arrays"
seoDescription: "ARRAY_AGG collapses multiple rows into one array per group. Control it with ORDER BY, DISTINCT, LIMIT, and STRUCT to shape exactly the output you need."
datePublished: 2023-11-07T22:46:08.974Z
dateUpdated: 2026-03-02T10:16:26.457Z
cover: "/images/using-array-agg-in-bigquery/cover.jpg"
coverCredit:
  name: "Rubén Bagüés"
  url: "https://unsplash.com/@rubavi78"
series: "bigquery-arrays-and-structs"
hashnodeCuid: "cloox73ny000308jn85ee6x4c"
---

Almost everybody knows the usual standard SQL aggregation functions like SUM, MAX or AVG. In this short post, we're going to look at ARRAY\_AGG: another useful aggregation function.

So, what does it do?

ARRAY\_AGG allows us to aggregate multiple rows into a single array, based on a particular grouping. It's quite useful when modeling one-to-many relationships, like customers and orders.

For example, let's analyze the following input table.

![](/images/using-array-agg-in-bigquery/1.png)

Let's say we'd like to aggregate the order data into an ARRAY of STRUCTs, grouped by customer\_id. Let's also order the resulting array decreasingly by the order\_total .

The code to do that would look as follows:

```sql

SELECT 

  customer_id, 
  ARRAY_AGG( STRUCT(order_id, order_total ) ORDER BY order_total DESC) AS order_details

FROM input_data

GROUP BY customer_id
```

Here's how the processed data looks like:

![](/images/using-array-agg-in-bigquery/2.png)

We can now see that instead of the 6 initial rows, we have 2 rows - 1 per customer\_id and an array of STRUCTS with order details.

Note that ARRAY\_AGG can be combined with:  
\- DISTINCT, to eliminate duplicates in the resulting ARRAY  
\- STRUCT, to create an ARRAY of STRUCTS  
\- ORDER BY, to order the ARRAY in a particular way  
\- LIMIT, to keep only first n entries (based on the ordering)

Thanks for reading!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [UNNESTING ARRAYS in BigQuery](/unnesting-arrays-in-bigquery)
- [Leveraging ARRAYS in BigQuery for query performance](/leveraging-arrays-in-bigquery-for-query-performance)
- [Accessing ARRAY elements in BigQuery](/accessing-array-elements-in-bigquery)
- [Enumerating ARRAY elements in BigQuery using WITH OFFSET](/enumerating-array-elements-in-bigquery-using-with-offset)
