---
title: "Pay attention to this when UNNESTING in BigQuery"
seoTitle: "BigQuery UNNEST: Why Rows Disappear with CROSS JOIN"
seoDescription: "In BigQuery, comma syntax before UNNEST behaves like CROSS JOIN and can drop rows with empty arrays. Compare it with LEFT JOIN UNNEST side by side."
datePublished: 2023-10-19T22:30:51.027Z
dateUpdated: 2026-04-28T08:33:45.141Z
cover: "/images/pay-attention-to-this-when-unnesting-in-bigquery/cover.jpg"
coverCredit:
  name: "Pierre Bamin"
  url: "https://unsplash.com/@bamin"
series: "bigquery-arrays-and-structs"
hashnodeCuid: "clnxra8pf000109la9lxd343d"
---

Here's a common confusion that I encounter while working with ARRAYs in BigQuery. This can lead to wrong queries in some situations. Consider the following two snippets:

```sql
FROM table,
UNNEST(repeated_column) AS single_item
```

versus

```sql

FROM table
LEFT JOIN UNNEST(repeated_column) AS single_item
```

They are very different.

In the first, the comma ',' essentially behaves like a CROSS JOIN, pairing each row of the table with every element of the array in its repeated\_column.

In the second, we're using a LEFT JOIN, ensuring retention of all rows in the table, even those without a value in the repeated\_column.

How is this important, you'll ask. Consider the following case.

Imagine you'd need to compute the number of unique banks a person is a customer of in the example below.

![BigQuery result grid of input\_data with a repeated bank\_accounts STRUCT (bank\_name, account\_type): John Smith has Bank A and Bank B, Jane Doe two Bank B accounts, Bob Johnson Bank C, while Alice Lee and Tom Wilson show null, meaning no accounts.](/images/pay-attention-to-this-when-unnesting-in-bigquery/1.jpg)

A person can be a customer of one, multiple or no bank at all. This becomes important if a customer has no accounts, using UNNEST joined with the comma (CROSS JOIN) would exclude these entries.

```sql
SELECT 
  person_id, 
  COUNT(DISTINCT bank_account.bank_name) AS count_distinct_banks 
FROM input_data,
UNNEST(bank_accounts) AS bank_account 

GROUP BY person_id
```

![BigQuery result of the comma (CROSS JOIN) UNNEST query with columns person\_id and count\_distinct\_banks: only persons 1, 2 and 3 appear, with 2, 1 and 1 banks; persons 4 and 5, who have no accounts, are missing.](/images/pay-attention-to-this-when-unnesting-in-bigquery/2.png)

If we want to keep these entries, we'd need to use LEFT JOIN.

```sql
SELECT 
person_id, 
COUNT(DISTINCT bank_account.bank_name) AS count_distinct_banks 
FROM input_data

LEFT JOIN UNNEST(bank_accounts) AS bank_account 
GROUP BY person_id
```

![BigQuery result of the LEFT JOIN UNNEST query with columns person\_id and count\_distinct\_banks: all five persons appear, 1 with 2 banks, 2 and 3 with 1 bank each, and persons 4 and 5 kept with 0.](/images/pay-attention-to-this-when-unnesting-in-bigquery/3.png)

In this case, the first approach would miss out on the people without a bank account, while the second would include them. Quite a big difference in query results if you ask me.

Have fun writing good SQL!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using ARRAY_AGG in BigQuery](/using-array-agg-in-bigquery)
- [UNNESTING ARRAYS in BigQuery](/unnesting-arrays-in-bigquery)
- [Leveraging ARRAYS in BigQuery for query performance](/leveraging-arrays-in-bigquery-for-query-performance)
- [Accessing ARRAY elements in BigQuery](/accessing-array-elements-in-bigquery)
