---
title: "Using MAX_BY / MIN_BY in BigQuery"
seoTitle: "BigQuery MAX_BY and MIN_BY: Fetch Values by Max/Min"
seoDescription: "Discover MAX_BY and MIN_BY in BigQuery SQL, compact shortcuts for ANY_VALUE with HAVING MAX/MIN, and see exactly how to retrieve a column value based on..."
datePublished: 2023-09-08T13:54:25.640Z
dateUpdated: 2026-03-02T10:50:36.254Z
cover: "/images/using-maxby-minby-in-bigquery/cover.jpg"
coverCredit:
  name: "Graphic Node"
  url: "https://unsplash.com/@graphicnode"
series: "practical-sql"
hashnodeCuid: "clmans6w8000p0amfclij7k86"
---

Just stumbled upon a nifty SQL function in BigQuery that was new to me.

Did you know about `MAX_BY / MIN_BY`? They're essentially shortcuts for `ANY_VALUE(columnA HAVING MIN/MAX(columnB))`. And guess what? I had no idea you could use `HAVING` within `ANY_VALUE`.

So, what does it do? It fetches the value from one column based on the minimum or maximum value of another column.

Here's a quick example of how it works.

![BigQuery results of the sample employees CTE with columns first\_name, last\_name, gross\_salary and hire\_date: Jane Doe 75000 2020-01-01, Callum Blake 55000 2022-06-01, Jack Dew 77000 2019-03-01, Emily Scott 80000 2021-01-01.](/images/using-maxby-minby-in-bigquery/1.png)

```sql
WITH employees AS (

  SELECT 'Jane' AS first_name, 'Doe' AS last_name, 75000 AS gross_salary, '2020-01-01' AS hire_date

  UNION ALL

  SELECT 'Callum' AS first_name, 'Blake' AS last_name, 55000 AS gross_salary, '2022-06-01' AS hire_date

  UNION ALL

  SELECT 'Jack' AS first_name, 'Dew' AS last_name, 77000 AS gross_salary, '2019-03-01' AS hire_date

  UNION ALL

  SELECT 'Emily' AS first_name, 'Scott' AS last_name, 80000 AS gross_salary, '2021-01-01' AS hire_date

)

SELECT 

MAX_BY(CONCAT(first_name,' ', last_name), gross_salary) AS employee_with_highest_gross_salary,
--same as 
ANY_VALUE(CONCAT(first_name,' ', last_name) HAVING MAX(gross_salary)) AS also_employee_with_highest_gross_salary,


MIN_BY(CONCAT(first_name,' ', last_name), hire_date) AS employee_hired_earliest,
--same as
ANY_VALUE(CONCAT(first_name,' ', last_name) HAVING MIN(hire_date)) AS also_employee_hired_earliest

FROM employees
```

This would produce the following output:

![BigQuery result row comparing MAX\_BY and MIN\_BY with ANY\_VALUE HAVING: employee\_with\_highest\_gross\_salary and also\_employee\_with\_highest\_gross\_salary are both Emily Scott; employee\_hired\_earliest and also\_employee\_hired\_earliest are both Jack Dew.](/images/using-maxby-minby-in-bigquery/2.png)

In our field, every day is a learning journey. Stay tuned for more insights on Analytics, SQL, Python and BigQuery. Follow along!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
