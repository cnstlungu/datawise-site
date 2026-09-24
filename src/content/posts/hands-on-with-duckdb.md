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

```sql
CREATE TABLE ecommerce_demo AS  SELECT * FROM './repos/duckdb-demo/export.csv';
SHOW ecommerce_demo;
```

![Terminal output: SHOW ecommerce\_demo lists 16 columns with their inferred types, all nullable: id, f\_orderquantity, f\_employeeid, f\_storeid, f\_vatrateid, f\_productid, f\_campaignid and created\_by BIGINT; f\_productprice, f\_NetAmountEUR and f\_GrossAmountEUR DOUBLE; f\_orderdate TIMESTAMP; is\_active, created\_on and modified\_on VARCHAR; modified\_by BIGINT.](/images/hands-on-with-duckdb/1-output.jpg)

Where can you use it? In the console, using a host of programming languages, and more recently in the cloud, with Motherduck, currently in beta, a new offering also based on DuckDB.

```sql
WITH input_data AS
(
SELECT
    CAST(f_orderdate AS DATE) AS order_date,
    SUM(f_NetAmountEUR) AS sum_net_amount,
    SUM(f_GrossAmountEUR) AS sum_gross_amount
FROM main.ecommerce_demo
GROUP BY
    CAST(f_orderdate AS DATE)
)

SELECT
    order_date,
    sum_net_amount,
    sum_gross_amount
FROM input_data;
```

![DuckDB results in DBeaver: order\_date with daily sum\_net\_amount and sum\_gross\_amount, starting 2014-01-01 at 398,607 and 483,941, then roughly 1.1 to 1.2 million net and 1.4 to 1.5 million gross per day through 2014-01-23.](/images/hands-on-with-duckdb/2-result.jpg)

```sql
WITH input_data AS
(
SELECT
    CAST(f_orderdate AS DATE) AS order_date,
    SUM(f_NetAmountEUR) AS sum_net_amount,
    SUM(f_GrossAmountEUR) AS sum_gross_amount
FROM export
GROUP BY
    CAST(f_orderdate AS DATE)
)

SELECT
    order_date,
    sum_net_amount,
    sum_gross_amount
FROM input_data;
```

![MotherDuck results: the query ran in 2.27 s and returned 730 rows of order\_date, sum\_net\_amount and sum\_gross\_amount, with a histogram over each amount column; the first row is Fri Oct 10 2014 with 1,155,998.00 net and 1,404,026.00 gross.](/images/hands-on-with-duckdb/3-result.jpg)

```sql
SELECT COUNT(1) FROM main."export";
```

![MotherDuck results: the count query ran in 2.53 s and returned count(1) 9305031.](/images/hands-on-with-duckdb/3-result-2.jpg)

Where do I see it applicable? Useful to DAs, DEs, and even those who only get started. One-off analysis, exploratory data analysis, super-fast DW for small-to-medium analytical apps, and prototypes. Anywhere else you might use a pop-up OLAP database. Further down, perhaps separate queues for workloads based on their size.

In the example below I'm using it to query a sample 9.3M row CSV file.

![Spreadsheet view of the sample e-commerce CSV used with DuckDB, with columns id, f\_orderquantity, f\_productprice, f\_employeeid, f\_storeid, f\_vatrateid, f\_orderdate, f\_productid, f\_campaignid, f\_NetAmountEUR, f\_GrossAmountEUR and audit columns.](/images/hands-on-with-duckdb/4.jpg)

Since competition in the analytics space is a driving force for progress, I'm enthusiastic about what's to come next. Hopefully, further democratization of this space can happen, so that even smaller companies are empowered by analytics.
