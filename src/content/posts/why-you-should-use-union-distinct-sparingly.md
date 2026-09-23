---
title: "Why you should use UNION DISTINCT sparingly"
seoTitle: "UNION ALL vs UNION DISTINCT in BigQuery: Avoid Wasted Slots"
seoDescription: "Using UNION DISTINCT on already-distinct sources wastes slot time on unnecessary deduplication in BigQuery. Switch to UNION ALL when sources are known to..."
datePublished: 2024-04-02T23:12:39.465Z
dateUpdated: 2026-03-02T10:52:11.695Z
cover: "/images/why-you-should-use-union-distinct-sparingly/cover.jpg"
coverCredit:
  name: "Randy Fath"
  url: "https://unsplash.com/@randyfath"
series: "practical-sql"
hashnodeCuid: "cluizvew9000008i88ygd6rxj"
---

Let's help BigQuery do less unneeded work!

If you're UNIONING two sources known to have distinct values (and they don't have duplicates), go for UNION ALL instead of UNION DISTINCT (UNION for some other sql dialects) to avoid redundant de-duplication.

In the example below, I've unioned two Google Trends tables - one that is only for US terms and another one for the rest of the world. Since one table only contains US and the other everything except the US, we know the union of the two tables to be distinct from the start, thus not needing the UNION DISTINCT.

```sql
SELECT
  dma_name AS region_name,
  term,
  week,
  score,
  rank,
  refresh_date,
  'US' AS country_code
FROM `bigquery-public-data.google_trends.top_terms` --US terms

UNION DISTINCT

SELECT
  region_name,
  term,
  week,
  score,
  rank,
  refresh_date,
  country_code
FROM `bigquery-public-data.google_trends.international_top_terms` --international terms excl US
```

![Execution details for the UNION DISTINCT query: elapsed time 21 sec, slot time consumed 47 min 31 sec, bytes shuffled 69.37 GB, bytes spilled to disk 0 B.](/images/why-you-should-use-union-distinct-sparingly/1-result.jpg)

```sql
SELECT
  dma_name AS region_name,
  term,
  week,
  score,
  rank,
  refresh_date,
  'US' AS country_code
FROM `bigquery-public-data.google_trends.top_terms` --US terms

UNION ALL

SELECT
  region_name,
  term,
  week,
  score,
  rank,
  refresh_date,
  country_code
FROM `bigquery-public-data.google_trends.international_top_terms` --international terms excl US
```

![Execution details for the UNION ALL query: elapsed time 15 sec, slot time consumed 25 min 45 sec, bytes shuffled 48.72 GB, bytes spilled to disk 0 B.](/images/why-you-should-use-union-distinct-sparingly/1-result-2.jpg)

There's no difference indeed for on-demand pricing (same amount of data scanned), but quite a difference for capacity pricing users ( 1/2 of slot usage).

So use UNION DISTINCT (and any other DISTINCT) sparingly and when you actually need it.

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [9 tips on writing cleaner SQL](/9-tips-on-writing-cleaner-sql)
- [Order of precedence in SQL: WHERE vs HAVING](/order-of-precedence-in-sql-where-vs-having)
- [Easy with that SELECT DISTINCT!](/easy-with-that-select-distinct)
- [Why you should use parentheses with AND & OR in SQL](/why-you-should-use-parentheses-with-and-or-in-sql)
