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

But with ON FALSE in the merge\_condition? [BigQuery docs](https://cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax#merge_statement) call it a "constant false predicate", perfect for atomic DELETEs on the target and INSERTs from a source. Essentially, a REPLACE operation.

I tested this on some data, especially after my previous post on [Primary and Foreign Keys](/bigquery-primary-key-foreign-key-constraints). The outcomes are looking super promising.

![](/images/merge-on-false-in-bigquery/1.jpg)

![](/images/merge-on-false-in-bigquery/2.jpg)

Testing that the expected changes happened.

![](/images/merge-on-false-in-bigquery/3.jpg)

Using the table version that has Primary Key and Foreign Key constraints has yielded even more impressive results.

![](/images/merge-on-false-in-bigquery/4.jpg)

Thanks for reading!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
