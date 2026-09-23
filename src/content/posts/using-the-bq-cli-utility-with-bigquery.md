---
title: "Using the bq CLI utility with BigQuery"
seoTitle: "BigQuery bq CLI: Queries, Tables, and IAM from Terminal"
seoDescription: "The bq command-line tool lets you run queries, manage tables, load data, and view IAM policies in BigQuery without the Console."
datePublished: 2024-05-24T05:02:45.443Z
dateUpdated: 2026-03-02T10:51:51.326Z
cover: "/images/using-the-bq-cli-utility-with-bigquery/cover.jpg"
coverCredit:
  name: "Gabriel Heinzer"
  url: "https://unsplash.com/@6heinz3r"
series: "practical-sql"
hashnodeCuid: "clwk7u37n000i09l36tamaxo5"
---

Remember that in additional to the Cloud Console GUI or client libraries, you can also perform BigQuery tasks using the `bq` command-line interface.

It's included with the gcloud SDK and once you have logged in, you can perform a number of operations such as:  
\- run queries against BQ  
\- create, copy and delete tables  
\- load data into tables  
\- view IAM policies for a BQ asset and much more

How I've used it until now:  
\- [impersonate service accounts](/using-subqueries-with-row-level-security-in-bigquery)  
\- perform operations that are/were not supported in the SQL interface, such as [copying partitions between tables](/swapping-partitions-in-bigquery)

Any other interesting ways you're using the bq cli tool?

![Bash terminal running the bq CLI: bq query --use\_legacy\_sql=false with SELECT \* FROM learning.employee\_data; the output is an ASCII table of nine employees with columns employee\_id, first\_name, last\_name and manager\_id, where John Smith has a NULL manager\_id.](/images/using-the-bq-cli-utility-with-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using GCP Cloud Functions in Data Engineering](/using-gcp-cloud-functions-in-data-engineering)
- [What are GCP Cloud Workflows and how can they help you as a Data Engineer](/what-are-gcp-cloud-workflows-and-how-can-they-help-you-as-a-data-engineer)
- [Loading data from Google Cloud Storage into BigQuery using Cloud Workflows](/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows)
- [Scheduled queries in BigQuery](/scheduled-queries-in-bigquery)
