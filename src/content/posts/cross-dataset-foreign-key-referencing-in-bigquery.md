---
title: "Cross-dataset Foreign Key referencing in BigQuery"
seoTitle: "BigQuery Cross-Dataset Foreign Keys Using Table Clones"
seoDescription: "BigQuery primary and foreign key constraints require tables to be in the same dataset, but table clones offer a workaround."
datePublished: 2024-04-19T14:51:22.575Z
dateUpdated: 2026-04-05T20:11:19.422Z
cover: "/images/cross-dataset-foreign-key-referencing-in-bigquery/cover.jpg"
coverCredit:
  name: "Jozsef Hocza"
  url: "https://unsplash.com/@hocza"
series: "practical-sql"
hashnodeCuid: "clv6sg8r3000909l05vzs7t4p"
---

In one of [my previous posts](/bigquery-primary-key-foreign-key-constraints) I've written about the then-newly-added Primary Key/Foreign Key constraints in BigQuery.

While they are not enforced like traditional RDBMS, they can still provide an improvement to query performance.

They have one important catch though - tables with a primary key and foreign key relationships must be in the same dataset - see error in (1)

How do you go around that?

Well, you could just do a regular copy of the referenced table into your dataset, but it would incur additional storage costs. Maybe not worth it if the table is big.

But there's another BQ feature we can use - table clones.

We can create a table clone of the table we want to reference in our desired dataset (2).

Then, we can reference the table clone when defining the Foreign Key constraints. (3)

We should keep in mind that identical data from source table and clone table is charged only one - so you'd only pay for the storage of different data, if that's the case.

![BigQuery SQL in three steps: ADD FOREIGN KEY(id) references auxiliary.ids(id) fails with FOREIGN KEY constraint cannot reference a table in a different dataset; CREATE OR REPLACE TABLE learning.ids CLONE auxiliary.ids with a PRIMARY KEY NOT ENFORCED; then the foreign key to learning.ids(id) succeeds.](/images/cross-dataset-foreign-key-referencing-in-bigquery/1.jpg)

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Cross-dataset foreign key relationships in BigQuery](/cross-dataset-foreign-key-relationships-in-bigquery)
