---
title: "Exploring the BigQuery Query History"
subtitle: ""
seoTitle: "BigQuery Query History: Job History and INFORMATION_SCHEMA"
seoDescription: "Access BigQuery query history via the console's Job History or INFORMATION_SCHEMA.JOBS. Filter by user, time, and status to audit cost and execution details."
datePublished: 2025-02-19T09:46:00.199Z
dateUpdated: 2026-04-05T20:11:10.937Z
cover: "/images/exploring-the-bigquery-query-history/cover.jpg"
coverCredit:
  name: "Markus Winkler"
  url: "https://unsplash.com/@markuswinkler"
series: "data-ops"
hashnodeCuid: "cm7bqa747000o09l54f2jex14"
---

Here’s a BigQuery trick I use all the time—seriously, not saying this to make my post catchier 😁.  
  
It’s not flashy or very complicated, but it’s one of my favorites: Job History.  
  
Under the Query Editor, you’ll find Job History, which stores all past queries—either your own (Personal History) or those run by others in the project (Project History).  
  
🔍 Why is this useful?  
  
✅ Quickly find queries you forgot to save.  
  
✅ Filter by date, SQL definition (summary), or user to track down past work.  
  
✅ For recent queries, you might even retrieve results from the temporary table—saving you from rerunning expensive queries.  
  
This has saved me so many times after accidentally closing a query tab. (Just remember: if you never executed the query, it won’t be there!)  
  
Also, please be reminded that the job data is also available via an INFORMATION SCHEMA view (check out the comments for a post about that one).

<!-- missing image, source no longer available: https://media.licdn.com/dms/image/v2/D4D22AQFGpdKJ6PunCA/feedshare-shrink_2048_1536/B4DZUZAbT4GcAo-/0/1739881298596?e=1743033600&v=beta&t=UHQg6L0vaIodzQ2HEuT0buNkNKY8Vd6U3VIVg71p9vw -->

*Found it useful? Subscribe to my Analytics newsletter at* [***notjustsql.com***](https://www.notjustsql.com/)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Change history in BigQuery](/change-history-in-bigquery)
- [BigQuery Saves Your Query Results — Here's How to Find Them](/bigquery-saves-your-query-results-here-s-how-to-find-them)
