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

![](/images/sometimes-you-have-to-use-subqueries/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [https://www.notjustsql.com](https://www.notjustsql.com/)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Beware of ROW_NUMBER without ORDER BY](/beware-of-rownumber-without-order-by)
- [Tidying up WINDOW functions in BigQuery with named windows](/tidying-up-window-functions-in-bigquery-with-named-windows)
- [Using RANGE in Window Functions in BigQuery](/using-range-in-window-functions-in-bigquery)
- [Computing a cumulative sum in BigQuery](/computing-a-cumulative-sum-in-bigquery)
