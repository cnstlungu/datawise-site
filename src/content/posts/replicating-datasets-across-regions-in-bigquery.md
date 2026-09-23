---
title: "Replicating datasets across regions in BigQuery"
seoTitle: "Replicate BigQuery Datasets Across GCP Regions"
seoDescription: "BigQuery now supports native cross-region dataset replication, removing the need for manual Transfer Service jobs."
datePublished: 2024-06-21T06:00:47.814Z
dateUpdated: 2026-03-02T10:53:08.434Z
cover: "/images/replicating-datasets-across-regions-in-bigquery/cover.jpg"
coverCredit:
  name: "Gianluca Cinnante"
  url: "https://unsplash.com/@gluca"
series: "practical-sql"
hashnodeCuid: "clxoa8kw6000209jy266offj9"
---

So this has been up for almost a year, but I've just found out that [you can replicate datasets across regions in BigQuery](https://docs.cloud.google.com/bigquery/docs/data-replication). Obligatory remark that this is still in preview.

This should help quite a bit if you're working with data distributed across multiple BQ regions.

A couple of years ago, when facing the same task, I had to resort to setting up recurring BigQuery Transfer Service jobs to move data across regions.

![BigQuery console Dataset replicas (Preview) screens: the Create replica panel for dataset learning in EU with Multi-region US selected as replica location, and the Replicas list afterwards showing a US Secondary replica from June 11, 2024 next to the EU Primary.](/images/replicating-datasets-across-regions-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
