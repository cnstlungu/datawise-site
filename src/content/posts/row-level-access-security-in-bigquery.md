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

![](/images/row-level-access-security-in-bigquery/1.png)

Let's define a **Row-level access policy**.

![](/images/row-level-access-security-in-bigquery/2.png)

This service account would now only be able to see rows where the country is the US or UK.

![](/images/row-level-access-security-in-bigquery/3.png)

Other users (without a Row-level access policy) would see the following:

![](/images/row-level-access-security-in-bigquery/4.png)

**Deleting a Row-level access policy**

This can be done using the following commands:

![](/images/row-level-access-security-in-bigquery/5.png)

Thanks for reading!

---

🚀 Delving into BigQuery, Google Cloud and Analytics? Stay connected with me for valuable insights, handy tips, and strategies to effortlessly traverse the vast universe of cloud computing and data analytics!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using subqueries with Row Level Security in BigQuery](/using-subqueries-with-row-level-security-in-bigquery)
- [Why basic roles in BigQuery are a bad idea](/why-basic-roles-in-bigquery-are-a-bad-idea)
- [Cross-dataset foreign key relationships in BigQuery](/cross-dataset-foreign-key-relationships-in-bigquery)
