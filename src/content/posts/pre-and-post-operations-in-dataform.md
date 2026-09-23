---
title: "pre_ and post_operations in Dataform"
subtitle: ""
seoTitle: "pre_ and post_operations in Dataform Explained"
seoDescription: "Learn how to use pre_ and post_operations in Dataform to manage variables, incremental watermarks, cleanup logic, and post-run tasks."
datePublished: 2026-05-20T07:11:29.953Z
dateUpdated: 2026-05-20T07:11:49.631Z
cover: "/images/pre-and-post-operations-in-dataform/cover.jpg"
series: "practical-sql"
tags: ["bigquery", "sql", "dataform", "google-cloud"]
hashnodeCuid: "cmpdq43hd006w1sn8cvep7ykj"
---

Here's a useful Dataform concept: pre\_operations and post\_operations. As the name implies, these represent a set of actions that run before and after the main operation (table, view, or SQL operations).

In practice it enables you to cleanly:

➡️ Declare and set a variable

➡️ Clean up before inserting into a table

➡️ Compute a watermark for your incremental model

➡️ Log run metadata after execution

➡️ Perform a maintenance task

What's the most interesting use case you've seen for pre\_operations / post\_operations (or pre\_hook / post\_hook if you're on dbt)?

![](/images/pre-and-post-operations-in-dataform/1.png)
