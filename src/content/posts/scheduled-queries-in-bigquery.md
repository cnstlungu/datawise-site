---
title: "Scheduled queries in BigQuery"
seoTitle: "BigQuery Scheduled Queries: UI, Terraform, and API Setup"
seoDescription: "Create BigQuery Scheduled Queries via the console, Terraform, or REST API. Covers cron syntax, write disposition, backfill, and monitoring execution history."
datePublished: 2023-09-02T22:05:58.629Z
dateUpdated: 2026-04-05T20:11:25.253Z
cover: "/images/scheduled-queries-in-bigquery/cover.jpg"
coverCredit:
  name: "Eric Rothermel"
  url: "https://unsplash.com/@erothermel"
series: "data-ops"
hashnodeCuid: "clm2kp7tx000608l7ecck8cqc"
---

### What are Scheduled Queries?

Scheduled Queries in BigQuery allow users to run SQL tasks on a predefined, automated schedule.

Instead of manually initiating a query each day or week, BigQuery can do it for you. This is perfect for light orchestration of repetitive data transformations, updates, and regular reporting tasks.

### Creating a Scheduled Query manually

A scheduled query can be created manually using the **Schedule button** in the Query window.

![BigQuery console query editor with the Schedule button highlighted in red, above the query SELECT GENERATE\_UUID() AS unique\_identifier, CURRENT\_TIMESTAMP() AS ingestion\_timestamp and its one-row result.](/images/scheduled-queries-in-bigquery/1.png)

A dialog box is presented where we are prompted to provide the following information:

* a name for the scheduled query
    
* a scheduling option or the option to run it manually (on demand)
    
* start date and end date for which this query would run
    
* optionally, a destination dataset and table for the query result (including the possibility of adding a partitioning field)
    
* region selection
    
* encryption options
    
* principal (user or service account) to run the query under
    
* write disposition, in order words what to do with the contents already in the table: keep (and append new data) or overwrite (and replace with the new data)
    
* notification options
    

![BigQuery New scheduled query dialog: custom repeat frequency every day 22:00 with a help popup of schedule syntax examples, start now and end never, and a destination table example\_table in dataset learning with Append to table or Overwrite table.](/images/scheduled-queries-in-bigquery/2.png)

![Lower half of the BigQuery New scheduled query dialog: EU multi-region location, Google-managed or customer-managed (CMEK) encryption, a service account field annotated Service account to run query as, and email or Pub/Sub notification options.](/images/scheduled-queries-in-bigquery/3.png)

### Creating a scheduled query using Terraform

A schedule can also be created using Terraform, as per the following example.

This option provides a subset of options from the manual method - at the time of writing, for example, the write disposition cannot be set up here.

```bash
variable "envConfig" {

    type = map(object({
        project_id = string
        service_account_name = string
    }))
}

variable "config" {
    type = map(object({
        name = string
        query = string
        destination_table_name_template = string
    }))
}
```

```bash
resource "google_bigquery_data_transfer_config" "query_config" {
    for_each = var.config
    display_name = each.value["name"]
    location = "europe"
    data_source_id = "scheduled_query"
    schedule = "every saturday 05:00"
    destination_dataset_id = "learning"
    params = {
        destination_table_name_template = each.value["destination_table_name_template"]
        write_disposition = "WRITE_APPEND"
        query = each.value["query"]
    }
    service_account_name = var.envConfig["dev"].service_account_name
    project = var.envConfig["dev"].project_id
}
```

### Creating a Scheduled Query using the API

It's also possible to create a scheduled query using one of the BigQuery APIs or the bq CLI command - check the GCP documentation [here](https://cloud.google.com/bigquery/docs/scheduling-queries#python).

### Viewing scheduled queries

Viewing the scheduled query can be done by Accessing the 'Scheduled queries' option in the BigQuery subgroup.

It will display a list of queries, their schedule, region, destination (if any) and next run time.

![BigQuery Scheduled queries page listing tf\_table\_query, source Scheduled Query, schedule every saturday 05:00 UTC, region europe, destination dataset learning, next run September 2, 2023; an annotation says clicking it lets you view all runs.](/images/scheduled-queries-in-bigquery/4.png)

Click on a particular query would present a Run history and its output. There is also an option for scheduling a backfill (which we can use for a Manual Run).

![BigQuery Scheduled query details for tf\_table\_query on the Run history tab, listing two successful transfer runs from August 30, 2023; annotations point to the Configuration tab and to Schedule backfill for a manual run.](/images/scheduled-queries-in-bigquery/5.png)

Clicking on the **Configuration** tab would display the configurations used to create the query.

![BigQuery Scheduled query details Configuration tab for tf\_table\_query: schedule every saturday 05:00 UTC, destination dataset learning, query string SELECT CURRENT\_TIMESTAMP() AS ingestion\_timestamp, GENERATE\_UUID() AS unique\_identifier into tf\_table with WRITE\_APPEND; resource name and user are redacted.](/images/scheduled-queries-in-bigquery/6.png)

In conclusion, BigQuery Scheduled queries can be a useful tool in your toolset, as a quick and easy way to do light orchestration of SQL tasks.

Thanks for reading!

---

🚀 Delving into BigQuery, Google Cloud and Analytics? Stay connected with me for valuable insights, handy tips, and strategies to effortlessly traverse the vast universe of cloud computing and data analytics!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using GCP Cloud Functions in Data Engineering](/using-gcp-cloud-functions-in-data-engineering)
- [What are GCP Cloud Workflows and how can they help you as a Data Engineer](/what-are-gcp-cloud-workflows-and-how-can-they-help-you-as-a-data-engineer)
- [Loading data from Google Cloud Storage into BigQuery using Cloud Workflows](/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows)
- [Using the bq CLI utility with BigQuery](/using-the-bq-cli-utility-with-bigquery)
- [Replicating datasets across regions in BigQuery](/replicating-datasets-across-regions-in-bigquery)
