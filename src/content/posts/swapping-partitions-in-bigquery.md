---
title: "Swapping Partitions in BigQuery"
seoTitle: "Copy BigQuery Partitions with bq cp Instead of MERGE"
seoDescription: "Skip costly MERGE jobs by using the bq cp command to swap partitions between a staging table and a target table in BigQuery, with a working bash script..."
datePublished: 2023-10-03T12:04:55.144Z
dateUpdated: 2026-03-02T10:50:52.019Z
cover: "/images/swapping-partitions-in-bigquery/cover.jpg"
series: "bigquery-performance"
hashnodeCuid: "clna9vnqg000909ju7efcgbv3"
---

A few years back, when working on SQL Server projects, I often utilized the ALTER TABLE SWITCH partition between staging and target tables. This left me pondering—could a similar functionality be achieved in BigQuery? 🤔

BigQuery facilitates copying a partition to another table using the bq cp command:

```bash
bq cp -f 'project:dataset.source_table$your_partition' 'project:dataset.target_table$your_partition'
```

🧪 Example Scenario 🧪

Imagine a staging table, where we extract the delta from a source table (based on the last entry seen in the target table), and MERGE it into the target table.

![BigQuery SQL selecting MIN(ds\_date) and MAX(ds\_date) from learning.data\_source\_staging; the result shows the staging table spans 2023-09-02 to 2023-09-30.](/images/swapping-partitions-in-bigquery/1.png)

![BigQuery SQL selecting MAX(ds\_date) from the target table learning.data\_source; the result is 2023-09-02, so the target is behind the staging table before the partitions are copied.](/images/swapping-partitions-in-bigquery/2.png)

Instead, we can craft a short script to copy delta partitions (new + changed, if any) into the target table, bypassing the need for MERGE altogether! This generates COPY jobs as opposed to QUERY jobs.

```bash
#!/bin/bash

# Check if the correct number of arguments is provided
if [[ "$#" -ne 2 ]]; then
    echo "Usage: $0 <start_date> <end_date>"
    exit 1
fi

# Define the project and dataset names
PROJECT="***********"
DATASET_SOURCE="learning.data_source_staging"
DATASET_DEST="learning.data_source"

# Assign start date and end date from input arguments
START_DATE=$1
END_DATE=$2

# Loop through the dates from START_DATE to END_DATE
for date in $(seq -w $START_DATE $END_DATE); do
  # Echo a message indicating the partition being swapped
  echo "Swapping partition $date"
  
  # Run the bq cp statement
  bq cp -f "${PROJECT}:${DATASET_SOURCE}\$$date" "${PROJECT}:${DATASET_DEST}\$$date"
done
```

Once this executes, we will have copied the partitions from the staging table to the target table using the `bq cp` command.

![Terminal output of bq cp -f commands copying partitions $20230928, $20230929 and $20230930 from learning.data\_source\_staging to learning.data\_source, one command per date; the project IDs are blacked out.](/images/swapping-partitions-in-bigquery/3.png)

We can confirm that all the partitions have been loaded properly and see the list of COPY jobs in the job history tab.

![BigQuery console screenshot: SELECT MAX(ds\_date) FROM learning.data\_source now returns 2023-09-30, and the Personal history tab below lists several successful COPY jobs from September 30, 2023 4:05 PM followed by one QUERY job.](/images/swapping-partitions-in-bigquery/4.png)

Also, don’t forget—leveraging the INFORMATION\_SCHEMA PARTITIONS view can assist in constructing even more advanced functionalities.

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
