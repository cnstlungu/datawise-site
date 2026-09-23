---
title: "MERGE ON FALSE in BigQuery"
seoTitle: "BigQuery MERGE ON FALSE: Atomic Delete and Insert"
seoDescription: "Learn how the ON FALSE clause in a BigQuery MERGE statement performs an atomic delete-then-insert (REPLACE) operation, and how pairing it with key..."
datePublished: 2023-09-16T14:15:37.912Z
dateUpdated: 2026-03-02T10:50:34.013Z
cover: "/images/merge-on-false-in-bigquery/cover.jpg"
coverCredit:
  name: "Chris Linnett"
  url: "https://unsplash.com/@chrislinnett"
series: "practical-sql"
hashnodeCuid: "clmm429x400010amnfemogmp4"
---

Merge statements are essential for crafting incremental datasets. They let us INSERT, UPDATE, and DELETE in a single command. 🛠️  
Recently, I dived into an [insightful blog post](https://levelup.gitconnected.com/powerful-feature-on-merge-statement-in-bigquery-i-e9c805b9bc9a) about the ON FALSE clause in merge statements. Ever heard of it?

Typical merge:

```sql
MERGE table1 AS target
USING table2 AS source ON table1.column = table2.column
WHEN MATCHED -- e.g., update target
WHEN NOT MATCHED BY source -- e.g., delete from target
WHEN NOT MATCHED BY target -- e.g., insert in target
```

But with ON FALSE in the merge\_condition? [BigQuery docs](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax#merge_statement) call it a "constant false predicate", perfect for atomic DELETEs on the target and INSERTs from a source. Essentially, a REPLACE operation.

I tested this on some data, especially after my previous post on [Primary and Foreign Keys](/bigquery-primary-key-foreign-key-constraints). The outcomes are looking super promising.

![BigQuery console Schema tab for table data\_source: fields id INTEGER with key PK/FK, value INTEGER with no key, and ds\_date DATE with key PK, all NULLABLE, showing the primary and foreign key constraints on the table.](/images/merge-on-false-in-bigquery/1.jpg)

```sql
-- NO PK/FK constraints  on the target table

MERGE `learning.data_source`  AS target

USING (

SELECT 44 AS id, 10 AS value, DATE('2023-09-01') AS ds_date

UNION ALL

SELECT 1000 AS id, 11 AS  value, DATE('2023-09-02') AS ds_date

) AS source

ON FALSE

WHEN NOT MATCHED BY TARGET THEN

INSERT ROW

WHEN MATCHED THEN

UPDATE SET target.value = source.value
```

![Execution details of the ON FALSE merge: elapsed time 1 sec, slot time consumed 12 sec, bytes shuffled 2.72 KB, bytes spilled to disk 0 B.](/images/merge-on-false-in-bigquery/2-result.jpg)

```sql
-- NO PK/FK constraints  on the target table

MERGE `learning.data_source`  AS target

USING (

SELECT 33 AS id, 7 AS value, DATE('2015-02-11') AS ds_date

UNION ALL

SELECT 999 AS id, 10 AS  value, DATE('2023-09-16') AS ds_date

) AS source

ON source.id = target.id AND source.ds_date = target.ds_date

WHEN NOT matched BY TARGET THEN

INSERT (id,ds_date,value)

VALUES (source.id, source.ds_date, source.value)

WHEN MATCHED THEN

UPDATE SET target.value = source.value
```

![Execution details of the key-based merge: elapsed time 5 sec, slot time consumed 14 min 13 sec, bytes shuffled 31.06 MB, bytes spilled to disk 0 B.](/images/merge-on-false-in-bigquery/2-result-2.jpg)

Testing that the expected changes happened.

```sql
WITH test_cases AS (


SELECT 33 AS id, 7 AS value, DATE('2015-02-11') AS ds_date

UNION ALL

SELECT 999 AS id, 10 AS  value, DATE('2023-09-16') AS ds_date

UNION ALL

SELECT 44 AS id, 10 AS value, DATE('2023-09-01') AS ds_date

UNION ALL

SELECT 1000 AS id, 11 AS  value, DATE('2023-09-02') AS ds_date
)

SELECT ds.* FROM learning.data_source ds

JOIN test_cases t USING (id, ds_date)
```

![BigQuery results: all four test rows are found, id 1000 value 11 on 2023-09-02, id 44 value 10 on 2023-09-01, id 33 value 7 on 2015-02-11 and id 999 value 10 on 2023-09-16.](/images/merge-on-false-in-bigquery/3-result.jpg)

Using the table version that has Primary Key and Foreign Key constraints has yielded even more impressive results.

```sql
-- PK/FK constraints  on the target table

MERGE `testing.data_source`  AS target

USING (

SELECT 44 AS id, 10 AS value, DATE('2023-09-01') AS ds_date

UNION ALL

SELECT 1000 AS id, 11 AS  value, DATE('2023-09-02') AS ds_date

) AS source

ON FALSE

WHEN NOT MATCHED BY TARGET THEN

INSERT ROW

WHEN MATCHED THEN

UPDATE SET target.value = source.value
```

![Execution details of the ON FALSE merge with PK/FK constraints: elapsed time 1 sec, slot time consumed 2 sec, bytes shuffled 84 B, bytes spilled to disk 0 B.](/images/merge-on-false-in-bigquery/4-result.jpg)

```sql
-- PK/FK constraints  on the target table

MERGE `testing.data_source`  AS target

USING (

SELECT 33 AS id, 7 AS value, DATE('2015-02-11') AS ds_date

UNION ALL

SELECT 999 AS id, 10 AS  value, DATE('2023-09-16') AS ds_date

) AS source

ON source.id = target.id AND source.ds_date = target.ds_date

WHEN NOT matched BY TARGET THEN

INSERT (id,ds_date,value)

VALUES (source.id, source.ds_date, source.value)

WHEN MATCHED THEN

UPDATE SET target.value = source.value
```

![Execution details of the key-based merge with PK/FK constraints: elapsed time 2 sec, slot time consumed 11 sec, bytes shuffled 56.02 MB, bytes spilled to disk 0 B.](/images/merge-on-false-in-bigquery/4-result-2.jpg)

Thanks for reading!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
