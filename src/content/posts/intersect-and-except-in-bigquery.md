---
title: "Intersect and Except in BigQuery"
seoTitle: "BigQuery INTERSECT and EXCEPT: SQL Set Operations Explained"
seoDescription: "INTERSECT DISTINCT finds common rows; EXCEPT DISTINCT finds rows missing from one side. Use them in BigQuery for data validation, deduplication, and diffing."
datePublished: 2023-10-30T11:52:25.308Z
dateUpdated: 2026-03-02T10:22:34.483Z
cover: "/images/intersect-and-except-in-bigquery/cover.jpg"
coverCredit:
  name: "Kelly Sikkema"
  url: "https://unsplash.com/@kellysikkema"
series: "practical-sql"
hashnodeCuid: "clocubl5o000e09lc0x9e5mbo"
---

Almost everyone working with SQL has used UNION and UNION ALL. But these are not the only set operations available in SQL. Meet INTERSECT and EXCEPT.

What do they do? As the name suggests they perform the following set operations:

* INTERSECT returns the common entries, all elements present both in A and B, so A ∩ B.
    
* EXCEPT returns the elements present in A, but not in B, so A **∖** B
    

I find them quite useful when doing data validation, although they can be easily replicated with JOINs.

It's worth noting that while BigQuery supports UNION ALL and UNION DISTINCT, we are required to specify DISTINCT for INTERSECT and EXCEPT. At the time of this writing, INTERSECT ALL and EXCEPT ALL are not supported.

Let's see an example of them in action. Say we have the following two inputs:

Input A:

![Rowset A](/images/intersect-and-except-in-bigquery/1.png)

Input B:

![](/images/intersect-and-except-in-bigquery/2.png)

Here's what the output of INTERSECT would look like:

![](/images/intersect-and-except-in-bigquery/3.png)

And EXCEPT:

![](/images/intersect-and-except-in-bigquery/4.png)

Thanks for reading!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
