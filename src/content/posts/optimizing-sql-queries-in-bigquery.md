---
title: "Optimizing SQL queries in BigQuery"
seoTitle: "BigQuery SQL Query Optimization: 11-Point Checklist"
seoDescription: "An actionable BigQuery query tuning checklist covering early filtering, partition pruning, deduplication, integer keys, CTE reuse, and nested data — with..."
datePublished: 2023-08-20T07:05:12.334Z
dateUpdated: 2026-03-02T10:52:00.287Z
cover: "/images/optimizing-sql-queries-in-bigquery/cover.jpg"
coverCredit:
  name: "Danil Shostak"
  url: "https://unsplash.com/@max010"
series: "bigquery-performance"
hashnodeCuid: "cllj3sqry000f09mmaqp0agx7"
---

When it comes to tuning a [#SQL](https://www.linkedin.com/feed/hashtag/?keywords=sql&highlightedUpdateUrns=urn%3Ali%3Aactivity%3A7098686521628581889) query in [#BigQuery](https://www.linkedin.com/feed/hashtag/?keywords=bigquery&highlightedUpdateUrns=urn%3Ali%3Aactivity%3A7098686521628581889) for top performance and cost-efficiency, here's my starting point:

🔍 1. Early Filtering:  
\- Filter out unnecessary rows at the earliest.  
\- Only select columns that are required.  
\- Remove all the redundant tables.

📊 2. Early Aggregation:  
If you're joining tables that need to be aggregated, always aggregate to the target granularity early on, before the join.

🔢 3. De-duplication:  
\- De-duplicate early to reduce row count and operate at the desired granularity.  
\- Use explicit de-duplication, such as ROW\_NUMBER() OVER (PARTITION BY a,b,c ORDER BY d asc/desc) coupled with QUALIFY for a compact form.

🔗 4. Partitioning & Clustering:  
\- Ensure joined tables are partitioned and clustered properly.  
\- Confirm partition pruning takes place: when using the partitioned column in a JOIN or WHERE clause, avoid on-the-fly transformations like DATETIME(left\_table.timestamp\_partitioning\_column, timezone) = right\_table.datetime\_partitioning\_column. This will hinder partition elimination.  
\- If clustering by multiple columns, ensure it mirrors the join and filter usage to be effective. If needed and possible, adjust clustering.

🔑 5. Data Types:  
\- Prefer integer keys over strings for joins.  
\- Transform columns to the appropriate data type: e.g. timestamps containing only a date to the date type.

🔗 6. Common Table Expressions (CTEs):  
\- Reuse of non-recursive CTE multiple times? Consider moving it to separate staging tables.  
\- Heavy operations in a CTE? Think about extracting it as a staging table, then partition and cluster it for subsequent joins.

🔀 7. Unnesting:  
\- While nested data is powerful, avoid unnesting when you can.  
For intervals like \[valid\_from, valid\_to\], refrain from unnesting them and work with the interval if possible.

⚠️ 8. Cross Joins:  
Limit their usage. BigQuery isn't fond of joins with more outputs than inputs.

📈 9. Order By:  
Only use ORDER BY in the last query or when necessary in window functions.

📜 10. Leverage Nested Data:  
Aggregate large rowsets of the same type into one ARRAY using ARRAY\_AGG to capitalize on compression benefits.

🔬 11. Experiment, Experiment, Experiment:  
The optimization journey is paved with trials and iterations. Aim for the best results by employing multiple strategies and seeing which one emerges as the most efficient in terms of runtime, slot time usage, and bytes processed. Often, hands-on experimentation reveals insights that theory might miss.  
Always remember, each query is unique. While this checklist provides a solid foundation, fine-tuning will often be specific to your individual use case.

Make sure to check out [BigQuery Documentation on the best practices](https://cloud.google.com/bigquery/docs/best-practices-performance-compute) and the [BigQuery Anti-pattern recognition tool](https://cloud.google.com/blog/products/data-analytics/bigquery-anti-pattern-recognition-tool-optimizes-performance).

Happy querying! 💼🚀

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Why partitioning tables is not a silver bullet for BigQuery performance](/why-partitioning-tables-is-not-a-silver-bullet-for-bigquery-performance)
- [Why you should care about partition pruning in BigQuery](/why-you-should-care-about-partition-pruning-in-bigquery)
- [Optimizing compute cost in BigQuery](/optimizing-compute-cost-in-bigquery)
- [Optimizing storage costs in BigQuery](/optimizing-storage-costs-in-bigquery)
