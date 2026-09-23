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

![](/images/a-quick-walkthrough-bigquery-remote-functions/1.png)

## Step 2: Create a connection

![](/images/a-quick-walkthrough-bigquery-remote-functions/2.png)

![](/images/a-quick-walkthrough-bigquery-remote-functions/3.png)

## Step 3: Set up permissions

![](/images/a-quick-walkthrough-bigquery-remote-functions/4.png)

## Step 4: Bind the connection with Cloud Run function

![](/images/a-quick-walkthrough-bigquery-remote-functions/5.png)

## Test run

![](/images/a-quick-walkthrough-bigquery-remote-functions/6.png)

*Found it useful? Subscribe to my Analytics newsletter at* [***notjustsql.com***](https://www.notjustsql.com/)*.*
