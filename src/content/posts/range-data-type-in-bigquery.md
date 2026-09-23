---
title: "RANGE data type in BigQuery"
seoTitle: "BigQuery RANGE Data Type for SCD2 and Temporal Tables"
seoDescription: "BigQuery's RANGE data type stores time intervals in a single column instead of separate valid_from/valid_to fields."
datePublished: 2024-03-21T14:52:10.414Z
dateUpdated: 2026-03-02T10:51:21.054Z
cover: "/images/range-data-type-in-bigquery/cover.jpg"
coverCredit:
  name: "Coline Beulin"
  url: "https://unsplash.com/@colinextremis"
series: "practical-sql"
hashnodeCuid: "clu1cpkby00030ajn1zk6dj9q"
---

I work quite a lot with temporal/SCD2 type table so the new (still in preview) RANGE data type in BigQuery (and its supporting methods) are a welcome addition.

What does it do?

So instead of storing valid\_from & valid\_to in separate columns, we now have a datatype to store the time segment in an \[valid\_from, valid\_to) interval, of the form:

`SELECT RANGE(DATE '2021-01-01', DATE '2023-01-01').`

Note that the interval is left closed, right open (so left bound is included while the right one not).

This new semantic comes with a set of compatible functions :

\- constructors for RANGE and arrays of RANGEs

\- RANGE\_START and RANGE\_END to determine start and end of a segment

\- RANGE\_OVERLAPS, RANGE\_INTERSECT and RANGE\_CONTAINS to test the existence of an overlap, obtain the segment that overlaps and test the inclusion of a RANGE in another RANGE , respectively

While perhaps not a game changer, I still find the value in this upcoming feature.

Again, since this is still in preview it is not yet ready to use used in production.

See below an illustration of how it is used.

```sql
WITH input_data AS (
  SELECT
    RANGE(DATE '2021-01-01', DATE'2021-04-01') AS range_a,
    RANGE(DATE '2021-03-01', DATE'2021-09-01') AS range_b,
    RANGE(DATE '2021-02-01', DATE'2021-03-01') AS range_c
)

SELECT

  range_a,
  range_b,
  range_c,
  RANGE_OVERLAPS(range_a, range_b) AS do_ranges_a_b_overlap,
  RANGE_INTERSECT(range_a, range_b) AS ranges_a_b_intersection,
  RANGE_START(range_a) AS range_a_start,
  RANGE_END(range_a) AS range_a_end,
  RANGE_CONTAINS(range_a, range_c) AS range_a_contains_c,
  RANGE_CONTAINS(range_a, '2021-01-15') AS range_a_contains_date

FROM input_data
```

![BigQuery JSON results: range\_a \[2021-01-01, 2021-04-01), range\_b \[2021-03-01, 2021-09-01), range\_c \[2021-02-01, 2021-03-01), do\_ranges\_a\_b\_overlap true, ranges\_a\_b\_intersection \[2021-03-01, 2021-04-01), range\_a\_start 2021-01-01, range\_a\_end 2021-04-01, range\_a\_contains\_c true and range\_a\_contains\_date true.](/images/range-data-type-in-bigquery/1-result.jpg)

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
