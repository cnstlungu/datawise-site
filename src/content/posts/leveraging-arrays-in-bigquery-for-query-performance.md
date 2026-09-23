---
title: "Leveraging ARRAYS in BigQuery for query performance"
seoTitle: "BigQuery ARRAY Storage: Performance and Cost Benefits"
seoDescription: "Compares flat row storage versus nested ARRAY storage in BigQuery using a 100-customer dataset benchmark. ARRAYs cut slot time to a fraction of the flat..."
datePublished: 2023-12-19T22:46:25.226Z
dateUpdated: 2026-03-02T10:51:07.492Z
cover: "/images/leveraging-arrays-in-bigquery-for-query-performance/cover.jpg"
coverCredit:
  name: "Pawel Czerwinski"
  url: "https://unsplash.com/@pawel_czerwinski"
series: "bigquery-arrays-and-structs"
hashnodeCuid: "clqcxp87e000108jrejscce9g"
---

Leveraging your platform functionality goes a long way. When developing data pipelines, besides the functional requirements, we try to optimize for some other important variables, such as cost, resources consumed or runtime. While working with big or complex datasets in BigQuery, I always try a test several approaches to see which one yields a better mix from the above.

Take ARRAYs, for example. They allow us to define one-to-many relationships inside tables while saving up on storage and potentially processing power too.

I'll provide a short example. Say we have 100 customers and several thousand dates they visited a website. We could store this in two ways:

\- classic approach with one row representing a unique id-date combination  
100 ids x 3640 dates each = 364k rows

![BigQuery console Schema tab for the partitioned table example\_without\_array, with two NULLABLE columns, id INTEGER and ds\_date DATE, so each row is one id and date pair.](/images/leveraging-arrays-in-bigquery-for-query-performance/1.png)

![BigQuery console table details for example\_without\_array: partitioned by DAY on ds\_date and clustered by id, with 364,000 rows in 3,640 partitions, 5.55 MB total logical bytes and 4.77 MB total physical bytes.](/images/leveraging-arrays-in-bigquery-for-query-performance/2.png)

\- leveraging ARRAYs and having one row = one id and its array of dates.  
100 ids with an array of 3640 dates each = 100 rows

![BigQuery console Schema tab for example\_with\_array, with id INTEGER NULLABLE and dates DATE REPEATED, so each row holds one id and an array of its dates.](/images/leveraging-arrays-in-bigquery-for-query-performance/3.png)

![BigQuery console Storage info for example\_with\_array, clustered by id: 100 rows, 2.78 MB total logical bytes and only 36.75 KB total physical bytes, plus 18.58 KB of time travel physical bytes.](/images/leveraging-arrays-in-bigquery-for-query-performance/4.png)

Let's run a quick query to test the performance of these two. In this particular case, the array example consumes a minuscule fraction of the slot time of the non-array example while still processing only half as many bytes.

![BigQuery console screenshots of two queries computing MIN and MAX of ds\_date GROUP BY id: on example\_with\_array via LEFT JOIN UNNEST(dates) it processes 2.78 MB with 86 ms of slot time; on example\_without\_array it processes 5.55 MB and uses 9 min 44 sec of slot time.](/images/leveraging-arrays-in-bigquery-for-query-performance/5.jpg)

I'm definitely not saying this is a "one size fits all" approach, depending of course on data structure, size, querying patterns and other constraints. But whenever you have a challenge like that, it's good to know your options, try out different strategies and pick the one that suits your use case best.

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using ARRAY_AGG in BigQuery](/using-array-agg-in-bigquery)
- [UNNESTING ARRAYS in BigQuery](/unnesting-arrays-in-bigquery)
- [Accessing ARRAY elements in BigQuery](/accessing-array-elements-in-bigquery)
- [Enumerating ARRAY elements in BigQuery using WITH OFFSET](/enumerating-array-elements-in-bigquery-using-with-offset)
