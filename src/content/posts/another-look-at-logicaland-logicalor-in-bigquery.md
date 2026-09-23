---
title: "Another look at LOGICAL_AND & LOGICAL_OR in BigQuery"
seoTitle: "BigQuery LOGICAL_AND and LOGICAL_OR: Practical Examples"
seoDescription: "LOGICAL_AND and LOGICAL_OR in BigQuery aggregate boolean values across GROUP BY buckets or window partitions. Learn how to check if all or any rows meet a..."
datePublished: 2024-06-05T21:21:22.141Z
dateUpdated: 2026-03-02T10:50:21.185Z
cover: "/images/another-look-at-logicaland-logicalor-in-bigquery/cover.jpg"
coverCredit:
  name: "Roberto Sorin"
  url: "https://unsplash.com/@roberto_sorin"
series: "practical-sql"
hashnodeCuid: "clx2c2tb1000c0al75muh8nbw"
---

Out of all those non-standard SQL functions in BigQuery, I think I like LOGICAL\_AND and LOGICAL\_OR the most.  
  
These are aggregation functions I've posted about before (link in my comments), but just wanted to showcase how versatile they can be.  
  
So:  
\- LOGICAL\_OR = at least one value in the grouping bucket is TRUE.  
\- LOGICAL\_AND = all the values in the grouping bucket are TRUE.  
  
Plenty of stuff you can do with it:  
\- pair them with NOT when needed  
\- since they're aggregation functions, you compute a result for a bucket with GROUP BY or you can opt for using a window function call OVER (PARTITION BY ...)  
\- if you opt for GROUP BY, you can opt for filtering output with HAVING; whereas if you go through the window function route, you have QUALIFY for that matter  
  
In the example below, I'm looking to compute three things about customers:  
\- are all their orders are paid?  
\- do they have any outstanding orders (i.e. not shipped yet)?  
\- whether they have ordered olives in the last 3 months  
  
I make use of LOGICAL\_AND and LOGICAL\_OR for that.  
  
As usual, one can achieve the same results using MIN and MAX, since:  
\- MIN(\[TRUE,..., FALSE\]) = FALSE AND MAX(\[TRUE,..., FALSE\]) = MAX.

![Input data: an orders table with customer\_id, order\_id, order\_date, product\_id, is\_paid and is\_shipped. Customer 1 has orders 101 to 103 (tomatoes, cucumbers, and olives on 2024-03-01, not shipped); Customer 2 has orders 201 to 203 (olives, mangoes, and grapes on 2024-04-01, neither paid nor shipped).](/images/another-look-at-logicaland-logicalor-in-bigquery/1-input.jpg)

```sql
SELECT
  customer_id,
  LOGICAL_AND(is_paid) AS all_orders_paid,
  LOGICAL_OR(NOT is_shipped) AS outstanding_orders,
  LOGICAL_OR(product_id = 'olives' AND
             order_date > DATE_SUB(CURRENT_DATE(),
                                   INTERVAL 3 MONTH)) AS ordered_olives_last_3_months
FROM input_data

GROUP BY customer_id
```

![Query results: Customer 1 has all\_orders\_paid true, outstanding\_orders true and ordered\_olives\_last\_3\_months true; Customer 2 has false, true and false.](/images/another-look-at-logicaland-logicalor-in-bigquery/1-result.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*https://www.notjustsql.com*](https://www.notjustsql.com/)*.*
