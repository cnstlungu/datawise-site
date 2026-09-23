---
title: "Choosing the Right Ranking Function: Why Ties in SQL Matter"
seoTitle: "Optimize SQL: The Importance of Ranking Ties"
seoDescription: "Discover the importance of choosing the right ranking function in SQL and how handling ties can impact your data analysis"
datePublished: 2025-02-12T13:12:33.974Z
dateUpdated: 2026-03-02T10:53:05.169Z
cover: "/images/choosing-the-right-ranking-function-why-ties-in-sql-matter/cover.jpg"
coverCredit:
  name: "Possessed Photography"
  url: "https://unsplash.com/@possessedphotography"
series: "bigquery-window-functions"
hashnodeCuid: "cm71xkvjq000209ju6hok1qhl"
---

If you’re like me, you probably use QUALIFY + ROW\_NUMBER() almost daily for deduplication or finding the first/last occurrence of something. It’s a powerful combo in modern SQL !

But here’s the catch: there are subtle nuances and edge cases that can cause some trouble.

The choice between ordering functions like ROW\_NUMBER(), DENSE\_RANK(), and RANK() isn’t always straightforward—it depends on the nature of your data and the question you’re trying to answer.

Check out [my previous post](/comparing-ranking-functions-in-bigquery) a quick overview of ordering functions.

Now, let me share a scenario.

![](/images/choosing-the-right-ranking-function-why-ties-in-sql-matter/1.png)

We want to find the first event type for each user. Simple enough, right?  
But in this case we can have two events happening at the exact same time.

Here’s where things get interesting:  
➡️ ROW\_NUMBER() would arbitrarily pick one event and mask the tie (non-deterministic behavior).  
➡️ DENSE\_RANK(), on the other hand, would preserve the tie, allowing us to decide how to handle it.

This subtle difference can have a huge impact on your results!

TL;DR: Keep ties in mind when deciding which numbering function to use.

As always, it’s about using the right tool for the right job.

Have you encountered any tricky scenarios with ties?

*Found it useful? Subscribe to my Analytics newsletter at* [***notjustsql.com***](https://www.notjustsql.com/)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Beware of ROW_NUMBER without ORDER BY](/beware-of-rownumber-without-order-by)
- [Tidying up WINDOW functions in BigQuery with named windows](/tidying-up-window-functions-in-bigquery-with-named-windows)
- [Using RANGE in Window Functions in BigQuery](/using-range-in-window-functions-in-bigquery)
- [Computing a cumulative sum in BigQuery](/computing-a-cumulative-sum-in-bigquery)
