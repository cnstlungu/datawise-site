---
title: "Here's a great use case for GenAI writing SQL"
seoTitle: "Boost SQL Efficiency with GenAI"
seoDescription: "Discover how generative AI assists in SQL writing with real use cases in data engineering, enhancing efficiency in specific tasks"
datePublished: 2025-02-08T14:11:29.823Z
dateUpdated: 2026-03-02T10:53:06.205Z
cover: "/images/heres-a-great-use-case-for-genai-writing-sql/cover.jpg"
coverCredit:
  name: "ZHENYU LUO"
  url: "https://unsplash.com/@mrnuclear"
series: "practical-sql"
hashnodeCuid: "cm6w9x95r000009lbge5m6t01"
---

Truth be told, I almost never use GenAI as part of my day-to-day work as a Data Engineer. For the most part, it’s just easier and faster for me to write the SQL code myself.

There are a few reasons for this:  
➡️ If the task is complex enough to need ChatGPT, it usually requires providing a lot of context, iterating on prompts, thinking up some illustrative play data (since sharing real customer data is a big no-go), and then thoroughly understanding and verifying the solution it suggests.  
➡️ Most of the time, by the time I’ve done all of that, I could’ve just written the code manually.  
➡️ I trust my 10+ years of experience writing SQL more.

That said, I’ve used GenAI occasionally for tasks that are tedious and time-consuming, like fixing scrambled code that needed proper formatting. And I fully recognize its value as a prototyping tool or as a quick way to iterate over ideas.

Now, I recently had a situation where the stars aligned perfectly.

I needed to compute the list of all possible combinations of 9 elements. Essentially: C(9, 1) + C(9, 2) + … + C(9, 9).  
In total, math tells us there should be 511 combinations.

This would’ve taken me quite a bit of time to write manually, but with 2–3 prompts (where GPT fixed its own errors), I ended up with the below solution.

If you're not familiar with recursive CTEs, check out [my previous post](/recursive-ctes-in-bigquery).

Sometimes, it’s about knowing when and where to use the tools at your disposal. While it might not work for many tasks, I appreciate the moments where it can help streamline things significantly.

What’s your experience? Do you use tools like ChatGPT regularly for your Data Engineering tasks?

![BigQuery SQL with WITH RECURSIVE combinations generating every combination of the letters a to i: the base case UNNESTs the array, the recursive case CROSS JOINs it with CONCAT and WHERE e \> SPLIT(c.combination, ',') at OFFSET(c.size - 1); the result has 511 rows, ending with a,b,c,d,e,f,g,h,i.](/images/heres-a-great-use-case-for-genai-writing-sql/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [***notjustsql.com***](https://www.notjustsql.com/)*.*
