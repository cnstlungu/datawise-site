---
title: "Joining temporal tables in BigQuery"
seoTitle: "Joining Temporal Tables in BigQuery: A Practical Guide"
seoDescription: "Learn how to join multiple temporal tables in BigQuery with SQL examples."
datePublished: 2023-03-11T21:04:11.499Z
dateUpdated: 2026-03-02T10:50:46.317Z
cover: "/images/practical-bigquery-joining-temporal-tables/cover.jpg"
coverCredit:
  name: "Waldemar"
  url: "https://unsplash.com/@waldemarbrandt67w"
series: "practical-sql"
hashnodeCuid: "clfn327oe000509la7z2l42ze"
---

In today’s practical BigQuery exercise, we’re going to look at how we can join multiple temporal tables in BigQuery. If the name *temporal tables* does not sound familiar, you might have heard about *transaction tables* or even a Slowly-Changing Type-2 table (typically dimension, but could also be a fact). In any case, chances are you might recognize it below:

```sql
+----+------------+------------+--------+
| id | valid_from | valid_to   | valueB |
+----+------------+------------+--------+
| 1  | 2022-04-01 | 2022-07-01 | b1     |
| 1  | 2022-07-01 | 2022-08-01 | b2     |
| 1  | 2022-08-01 | 9999-01-01 | b3     |
+----+------------+------------+--------+
```

The above table defines an interval that includes the right but not the left bounds, as follows:

`[valid_from, valid_to)`

Now, if we want to find out what was the *valueB* for *ID = 1* for a particular moment in time, say - today - the query would be pretty straightforward:

```sql
SELECT
id,
valid_from,
valid_to,
valueB
FROM
table_b
WHERE
CURRENT_DATE() > valid_from AND valid_to > CURRENT_DATE()
```

which evaluates today to the following:

```sql
+----+------------+------------+--------+
| id | valid_from | valid_to   | valueB |
+----+------------+------------+--------+
| 1  | 2022-08-01 | 9999-01-01 | b3     |
+----+------------+------------+--------+
```

But what if we have multiple temporal tables like the above and we’d like to look at them together, displaying the data for *ID = 1* (be that a store\_id or a product\_id). How can we join multiple temporal tables into one?

## Problem statement

Given several temporal tables, **table\_a, table\_b** and **table\_c**, presenting different time-bound contexts about the same entity (id):

```sql
-- table_a
+----+------------+------------+--------+
| id | valid_from | valid_to   | valueA |
+----+------------+------------+--------+
| 1  | 2022-01-01 | 2022-06-01 | a1     |
| 1  | 2022-06-01 | 2022-08-01 | a2     |
+----+------------+------------+--------+

-- table_b
+----+------------+------------+--------+
| id | valid_from | valid_to   | valueB |
+----+------------+------------+--------+
| 1  | 2022-04-01 | 2022-07-01 | b1     |
| 1  | 2022-07-01 | 2022-08-01 | b2     |
| 1  | 2022-08-01 | 9999-01-01 | b3     |
+----+------------+------------+--------+

-- table_c
+----+------------+------------+--------+
| id | valid_from | valid_to   | valueC |
+----+------------+------------+--------+
| 1  | 2022-02-01 | 2022-05-01 | c1     |
| 1  | 2022-05-01 | 2022-09-01 | c2     |
| 1  | 2022-09-01 | 9999-01-01 | c3     |
+----+------------+------------+--------+
```

compute a joined temporal table that looks as follows:

```sql
+------------+------------+----+--------+--------+--------+
| valid_from | valid_to   | id | valueA | valueB | valueC |
+------------+------------+----+--------+--------+--------+
| 2022-01-01 | 2022-02-01 | 1  | a1     |        |        |
| 2022-02-01 | 2022-04-01 | 1  | a1     |        | c1     |
| 2022-04-01 | 2022-05-01 | 1  | a1     | b1     | c1     |
| 2022-05-01 | 2022-06-01 | 1  | a1     | b1     | c2     |
| 2022-06-01 | 2022-07-01 | 1  | a2     | b1     | c2     |
| 2022-07-01 | 2022-08-01 | 1  | a2     | b2     | c2     |
| 2022-08-01 | 2022-09-01 | 1  |        | b3     | c2     |
| 2022-09-01 | 9999-01-01 | 1  |        | b3     | c3     |
+------------+------------+----+--------+--------+--------+
```

## Trying it out

Let’s try and decompose this problem. In the below representation, I’ve marked with red the occurrence of an event — change of state for one of the three attributes we’re interested. We can deduce that an event for one attribute must become an event for all the other attributes, as it basically slices the other intervals into smaller intervals.

For instance, the value ***a1*** has full overlap with value ***c1*** , but limited overlap with values ***b1*** and ***c2*.**

![Diagram of validity intervals in three tables on a shared timeline: table\_a has a1 and a2 and ends early, table\_b starts later with b1, b2 and b3, and table\_c spans the whole range as c1, c2 and c3; red markers show the interval boundaries do not line up across tables.](/images/practical-bigquery-joining-temporal-tables/1.png)

Graphical representation of the issue

We’re going to start our query by creating this list of events (validity start or ending) across all the attributes. Notice we’re interested in a unique list, therefore using distinct. The list needs to be created at our desired grain, in our case — by ***id*** .

```sql
WITH dates AS (

SELECT id, valid_from AS event_date FROM table_a

UNION DISTINCT

SELECT id, valid_to AS event_date FROM table_a

UNION DISTINCT

SELECT id, valid_from AS event_date FROM table_b

UNION DISTINCT

SELECT id, valid_to AS event_date FROM table_b

UNION DISTINCT

SELECT id, valid_from AS event_date FROM table_c

UNION DISTINCT

SELECT id, valid_to AS event_date FROM table_c

)
```

We will now join each table to our *dates* common table expression.

We’ll join on our grain (in our case: ***id*** ) and the date condition, the ***event\_date*** needs greater or equal to ***valid\_from*** but strictly less than ***valid\_to***.

In the *SELECT* part, we’ll use the event\_date as the valid\_from of the new raw. We’ll then use the LEAD window function to fetch the next **valid\_from** entry (while partitioning by our grain and ordering by the **event\_date**) which will become our **valid\_to**. We include the attributes we need from each table — **valueA**, **valueB** and **valueC**.

We’ll also order the output by **valid\_from** to get a nice chronological view of events.

```sql
SELECT
d.event_date AS valid_from,
LEAD(d.event_date, 1) OVER (PARTITION BY d.id ORDER BY d.event_date) AS valid_to,
d.id,
a.valueA,
b.valueB,
c.valueC

FROM dates d

LEFT JOIN table_a a ON d.id = a.id AND d.event_date >= a.valid_from AND d.event_date < a.valid_to

LEFT JOIN table_b b ON d.id = b.id AND d.event_date >= b.valid_from AND d.event_date < b.valid_to

LEFT JOIN table_c c ON d.id = c.id AND d.event_date >= c.valid_from AND d.event_date < c.valid_to

ORDER BY valid_from
```

The above query produces the following results:

```sql
+------------+------------+----+--------+--------+--------+
| valid_from | valid_to   | id | valueA | valueB | valueC |
+------------+------------+----+--------+--------+--------+
| 2022-01-01 | 2022-02-01 | 1  | a1     |        |        |
| 2022-02-01 | 2022-04-01 | 1  | a1     |        | c1     |
| 2022-04-01 | 2022-05-01 | 1  | a1     | b1     | c1     |
| 2022-05-01 | 2022-06-01 | 1  | a1     | b1     | c2     |
| 2022-06-01 | 2022-07-01 | 1  | a2     | b1     | c2     |
| 2022-07-01 | 2022-08-01 | 1  | a2     | b2     | c2     |
| 2022-08-01 | 2022-09-01 | 1  |        | b3     | c2     |
| 2022-09-01 | 9999-01-01 | 1  |        | b3     | c3     |
| 9999-01-01 |            | 1  |        |        |        |
+------------+------------+----+--------+--------+--------+
```

In the output, you’ll notice that there is an extra row for valid\_from = *9999–01–01.* This one can be excluded in the query above using QUALIFY, the query becoming:

```sql
SELECT
d.event_date AS valid_from,
LEAD(d.event_date, 1) OVER (PARTITION BY d.id ORDER BY d.event_date) AS valid_to,
d.id,
a.valueA,
b.valueB,
c.valueC

FROM dates d

LEFT JOIN table_a a ON d.id = a.id AND d.event_date >= a.valid_from AND d.event_date < a.valid_to

LEFT JOIN table_b b ON d.id = b.id AND d.event_date >= b.valid_from AND d.event_date < b.valid_to

LEFT JOIN table_c c ON d.id = c.id AND d.event_date >= c.valid_from AND d.event_date < c.valid_to

QUALIFY valid_to IS NOT NULL

ORDER BY valid_from
```

```sql
+------------+------------+----+--------+--------+--------+
| valid_from | valid_to   | id | valueA | valueB | valueC |
+------------+------------+----+--------+--------+--------+
| 2022-01-01 | 2022-02-01 | 1  | a1     |        |        |
| 2022-02-01 | 2022-04-01 | 1  | a1     |        | c1     |
| 2022-04-01 | 2022-05-01 | 1  | a1     | b1     | c1     |
| 2022-05-01 | 2022-06-01 | 1  | a1     | b1     | c2     |
| 2022-06-01 | 2022-07-01 | 1  | a2     | b1     | c2     |
| 2022-07-01 | 2022-08-01 | 1  | a2     | b2     | c2     |
| 2022-08-01 | 2022-09-01 | 1  |        | b3     | c2     |
| 2022-09-01 | 9999-01-01 | 1  |        | b3     | c3     |
| 9999-01-01 |            | 1  |        |        |        |
+------------+------------+----+--------+--------+--------+
```

We can now find out what was the value for all three attributes of our id at a particular point in time, for example:

```sql
SELECT
valid_from,
valid_to,
id,
valueA,
valueB,
valueC

FROM results

WHERE valid_from < DATE("2022-05-04") AND valid_to > DATE("2022-05-04")
```

```sql
+------------+------------+----+--------+--------+--------+
| valid_from | valid_to   | id | valueA | valueB | valueC |
+------------+------------+----+--------+--------+--------+
| 2022-05-01 | 2022-06-01 | 1  | a1     | b1     | c2     |
+------------+------------+----+--------+--------+--------+
```

If you like to play around with the query, please see the entire SQL script below (including the raw data).

## Conclusion

In this short practical exercise, we’ve looked at joining multiple temporal tables into a single one.

Thanks for reading and stay tuned for other interesting stories.

```sql
with table_a AS (

SELECT 1 AS id, DATE('2022-01-01') AS valid_from, DATE('2022-06-01') AS valid_to, 'a1' AS valueA

UNION ALL 

SELECT 1 AS id, DATE('2022-06-01') AS valid_from, DATE('2022-08-01') AS valid_to, 'a2' AS valueA

),

table_b AS (


SELECT 1 AS id, DATE('2022-04-01') AS valid_from, DATE('2022-07-01') AS valid_to, 'b1' AS valueB

UNION ALL 

SELECT 1 AS id, DATE('2022-07-01') AS valid_from, DATE('2022-08-01') AS valid_to, 'b2' AS valueB

UNION ALL

SELECT 1 AS id, DATE('2022-08-01') AS valid_from, DATE('9999-01-01') AS valid_to, 'b3' AS valueB

),


table_c AS (



SELECT 1 AS id, DATE('2022-02-01') AS valid_from, DATE('2022-05-01') AS valid_to, 'c1' AS valueC

UNION ALL 

SELECT 1 AS id, DATE('2022-05-01') AS valid_from, DATE('2022-09-01') AS valid_to, 'c2' AS valueC

UNION ALL

SELECT 1 AS id, DATE('2022-09-01') AS valid_from, DATE('9999-01-01') AS valid_to, 'c3' AS valueC



),



dates AS (

SELECT id, valid_from AS event_date FROM table_a

UNION DISTINCT

SELECT id, valid_to AS event_date FROM table_a

UNION DISTINCT


SELECT id, valid_from AS event_date FROM table_b


UNION DISTINCT

SELECT id, valid_to AS event_date FROM table_b

UNION DISTINCT


SELECT id, valid_from AS event_date FROM table_c


UNION DISTINCT

SELECT id, valid_to AS event_date FROM table_c

),

results AS (


  SELECT 
  d.event_date AS valid_from,
  LEAD(d.event_date, 1) OVER (PARTITION BY d.id ORDER BY d.event_date) AS valid_to, 
  d.id, 
  a.valueA, 
  b.valueB, 
  c.valueC

FROM dates d

LEFT JOIN table_a a ON d.id = a.id AND d.event_date >= a.valid_from AND d.event_date < a.valid_to

LEFT JOIN table_b b ON d.id = b.id AND d.event_date >= b.valid_from AND d.event_date < b.valid_to

LEFT JOIN table_c c ON d.id = c.id AND d.event_date >= c.valid_from AND d.event_date < c.valid_to

QUALIFY valid_to IS NOT NULL


)

SELECT 
  valid_from,
  valid_to,
  id,
  valueA,
  valueB,
  valueC

FROM results
```

*[View on GitHub Gist](https://gist.github.com/cnstlungu/742c5f606d53d9258c2c97fa697d48e1)* 

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Generating a compact temporal table in BigQuery](/generating-a-compact-temporal-table-in-bigquery)
- [Aggregating Multiple SCD-2 Attribute Timelines in BigQuery](/aggregating-multiple-scd-2-attribute-timelines-in-bigquery)
- [Compacting date intervals in BigQuery](/compacting-date-intervals-in-bigquery)
- [Transforming cumulative sums into monthly values](/transforming-cumulative-sums-into-monthly-values)
