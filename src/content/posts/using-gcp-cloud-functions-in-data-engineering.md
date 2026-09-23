---
title: "Using GCP Cloud Functions in Data Engineering"
seoTitle: "GCP Cloud Functions for Data Engineering Pipelines"
seoDescription: "How Google Cloud Functions fit into data engineering: serverless ETL, lightweight APIs, file parsing, and orchestration via Cloud Workflows — with key..."
datePublished: 2023-10-06T23:31:07.434Z
dateUpdated: 2026-03-02T10:52:07.247Z
cover: "/images/using-gcp-cloud-functions-in-data-engineering/cover.jpg"
coverCredit:
  name: "Guillaume Bourdages"
  url: "https://unsplash.com/@graphem"
series: "data-ops"
hashnodeCuid: "clnf8poh6000109l9em0q8yph"
---

Some of the most interesting Data Engineering projects I've worked with leveraged Google Cloud Functions. It's a serverless execution environment that lets you run your code without provisioning or managing servers.

I found it to be very versatile, even more so for Data Processing tasks. Things like ingesting data, developing a lightweight API or consuming data from an endpoint, parsing and transforming a flat file.

As expected, it's very well integrated with other GCP services, so you could easily say, orchestrate run from a Google Cloud Workflow (a pairing that I used and enjoyed).

The advantages are pretty obvious: no server to manage, pay per invocation, scalability (if you need it) and simplicity to get started.

Now, there are of course a lot of things to think about when setting up such serverless functions :  
\- the size of the unit of work and runtime resources  
\- authentication (unauthenticated/authentication required)  
\- networking - where can the function can be invoked from  
\- auto-scaling and concurrency  
\- avoiding cold starts  
\- reusing heavy computations across invocations

![Google Cloud console screenshot of the Cloud Functions welcome page, describing it as a lightweight, event-based compute solution, with a Create Function button and cards for local development, testing, how-to guides, tips, tutorials and billing.](/images/using-gcp-cloud-functions-in-data-engineering/1.png)

![Google Cloud console screenshot of the Cloud Functions Create function configuration: 2nd gen environment, test-cloud-function in europe-west1, HTTPS trigger with Require authentication, 256 MiB memory, 60 s timeout, concurrency 1, autoscaling 0 to 100 instances, service account dev-tf-sa.](/images/using-gcp-cloud-functions-in-data-engineering/2.png)

![Cloud Functions console, Code step: Runtime Python 3.11, Entry point hello\_http, and a TEST FUNCTION button.](/images/using-gcp-cloud-functions-in-data-engineering/3-input.png)

```python
import functions_framework

@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'
    return 'Hello {}!'.format(name)
```

![Google Cloud Functions console Configure pre-deployment test panel: the triggering event is the JSON body {"name": "fellow earthlings"}, HTTP method POST, with a Run Test button and a last test on Oct 5, 2023 that returned HTTP status 200.](/images/using-gcp-cloud-functions-in-data-engineering/4.png)

![Cloud Functions pre-deployment test log: builder steps run pip check with no broken requirements, then Function is ready to test, followed by execution responses Hello Greetings, fellow earthlings!! and Hello fellow earthlings!](/images/using-gcp-cloud-functions-in-data-engineering/5.png)

But overall, it felt like the setup was pretty straightforward and the first time I tried it, I was able to get off the ground pretty quickly. You can of course test the function on your local machine (until you're happy with it) and automate its deployment with Terraform.

When used properly, a cloud function can be very useful for Real-Time and Batch ETL, automation and API Development, all while being scalable and flexible.

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [What are GCP Cloud Workflows and how can they help you as a Data Engineer](/what-are-gcp-cloud-workflows-and-how-can-they-help-you-as-a-data-engineer)
- [Loading data from Google Cloud Storage into BigQuery using Cloud Workflows](/loading-data-from-google-cloud-storage-into-bigquery-using-cloud-workflows)
- [Scheduled queries in BigQuery](/scheduled-queries-in-bigquery)
- [Using the bq CLI utility with BigQuery](/using-the-bq-cli-utility-with-bigquery)
