---
title: "Transactions in BigQuery"
seoTitle: "BigQuery Transactions: BEGIN and COMMIT Explained"
seoDescription: "Learn how BEGIN TRANSACTION and COMMIT TRANSACTION work in BigQuery for all-or-nothing multi-step operations. Any error inside the block rolls back all..."
datePublished: 2024-05-09T20:57:23.164Z
dateUpdated: 2026-03-02T10:50:58.795Z
cover: "/images/transactions-in-bigquery/cover.jpg"
coverCredit:
  name: "Brett Jordan"
  url: "https://unsplash.com/@brett_jordan"
series: "practical-sql"
hashnodeCuid: "clvzqbyzf00010al9ejwfcf67"
---

For a long time I didn't even know transactions existed in BigQuery. How are they useful?

Say you are performing a number of operations that you would like to succeed in full (so all steps are successful) or be aborted entirely (reverting to the previous state), basically ALL or NOTHING.

In case an error occurs in any of the operations inside the transaction block (BEGIN TRANSACTION -&gt; COMMIT TRANSACTION), all the operations are rolled back, with the state being reverted to what it was before.

The docs point out that use cases for transactions could include:  
\- changes to multiple tables at ones  
\- changes to one table in stages, based on some intermediate calculations we perform

In the example below, we wanted to perform another operation after inserting a row in the table, but upon encountering an error, that change is reverted as well, leaving us with the state we had before running this code.

![BigQuery SQL script with BEGIN TRANSACTION, an INSERT INTO learning.some\_table and a SELECT ERROR call before COMMIT TRANSACTION, plus an EXCEPTION WHEN ERROR THEN block that selects @@error.message and runs ROLLBACK TRANSACTION; the execution list shows the ERROR step failing and the rollback succeeding.](/images/transactions-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
