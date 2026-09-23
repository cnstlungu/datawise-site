---
title: "A quick walkthrough BigQuery Remote Functions"
seoTitle: "BigQuery Remote Functions: Quick Guide"
seoDescription: "Explore how BigQuery Remote Functions enable data processing using external resources with step-by-step guidance"
datePublished: 2025-03-08T22:16:09.060Z
dateUpdated: 2026-03-02T10:51:52.454Z
cover: "/images/a-quick-walkthrough-bigquery-remote-functions/cover.jpg"
coverCredit:
  name: "Willian Justen de Vasconcellos"
  url: "https://unsplash.com/@willianjusten"
series: "data-ops"
hashnodeCuid: "cm80rkdic000009jp4rkq51l5"
---

In [a previous post](/a-quick-overview-of-bigquery-functions), I mentioned Remote Functions—a powerful way to send data from BigQuery to an external service for processing, including a Cloud Run function.

This is especially useful when SQL lacks built-in support for your specific needs, and writing a UDF isn’t an option (for example, if you need a highly specialized Python function).

Before building your own, check out [bigfunctions](https://unytics.io/bigfunctions/)—many common use cases have already been solved by others!

## What are remote functions in BigQuery?

These are a special type of function that delegates processing of input to an external resource, allowing us to:

* **send** **data** from BigQuery to Google Cloud Functions or other external services
    
* **process** **it** using a programming language
    
* **return results** to our query
    

## Why is that important?

A Google Remote function can encapsulate any kind of logic in major programming languages.

This opens the door to vast a ecosystem of libraries such at the Python packages.

Let’s look at a step-by-step example of creating a Remote Function.

## Step 1: Create the Cloud Run Function

![Python source of a Cloud Run function (entry point get\_next\_public\_holiday) in the Cloud Run console: it reads the BigQuery calls array from request.get\_json(), uses holidays.country\_holidays and next() to find each country's next holiday, and returns jsonify with a replies list.](/images/a-quick-walkthrough-bigquery-remote-functions/1.png)

## Step 2: Create a connection

![BigQuery console screenshot of the External data source panel for a new connection: type Vertex AI remote models, remote functions and BigLake (Cloud Resource), Connection ID test-remote-functions, US multi-region, and the CREATE CONNECTION button.](/images/a-quick-walkthrough-bigquery-remote-functions/2.png)

![BigQuery console screenshot of the Connection info page for test-remote-functions in the us location, type Cloud Resource, with the service account id shown as a YOUR SERVICE ACCOUNT placeholder at gcp-sa-bigquery-condel.iam.gserviceaccount.com.](/images/a-quick-walkthrough-bigquery-remote-functions/3.png)

## Step 3: Set up permissions

![Cloud Run console screenshot with the test-bigquery-processing function selected and the PERMISSIONS button highlighted; the Permissions panel shows the Cloud Run Invoker role granted to a YOUR SERVICE ACCOUNT FROM (2) placeholder, meaning the connection's service account.](/images/a-quick-walkthrough-bigquery-remote-functions/4.png)

## Step 4: Bind the connection with Cloud Run function

![BigQuery SQL CREATE FUNCTION learning.get\_next\_public\_holidays(country\_code STRING) RETURNS STRING REMOTE WITH CONNECTION to an eu test-bigquery-connection, with OPTIONS endpoint set to the Cloud Run europe-west1.run.app URL; red placeholders mark your project, connection and endpoint.](/images/a-quick-walkthrough-bigquery-remote-functions/5.png)

## Test run

![BigQuery SQL calling the remote function learning.get\_next\_public\_holidays(country\_code) for RO, BE and VN; results read Next holiday is on 2025-04-18 and is called Easter for RO, 2025-04-20 Easter Sunday for BE and 2025-04-07 Hung Kings' Commemoration Day for VN.](/images/a-quick-walkthrough-bigquery-remote-functions/6.png)

*Found it useful? Subscribe to my Analytics newsletter at* [***notjustsql.com***](https://www.notjustsql.com/)*.*
