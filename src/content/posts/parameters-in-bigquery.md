---
title: "Parameters in BigQuery"
subtitle: ""
seoTitle: "BigQuery Parameters vs Variables: What's the Difference?"
seoDescription: "Query parameters and variables both hold typed values in BigQuery. Learn when to pass parameters in from outside and when to DECLARE and SET variables."
datePublished: 2026-02-07T12:37:25.972Z
dateUpdated: 2026-04-05T20:11:26.777Z
cover: "/images/parameters-in-bigquery/cover.jpg"
coverCredit:
  name: "Buddha Elemental 3D"
  url: "https://unsplash.com/@buddhaelemental3d"
series: "practical-sql"
hashnodeCuid: "cmlcaud04000802jv5gzp5qxk"
---

You can use query parameters in BigQuery SQL (now in the console as well!) — but how are they different from variables, and when should you use each?

Both parameters and variables act as placeholders and have a defined data type. The difference is where their value comes from and how they’re used.

Parameters (like @corpus)  
👉 Are not computed inside the query  
👉 Are passed from the outside (Python, UI, API, etc.)

Variables (DECLARE, SET)  
👉 Are defined and computed inside a SQL script or stored procedure  
👉 Let you store a value and reuse it later in the same script

So what’s the real difference?  
➡️ Variables are essential for Dynamic SQL (EXECUTE IMMEDIATE)  
➡️ Parameters can filter data, but cannot control identifiers (e.g. table or column names)

🚨 Security  
When values come from user input or external sources, parameters are the safer choice—they reduce the risk of SQL injection.

🚅 Performance  
Parameters may allow the optimizer to reuse execution plans, while variables can sometimes prevent that.

![BigQuery SQL comparing a query parameter and a variable on bigquery-public-data.samples.shakespeare: WHERE corpus = @corpus with corpus set to sonnets under Query parameters, versus DECLARE corpus\_var STRING DEFAULT 'sonnets'; both process 4.88 MB and return the same word counts.](/images/parameters-in-bigquery/1.png)

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
