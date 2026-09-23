---
title: "SESSION_USER in BigQuery"
seoTitle: "BigQuery SESSION_USER: Get the Current Query's Principal"
seoDescription: "SESSION_USER() in BigQuery returns the email or principal of the user or service account running the current query."
datePublished: 2024-05-02T21:24:37.465Z
dateUpdated: 2026-03-02T10:51:23.334Z
cover: "/images/sessionuser-in-bigquery/cover.jpg"
coverCredit:
  name: "Scott Webb"
  url: "https://unsplash.com/@scottwebb"
series: "practical-sql"
hashnodeCuid: "clvpr81cp00010amh99yb7fvy"
---

SESSION\_USER is currently listed as the only "Security" function in the BigQuery documentation. What does it do?

It can help you find out the email or the principal of the user that is running the query.

This might a person or a service account that is impersonated. As far as I know, one could only impersonate the service account when using the bq cli (and not the GUI).

I remember using SESSION\_USER / CURRENT USER in my SQL Server days as well.

The only use case I thought of was a poor man's row-level security for tables, effectively filtering the rows you can see based on who you are. But there is a proper solution for this problem - [Row-level access policies](/row-level-access-security-in-bigquery).

Any interesting use cases which involve SESSION\_USER in your projects?

![](/images/sessionuser-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
