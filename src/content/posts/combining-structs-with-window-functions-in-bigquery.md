---
title: "Combining STRUCTs with Window Functions in BigQuery"
seoTitle: "Use STRUCTs with LEAD/LAG in BigQuery Window Functions"
seoDescription: "Reduce repeated LEAD and LAG window function calls in BigQuery by wrapping multiple attributes into a STRUCT, then applying a single window function to..."
datePublished: 2023-10-18T17:30:12.805Z
dateUpdated: 2026-03-02T15:57:32.201Z
cover: "/images/combining-structs-with-window-functions-in-bigquery/cover.jpg"
coverCredit:
  name: "Alain Pham"
  url: "https://unsplash.com/@alain_pham"
series: "bigquery-window-functions"
hashnodeCuid: "clnw13rnp000409mj9fqs6nf0"
---

How often do you use STRUCTs in BigQuery? I do a lot, and here's an interesting use case.

### **First, what is a STRUCT?**

So, if you're not familiar with them, a STRUCT is a data type used to represent an object, allowing us to group related fields within one data cell.

Think of it as the ability to store complex 'things' inside a BigQuery row, in addition to the 'primitive' types like INT64 or STRING. So you can have a STRUCT '*person'* that has attributes like name, age and salary. This can of course be REPEATED to obtain an ARRAY of person STRUCTs.

Now, STRUCTs are useful for many things, one of which I'm going to present today.

Here is a trick I use when working with window functions like LEAD and LAG that involve STRUCTs in BigQuery.

### Problem statement

Did you ever have to retrieve the historical attribute (previous or next) of an entity in a temporal table (SCD-type 2)?

Here's how an example could look.

```sql
SELECT 
    id, 
    value_int, 
    value_text, 
    valid_from, 
    valid_to,
    LEAD(value_int) OVER (PARTITION BY id ORDER BY valid_from) AS next_value_int,
    LEAD(value_text) OVER (PARTITION BY id ORDER BY valid_from) AS next_value_text,
    LAG(value_int) OVER (PARTITION BY id ORDER BY valid_from) AS prev_value_int,
    LAG(value_text) OVER (PARTITION BY id ORDER BY valid_from) AS prev_value_text
    
FROM `learning.input_data` 

ORDER BY id, valid_from
```

![](/images/combining-structs-with-window-functions-in-bigquery/1.png)

Okay, but what if you have a dozen attributes? Instead of writing tens of LEAD or LAG functions, leverage STRUCT and look up an entire STRUCT of attributes.

### The solution

Here's an adapted example that uses STRUCTs.

```sql
WITH input_data AS (
    SELECT 
        id, 
        value_int, 
        value_text, 
        STRUCT(value_int, value_text) AS value, 
        valid_from, 
        valid_to
    FROM `learning.input_data` )
 SELECT 
     id, 
     value_int, 
     value_text, 
     valid_from, 
     valid_to,
     LAG(value) OVER (PARTITION BY id ORDER BY valid_from) AS prev_value,
     LEAD(value) OVER (PARTITION BY id ORDER BY valid_from) AS next_value
 FROM input_data

ORDER BY id, valid_from
```

![](/images/combining-structs-with-window-functions-in-bigquery/2.png)

This way, you can use LEAD or LAG only once, regardless of how many attributes you need to look up.

There are of course other interesting use cases for STRUCTs, which we will explore in upcoming posts. Stay tuned!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using ARRAY_AGG in BigQuery](/using-array-agg-in-bigquery)
- [UNNESTING ARRAYS in BigQuery](/unnesting-arrays-in-bigquery)
- [Leveraging ARRAYS in BigQuery for query performance](/leveraging-arrays-in-bigquery-for-query-performance)
- [Accessing ARRAY elements in BigQuery](/accessing-array-elements-in-bigquery)
- [Using LAST_VALUE with STRUCTS](/using-lastvalue-with-structs)
