---
title: "Importing Google Sheets into BigQuery"
seoTitle: "Connect Google Sheets to BigQuery as an External Table"
seoDescription: "Step-by-step guide to importing a Google Sheets spreadsheet into BigQuery as an external table via Google Drive, including schema setup and viewing the..."
datePublished: 2023-10-24T11:09:33.294Z
dateUpdated: 2026-03-02T10:51:56.894Z
cover: "/images/importing-google-sheets-into-bigquery/cover.jpg"
coverCredit:
  name: "Rubaitul Azad"
  url: "https://unsplash.com/@rubaitulazad"
series: "data-ops"
hashnodeCuid: "clo485cku000c08mvd5g0fcpw"
---

Spreadsheets are a central part of a modern workplace. Pretty much every office workplace uses one. It's also quite used for personal use cases. One such product is Google Sheets.

I use it for many things - organizing finance, planning travel itineraries, collecting data and expenses.

Today I want to illustrate how we can integrate data from Google Sheets to BigQuery.

In BigQuery, a Google Sheets page can be represented as an external table - a type of table where the data is stored outside of BigQuery.

### Where to use it?

I've seen them used for holding static (seed) data and mapping tables, an improvised Master Data Management of sorts, allowing analysts to edit data as business realities change.

### What to pay attention to?

* Security - who can view and edit Sheets
    
* History - how do you handle change in sheets? Do you need snapshots?
    
* Recovery - what if someone deletes data from the worksheet?
    

Let's see an example of how to set it up.

### Setting up a Google Sheet as an External Table

![Google Sheets screenshot of ExampleFile with header row FirstName, LastName, City, Country and three data rows: Jane Doe, New York, USA; Max Muller, Munich, Germany; Amelie Johnson, London, UK.](/images/importing-google-sheets-into-bigquery/1.png)

We start by adding a new data source.

![Google Cloud BigQuery console screenshot of the Explorer panel with the + ADD button highlighted in yellow, the starting point for adding a new data source.](/images/importing-google-sheets-into-bigquery/2.png)

We pick the **Google Drive** as the source.

![BigQuery console Add dialog listing popular sources (Local file, Google Cloud Storage, Connections to external data sources) and additional sources such as Analytics Hub and Amazon S3, with the Google Drive option circled in yellow.](/images/importing-google-sheets-into-bigquery/3.jpg)

We provide the necessary configuration:

* Google Sheets URL
    
* Destination Table: project, dataset, table name
    
* We provide the schema: column names and types
    
* We provided the number of header rows to be skipped
    

![BigQuery console Create table form: source Drive with a Google Sheets URI (partly redacted), file format Google Sheet, sheet range A1:D4, dataset learning, table example\_table, table type External table, four STRING fields FirstName, LastName, City, Country, and 1 header row to skip.](/images/importing-google-sheets-into-bigquery/4.jpg)

After we hit ***Create Table*** the external table is created. We can verify that the data has been properly created.

```sql
SELECT * FROM `learning.example_table` LIMIT 1000
```

![BigQuery results: FirstName, LastName, City and Country for Jane Doe (New York, USA), Max Muller (Munich, Germany) and Amelie Johnson (London, UK).](/images/importing-google-sheets-into-bigquery/5-result.png)


### Viewing the DDL of an (external) table

We might need to see the DDL (data definition language) statement for a table. This can be achieved using one of the INFORMATION\_SCHEMA tables.

Using the query below you can see how the (external in our case) table is defined.

```sql
SELECT
 table_name, ddl
FROM
 learning.INFORMATION_SCHEMA.TABLES;
```

```sql
SELECT
 table_name, ddl
FROM `learning.INFORMATION_SCHEMA.TABLES`

WHERE table_name = 'example_table';
```

![BigQuery results: table\_name example\_table, with a ddl that starts CREATE EXTERNAL TABLE followed by the project name (hidden with yellow marks) and .learning.example\_table.](/images/importing-google-sheets-into-bigquery/6-result.jpg)

```sql
CREATE EXTERNAL TABLE `learning.example_table`
(
  FirstName STRING OPTIONS(description="First Name"),
  LastName STRING OPTIONS(description="Last Name"),
  City STRING OPTIONS(description="City"),
  Country STRING OPTIONS(description="Country")
)
OPTIONS(
  sheet_range="A1:D4",
  skip_leading_rows=1,
  format="GOOGLE_SHEETS",
  uris=["https://docs.google.com/spreadsheets/d/**edited_text**/edit#gid=0"]
);
```

Thanks for reading and keep enjoying SQL!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
