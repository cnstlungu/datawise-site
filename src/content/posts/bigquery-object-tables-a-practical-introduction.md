---
title: "BigQuery Object Tables: A Practical Introduction\n"
subtitle: ""
seoTitle: "BigQuery Object Tables Explained"
seoDescription: "Learn how BigQuery Object Tables work, how to create them, and how to use ML.GENERATE_TEXT to run AI inference on unstructured data stored in GCS."
datePublished: 2026-05-15T10:28:23.506Z
dateUpdated: 2026-05-15T10:29:19.453Z
cover: "/images/bigquery-object-tables-a-practical-introduction/cover.jpg"
series: "practical-sql"
tags: ["bigquery", "ml", "gcp", "sql"]
hashnodeCuid: "cmp6ry1jj001m1shx1hfifvio"
---

**BigQuery** has always been a SQL engine for tabular data. Object tables add an interesting twist to that.  
  
Instead of rows containing values, an object table gives you one row per file — pointing at data stored in Cloud Storage: images, PDFs, audio, video, or JSON.  
  
Each row includes:  
→ the GCS URI  
→ file metadata (size, content type, updated timestamp)  
→ a hidden data column that can be passed directly into ML functions  
  
That last part is especially important. You can feed that data straight into ML.GENERATE\_TEXT or AI.GENERATE\_EMBEDDING — meaning you can run inference on unstructured data directly with BigQuery **SQL** .  
  
BigQuery is no longer just querying tables. It’s increasingly becoming an execution layer over files and AI models too.

Let's now walk through a practical example.  
  
First, we're going to start with a Google Cloud Storage bucket.

![Google Cloud Storage console screenshot of the object-tables-demo-animals bucket (eu multi-region) on the Objects tab, listing four JPEG thumbnails such as NZP-20070705-593MM\_thumb.jpg, each about 38 to 43 KB with type image/jpeg.](/images/bigquery-object-tables-a-practical-introduction/1.png)

These are images of animals sourced [Open Access Animals](https://www.si.edu/spotlight/open-access-animals) collection.

![Four animal thumbnail images from the bucket shown as files: a giant panda eating bamboo, a lion cub, a tiger standing in grass and an elephant spraying water, named NZP-20070705-593MM\_thumb.jpg to NZP-20180628-596SB\_thumb.jpg.](/images/bigquery-object-tables-a-practical-introduction/2.png)

Next, just like in the [BigLake tutorial](/bigquery-biglake-tables-explained-what-they-are-and-when-to-use-them) we'd need a BigQuery connection created with its service account being granted **both** `storage.objectViewer` on the bucket *and* `Vertex AI User` on the project.

  
We can now create the object table:

![BigQuery SQL creating an object table: CREATE OR REPLACE EXTERNAL TABLE learning.animals WITH CONNECTION to the eu demo-biglake-connection (project ID hidden), OPTIONS object\_metadata = 'SIMPLE' and uris gs://object-tables-demo-animals/\*.jpg; the console confirms a new table named animals.](/images/bigquery-object-tables-a-practical-introduction/3.png)

Here are the fields exposed:

![BigQuery console screenshot of the Schema tab for the animals object table (Lakehouse), listing the fields uri, generation, content\_type, size, md5\_hash and updated, plus metadata as a REPEATED RECORD and ref as a RECORD.](/images/bigquery-object-tables-a-practical-introduction/4.png)

![BigQuery SQL SELECT \* FROM learning.animals on the object table, processing 0 B; the results have columns uri, generation, content\_type, size, md5\_hash and updated, with four gs://object-tables-demo-animals rows of type image/jpeg sized 37558 to 43079 bytes.](/images/bigquery-object-tables-a-practical-introduction/5.png)

We can now create the model that we will be passing these images to.

![BigQuery SQL creating a remote model pointing at Gemini: CREATE OR REPLACE MODEL learning.gemini\_flash REMOTE WITH CONNECTION to the eu demo-biglake-connection, with OPTIONS (endpoint = 'gemini-2.5-flash'); the project ID is blanked out.](/images/bigquery-object-tables-a-practical-introduction/6.png)

  
We're going to use ML.GENERATE\_TEXT function, providing the object table to the model we've previously created to identify what animal is depicted on each image.

![BigQuery SQL running inference over the object table with ML.GENERATE\_TEXT, passing MODEL learning.gemini\_flash, TABLE learning.animals and a STRUCT with a prompt asking what animal is depicted; ml\_generate\_text\_llm\_result AS animal\_detected returns Lion cub, Tiger, Panda and Elephant.](/images/bigquery-object-tables-a-practical-introduction/7.png)

As you can see, the model correctly identified each of the animals.

The animal detection example might look simple, but it opens new possibilites. Product image classification, PDF extraction, audio transcription would have the same approach. If your data lives in GCS and your questions can be expressed as a prompt, BigQuery can now answer them.

Thanks for reading and stay tuned for more content like this.
