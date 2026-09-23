---
title: "De-duplicating with ROW_NUMBER vs ARRAY_AGG"
seoTitle: "BigQuery Deduplication: ARRAY_AGG vs ROW_NUMBER Performance"
seoDescription: "Compares ARRAY_AGG and ROW_NUMBER for deduplication in BigQuery with real slot time benchmarks. ARRAY_AGG consumed only 40% of the slot time, making it a..."
datePublished: 2023-12-02T13:23:45.062Z
dateUpdated: 2026-03-02T10:50:30.621Z
cover: "/images/de-duplicating-with-rownumber-vs-arrayagg/cover.jpg"
coverCredit:
  name: "Austris Augusts"
  url: "https://unsplash.com/@austris_a"
series: "bigquery-window-functions"
hashnodeCuid: "clpo345d2000109lc10fj0r9z"
---

What function do you use to explicitly de-duplicate in BigQuery?  
I normally use ROW\_NUMBER(), but I've recently encountered a really interesting [blog post](https://cloud.google.com/blog/topics/developers-practitioners/bigquery-admin-reference-guide-query-optimization) suggesting ARRAY\_AGG might be more performant for the task.

The explanation given is that the `ORDER BY` is allowed to drop everything except the top record on each GROUP BY, making ARRAY\_AGG more efficient.

Sure enough, I did give it a try on some sample data.

![BigQuery result grid of the sample data used for the de-duplication test, with columns id, value and ds\_date: 25 rows of random ids such as 37, 75 and 2 with single-digit values, all dated 2020-12-18.](/images/de-duplicating-with-rownumber-vs-arrayagg/1.png)

In the below example, we'd like to pick the latest date available per id. The `ROW_NUMBER` example is pretty straightforward - we partition by id and order by `ds_date` decreasingly, then use the `QUALIFY` clause to keep only the record we want.

![BigQuery SQL de-duplicating learning.data\_source with QUALIFY ROW\_NUMBER() OVER (PARTITION BY id ORDER BY ds\_date DESC) = 1; the Execution Details tab shows 3 sec elapsed, 20 min 19 sec slot time consumed and 8.77 MB bytes shuffled.](/images/de-duplicating-with-rownumber-vs-arrayagg/2.png)

The `ARRAY_AGG` example, while looking a bit more intimidating, does the same thing.

![BigQuery SQL de-duplicating with a last\_events CTE using SELECT AS VALUE ARRAY\_AGG(t ORDER BY t.ds\_date DESC LIMIT 1) with OFFSET(0) FROM learning.data\_source GROUP BY id; Execution Details show 2 sec elapsed, 8 min 8 sec slot time consumed and 33.94 MB bytes shuffled.](/images/de-duplicating-with-rownumber-vs-arrayagg/3.png)

It turns out that the recommendation holds - slot time for the ARRAY\_AGG version was only 40% of the ROW\_NUMBER. Another day, another lesson learned.

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Beware of ROW_NUMBER without ORDER BY](/beware-of-rownumber-without-order-by)
- [Tidying up WINDOW functions in BigQuery with named windows](/tidying-up-window-functions-in-bigquery-with-named-windows)
- [Using RANGE in Window Functions in BigQuery](/using-range-in-window-functions-in-bigquery)
- [Computing a cumulative sum in BigQuery](/computing-a-cumulative-sum-in-bigquery)
