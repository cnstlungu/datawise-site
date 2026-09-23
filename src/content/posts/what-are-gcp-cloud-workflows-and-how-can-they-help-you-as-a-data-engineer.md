---
title: "What are GCP Cloud Workflows and how can they help you as a Data Engineer"
seoTitle: "GCP Cloud Workflows for BigQuery Orchestration"
seoDescription: "Cloud Workflows is a serverless GCP orchestration engine that can replace Airflow for simple BigQuery pipelines."
datePublished: 2024-05-24T05:12:54.320Z
dateUpdated: 2026-03-29T07:43:21.024Z
cover: "/images/what-are-gcp-cloud-workflows-and-how-can-they-help-you-as-a-data-engineer/cover.jpg"
coverCredit:
  name: "Denys Nevozhai"
  url: "https://unsplash.com/@dnevozhai"
series: "practical-sql"
hashnodeCuid: "clwk8750w00000akv9kixdajr"
---

A reminder that you don't necessarily need Airflow / Composer to orchestrate data in and out of BigQuery. If your workflows are not that complex or numerous, take a look at Google Cloud Workflows.  
  
It's a serverless orchestration engine, with good integration with other GCP services, but you can also call external APIs.  
  
Some advantages I see:  
\- serverless, no servers to manage  
\- your workflows stored as code, manage Infra as Code with Terraform  
\- interact with external APIs  
\- good connectors to interact with other GCP services  
\- straightforward pricing: at the time of writing: 5k steps free per month, 0.01 USD per 1k steps after, external API call are priced separately (2k/mo free, 0.025 USD per 1k after)  
  
I've used it before to load data from Google Cloud Storage into BigQuery tables on a schedule and perform other simple tasks. It gets the job done with no fuss. You can of course schedule the Workflow to run with Cloud Scheduler.  
  
See [my previous post](/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows) for a short walk through showcasing how BQ and Workflows play together.

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using GCP Cloud Functions in Data Engineering](/using-gcp-cloud-functions-in-data-engineering)
- [Loading data from Google Cloud Storage into BigQuery using Cloud Workflows](/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows)
- [Scheduled queries in BigQuery](/scheduled-queries-in-bigquery)
- [Using the bq CLI utility with BigQuery](/using-the-bq-cli-utility-with-bigquery)

- [Preparing for the AWS Certified Data Analytics - Specialty (DAS-C01) Certification](/preparing-for-the-aws-certified-data-analytics-specialty-das-c01-certification)
