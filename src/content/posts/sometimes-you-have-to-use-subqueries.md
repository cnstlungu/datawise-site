---
title: "Sometimes, you have to use subqueries!"
seoTitle: "Embrace the Power of Subqueries!"
seoDescription: "Learn how to handle SQL subqueries to filter errors and construct arrays, even with NULL values in your database"
datePublished: 2024-11-01T15:40:11.977Z
dateUpdated: 2026-03-02T10:51:42.414Z
cover: "/images/sometimes-you-have-to-use-subqueries/cover.jpg"
coverCredit:
  name: "Rohit Choudhari"
  url: "https://unsplash.com/@iamrohitchoudhari"
series: "practical-sql"
hashnodeCuid: "cm2ywhzrd000a09kxhhzxayso"
---

Query without FROM clause cannot have a WHERE clause, goes the old SQL adage.

So I had this interesting problem the other day. Let's say an order has three boolean flags, each indicating whether a particular error has occurred during its lifetime. Our task is to create an array of all the errors that occurred for each order.

In order to solve it, we:  
\- create a scalar subquery  
\- since the flags can have the NULL value, we'd need to filter them out before passing them to the arrays constructor (which doesn't like nulls)  
\- create the array using the ARRAY () constructor

```sql
WITH input_data AS (

  SELECT 1 AS order_id, TRUE AS payment_error, FALSE AS fulfilment_error, TRUE AS delivery_error UNION ALL
  SELECT 2 AS order_id, FALSE AS payment_error, FALSE AS fulfilment_error, FALSE AS delivery_error UNION ALL
  SELECT 3 AS order_id, FALSE AS payment_error, TRUE AS fulfilment_error, NULL AS delivery_error UNION ALL
  SELECT 4 AS order_id, TRUE AS payment_error, TRUE AS fulfilment_error, NULL AS delivery_error
)

SELECT

  order_id,
  ARRAY(
    SELECT error_type

    FROM (
        SELECT payment_error AS has_error, "Payment" AS error_type
        UNION ALL
        SELECT delivery_error AS has_error, "Delivery" AS error_type
        UNION ALL
        SELECT fulfilment_error AS has_error, "Fulfilment" AS error_type
    ) errors

    WHERE has_error
  ) AS errors

FROM input_data
```

![BigQuery results: order 1 has errors Payment and Delivery, order 2 an empty array (0 rows), order 3 Fulfilment, and order 4 Payment and Fulfilment.](/images/sometimes-you-have-to-use-subqueries/1-result.jpg)

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Beware of ROW_NUMBER without ORDER BY](/beware-of-rownumber-without-order-by)
- [Tidying up WINDOW functions in BigQuery with named windows](/tidying-up-window-functions-in-bigquery-with-named-windows)
- [Using RANGE in Window Functions in BigQuery](/using-range-in-window-functions-in-bigquery)
- [Computing a cumulative sum in BigQuery](/computing-a-cumulative-sum-in-bigquery)
