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

![Google Cloud IAM project roles screenshot showing the service account mini-sa granted the BigQuery Job User role, which it needs to run BigQuery load jobs.](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/1.png)

Project roles for our service account

We’re also granted permission to the same service account to the Google Cloud Storage bucket from where we intend to load data from.

![Google Cloud Storage bucket permissions for the service account mini-sa, which holds the Storage Legacy Bucket Reader and Storage Legacy Object Reader roles on the source bucket.](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/2.png)

Bucket permissions for the service account

Next, we need to create a destination BigQuery dataset and provide the service account “Big Query Data Editor” role on it. Note that the dataset needs to be in the same GCP region (or multi-region) as the bucket load our data into.

![BigQuery Dataset Permissions panel for the destination dataset, with Show inherited permissions switched on and the BigQuery Data Editor role (2) granted to Editors of project and the mini-sa service account.](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/3.png)

BigQuery Destination dataset permissions

Now, let’s have a look at our file — a regular comma-delimited CSV, with the first row being the header row.

![Spreadsheet import preview of the orders CSV with columns date, order\_id, product\_id, price, quantity and amount: nine rows dated 2022-09-01 for order\_id 1 to 5, e.g. product 100 at price 4.5, quantity 2, amount 9.](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/4.png)

![CSV file in a text editor: header row date,order\_id,product\_id,price,quantity,amount followed by nine comma-delimited sales rows dated 2022-09-01, such as 2022-09-01,1,100,4.5,2,9.](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/5.png)

By our legend, this file follows the below naming convention, with the first part being the date of the sale.

![Google Cloud Storage bucket listing with two CSV files named by sale date, 20220901\_orders.csv and 20220902\_orders.csv, showing the date-prefixed naming convention.](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/6.png)

All good, now let’s get to the workflow itself.

#### Creating the workflow

![Google Cloud console Workflows page in project learning-by-doing-gcp with no workflows yet: the No workflows to display message, CREATE and START TUTORIAL buttons, and a New feature: Parallel Steps preview banner.](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/7.png)

In the dialog box we are presented, we give our workflow a name, pick the region and a service account (same as the one that we granted permissions above) to run the workflow under.

![Cloud Workflows create form: workflow name load-gcs-data, region europe-west6 (Zurich) and service account mini-sa, with an empty description and optional Labels and Triggers sections offering Add label and Add new trigger.](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/8.png)

If, let’s say, we’d like to read the file every day, that is — run the workflow on a particular schedule, we can create a Cloud Scheduler Trigger. This would automatically run the workflows at the given cadence.

Note that the project-level role “Workflows Invoker” needs to be attached to the service account triggering the Workflow.

![Google Cloud Create a Cloud Scheduler job dialog for the workflow trigger: name daily-12am-utc, region europe-west6 (Zurich), frequency 0 12 \* \* \* in unix-cron format, timezone UTC, workflow argument {}, No logs call level and service account mini-sa.](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/9.png)

A workflow with a trigger would look as follows

![Cloud Workflows create form for load-gcs-data (europe-west6, service account mini-sa) with a Cloud Scheduler trigger added: daily-12am-utc on schedule 0 12 \* \* \*, timezone Etc/UTC, region europe-west6, above the Next button.](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/10.png)

#### Creating the steps

We now have the Workflow development window, where we can write the definition for our workflow in YAML-esque syntax. If you aren’t familiar with Workflow syntax, a good place to start is the [Workflows tutorials page](https://cloud.google.com/functions/docs/tutorials). Also, note the pane on the right side, illustrating our control flow

![Cloud Workflows editor with the default sample workflow in YAML (steps checkSearchTermInInput with a switch, getCurrentTime and readWikipedia using http.get, setFromCallResult, returnOutput) and the Visualization pane drawing those steps as a flowchart from START.](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/11.png)

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

![BigQuery schema tab of the sales\_autodetect table loaded with schema auto-detection: date DATE, order\_id INTEGER, product\_id INTEGER, price FLOAT, quantity INTEGER and amount FLOAT, all NULLABLE.](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/12.png)

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

![BigQuery query result of the table loaded with a provided schema: columns date, order\_id, product\_id, price, quantity and amount across nine 2022-09-02 rows, e.g. order 6 buying product 100 at price 4.5, quantity 3, amount 13.5.](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/13.png)

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

![BigQuery sales table page with the notice This is a partitioned table; the schema tab lists date DATE, order\_id INTEGER, product\_id INTEGER, price NUMERIC, quantity INTEGER and amount NUMERIC, all NULLABLE.](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/14.png)

![BigQuery SQL on the partitioned sales\_data.sales table selecting date AS SalesDate, count(distinct order\_id) AS CountOrders and sum(Amount) AS TotalAmount, GROUP BY date; results show 2022-09-02 with 5 orders and 135.8, and 2022-09-01 with 5 orders and 93.7.](/images/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows/15.png)

#### Conclusion

As we have seen in this exercise, loading data from Google Cloud Storage into BigQuery using Cloud Workflows is quite straightforward and allows us to leverage the BQ API to build repeatable and low-overhead data pipelines in Google Cloud. Thanks for reading!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using GCP Cloud Functions in Data Engineering](/using-gcp-cloud-functions-in-data-engineering)
- [What are GCP Cloud Workflows and how can they help you as a Data Engineer](/what-are-gcp-cloud-workflows-and-how-can-they-help-you-as-a-data-engineer)
- [Scheduled queries in BigQuery](/scheduled-queries-in-bigquery)
- [Using the bq CLI utility with BigQuery](/using-the-bq-cli-utility-with-bigquery)
