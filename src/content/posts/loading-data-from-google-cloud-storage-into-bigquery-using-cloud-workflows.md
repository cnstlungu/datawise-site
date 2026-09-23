---
title: "Loading data from Google Cloud Storage into BigQuery using Cloud Workflows"
seoTitle: "Load GCS Data to BigQuery with Cloud Workflows"
seoDescription: "Step-by-step guide to loading CSV files from Google Cloud Storage into BigQuery using Cloud Workflows. Learn to set up IAM, auto-detect schemas, and load..."
datePublished: 2022-10-04T22:52:23.622Z
dateUpdated: 2026-03-02T10:51:58.031Z
cover: "/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/cover.png"
series: "data-ops"
hashnodeCuid: "clfmn9zn5000p0amlcs0yd6jz"
---

[Google Cloud Workflows](https://cloud.google.com/workflows/docs/overview) is a serverless orchestration platform that allows us to combine services into repeatable and observable sets of actions, connecting typically other GCP services. These are called, you guessed it, **workflows**.

While working as a Data Engineer and extensively using Apache Airflow (and its GCP implementation called Composer), I was a little skeptical in the beginning about what it is offering but came to appreciate its straightforwardness and simplicity.

In this quick exercise, we’re going to illustrate a simple use case — loading a CSV file from Google Cloud Storage into BigQuery.

#### Preparation work

Let’s set up the appropriate accounts and permissions. For this job, we’ve created a service account and assigned it the role “Big Query Job User”

![](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/1.png)

Project roles for our service account

We’re also granted permission to the same service account to the Google Cloud Storage bucket from where we intend to load data from.

![](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/2.png)

Bucket permissions for the service account

Next, we need to create a destination BigQuery dataset and provide the service account “Big Query Data Editor” role on it. Note that the dataset needs to be in the same GCP region (or multi-region) as the bucket load our data into.

![](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/3.png)

BigQuery Destination dataset permissions

Now, let’s have a look at our file — a regular comma-delimited CSV, with the first row being the header row.

![](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/4.png)

![](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/5.png)

By our legend, this file follows the below naming convention, with the first part being the date of the sale.

![](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/6.png)

All good, now let’s get to the workflow itself.

#### Creating the workflow

![](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/7.png)

In the dialog box we are presented, we give our workflow a name, pick the region and a service account (same as the one that we granted permissions above) to run the workflow under.

![](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/8.png)

If, let’s say, we’d like to read the file every day, that is — run the workflow on a particular schedule, we can create a Cloud Scheduler Trigger. This would automatically run the workflows at the given cadence.

Note that the project-level role “Workflows Invoker” needs to be attached to the service account triggering the Workflow.

![](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/9.png)

A workflow with a trigger would look as follows

![](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/10.png)

#### Creating the steps

We now have the Workflow development window, where we can write the definition for our workflow in YAML-esque syntax. If you aren’t familiar with Workflow syntax, a good place to start is the [Workflows tutorials page](https://cloud.google.com/functions/docs/tutorials). Also, note the pane on the right side, illustrating our control flow

![](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/11.png)

We now need the build the workflow logic. For this exercise, we’ll need to check the configuration options we can set up for the BigQuery job, documented at the following link

[**Method: googleapis.bigquery.v2.jobs.insert | Workflows | Google Cloud**  
\*Whether your business is early in its journey or well on its way to digital transformation, Google Cloud can help solve…\*cloud.google.com](https://cloud.google.com/workflows/docs/reference/googleapis/bigquery/v2/jobs/insert)

The easiest approach is to try to load data while using the schema auto-detect. Note the `autodetect: true` part in the load configuration.

The below code will:

* declare a resultsList List where we would accumulate job results
    
* create a BigQuery insert job with a set of provided arguments
    
* append the end state of the insert job to the list previously created
    
* print the list of job statuses us upon workflow completion
    

```yaml
- declare:
    assign:
        - resultsList: []

- insertAutoDetect:
    call: googleapis.bigquery.v2.jobs.insert
    args:
        projectId: "YOUR-PROJECT-ID-HERE"
        body:
            configuration:
                load:
                    autodetect: true
                    destinationTable:
                        datasetId: "sales_data"
                        projectId: "YOUR-PROJECT-ID-HERE"
                        tableId: "sales_autodetect"
                    fieldDelimiter: ","
                    skipLeadingRows: 1
                    sourceFormat: "csv"
                    sourceUris: "gs://YOUR-BUCKET-NAME-HERE/20220901_orders.csv"
                    writeDisposition: "WRITE_TRUNCATE"
    result: insertAutoDetectResult
- appendInsertAutoDetectResult:
    assign:
      - resultsList: '${list.concat(resultsList, insertAutoDetectResult.status.state + " for " + insertAutoDetectResult.configuration.load.destinationTable.tableId)}'

- returnOutput:
    return: ${resultsList}
```

*[View on GitHub Gist](https://gist.github.com/cnstlungu/e7507e0b71660d94ca58d2fcd747d450)* 

BigQuery has auto-detected the column types and loaded the data.

![](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/12.png)

If we were to choose to provide the schema to the job, we can do the following:

```yaml
- declare:
    assign:
        - resultsList: []

- insertWithProvidedSchema:
    call: googleapis.bigquery.v2.jobs.insert
    args:
        projectId: "YOUR-PROJECT-ID-HERE"
        body:
            configuration:
                load:
                    destinationTable:
                        datasetId: "sales_data"
                        projectId: "YOUR-PROJECT-ID-HERE"
                        tableId: "sales_provided_schema"
                    fieldDelimiter: ","
                    schema:
                        fields:
                            - name: "date"
                              type: "DATE"
                            - name: "order_id"
                              type: "INTEGER"
                            - name: "product_id"
                              type: "INTEGER"
                            - name: "price"
                              type: "NUMERIC"
                            - name: "quantity"
                              type: "INTEGER"
                            - name: "amount"
                              type: "NUMERIC"
                    skipLeadingRows: 1
                    sourceFormat: "csv"
                    sourceUris: "gs://YOUR-BUCKET-NAME-HERE/20220902_orders.csv"
                    writeDisposition: "WRITE_TRUNCATE"
    result: insertWithProvidedSchemaResult
    
- appendinsertWithProvidedSchemaResult:
    assign:
      - resultsList: '${list.concat(resultsList, insertWithProvidedSchemaResult.status.state + " for " + insertWithProvidedSchemaResult.configuration.load.destinationTable.tableId)}'
```

*[View on GitHub Gist](https://gist.github.com/cnstlungu/befa89679a802613202c49c3f96dac92)* 

Upon execution, this produces the following result.

![](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/13.png)

What if we have a slightly more advanced use case, and would like to read hundreds of files, which can be quite big, into a partitioned table? The code could look something like the one below.

Notice the following:

* timePartitioning by “DAY” based on field **date**
    
* the sourceUris now has a wildcard “\*” to catch all the files ending in “\_orders.csv”.
    

```yaml
- declare:
    assign:
        - resultsList: []

- insertIntoPartitioned:
    call: googleapis.bigquery.v2.jobs.insert
    args:
        projectId: "YOUR-PROJECT-HERE"
        body:
            configuration:
                load:
                    destinationTable:
                        datasetId: "sales_data"
                        projectId: "YOUR-PROJECT-HERE"
                        tableId: "sales"
                    fieldDelimiter: ","
                    timePartitioning:
                      field: "date"
                      type: "DAY"
                    schema:
                        fields:
                            - name: "date"
                              type: "DATE"
                            - name: "order_id"
                              type: "INTEGER"
                            - name: "product_id"
                              type: "INTEGER"
                            - name: "price"
                              type: "NUMERIC"
                            - name: "quantity"
                              type: "INTEGER"
                            - name: "amount"
                              type: "NUMERIC"
                    skipLeadingRows: 1
                    sourceFormat: "csv"
                    sourceUris: "gs://YOUR-BUCKET-NAME-HERE/*_orders.csv"
                    writeDisposition: "WRITE_TRUNCATE"
    result: insertIntoPartitionedResult
- appendInsertIntoPartitionedResult:
    assign:
      - resultsList: '${list.concat(resultsList, insertIntoPartitionedResult.status.state + " for " + insertIntoPartitionedResult.configuration.load.destinationTable.tableId)}'
```

*[View on GitHub Gist](https://gist.github.com/cnstlungu/4c7237408a32161341f2e7ee2ade18cd)* 

We now have a partitioned table

![](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/14.png)

![](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/15.png)

#### Conclusion

As we have seen in this exercise, loading data from Google Cloud Storage into BigQuery using Cloud Workflows is quite straightforward and allows us to leverage the BQ API to build repeatable and low-overhead data pipelines in Google Cloud. Thanks for reading!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using GCP Cloud Functions in Data Engineering](/using-gcp-cloud-functions-in-data-engineering)
- [What are GCP Cloud Workflows and how can they help you as a Data Engineer](/what-are-gcp-cloud-workflows-and-how-can-they-help-you-as-a-data-engineer)
- [Scheduled queries in BigQuery](/scheduled-queries-in-bigquery)
- [Using the bq CLI utility with BigQuery](/using-the-bq-cli-utility-with-bigquery)
