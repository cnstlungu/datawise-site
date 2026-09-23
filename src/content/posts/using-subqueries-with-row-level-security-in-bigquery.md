---
title: "Using subqueries with Row Level Security in BigQuery"
seoTitle: "BigQuery Row-Level Security with Subquery Lookup"
seoDescription: "BigQuery now supports subqueries in CREATE ROW ACCESS POLICY, letting you reference a lookup table with SESSION_USER for dynamic row-level security — no..."
datePublished: 2024-05-16T09:35:52.546Z
dateUpdated: 2026-03-02T10:51:50.191Z
cover: "/images/using-subqueries-with-row-level-security-in-bigquery/cover.jpg"
coverCredit:
  name: "FlyD"
  url: "https://unsplash.com/@flyd2069"
series: "practical-sql"
hashnodeCuid: "clw922i8y00010al7d4jg0mx9"
---

I've [previously posted](/row-level-access-security-in-bigquery) about row-level security in BigQuery.

One of the gotchas back then was the fact that you needed to manually specify what values should the access be filtered for. If only a sub-query was allowed there!

Well, a new feature, currently in preview, allows for it, even though the `CREATE ROW ACCESS POLICY` DDL reference still says it's not.

Now, one can refer to a lookup table and use that in conjunction with the SESSION\_USER function (which we've also previously looked at) to filter the values that a principal should see.

The result is the same, but this adds a degree of simplicity and easiness when managing row-level access security in BigQuery.

![BigQuery SQL comparing CREATE ROW ACCESS POLICY with a static FILTER USING (country IN ('US', 'UK')) to the preview version whose FILTER USING subquery reads lookup\_table, UNNESTs country\_list and matches user\_principal = SESSION\_USER(); both let the service account see only the UK and US customers.](/images/using-subqueries-with-row-level-security-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Row-level access security in BigQuery](/row-level-access-security-in-bigquery)
- [Why basic roles in BigQuery are a bad idea](/why-basic-roles-in-bigquery-are-a-bad-idea)
- [Cross-dataset foreign key relationships in BigQuery](/cross-dataset-foreign-key-relationships-in-bigquery)
