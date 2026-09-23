---
title: "The NOT NULL Constraint in BigQuery"
seoTitle: "BigQuery NOT NULL Constraint: REQUIRED vs NULLABLE Modes"
seoDescription: "BigQuery enforces NOT NULL via REQUIRED column mode. Learn how to set REQUIRED vs NULLABLE at table creation and how it interacts with INSERT and UPDATE."
datePublished: 2024-05-16T09:43:45.044Z
dateUpdated: 2026-03-02T10:16:35.479Z
cover: "/images/the-not-null-constraint-in-bigquery/cover.jpg"
coverCredit:
  name: "Pierre Bamin"
  url: "https://unsplash.com/@bamin"
series: "practical-sql"
hashnodeCuid: "clw92cmtw000m09mk8mj0ev4i"
---

Are you using the NOT NULL constraint in BigQuery? This constraint is a staple when working with databases.  
  
So, when creating a table, you have the option to declare if a particular column is required and should not be null. We do that by simply adding the NOT NULL to the column declaration.  
  
You also can check it on an existing table by checking the column (field) MODE.  
  
It can have 3 values:  
\- NULLABLE (which is the default if you've haven't set anything)  
\- REQUIRED (if you've set NOT NULL for this columns)  
\- REPEATED (for ARRAYS).  
  
Upon trying insert or update data that will violated this constraint, the statement will fail.  
  
Overall, setting the right MODE for your field helps enforce your expectations about the data that should be inserted or updated in a particular table.

![BigQuery SQL creating learning.customers with first\_name STRING NOT NULL, the console Schema tab showing first\_name Mode REQUIRED and phone\_number NULLABLE, and an INSERT with NULL AS first\_name that fails with the error Required field first\_name cannot be null.](/images/the-not-null-constraint-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
