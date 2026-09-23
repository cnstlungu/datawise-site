---
title: "Comparing tables with FULL OUTER JOIN"
seoTitle: "Compare Two BigQuery Tables with FULL OUTER JOIN"
seoDescription: "Use FULL OUTER JOIN in BigQuery to identify differences between dev and prod table versions before deploying changes."
datePublished: 2024-04-11T21:25:10.428Z
dateUpdated: 2026-03-02T10:51:30.121Z
cover: "/images/comparing-tables-with-full-outer-join/cover.jpg"
coverCredit:
  name: "Dietmar Becker"
  url: "https://unsplash.com/@dietmarbecker"
series: "practical-sql"
hashnodeCuid: "cluvqzusc000308jxgpz8bg1d"
---

Does your Data Engineering project use a data-diffing tool?

Say you're preparing to deploy a change to a prod table. You've changed the way some metrics are calculated and twisted some filters. How do you find out what's different between two tables? Identify expected vs unexpected differences?

If lacking a specialized tool for data-diffing (like Datafold, Recce ) perhaps the simplest validation you can do when comparing two tables (dev and prod versions for example) leverages the FULL OUTER JOIN (or FULL JOIN in some RDBMS).

Start with the grain. Is there any way you can bring the tables to the same grain?

Once you have aligned them to the same grain, you can now join on the respective keys and COUNT the occurrences you care about - what's missing from A, what's missing from B, totals overall. Depending on attributes, you can use other aggregate functions to assess differences - for example, does the SUM of sales amounts match in prod vs dev?

You could also leverage a hashing function + TO\_JSON\_ARRAY ([check my previous post](/using-bigquery-hashing-functions)) to see which rows are different in the two tables.

```sql
SELECT

  COUNTIF (prod.term IS NULL AND dev.term IS NOT NULL) AS cnt_missing_prod,
  COUNT (DISTINCT CASE WHEN prod.term IS NULL AND dev.term IS NOT NULL THEN dev.term END) AS distinct_terms_missing_from_prod,

  COUNTIF (dev.term IS NULL AND prod.term IS NOT NULL) AS cnt_missing_dev,
  COUNT (DISTINCT CASE WHEN dev.term IS NULL AND prod.term IS NOT NULL THEN prod.term END) AS distinct_terms_missing_from_dev,

  COUNT(1) AS total_rows,
  COUNT(DISTINCT COALESCE(prod.term, dev.term)) AS total_distinct_terms,

  COUNTIF(FARM_FINGERPRINT(TO_JSON_STRING(prod))  <> FARM_FINGERPRINT(TO_JSON_STRING(dev))) AS rows_different


FROM `learning_us.trends_us_prod` prod

FULL OUTER JOIN `learning_us.trends_us_dev` dev ON prod.refresh_date = dev.refresh_date AND
                                                   prod.week = dev.week AND
                                                   prod.dma_id = dev.dma_id AND
                                                   prod.term = dev.term
```

![BigQuery results: cnt\_missing\_prod 3954227, distinct\_terms\_missing\_from\_prod 660, cnt\_missing\_dev 3956293, distinct\_terms\_missing\_from\_dev 660, total\_rows 43514223, total\_distinct\_terms 660 and rows\_different 7910520.](/images/comparing-tables-with-full-outer-join/1-result.jpg)

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Self-joins in SQL](/self-joins-in-sql)
- [Anti-joins in SQL](/anti-joins-in-sql)
- [SEMI-JOINS in SQL](/semi-joins-in-sql)
- [NON-EQUI joins in SQL](/non-equi-joins-in-sql)
