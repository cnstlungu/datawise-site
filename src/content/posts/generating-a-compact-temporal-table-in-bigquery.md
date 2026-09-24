---
title: "Generating a compact temporal table in BigQuery"
seoTitle: "Build a Compact Temporal Table in BigQuery with SQL"
seoDescription: "Learn how to deduplicate and compact redundant SCD-2 rows in BigQuery using FARM_FINGERPRINT, LEAD, and QUALIFY to produce a clean valid_from/valid_to..."
datePublished: 2023-03-20T13:45:27.556Z
dateUpdated: 2026-03-02T10:51:55.810Z
cover: "/images/generating-a-compact-temporal-table-in-bigquery/cover.jpg"
coverCredit:
  name: "Nana Smirnova"
  url: "https://unsplash.com/@nananadolgo"
series: "practical-sql"
hashnodeCuid: "clfmp78lq000109mh39af5uao"
---

In one of my [previous posts](/practical-bigquery-joining-temporal-tables), we discussed what temporal tables are and how to join multiple such tables into a single one. In this short practical exercise, we’re going to look at how we can generate a compact temporary table given possible redundant values as input.

### Problem statement

Let’s consider an example.

```sql
+----+------------+-----------+-------------+
| id | value_text | value_int | update_date |
+----+------------+-----------+-------------+
| 1  | a          | 12        | 2021-01-01  |
| 1  | b          | 30        | 2021-11-01  |
| 1  | b          | 25        | 2022-02-01  |
| 1  | b          | 25        | 2022-04-01  |
| 1  | a          | 11        | 2022-05-01  |
| 1  | c          | 11        | 2022-06-01  |
| 1  | d          | 20        | 2022-11-01  |
| 1  | e          | 20        | 2022-12-01  |
| 1  | e          | 20        | 2023-03-01  |
+----+------------+-----------+-------------+
```

In our input data, we can see that at our grain (column *id* ) we’re provided updates on a particular set of dates. But for dates ‘2022–04–01’ and ‘2023–03–01’ the updates are redundant — there is no new information provided.

This can happen, for example, when we extract only a subset of attributes from the data source (where other attributes, which we don’t use, do change).

Now, If we were to transform the above into a temporal table without compacting, we would obtain the following. Notice that, as expected from our input data, two of the periods could be compacted — merged with another adjacent period.

```sql
+----+------------+-----------+------------+------------+
| id | value_text | value_int | valid_from | valid_to   |
+----+------------+-----------+------------+------------+
| 1  | a          | 12        | 2021-01-01 | 2021-10-31 |
| 1  | b          | 30        | 2021-11-01 | 2022-01-31 |
| 1  | b          | 25        | 2022-02-01 | 2022-03-31 |
| 1  | b          | 25        | 2022-04-01 | 2022-04-30 |
| 1  | a          | 11        | 2022-05-01 | 2022-05-31 |
| 1  | c          | 11        | 2022-06-01 | 2022-10-31 |
| 1  | d          | 20        | 2022-11-01 | 2022-11-30 |
| 1  | e          | 20        | 2022-12-01 | 2023-02-28 |
| 1  | e          | 20        | 2023-03-01 | 9999-01-01 |
+----+------------+-----------+------------+------------+
```

Compare with the below-compacted version. Notice that two periods **2022–04–01 | 2022–04–30** and **2023–03–01 | 9999–01–01** have been merged with other periods, resulting in a more compact table.

```sql
+----+------------+-----------+------------+------------+
| id | value_text | value_int | valid_from | valid_to   |
+----+------------+-----------+------------+------------+
| 1  | a          | 12        | 2021-01-01 | 2021-10-31 |
| 1  | b          | 30        | 2021-11-01 | 2022-03-31 |
| 1  | b          | 25        | 2022-04-01 | 2022-04-30 |
| 1  | a          | 11        | 2022-05-01 | 2022-05-31 |
| 1  | c          | 11        | 2022-06-01 | 2022-10-31 |
| 1  | d          | 20        | 2022-11-01 | 2023-02-28 |
| 1  | e          | 20        | 2023-03-01 | 9999-01-01 |
+----+------------+-----------+------------+------------+
```

Note that in both above implementations of the temporal tables the validity period contains both bounds, in other words:

```sql
[ valid_from, valid_to ]
```

### Implementation

It’s obvious from the above input that we cannot use DISTINCT or any other de-duplication technique (e.g. with ROW\_NUMBER) since these are not duplicates. We’d need a way to look at the attribute values and determine if there is any change (at our grain, in this case by *id* ).

For this, we’ll use the [**FARM\_FINGERPRINT**](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/hash_functions#farm_fingerprint) hashing function, applied to attribute values. Notice the **IFNULL** wrapper around each attribute, since a *NULL* value would render the entire hash output *NULL* as well.

```sql
SELECT

id,
value_text,
value_int,
update_date,
FARM_FINGERPRINT(CONCAT(IFNULL(value_text, 'N/A'),
IFNULL(value_int, -1))) AS row_hash

FROM input_datas
```

This will compute a hash value from our attributes, allowing us to discern between an actual update and a redundant one.

![Text query output of the hashed input with columns id, value\_text, value\_int, update\_date and row\_hash for nine updates of id 1; repeated values produce identical hashes, e.g. b/25 on 2022-02-01 and 2022-04-01, and e/20 on 2022-12-01 and 2023-03-01.](/images/generating-a-compact-temporal-table-in-bigquery/1.png)

We can now compact the input. We’re going to use a LEAD window function to get, for each row, the value of the next hash (at our grain). Subsequent rows with the same hash values are deemed redundant. We’ll use qualify to exclude the redundant rows.

Notice the **IFNULL** in the QUALIFY block — this would allow us to keep the last row.

```sql
SELECT

id,
value_text,
value_int,
update_date,
row_hash,
LEAD(row_hash,1) OVER (PARTITION BY ID order by update_date) AS next_hash

FROM hashed

QUALIFY row_hash <> IFNULL(next_hash, -1)
```

This will yield the following data.

![Text query output after LEAD and QUALIFY, with columns id, value\_text, value\_int, update\_date, row\_hash and next\_hash: seven rows remain, the redundant duplicates are gone, keeping b/25 on 2022-04-01 and the final e/20 row on 2023-03-01 whose next\_hash is empty.](/images/generating-a-compact-temporal-table-in-bigquery/2.png)

We can now generate our temporary table. We’ll start with our update\_date as our **valid\_from**, then use the LEAD function the get the next update\_date as our **valid\_to**.

Since we’re building a `[valid_from, valid_to]` implementation, we’ll need to get the value preceding the start of the next period as the end of a period — in our case, subtract a day from the next update\_date/valid\_form. We’ll also provide a default value for the last known (current) value.

```sql
SELECT

id,
value_text,
value_int,
update_date AS valid_from,
IFNULL(DATE_SUB(LEAD(update_date,1) OVER(PARTITION BY id ORDER BY update_date),
INTERVAL 1 DAY),
DATE('9999-01-01')) AS valid_to

FROM compacted
```

This produces the following output:

```sql
+----+------------+-----------+------------+------------+
| id | value_text | value_int | valid_from | valid_to   |
+----+------------+-----------+------------+------------+
| 1  | a          | 12        | 2021-01-01 | 2021-10-31 |
| 1  | b          | 30        | 2021-11-01 | 2022-03-31 |
| 1  | b          | 25        | 2022-04-01 | 2022-04-30 |
| 1  | a          | 11        | 2022-05-01 | 2022-05-31 |
| 1  | c          | 11        | 2022-06-01 | 2022-10-31 |
| 1  | d          | 20        | 2022-11-01 | 2023-02-28 |
| 1  | e          | 20        | 2023-03-01 | 9999-01-01 |
+----+------------+-----------+------------+------------+
```

For the full script (including input data), see below.

### Conclusion

In today’s practical exercise, we’ve looked at how we can transform possibly-redundant input event data into a compact temporal table.

Thanks for reading and stay tuned for more Data Engineering content.

```sql
with input_data AS (

SELECT 1 AS id, 'a' AS value_text, 12 as value_int, DATE('2021-01-01') AS update_date

UNION ALL

SELECT 1 AS id, 'b' AS value_text, 30 AS value_int, DATE('2021-11-01') AS update_date

UNION ALL

SELECT 1 AS id, 'b' AS value_text, 25 AS value_int, DATE('2022-02-01') AS update_date

UNION ALL

SELECT 1 AS id, 'b' AS value_text, 25 AS value_int, DATE('2022-04-01') AS update_date

UNION ALL

SELECT 1 AS id, 'a' AS value_text, 11 AS value_int, DATE('2022-05-01') AS update_date

UNION ALL

SELECT 1 AS id, 'c' AS value_text, 11 AS value_int, DATE('2022-06-01') AS update_date

UNION ALL

SELECT 1 AS id, 'd' AS value_text, 20 AS value_int, DATE('2022-11-01') AS update_date

UNION ALL

SELECT 1 AS id, 'e' AS value_text, 20 AS value_int, DATE('2022-12-01') AS update_date

UNION ALL

SELECT 1 AS id, 'e' AS value_text, 20 AS value_int,  DATE('2023-03-01') AS update_date

)

,hashed AS (

SELECT 

  id, 
  value_text, 
  value_int, 
  update_date, 
  FARM_FINGERPRINT(CONCAT(IFNULL(value_text, 'N/A'),
                          IFNULL(value_int, -1))) AS row_hash 

FROM input_data


)


,compacted AS (


SELECT 

  id, 
  value_text, 
  value_int, 
  update_date, 
  row_hash, 
  LEAD(row_hash,1) OVER (PARTITION BY id ORDER BY update_date) AS next_hash

FROM hashed

QUALIFY row_hash <> IFNULL(next_hash, -1)





)
SELECT 


  id, 
  value_text, 
  value_int, 
  update_date AS valid_from, 
  IFNULL(DATE_SUB(LEAD(update_date,1) OVER(PARTITION BY id ORDER BY update_date), 
                  INTERVAL 1 DAY),
         DATE('9999-01-01')) AS valid_to 
  
FROM compacted
```

*[View on GitHub Gist](https://gist.github.com/cnstlungu/732b9d64367b6eec012727d1d08151e5)* 

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Joining temporal tables in BigQuery](/practical-bigquery-joining-temporal-tables)
- [Aggregating Multiple SCD-2 Attribute Timelines in BigQuery](/aggregating-multiple-scd-2-attribute-timelines-in-bigquery)
- [Compacting date intervals in BigQuery](/compacting-date-intervals-in-bigquery)
- [Transforming cumulative sums into monthly values](/transforming-cumulative-sums-into-monthly-values)
