---
title: "Cross-dataset foreign key relationships in BigQuery"
seoTitle: "Link Foreign Keys Across Datasets in BigQuery"
seoDescription: "Learn to create cross-dataset foreign key relationships in BigQuery and explore metadata enhancements for SQL tables with ease"
datePublished: 2025-06-09T21:12:58.222Z
dateUpdated: 2026-03-02T10:52:58.488Z
cover: "/images/cross-dataset-foreign-key-relationships-in-bigquery/cover.jpg"
coverCredit:
  name: "Will Francis"
  url: "https://unsplash.com/@willfrancis"
series: "practical-sql"
hashnodeCuid: "cmbpl9ch9000102i870lugcnt"
---

It turns out you can now (don't know since when though) create cross-dataset foreign key relationships in BigQuery hashtag#SQL. Previously this was only possible for tables that are in the same dataset (but there were workarounds).

While the performance gain when using these *unenforced* PK/FK constraints in general may be up for discussion, it's definitely nice to be able to see this table metadata there, including the table grain 👍

For a refresher on what these constraints are, see [my previous post](/bigquery-primary-key-foreign-key-constraints).

![](/images/cross-dataset-foreign-key-relationships-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [***notjustsql.com***](https://www.notjustsql.com/)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Row-level access security in BigQuery](/row-level-access-security-in-bigquery)
- [Using subqueries with Row Level Security in BigQuery](/using-subqueries-with-row-level-security-in-bigquery)
- [Why basic roles in BigQuery are a bad idea](/why-basic-roles-in-bigquery-are-a-bad-idea)
