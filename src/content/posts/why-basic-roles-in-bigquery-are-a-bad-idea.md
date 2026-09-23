---
title: "Why basic roles in BigQuery are a bad idea"
seoTitle: "BigQuery IAM: Why Owner/Editor Roles Are a Security Risk"
seoDescription: "Basic IAM roles like Owner and Editor grant thousands of permissions across all BigQuery datasets, violating least privilege."
datePublished: 2024-06-08T18:15:11.473Z
dateUpdated: 2026-03-02T10:52:48.100Z
cover: "/images/why-basic-roles-in-bigquery-are-a-bad-idea/cover.jpg"
coverCredit:
  name: "Arthur Mazi"
  url: "https://unsplash.com/@arthurbizkit"
series: "practical-sql"
hashnodeCuid: "clx6fqxyo00000ajoglyvh7j6"
---

> Paul Atreides: "He who can destroy a thing, controls a thing".

Remember to avoid as much as possible using the basic roles in BigQuery such as Owner, Editor or Viewer.

It may sound 'easier' to manage access using them, but it's a bad idea.

They make way for a number of problems:

* overly broad permissions: Editor = several thousand permissions, including read / write on ALL datasets, of course very far from the least privilege principle
    
* no granularity: not much wiggle room between these 3 roles
    
* security risk: one compromised Editor means a lot of trouble
    
* compliance: it's also a bad idea because it can land you in hot water with privacy regulations😁
    
* What to do instead:
    
* use one of many predefined roles that grant granular access to perform a specific set of tasks
    
* if you don't find the one you need (and the combination of multiple predefined ones that cover your use-case is too vast), you can create a custom role, bundling together minimum amount of rights you need to perform a particular task
    
* again, follow the principle of least privilege
    
* regularly review who has privilege to do what and why they need it, then clean up
    
* remember that you can also enforce dataset, table and even column/row-level security for a even more granular control
    
* use service accounts with minimal rights to handle processes
    
* use groups for easier management of privileges for a particular role (in a team) or function
    

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Row-level access security in BigQuery](/row-level-access-security-in-bigquery)
- [Using subqueries with Row Level Security in BigQuery](/using-subqueries-with-row-level-security-in-bigquery)
- [Cross-dataset foreign key relationships in BigQuery](/cross-dataset-foreign-key-relationships-in-bigquery)
