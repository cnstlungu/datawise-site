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

![Cloud Run console service details for test-bigquery-processing in europe-west1: all deployment steps completed, the service URL is marked as your endpoint URL, and the Source tab shows base image Python 3.12 and function entry point get\_next\_public\_holiday.](/images/a-quick-walkthrough-bigquery-remote-functions/1-output.png)

```python
    try:
        # Read request JSON (BigQuery sends input in "calls" array)
        request_json = request.get_json()
        calls = request_json.get("calls", [])

        responses = []  # This will store the results

        today = datetime.date.today()
        year = today.year

        for call in calls:
            try:
                country_code = call[0].upper()  # Extract country_code from input
                country_holidays = holidays.country_holidays(country_code, years=[year, year + 1])

                # Find the next upcoming holiday
                next_holiday = next(
                    ((str(date), name) for date, name in sorted(country_holidays.items()) if date >= today),
                    None
                )

                if next_holiday:
                    response = f"Next holiday is on {next_holiday[0]} and is called {next_holiday[1]}"
                else:
                    response = f"No upcoming holidays found for {country_code} in {year}."

            except KeyError:
                response = f"Error: Invalid or unsupported country code: {call[0]}"

            responses.append(response)

        return jsonify({"replies": responses})  # Send the list of replies

    except Exception as e:
        return jsonify({"errorMessage": str(e)})
```

## Step 2: Create a connection

![BigQuery console screenshot of the External data source panel for a new connection: type Vertex AI remote models, remote functions and BigLake (Cloud Resource), Connection ID test-remote-functions, US multi-region, and the CREATE CONNECTION button.](/images/a-quick-walkthrough-bigquery-remote-functions/2.png)

![BigQuery console screenshot of the Connection info page for test-remote-functions in the us location, type Cloud Resource, with the service account id shown as a YOUR SERVICE ACCOUNT placeholder at gcp-sa-bigquery-condel.iam.gserviceaccount.com.](/images/a-quick-walkthrough-bigquery-remote-functions/3.png)

## Step 3: Set up permissions

![Cloud Run console screenshot with the test-bigquery-processing function selected and the PERMISSIONS button highlighted; the Permissions panel shows the Cloud Run Invoker role granted to a YOUR SERVICE ACCOUNT FROM (2) placeholder, meaning the connection's service account.](/images/a-quick-walkthrough-bigquery-remote-functions/4.png)

## Step 4: Bind the connection with Cloud Run function

```sql
CREATE FUNCTION learning.get_next_public_holidays(country_code STRING) RETURNS STRING

REMOTE WITH CONNECTION `YOUR_PROJECT.eu.test-bigquery-connection`

OPTIONS (endpoint = 'https://YOUR_ENDPOINT_URL.europe-west1.run.app')
```

![BigQuery results message: This statement created a new function named YOUR PROJECT.learning.get\_next\_public\_holidays.](/images/a-quick-walkthrough-bigquery-remote-functions/5-result.png)

## Test run

```sql
WITH input AS (

  SELECT 'RO' AS country_code UNION ALL
  SELECT 'BE' AS country_code UNION ALL
  SELECT 'VN' AS country_code
)

SELECT country_code, learning.get_next_public_holidays(country_code)


FROM input
```

![BigQuery results: RO gets Next holiday is on 2025-04-18 and is called Easter, BE gets 2025-04-20 Easter Sunday, and VN gets 2025-04-07 Hung Kings' Commemoration Day.](/images/a-quick-walkthrough-bigquery-remote-functions/6-result.png)
