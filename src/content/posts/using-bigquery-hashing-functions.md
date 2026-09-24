---
title: "Using BigQuery hashing functions"
seoTitle: "BigQuery Hashing: FARM_FINGERPRINT, MD5, and SHA256"
seoDescription: "Use FARM_FINGERPRINT in BigQuery for surrogate keys and change detection. Covers MD5, SHA256, and how to pick the right hash function for MERGE conditions."
datePublished: 2023-10-20T12:32:28.250Z
dateUpdated: 2026-03-02T10:16:27.597Z
cover: "/images/using-bigquery-hashing-functions/cover.jpg"
coverCredit:
  name: "Markus Spiske"
  url: "https://unsplash.com/@markusspiske"
series: "practical-sql"
hashnodeCuid: "clnylckm2000209mi5p3x3hvb"
---

Today I want to highlight hash functions and showcase how I use them in BigQuery.

## What's a hashing function?

It's an algorithm that takes an input and returns a fixed-size output. But there are a few very interesting particularities to that.

A hashing function is:

\- fixed-size =&gt; you always get an output of the same size  
\- deterministic =&gt; for the same input, you'll always get the same output back  
\- fast =&gt; the hashing function should be quick and resource-efficient  
\- resistant =&gt; very difficult to find out what was the input based on the output - sensitive to change =&gt; even adding one letter to a page of text would produce a totally different output  
\- low chance of collision =&gt; it is *very* improbable to have two different inputs produce the same output.

Now, hashing functions have multiple use cases in security, cryptography and computer science in general, but I want to showcase how I'm using it in my day-to-day as a Data Engineer.

## Use cases in data engineering

As one can deduct from the proprieties above, the hashing function can very efficiently compare (as in assessing if they are different or the same) vast amounts of information.  
BigQuery offers a range of hash functions such as MD5, SHA1 and FARM\_FINGERPRINT. So, Where is this useful?

1\. Creating surrogate keys. Say you have two source systems, each with unique identifiers (like IDs), but that do have an overlap between themselves. One could do FARM\_FINGERPRINT(CONCAT(source\_system\_name, source\_id )) to obtain a unique identifier across all systems.

2\. Use it in conjunction with WINDOW functions to determine whether something has changed between two snapshots. See below an example of how it's done.

```sql
WITH input_data AS (
  SELECT 1 AS ID, date('2020-01-01') AS Snapshot_Date, 'John Doe' AS Name, 'Berlin' AS City, '55000' AS Salary
  UNION ALL  
  SELECT 1 AS id, date('2022-04-01') AS Snapshot_Date,  'John Doe' AS Name, 'New York' AS City, '55000' AS Salary
  UNION ALL 
  SELECT 2 AS id, date('2022-07-01') AS Snapshot_Date, 'Jessica Taylor' AS Name, 'Paris' AS City, '70000' AS Salary
  UNION ALL
  SELECT 2 AS id, date('2022-08-01') AS Snapshot_Date,  'Jessica Taylor' AS Name, 'Paris' AS City, '70000' AS Salary
  UNION ALL
  SELECT 2 AS id, date('2022-09-01') AS Snapshot_Date, 'Jessica Taylor' AS Name, 'London' AS City , '70000' AS Salary
), 
compute_hash AS 
(
SELECT 
  ID, 
  Name, 
  City, 
  Salary,
  Snapshot_Date,
  FARM_FINGERPRINT(CONCAT(Name, City, Salary)) AS attribute_hash,
FROM input_data
)
SELECT 
  ID,
  Name, 
  City,
  Salary,
  Snapshot_Date,
LAG(attribute_hash) OVER (PARTITION BY ID ORDER BY Snapshot_Date) <> attribute_hash AS ChangedSinceLastSnapshot
FROM compute_hash
```

![BigQuery result grid with ID, Name, City, Salary, Snapshot\_Date and a truncated ChangedSinceLastSnapshot flag: null on each ID's first snapshot, true when John Doe moves from Berlin to New York, false for an unchanged Jessica Taylor row and true when she moves from Paris to London.](/images/using-bigquery-hashing-functions/1.png)

3\. Ever had to write a MERGE statement where you need to compare 12 different attributes between source and target? Concatenate the attributes and pass them on to a function like FARM\_FINGERPRINT and compare the outputs to see if there was any change. Even better if you have a hash like that already computed in each of the tables (staging source and target).

```sql
MERGE `learning.Customers` AS target

USING (

SELECT 
    1 AS CustomerId, 
    31 AS Age, 
    'John' AS FirstName, 
    'Doe' AS LastName, 
    'IE' AS Country, 
    150000 AS Salary, 
    '2021-01-01' AS FirstOrderDate

) AS source ON source.CustomerId = target.CustomerId

WHEN MATCHED AND 
-- OPTION 1
  --  (
  --   target.age <> source.age OR 
  --   target.firstname <> source.firstname OR
  --   target.lastname <> source.lastname OR
  --   target.country <> source.country OR
  --   target.salary <> source.salary OR  
  --   target.firstorderdate <> source.firstorderdate 
  --  )

-- OPTION 2
FARM_FINGERPRINT(CONCAT(
                        target.age, 
                        target.firstname, 
                        target.lastname, 
                        target.country, 
                        target.salary, 
                        target.firstorderdate )) <> 

FARM_FINGERPRINT(CONCAT(source.age, 
                        source.firstname, 
                        source.lastname, 
                        source.country, 
                        source.salary, 
                        source.firstorderdate ))

THEN UPDATE
SET 
  target.age = source.age,
  target.firstname = source.firstname,
  target.lastname = source.lastname,
  target.country = source.country, 
  target.salary =  source.salary,  
  target.firstorderdate = source.firstorderdate
```

P.S. Also note that you can hash an entire row in SQL using TO\_JSON\_STRING:

```sql
SELECT t.*, FARM_FINGERPRINT(TO_JSON_STRING(t)) AS row_hash
FROM learning.Customers AS t;
```

![BigQuery results listing the four customers with an extra row\_hash column of large signed integers, shown truncated.](/images/using-bigquery-hashing-functions/2-result.png)

Thanks for reading!
