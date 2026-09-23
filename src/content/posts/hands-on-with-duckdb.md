---
title: "Hands-on with DuckDB"
seoTitle: "DuckDB Hands-On: In-Process OLAP for Data Engineers"
seoDescription: "A practical introduction to DuckDB as a lightweight OLAP database for local analytics, prototyping, and data warehouse proofs of concept — including..."
datePublished: 2023-09-25T20:58:27.708Z
dateUpdated: 2026-03-02T10:51:17.641Z
cover: "/images/hands-on-with-duckdb/cover.jpg"
coverCredit:
  name: "Andrew Wulf"
  url: "https://unsplash.com/@andreuuuw"
series: "my-data-journey"
hashnodeCuid: "clmzdezgc000809leg2dj34cp"
---

The right tool for the right job, right?

When developing a basic application or testing a concept, an option could be SQLite. It's a self-contained database system that offers a SQL interface and conveniently stores data in a file on your device. Perfect for straightforward tasks.

But what if you need an OLAP solution? There's DuckDB. This in-process DBMS is great for extracting, processing, and analyzing data. It can even support an analytical application you're working on. It's also super-fast.

I've had the pleasure of using DuckDB to establish a Data Warehouse for a quick proof of concept \[link in comments\]. Pairing it with Apache Superset was interesting – a robust BI toolkit right there.

Many analytical workloads don't demand the vast scale of cloud data warehouses like BigQuery or Snowflake. DuckDB offers a simple yet very powerful alternative, making analytics more accessible to all.

How easy is it to use it? Simply download an executable and start querying your files.

![](/images/hands-on-with-duckdb/1.jpg)

Where can you use it? In the console, using a host of programming languages, and more recently in the cloud, with Motherduck, currently in beta, a new offering also based on DuckDB.

![](/images/hands-on-with-duckdb/2.jpg)

![](/images/hands-on-with-duckdb/3.jpg)

Where do I see it applicable? Useful to DAs, DEs, and even those who only get started. One-off analysis, exploratory data analysis, super-fast DW for small-to-medium analytical apps, and prototypes. Anywhere else you might use a pop-up OLAP database. Further down, perhaps separate queues for workloads based on their size.

In the example below I'm using it to query a sample 9.3M row CSV file.

![](/images/hands-on-with-duckdb/4.jpg)

Since competition in the analytics space is a driving force for progress, I'm enthusiastic about what's to come next. Hopefully, further democratization of this space can happen, so that even smaller companies are empowered by analytics.

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
