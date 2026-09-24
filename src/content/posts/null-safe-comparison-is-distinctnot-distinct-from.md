---
title: "Null-safe comparison: IS DISTINCT/NOT DISTINCT FROM"
seoTitle: "Understanding NULL-safe comparisons"
seoDescription: "Discover NULL-safe SQL operators IS DISTINCT FROM and IS NOT DISTINCT FROM for safer comparisons without IFNULLs or COALESCE in BigQuery"
datePublished: 2025-05-06T07:32:11.984Z
dateUpdated: 2026-03-02T10:53:00.724Z
cover: "/images/null-safe-comparison-is-distinctnot-distinct-from/cover.jpg"
coverCredit:
  name: "Matthew Waring"
  url: "https://unsplash.com/@matthewwaring"
series: "practical-sql"
hashnodeCuid: "cmac6yv68000d09hza6gm41ob"
---

I've been working for surprisingly long with SQL to have found this only a few days ago. Not long enough I guess 🤓.

I'm talking about the NULL-safe operators IS DISTINCT FROM and IS NOT DISTINCT FROM. I found about their existence from a [Linkedin post](https://www.linkedin.com/posts/sebastian-flak_the-sql-comparison-operator-you-should-activity-7322288997945212928-3hOZ?utm_source=share&utm_medium=member_desktop&rcm=ACoAAAvrnvABKPsQ1CE0m9jhBpQ-Vr-YZbN9dqg).

Works on BigQuery too, so I guess less need of adding IFNULLs / COALESCE for safety.

```sql
SELECT
  'a' <> CAST(NULL AS STRING) AS a_different_null,
  'a' = CAST(NULL AS STRING) AS a_equals_null,
  'a' IS DISTINCT FROM CAST(NULL AS STRING) AS a_distinct_null,
  'a' IS NOT DISTINCT FROM CAST(NULL AS STRING) AS a_not_distinct_null
```

![BigQuery results in the JSON tab: a\_different\_null and a\_equals\_null are null, a\_distinct\_null is "true" and a\_not\_distinct\_null is "false".](/images/null-safe-comparison-is-distinctnot-distinct-from/1-result.jpg)

PS This choice of keyword "FROM", together with the one in EXTRACT(HOUR FROM DATETIME '2021-01-01'), feels pretty weird.

---

*Enjoyed this? Here are some related articles you might find useful:*

- [A couple of fun things about NULL in SQL](/a-couple-of-fun-things-about-null-in-sql)
- [Not all NULLS are the same](/not-all-nulls-are-the-same)
- [COALESCE vs IFNULL vs NULLIF in BigQuery](/coalesce-vs-ifnull-vs-nullif-in-bigquery)
- [Controlling ordering of NULL values in the ORDER BY clause](/controlling-ordering-of-null-values-in-the-order-by-clause)
