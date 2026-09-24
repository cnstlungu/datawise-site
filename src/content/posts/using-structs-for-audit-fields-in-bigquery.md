---
title: "Using STRUCTS for Audit Fields in BigQuery"
seoTitle: "BigQuery STRUCT Columns for Data Pipeline Audit Fields"
seoDescription: "Shows how to use nested STRUCT columns in BigQuery to store audit metadata without cluttering your schema. Practical pattern for tracking source event IDs..."
datePublished: 2023-11-25T23:20:56.566Z
dateUpdated: 2026-03-02T15:57:36.258Z
cover: "/images/using-structs-for-audit-fields-in-bigquery/cover.jpg"
coverCredit:
  name: "Waldemar"
  url: "https://unsplash.com/@waldemarbrandt67w"
series: "bigquery-arrays-and-structs"
hashnodeCuid: "clpeod6gl000009kyb2bs8rvj"
---

I use STRUCTS in **#BigQuery** quite a bit. One interesting use case for them is for audit purposes a separate column containing metadata about how the data in that row was sourced.

Sure enough, you don't need a STRUCT for that, but you don't want to crowd your *already massive* schema with 10 auxiliary columns which would confuse the users.

## The scenario

Here's a scenario: say you join data from two different systems, one that provides daily events and one that provides weekly updates. When joining the two together it would be of course useful to know how the resulting data was obtained i.e. what weekly or daily event was used as a base for that attribute.

Creating an audit STRUCT column will help us with that. Let's look at how such an example could look like.

System 1: Daily (but not guaranteed!) data

```sql
attribute_date	id  value	    event_timestamp	                event_id
2023-12-18	    1	daily-1-B	2023-12-18 23:21:38.000000 UTC	ee727a26-2c94-4a72-a321-d1bfb6761937
2023-12-19	    1	daily-1-A	2023-12-19 23:41:38.000000 UTC	70385f93-36ef-4ce3-be21-e2206a25eebc
2023-12-20	    1	daily-1-F	2023-12-20 22:35:38.000000 UTC	ef64e3cb-1943-4c34-b57a-eb9e2a78ffd7
2023-12-22	    1	daily-1-F	2023-12-22 20:33:38.000000 UTC	0a484983-1f5e-40a8-8375-6bb16d340904
2023-12-24	    1	daily-1-G	2023-12-24 23:31:38.000000 UTC	8d9b0fc8-174b-4ab8-ab99-1c69c03549fe
2023-12-25	    1	daily-1-U	2023-12-25 23:41:38.000000 UTC	60f062ba-f314-4001-be0c-5d13289895e1
2023-12-26	    1	daily-1-J	2023-12-26 23:50:38.000000 UTC	55d61056-6317-408c-b15b-f0e081505a72
2023-12-27	    1	daily-1-K	2023-12-27 21:55:38.000000 UTC	d1f5801c-93e6-4734-a7db-6fdd7613db13
2023-12-28	    1	daily-1-L	2023-12-28 22:35:38.000000 UTC	704347ff-898c-4cc0-8198-3e522289eee3
2023-12-29	    1	daily-1-B	2023-12-29 20:11:38.000000 UTC	3ebe0c05-4ba8-470c-8dce-0af6256e7617
2023-12-18	    2	daily-2-B	2023-12-18 23:21:38.000000 UTC	2e03cc56-c5a4-4b8b-9a15-3fbf53536a67
2023-12-19	    2	daily-2-C	2023-12-19 23:41:38.000000 UTC	fd049e99-ead2-46ce-94de-b44e16ef43f5
2023-12-20	    2	daily-2-B	2023-12-20 22:35:38.000000 UTC	4e4a96b1-9c3d-479d-9541-78948a1bfea8
2023-12-22	    2	daily-2-Q	2023-12-22 20:33:38.000000 UTC	ceaaae84-d335-4e9f-ad66-09a374794e3e
2023-12-23	    2	daily-2-H	2023-12-23 22:50:38.000000 UTC	7b2dda93-f80f-40e5-8ac4-40c6f6ada1e2
2023-12-24	    2	daily-2-B	2023-12-24 23:31:38.000000 UTC	3e66d7c8-d936-4461-b10a-353968a1eb1d
2023-12-25	    2	daily-2-F	2023-12-25 23:41:38.000000 UTC	2332a263-ee03-4bfb-aa2f-53652aafe0f0
2023-12-26	    2	daily-2-O	2023-12-26 23:50:38.000000 UTC	1f70c46c-83c4-4632-980d-d04aa980e86a
2023-12-27	    2	daily-2-M	2023-12-27 21:55:38.000000 UTC	3a3aa83c-ed93-4b4d-b5e5-88df2b627c01
2023-12-28	    2	daily-2-L	2023-12-28 22:35:38.000000 UTC	9ecfa0c3-d34c-43cc-aebf-44fe2fd3a3ac
2023-12-30	    2	daily-2-B	2023-12-30 18:21:38.000000 UTC	9c87029f-3e67-488a-bcd7-a8cc4ef304c5
```

System 2: Weekly data

```sql
weekstart	id	value	    event_timestamp	                event_id
2023-12-17	1	weekly-1-A	2023-12-24 23:50:01.000000 UTC	e5d6faaa-12f6-4869-8993-5eae0e8399df
2023-12-24	1	weekly-1-B	2023-12-30 22:45:44.000000 UTC	0f28f4d5-0966-47f2-bfc7-ad8aebc42719
2023-12-17	2	weekly-2-A	2023-12-24 23:55:22.000000 UTC	190aa292-9cf1-4dda-9cb4-c713ca003b3b
2023-12-24	2	weekly-2-B	2023-12-30 22:35:11.000000 UTC	bc45e078-0bb6-4b8e-8082-488b941b8b01
```

## Building the audit STRUCT column

When joining the two sources together, we can generate the STRUCT audit columns. We'll nest another level of STRUCTs below to keep it clean.

```sql
last_daily_attribute AS (

  SELECT id, attribute_date, value, event_timestamp, event_id,  DATE_TRUNC(attribute_date, WEEK) AS weekstart,  FROM daily_attributes

  QUALIFY ROW_NUMBER() OVER (PARTITION BY id, DATE_TRUNC(attribute_date, WEEK) ORDER BY attribute_date DESC ) =1
)

SELECT 

COALESCE(w.id,d.id) AS id, 
COALESCE(w.weekstart, d.weekstart) AS weekstart, 

w.value AS weekly_value,
d.value AS daily_value,

STRUCT( STRUCT(d.attribute_date, d.event_timestamp, d.event_id) AS daily_metadata, 
        STRUCT(w.weekstart, w.event_timestamp, w.event_id) AS weekly_metadata) AS audit_column


FROM last_daily_attribute d

FULL OUTER JOIN weekly_attributes w ON w.id = d.id and w.weekstart = d.weekstart
```

Now, the result set will contain a (STRUCT) column called 'audit\_column', which will contain two STRUCTS - one for weekly and one for daily metadata, each with information about the date used, the event timestamp and event id that was used.

![BigQuery result grid with the audit\_column STRUCT expanded into daily\_metadata fields (attribute\_date, event\_timestamp, event\_id) and weekly\_metadata fields (weekstart, event\_timestamp, event\_id), e.g. attribute\_date 2023-12-22 with weekstart 2023-12-17; event\_id UUIDs are truncated.](/images/using-structs-for-audit-fields-in-bigquery/1.png)

This is perhaps even better reflected when looking at the data structure.

```sql
{
  "id": "1",
  "weekstart": "2023-12-17",
  "weekly_value": "weekly-1-A",
  "daily_value": "daily-1-F",
  "audit_column": {
    "daily_metadata": {
      "attribute_date": "2023-12-22",
      "event_timestamp": "2023-12-22 20:33:38.000000 UTC",
      "event_id": "bc3060cf-08af-4c9a-82e0-9654a1d1c7bd"
    },
    "weekly_metadata": {
      "weekstart": "2023-12-17",
      "event_timestamp": "2023-12-24 23:50:01.000000 UTC",
      "event_id": "147ddd27-be74-4b85-9e2d-3d9eb86af48d"
    }
  }
}
```

Now, should we investigate why a particular result was obtained, we can just grab the event id from the audit column and investigate in the upstream system.

Thanks for reading and hope this was useful!

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Understanding STRUCTS in BigQuery](/understanding-structs-in-bigquery)
- [Constructing STRUCTS in BigQuery](/constructing-structs-in-bigquery)
- [Using STRUCTS for quick analysis in BigQuery](/using-structs-for-quick-analysis-in-bigquery)
- [Using LAST_VALUE with STRUCTS](/using-lastvalue-with-structs)
- [Change history in BigQuery](/change-history-in-bigquery)
