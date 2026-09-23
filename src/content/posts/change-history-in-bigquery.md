---
title: "Change history in BigQuery"
seoTitle: "Track Changes in BigQuery"
seoDescription: "Discover how BigQuery's Change History features track data changes, including updates and deletes, using APPENDS and CHANGES TVFs"
datePublished: 2025-03-06T15:44:40.216Z
dateUpdated: 2026-03-02T10:53:01.853Z
cover: "/images/change-history-in-bigquery/cover.jpg"
coverCredit:
  name: "Chris Lawton"
  url: "https://unsplash.com/@chrislawton"
series: "practical-sql"
hashnodeCuid: "cm7xip82g000009jz2esefw0n"
---

Ever needed to track what changed in a table and when? In data engineering, this is known as Change Data Capture (CDC)—a fundamental challenge when dealing with evolving datasets.

Now, the Change History features in BigQuery sound pretty interesting.

BigQuery SQL has had the APPENDS table-valued function (TVF) for some time now, which works well for append-only scenarios. But it didn’t capture updates or deletes.

A few months ago a CHANGES TVF was added, which provides visibility into UPDATE and DELETE operations.

Unlike APPENDS (which works right out of the box), you need to enable change history tracking manually either at table creation or with an `ALTER TABLE ... SET OPTIONS()` command.

To illustrate how it all works I've:  
1️⃣ Created a table 2️⃣ Inserted a row 3️⃣ Updated a row

![](/images/change-history-in-bigquery/1.jpg)

As you will be able to see:  
✅ APPENDS captures new rows only.  
✅ CHANGES logs updates too (as a DELETE + INSERT).

Key things to note:

⚠️ Both features are still in preview, so not production-ready.  
💰 Querying this data still incurs processing costs.  
⏳ CHANGES only tracks modifications older than 10 minutes.  
📦 Enabling Change History means extra storage costs for metadata.

Has anyone tried using these in real-life scenarios?

*Found it useful? Subscribe to my Analytics newsletter at* [***notjustsql.com***](https://www.notjustsql.com/)*.*
