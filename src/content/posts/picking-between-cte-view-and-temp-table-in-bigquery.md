---
title: "Picking between CTE, View and Temp Table in BigQuery"
seoTitle: "CTE vs View vs Temp Table in BigQuery: How to Choose"
seoDescription: "A practical decision framework for choosing between CTEs, views, temp tables, materialized views, and staging tables in BigQuery."
datePublished: 2023-10-28T13:57:36.218Z
dateUpdated: 2026-03-02T10:51:08.557Z
cover: "/images/picking-between-cte-view-and-temp-table-in-bigquery/cover.jpg"
coverCredit:
  name: "JJ Ying"
  url: "https://unsplash.com/@jjying"
series: "practical-sql"
hashnodeCuid: "cloa3wva2000608l20w2c3c2g"
---

When it comes to choosing between different abstractions in your database system - be it CTE (common table expression), logical view, temporary table, materialized view, or a standalone staging table - what factors do you take into account?

Reflecting on my SQL Server work, here’s roughly my train of thought around these options:

\- CTE: My go-to for cleaning up my queries and enhancing readability.

\- Logical View: Ideal for scenarios where I intended to reuse my CTE, and the data volumes were manageable enough to not compromise performance.

\- Table-Valued Variables: Perfect for smaller tasks (think a handful of variables), especially when I didn't have tempdb permissions. This sometimes overlapped with my use of CTEs. You can also add an index to it.

\- Temp Table: This was the middle ground - not something I’d reuse across different workflows, yet substantial enough to demand more than what a CTE could offer without overloading tempdb. This also supported an index.

\- Standalone Materialized Staging Table: My choice for heavy-duty tasks. Whether it was something reusable or an exceptionally large dataset, this option provided the robustness I needed, complete with partitioning and indexing capabilities.

Nowadays, here's how I think about the same situation in BigQuery:

\- CTE: Even more of a staple in my toolkit, unless I hit a performance roadblock. Worth noting: it’s evaluated every time it’s called unless it’s recursive.

\- Temp Table: Not using it that often, although I know it can be a cost-effective alternative since it doesn’t persist like a materialized staging table. So storage savings are possible with this option.

\- Materialized Views: Yet to use one in production, but I’m excited about the flexibility and potential performance perks they bring to the table, also has some limitations. I think it would work great on pre-filtering or pre-aggregating a big result set.

\- Staging Table: My go-to when a CTE is called upon multiple times (or similar CTEs exist in multiple pipelines), or when I need to have partitioning and clustering ahead of a big join.

\- Logical View: When data volume isn’t an issue, and I’m looking to reuse and enhance readability, this is my pick. It also doubles up as a wrapper.

How does your decision tree look like? Which one do you use in which cases?

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Why partitioning tables is not a silver bullet for BigQuery performance](/why-partitioning-tables-is-not-a-silver-bullet-for-bigquery-performance)
- [Why you should care about partition pruning in BigQuery](/why-you-should-care-about-partition-pruning-in-bigquery)
- [Optimizing SQL queries in BigQuery](/optimizing-sql-queries-in-bigquery)
- [Optimizing compute cost in BigQuery](/optimizing-compute-cost-in-bigquery)
