---
title: "A portable data stack with Dagster, Docker, DuckDB, dbt and Superset"
seoTitle: "Portable Data Stack: Dagster, DuckDB, dbt & Superset"
seoDescription: "Build a fully containerized local data stack with Dagster, DuckDB, dbt Core, and Apache Superset using Docker Compose — a realistic, runnable data..."
datePublished: 2023-08-16T21:24:10.735Z
dateUpdated: 2026-03-02T10:50:29.490Z
cover: "/images/a-portable-data-stack-with-dagster-docker-duckdb-dbt-and-superset/cover.png"
series: "my-data-journey"
hashnodeCuid: "clle8pze6000009l79cia9d36"
---

I've previously mentioned how pet projects are good for exploring new technologies. It's not every day that you can work on a greenfield project with just the stack you want.

So while ago I decided to spin off a previous proof of concept I've had ([portable data stack with Airflow](https://github.com/cnstlungu/portable-data-stack-airflow)) and create one just like that, but better. I was also curious to try out a new orchestrator - Dagster and DuckDB - an in-process OLAP DMBS.

Scenario:  
Imagine a company selling postcards of European cities:  
\- Their main system? A Postgres OLTP for direct sales & customer data.  
\- They collaborate with resellers, obtaining indirect sales data via JSON & CSV.  
\- The need? A Data Warehouse to fuel their analytical insights and provide dashboards.

Objective: Craft a completely portable system with every component containerized. The aim? Minimalism yet realistic functionality.

The Build:  
\- Python scripts churn out sample data.  
\- dbt Core for model building.  
\- Dagster for orchestration (bonus: used Polars backend).  
\- DuckDB as our OLAP database for the Data Warehouse.  
\- Superset for visualization, aiding the data analyst.  
\- Docker and Docker-compose for containerization

Takeaways:  
🌟 DuckDB: An OLAP gem! Think of it as Sqlite’s OLAP counterpart: versatile, user-friendly, and a powerhouse for these applications.  
📘 Dagster: A joy to navigate. Stellar documentation, impressive dbt integration, and the concept of the software-defined asset? A game-changer.  
📊 Superset + DuckDB: Craft SQL queries, visualize, repeat. So smooth!

Real-world Utility:  
\- A playground to explore these technologies.  
\- A striking demo.  
\- A starting point for someone still doing (only) Excel analytics. It might need some more love, but I'll refer to it as a starting point in the future.

Eager to dive in? See the [Github repository](https://github.com/cnstlungu/portable-data-stack-dagster).

Your insights and feedback are golden—do share! ✨

![Apache Superset Sales dashboard from the portable data stack: Sales per region table (Eastern Europe leads at 6.56k), Sales per country world map, Channel sales evolution line chart for 2019-2020, average order size of 8.99 USD, Sales by month table and a Day of Week Trends table by city.](/images/a-portable-data-stack-with-dagster-docker-duckdb-dbt-and-superset/1.png)
