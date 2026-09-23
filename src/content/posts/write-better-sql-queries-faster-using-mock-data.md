---
title: "Write better SQL queries faster using Mock Data"
seoTitle: "Use Mock Data CTEs to Write BigQuery SQL Queries Faster"
seoDescription: "A practical SQL development technique: prototype complex BigQuery queries using inline CTE mock data to iterate quickly, cover edge cases, and reduce..."
datePublished: 2023-10-03T12:15:05.143Z
dateUpdated: 2026-03-02T10:52:49.497Z
cover: "/images/write-better-sql-queries-faster-using-mock-data/cover.jpg"
coverCredit:
  name: "Thao LEE"
  url: "https://unsplash.com/@h4x0r3"
series: "practical-sql"
hashnodeCuid: "clnaa8qev000d08if0qzh22kl"
---

🛠️ Here's a technique I frequently employ to streamline my query development process.

Ever find yourself stuck in the complexity of writing non-trivial queries, especially with voluminous tables? 🤔 The amalgamation of query complexity and business problems can sometimes make writing your SQL take more time than necessary.

When exploring a new coding approach, utilizing an unfamiliar function, or navigating through unseen data, I create a simplified, representative example using dummy data and a few test cases.

In a blank BigQuery window, I write a couple of Common Table Expressions (CTEs) to simulate input, then focus on mimicking only the pivotal columns - maintaining the grain and incorporating one representative value, along with the join columns. A single value can often represent a surrogate key for the grain of the tables.

🚀 This approach enables me to:

\- Iterate rapidly, considering edge cases irrespective of the data subset.  
\- Sharpen the technical requirements by applying the solution to the available data and addressing the business question.  
\- Contemplate how the technical solution can be optimized for data scale and manage real-world corner cases or unexpected scenarios.  
\- Save processing costs, since I'm working only on kilobytes of data until I have a solution that is &gt;80% ready

👀 So, the next time you have to write a big query (pun unintended), especially when dealing with unfamiliar data or functions, take a moment to code a swift example in a blank BigQuery window. It pays off to think simply first.

🔄 Is this Test-Driven Development (TDD) for BigQuery? Perhaps. I like to term it *Iterative Development*.

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
