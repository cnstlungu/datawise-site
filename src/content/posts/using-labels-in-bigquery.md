---
title: "Using Labels in BigQuery"
seoTitle: "BigQuery Labels: Track Costs and Manage Resources by Tag"
seoDescription: "BigQuery labels are key-value tags on jobs, tables, and datasets. Use them to break down billing by team, filter INFORMATION_SCHEMA, and manage via Terraform."
datePublished: 2023-09-25T21:18:50.147Z
dateUpdated: 2026-03-02T10:22:37.859Z
cover: "/images/using-labels-in-bigquery/cover.jpg"
coverCredit:
  name: "Angèle Kamp"
  url: "https://unsplash.com/@angelekamp"
series: "data-ops"
hashnodeCuid: "clmze56oz000308ld27v2crzo"
---

🔍 What exactly are BigQuery Labels? They're key-value pairs that you can associate with different BigQuery resources like datasets, tables, views, and even jobs within a session. Consider them as 'tags' that streamline the organization, tracking, and management of your resources.

In the examples shared, we demonstrate how to label BigQuery jobs within a query and then fetch them using the INFORMATION\_SCHEMA . JOBS view.

🌟 Wondering about how is it useful?

1️⃣ Expense Breakdown - With labels, you can categorize your BigQuery  
expenses by department, project, or any other segment, promoting clear billing.

```sql
SET @@query_label = "cost_center:demo";


SELECT id, max(ds_date) AS max_date

FROM learning.data_source

GROUP BY id
```

![Execution details: elapsed time 2 sec, slot time consumed 9 min 14 sec, bytes shuffled 5.3 MB, bytes spilled to disk 0 B.](/images/using-labels-in-bigquery/1-result.jpg)

```sql
SELECT creation_time, job_type, query, label.key, label.value, total_bytes_billed, total_bytes_processed, total_slot_ms

FROM `region-eu`.INFORMATION_SCHEMA.JOBS,

UNNEST(labels) AS label

WHERE label.key = 'cost_center'
```

![BigQuery results: one QUERY job, SELECT id, max(ds\_date) AS max\_date FROM learning.data\_source, with key cost\_center, value demo, total\_bytes\_billed 10485760, total\_bytes\_processed 6350528 and total\_slot\_ms 554752.](/images/using-labels-in-bigquery/1-result-2.jpg)

2️⃣ Efficient Resource Handling - Recognize and handle resources based on their labels, facilitating a tidy and systematic workspace.

3️⃣ Streamlined Automation - Pair labels with Cloud Functions or other GCP tools to automate tasks based on specific labeled criteria.

If you haven't explored labels in BigQuery yet, I urge you to do so. They offer a straightforward approach to instill organization and transparency in your data workspace.

Enjoy your data exploration! 📊
