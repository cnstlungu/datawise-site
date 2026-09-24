---
title: "Using SELECT * with EXCEPT and REPLACE"
seoTitle: "BigQuery SELECT * EXCEPT and REPLACE, with Examples"
seoDescription: "Use SELECT * EXCEPT and REPLACE in BigQuery to exclude or transform columns without rewriting the full select list. Includes practical examples."
datePublished: 2023-11-30T12:27:11.830Z
dateUpdated: 2026-04-28T08:33:48.075Z
cover: "/images/using-select-with-except-and-replace/cover.jpg"
coverCredit:
  name: "Randy Fath"
  url: "https://unsplash.com/@randyfath"
series: "practical-sql"
hashnodeCuid: "clpl67psm000509jm1qh1gms1"
---

`SELECT *` is not a good practice in production, but I still use it for spot checks, when debugging, analyzing or validating data - especially when working with wide tables.

Here are two useful clauses to keep in mind when working with `SELECT *` in BigQuery: `EXCEPT` and `REPLACE`.

➡ `EXCEPT` will exclude one or more columns from the output.  
➡ `REPLACE` will swap the enumerated columns with the new definitions you provide.

Also, since `SELECT DISTINCT *` won't work when you have a `STRUCT` column, you can use `EXCEPT` to exclude struct columns.

Let's look at an example. Say we'd like to select all the columns but exclude the Salary and modify the CustomerId.

![Table of the Customers input data with columns CustomerId, Age, FirstName, LastName, Country, Salary and FirstOrderDate for four customers: John Doe (CA, 150000), Bianca Moretti (IT, 75000), Jane Springer (UK, 88000) and Michelle Dubois (FR, 78000).](/images/using-select-with-except-and-replace/1.png)

Here's how the code would look:

```sql
SELECT * 

EXCEPT(Salary) 

REPLACE(CONCAT('SystemA','-',CustomerId) AS CustomerId) 

FROM `learning.Customers`
```

This would produce the following output!

![Output table of SELECT \* EXCEPT(Salary) REPLACE(...) on the Customers data: the Salary column is gone and CustomerId values are rewritten as SystemA-1, SystemA-3, SystemA-4 and SystemA-2, while Age, FirstName, LastName, Country and FirstOrderDate are unchanged.](/images/using-select-with-except-and-replace/2.png)

Thanks for reading!
