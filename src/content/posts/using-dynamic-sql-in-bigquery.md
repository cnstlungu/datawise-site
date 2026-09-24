---
title: "Using Dynamic SQL in BigQuery"
seoTitle: "Dynamic SQL in BigQuery: EXECUTE IMMEDIATE with Examples"
seoDescription: "EXECUTE IMMEDIATE in BigQuery runs a dynamically built SQL string at runtime. Use it to generate UNPIVOT queries from metadata, loop over values, or run DDL."
datePublished: 2023-10-11T14:14:02.579Z
dateUpdated: 2026-03-02T10:22:45.742Z
cover: "/images/using-dynamic-sql-in-bigquery/cover.jpg"
coverCredit:
  name: "Mathew Schwartz"
  url: "https://unsplash.com/@cadop"
series: "practical-sql"
hashnodeCuid: "clnlu0j0z000m08laeovabwmn"
---

Today I want to spotlight an interesting tool, present in multiple database systems, including BigQuery - Dynamic SQL.

You might have encountered it before. I used to use it a lot before, but not so much anymore.

First, what is Dynamic SQL?

We use the term Dynamic SQL when we mean SQL queries that are built and executed dynamically at runtime. It allows us to compose statements on the fly and run them. This is quite useful for running flexible and parameterized queries.

In BigQuery for instance, we build a STRING based on some runtime variable or values in another table, then pass it on to the EXECUTE IMMEDIATE command.  
This way, the STRING is first evaluated, and then becomes the text of the query we execute.

A basic example would look like this:

```sql
DECLARE dynamic_query STRING;
SET dynamic_query = CONCAT('SELECT * FROM your_project_id.your_dataset_id.', 'your_table_name', ' WHERE column_name = "', 'your_value', '"');
EXECUTE IMMEDIATE dynamic_query;
```

Now, when is this useful? It's helpful when we:

\- need to dynamically generate a query based on external inputs  
\- want to build flexible data analysis queries  
\- are automate an operation across multiple tables: think inserting a new audit column to all the tables inside a dataset

What to look out for:  
\- Security: be wary of any external input to avoid the possibility of a SQL injection attack. Never run queries constructed with external input that is not sanitized or you know is safe  
\- Performance: if writing more complex dynamic SQL queries, pay attention to the performance of the resulting query. Are they all behaving the way you expect?  
\- Readability: Dynamic SQL can become indeed hard to read. Don't over-complicate things and provide useful comments for maintainability.

Practical example:

Probably the most common use case for me is dynamically UNPIVOTING columns. One would need to know the columns in a table at runtime to be able to build the UNPIVOT clause. You may write the columns by hand when you have a handful of them, but what if there are dozens?

![BigQuery result grid of a wide customers table with columns CustomerId, FirstName, LastName, Country and FirstOrderDate for four customers (Michelle Dubois, Jane Springer, Bianca Moretti, John Doe), the columns to be unpivoted.](/images/using-dynamic-sql-in-bigquery/1.png)

![BigQuery result grid of the unpivoted output with columns customer\_id, key and value: each customer becomes one row per attribute, e.g. customer 2 has FirstName Michelle, LastName Dubois, Country FR and FirstOrderDate 2021-06-01.](/images/using-dynamic-sql-in-bigquery/2.png)

Here is where Dynamic SQL can help.

1\. We start by reading the columns from the INFORMATION\_SCHEMA COLUMNS view.  
2\. We use that to build a list of columns that we will inject in the query containing the UNPIVOT.  
3\. Finally, we run EXECUTE IMMEDIATE to get our UNPIVOTED result back.

```sql
DECLARE dynamic_string STRING;
SET dynamic_string = (
  SELECT CONCAT('(', STRING_AGG( column_name, ','), ')'),
FROM(
SELECT column_name FROM learning.INFORMATION_SCHEMA.COLUMNS
WHERE table_name ="Customer_Data" 
AND column_name NOT IN ("CustomerId")  ));

EXECUTE IMMEDIATE FORMAT("""
  SELECT 
    CustomerId as customer_id, 
    key, 
    value 
  FROM learning.Customer_Data
  UNPIVOT
  (
    value 
    FOR key IN %s
  )
""", dynamic_string);
```

Thanks for reading and keep enjoying SQL!
