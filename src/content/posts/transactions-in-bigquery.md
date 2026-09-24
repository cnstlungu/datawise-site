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

```sql
BEGIN

  BEGIN TRANSACTION;
  -- ALL OR NOTHING: Operations inside transaction happen successfully as a whole,
  -- or are being rolled back to previous state
  INSERT INTO learning.some_table
    VALUES (1, 'New York', 'USA');

  -- An operation that produces an error.
  SELECT ERROR("Some VERY unexpected error");
  COMMIT TRANSACTION;

EXCEPTION WHEN ERROR THEN
  -- Rollback the transaction and the changes happening inside it
  SELECT @@error.message;
  ROLLBACK TRANSACTION;
END;
```

![BigQuery script results: 5 statements processed in 4 sec; BEGIN TRANSACTION, INSERT INTO learning.some\_table, SELECT @@error.message and ROLLBACK TRANSACTION succeed, while SELECT ERROR("Some VERY unexpected error") fails.](/images/transactions-in-bigquery/1-result.jpg)
