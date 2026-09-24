---
title: "Row-level access security in BigQuery"
seoTitle: "BigQuery Row-Level Security: Set Up Access Policies"
seoDescription: "How to create and delete BigQuery row-level access policies so users only see the rows they are permitted to, with a working example using service..."
datePublished: 2023-08-29T14:03:01.326Z
dateUpdated: 2026-03-02T10:51:40.259Z
cover: "/images/row-level-access-security-in-bigquery/cover.jpg"
coverCredit:
  name: "Maxim Zhgulev"
  url: "https://unsplash.com/@jemjoyrussia"
series: "data-ops"
hashnodeCuid: "cllwdoq4t000009l0f0b3bzgh"
---

Whether you're an experienced data engineer or just embarking on your cloud data adventure, prioritizing security is crucial.

Here's a quick tour of BigQuery's row-level security features.

Suppose you have the following BigQuery table. Each sales representative should only have access to the data for the country they are catering to.

![Sample BigQuery Customers table with columns CustomerId, Age, FirstName, LastName, Country, Salary and FirstOrderDate, holding four customers: John Doe (US), Jane Springer (UK), Bianca Moretti (IT) and Michelle Dubois (FR).](/images/row-level-access-security-in-bigquery/1.png)

Let's define a **Row-level access policy**.

```sql
CREATE ROW ACCESS POLICY us_uk_country_filter

ON `learning.Customers`

GRANT TO ('serviceAccount:test-access-control@REDACTED.iam.gserviceaccount.com')

FILTER USING (country IN ('US', 'UK'));
```

This service account would now only be able to see rows where the country is the US or UK.

![BigQuery query result for the service account covered by the row access policy: the Customers table (CustomerId, Age, FirstName, LastName, Country, Salary, FirstOrderDate) now returns only two rows, John Doe from the US and Jane Springer from the UK.](/images/row-level-access-security-in-bigquery/3.png)

Other users (without a Row-level access policy) would see the following:

```sql
SELECT * FROM `REDACTED.learning.Customers` LIMIT 1000
```

![BigQuery results: no rows, only the notices Your query results may be limited because you do not have access to certain rows, and There is no data to display.](/images/row-level-access-security-in-bigquery/4-result.png)

**Deleting a Row-level access policy**

This can be done using the following commands:

```sql
-- Deleting a specific policy on this table
DROP ROW ACCESS POLICY us_uk_country_filter ON learning.Customers;

-- Deleting ALL policies on this table
DROP ALL ROW ACCESS POLICIES ON learning.Customers;
```

Thanks for reading!

---

🚀 Delving into BigQuery, Google Cloud and Analytics? Stay connected with me for valuable insights, handy tips, and strategies to effortlessly traverse the vast universe of cloud computing and data analytics!

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using subqueries with Row Level Security in BigQuery](/using-subqueries-with-row-level-security-in-bigquery)
- [Why basic roles in BigQuery are a bad idea](/why-basic-roles-in-bigquery-are-a-bad-idea)
- [Cross-dataset foreign key relationships in BigQuery](/cross-dataset-foreign-key-relationships-in-bigquery)
