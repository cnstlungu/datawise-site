---
title: "Revisiting GROUP BY ROLLUP with a more realistic example"
seoTitle: "GROUP BY ROLLUP: Practical Example Revisited"
seoDescription: "Learn how to effectively use GROUP BY ROLLUP to manage hierarchical data summaries in SQL, with practical examples and real-world insights"
datePublished: 2025-02-22T14:56:13.139Z
dateUpdated: 2026-03-02T10:52:35.240Z
cover: "/images/revisiting-group-by-rollup-with-a-more-realistic-example/cover.jpg"
coverCredit:
  name: "Didssph"
  url: "https://unsplash.com/@didsss"
series: "practical-sql"
hashnodeCuid: "cm7gbooyb000c09lagnce7532"
---

Ever had a random piece of knowledge from school suddenly click in a real-world scenario?

It felt like that for me remembering about ROLLUP a few days ago.

I wrote about GROUP BY ROLLUP roughly 1.5 years ago—[one of my first posts here](/using-rollup-in-bigquery). At the time, it was unfamiliar to me, and I had no idea I’d ever need it. But this week, I finally encountered a real use case.

𝐓𝐡𝐞 𝐏𝐫𝐨𝐛𝐥𝐞𝐦

Imagine we have sales data for a retail store, where each product belongs to a subcategory and a category (e.g., Apples → Fruits → Food).

We want to compute the average ordered quantity per product, but with a hierarchical fallback:  
1. If there’s no product-level data, use the subcategory average.  
2. If that’s missing, use the category average.  
3. If still unavailable, fall back to the overall average across all products.

𝐇𝐨𝐰 𝐑𝐎𝐋𝐋𝐔𝐏 𝐇𝐞𝐥𝐩𝐬

When we GROUP BY ROLLUP (category, subcategory, product\_id), we get multiple aggregation levels in one query:  
✅ Per product  
✅ Per subcategory  
✅ Per category  
✅ Across all rows

This allows us to build a lookup table, which we can use with multiple LEFT JOINs to apply the fallback logic.

𝐋𝐞𝐭'𝐬 𝐭𝐞𝐬𝐭 𝐢𝐭

Here’s how it works in practice:  
• Apples → Direct sales data → AVG(quantity) = 6  
• Mangoes → No past sales → Uses Fruits subcategory → AVG(quantity) = 4.67  
• Cucumbers → No past sales, no Vegetables subcategory data → Uses Food category → AVG(quantity) = 4.67  
• Washing Machine → No sales data, no relevant category → Uses overall average → AVG(quantity) = 6

![BigQuery SQL building calculated\_averages from sales\_data with ROUND(AVG(quantity),2) and GROUP BY ROLLUP (category, subcategory, product\_id), then LEFT JOINs and COALESCE for a fallback average; results give Mangoes 4.67 from Fruits, Cucumbers 4.67 from Food and Washing Machine 6.0 overall.](/images/revisiting-group-by-rollup-with-a-more-realistic-example/1.jpg)

𝐈𝐧 𝐥𝐢𝐞𝐮 𝐨𝐟 𝐚 𝐜𝐨𝐧𝐜𝐥𝐮𝐬𝐢𝐨𝐧

This was a fun experiment, but let’s be honest—this could also be done with window functions!

Still, ROLLUP provides an perspective, and I’m on the lookout for an even better use case.

Have you ever had an SQL feature suddenly “click” for you?

*Found it useful? Subscribe to my Analytics newsletter at* [***notjustsql.com***](https://www.notjustsql.com/)*.*
