---
title: "Recursive CTEs in BigQuery"
seoTitle: "Recursive CTEs in BigQuery: WITH RECURSIVE Explained"
seoDescription: "BigQuery recursive CTEs use WITH RECURSIVE to self-reference. Use them for hierarchies, date sequences, and graph traversal — with syntax and worked examples."
datePublished: 2023-04-10T14:39:26.108Z
dateUpdated: 2026-03-02T10:16:37.564Z
cover: "/images/recursive-ctes-in-bigquery/cover.jpg"
coverCredit:
  name: "Adrien Olichon"
  url: "https://unsplash.com/@adrienolichon"
series: "practical-sql"
hashnodeCuid: "clgaxwfx8000d0amgaaq13gy9"
---

In this practical BigQuery exercise, we’re going to look at what are recursive CTEs and how can they be useful in our tool set.

## What is a CTE?

First of all, what is a CTE? Well, it stands for **Common Table Expression** and is essentially a named query that can be referenced multiple times in the same query.

An example of a Common Table Expression (CTE) can be seen below:

```sql
WITH people AS 

( SELECT 'John' AS first_name, 'Doe' AS last_name
  UNION ALL
  SELECT 'Jane' AS first_name, 'Dow' AS last_name)

SELECT 
  first_name, 
  last_name
FROM people
```

CTEs are used widely for improving query readability as well as making debugging easier.

## Enter the recursive variety

Adding the **RECURSIVE** keyword after **WITH** enables us to reference a CTE from within itself, essentially creating a recursion, hence the name.

Let’s consider an example:

```sql
WITH RECURSIVE cte AS

(


  SELECT 1 AS id

  UNION ALL

  SELECT id + 1

  FROM cte

  WHERE id < 10
)


SELECT id FROM cte

ORDER BY id
```

What does it do? We’re essentially generating a list of integers 1 through 10.

In the above query, we start by selecting ID = 1 as our base case —  ‘anchor’, and UNION to it all the cases building from it, by adding 1 to the previous case.

Notice the **WHERE id &lt; 10** . This is very important as it tells when to stop the recursion.

![BigQuery query result from the recursive CTE number generator: a single id column holding the consecutive integers 1 through 10, one per row, in rows 1 to 10.](/images/recursive-ctes-in-bigquery/1.png)

The same can be done to say generate a list of 100 consecutive days. In practice though, the same can be achieved using functions such as [GENERATE\_ARRAY or GENERATE\_DATE\_ARRAY.](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/array_functions)

Now where a recursive CTE would be really useful is where we have hierarchical data.

## Recursive CTEs and hierarchical data

Consider the following data. We have a list of employees and the ID of the manager they report to. Our task is to retrieve each person’s manager's first and last name.

One way to do it would be to self-join the table multiple times. But how would you know how many times you’d need to self-join or what if there is a new hierarchical level down the line?

![BigQuery employees table with employee\_id, first\_name, last\_name and manager\_id: John Smith (1) has a null manager\_id, Jane Doe and Bob Johnson report to 1, Alice Lee and Tom Wilson to 2, Mike Brown and Sarah Kim to 3, and David Lee and Emily Davis to 4.](/images/recursive-ctes-in-bigquery/2.png)

Here’s what using a recursive CTE to solve this would look like.

```sql

WITH RECURSIVE hierarchy as (

  SELECT 
    employee_id, 
    first_name, 
    last_name, 
    manager_id, 
    0 AS level, 
    CAST(NULL AS STRING) AS manager_first_name, 
    CAST(NULL AS STRING) AS manager_last_name

  FROM `learning.employee_data`
  WHERE manager_id IS NULL

  UNION ALL

  SELECT 
    e.employee_id, 
    e.first_name, 
    e.last_name, 
    e.manager_id, level + 1 AS level, 
    h.first_name AS manager_first_name, 
    h.last_name AS manager_last_name

  FROM `learning.employee_data` e
  INNER JOIN hierarchy h ON e.manager_id = h.employee_id

)

SELECT 

  employee_id,
  first_name,
  last_name,
  manager_id,
  level,
  manager_first_name,
  manager_last_name 

FROM hierarchy
```

We start with the anchor record (top-level employee, our CEO) and then traverse the employee hierarchy by joining the manager\_id with the employee\_id. We’ve also created a new ‘level’ column to show the hierarchical level — the distance between the employee and the CEO.

![BigQuery result of the recursive CTE, adding level, manager\_first\_name and manager\_last\_name to each employee: John Smith is level 0 with null manager, Jane Doe and Bob Johnson are level 1 under John Smith, Alice, Tom, Sarah and Mike are level 2, and Emily Davis and David Lee are level 3 under Alice Lee.](/images/recursive-ctes-in-bigquery/3.png)

## Performance considerations

It should be noted that according to [BigQuery documentation](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#with_clause), as opposed to non-recursive CTEs, the recursive CTEs are materialized (so executed only once).

> GoogleSQL only materializes the results of recursive CTEs, but does not materialize the results of non-recursive CTEs inside the `WITH` clause. If a non-recursive CTE is referenced in multiple places in a query, then the CTE is executed once for each reference. The `WITH` clause with non-recursive CTEs is useful primarily for readability.

## Conclusion

In today’s exercise, we’ve looked at recursive Common Table Expressions, or CTEs as yet another valuable tool on our belt when working with data in BigQuery.

Thanks for reading and stay tuned for more BigQuery topics.
