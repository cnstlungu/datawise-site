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

```sql
CREATE OR REPLACE TABLE learning.customers (id INT64 NOT NULL,
                                            first_name STRING NOT NULL,
                                            last_name STRING NOT NULL,
                                            phone_number STRING );
```

![BigQuery console Schema tab for learning.customers: id, first\_name and last\_name have Mode REQUIRED, phone\_number is NULLABLE.](/images/the-not-null-constraint-in-bigquery/1-schema.jpg)

```sql
INSERT INTO `learning.customers`

SELECT 1 AS id, 'John' AS first_name, 'Doe' AS last_name, '555-12345' AS phone_number

UNION ALL

SELECT 2 AS id, NULL AS first_name, 'Doe' AS last_name, '555-12345' AS phone_number
```

The insert fails with the error `Required field first_name cannot be null`.
