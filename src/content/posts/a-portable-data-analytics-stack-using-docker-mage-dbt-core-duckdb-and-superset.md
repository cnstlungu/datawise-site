---
title: "A portable Data Analytics stack using Docker, Mage, dbt-core, DuckDB and Superset"
seoTitle: "Portable Analytics Stack: Mage, dbt-core, DuckDB, Superset"
seoDescription: "A containerized end-to-end data analytics stack using Mage, dbt-core, DuckDB, and Superset, all wired together with Docker Compose."
datePublished: 2024-04-05T08:55:24.343Z
dateUpdated: 2026-03-02T10:50:49.750Z
cover: "/images/a-portable-data-analytics-stack-using-docker-mage-dbt-core-duckdb-and-superset/cover.jpg"
coverCredit:
  name: "frank mckenna"
  url: "https://unsplash.com/@frankiefoto"
series: "my-data-journey"
hashnodeCuid: "clumfkjav000b08jngbuj1mpj"
---

Just wanted to share a [small learning-by-doing project of mine](https://github.com/cnstlungu/portable-data-stack-mage). It's a containerized Data Analytics suite, covering end-to-end analytics process for a small (imaginary) company.

We're talking about:  
\- generating example data in parquet files using Python  
\- ingesting data into DuckDB  
\- model data using dbt-core  
\- loading a DuckDB datamart  
\- orchestrate using MageAI  
\- displaying it all in a Superset dashboard.

![Apache Superset Sales dashboard screenshot with a sales per region table, a sales per country map, a channel sales evolution line chart for 2019 to 2020, an average order size of 8.99 USD, sales by month and a day-of-week trends pivot by city.](/images/a-portable-data-analytics-stack-using-docker-mage-dbt-core-duckdb-and-superset/1.png)

Each of the components is in a separate Docker container, tied all together with docker-compose.

I've previously set up similar projects with [Airflow](https://github.com/cnstlungu/portable-data-stack-airflow) and [Dagster](https://github.com/cnstlungu/portable-data-stack-dagster).

It's pretty bare bones (somewhat as intended) and has some rough edges, but it should be a good starting point for a demo, template or learn how all these components works together.

I would of course appreciate any feedback or suggestions on how to make it better.

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
