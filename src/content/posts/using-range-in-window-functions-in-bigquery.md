---
title: "Using RANGE in Window Functions in BigQuery"
seoTitle: "ROWS vs RANGE in BigQuery Window Functions Explained"
seoDescription: "ROWS counts physical rows from the current row; RANGE includes all peers with the same ORDER BY value. Learn when each frame clause changes your window results."
datePublished: 2024-01-11T10:39:12.828Z
dateUpdated: 2026-03-02T10:16:38.727Z
cover: "/images/using-range-in-window-functions-in-bigquery/cover.jpg"
coverCredit:
  name: "Willian Justen de Vasconcellos"
  url: "https://unsplash.com/@willianjusten"
series: "bigquery-window-functions"
hashnodeCuid: "clr92umkc000c09kwedxkf8gj"
---

On [my previous post about computing a cumulative sum](/computing-a-cumulative-sum-in-bigquery) in BigQuery I've got a question regarding the RANGE in the row\_range specification of a window function. I've realized I never used it before. So I've decided to see what it's about.

So how does using RANGE inside an OVER() block differ from using ROWS?

First, it bears noting that unlike ROWS, which uses physical rows representation (previous row, next row etc) in a window, RANGE uses logical (previous value, next value), so that makes it quite useful in some situations.

Let's imagine the following scenario:

We have a group of athletes that compete in a running contest. We would like to compare each athlete's time to their peers - but we'll define a peer as someone who is born anywhere between the year before and the year after the athlete was. So for someone born in 1992, we would like to compute the average of athletes born in '91, '92 and '93 for comparison.

How will this be achieved?

We'll use the AVG aggregation function with a window function call, ORDER BY birth\_year and set up a RANGE BETWEEN 1 PRECEDING year and 1 FOLLOWING year. This way, for our athlete born in '92, the average will be computed by including all athletes born in 1991, 1992, 1993.

To illustrate why the ROWS would not work here, look at the results for 1991. Since there's two athletes born in 1991, the ROWS clause would include only the previous row (also born in 1991) and the next row (born in 1992), thus missing the mark. Check the result in neighbours\_average vs neighbours\_average\_wrong.

```sql
SELECT
  athlete_name,
  finish_time,
  birth_year,
  AVG(finish_time) OVER (ORDER BY birth_year
                         RANGE BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS neighbours_average,
  AVG(finish_time) OVER (ORDER BY birth_year
                         ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS neighbours_average_wrong
FROM input_data
```

![Results: for the two athletes born in 1991 (Jack Dalton 115, George Downey 125), neighbours\_average is 117.5 for both, while neighbours\_average\_wrong gives 120.0 and 116.66666666666667; all seven athletes from John Doe (1990) to Robert Key (1995) are listed.](/images/using-range-in-window-functions-in-bigquery/1-result.jpg)

RANGE comes with a limitation though - you can only order by a single numerical column.

Hope this was interesting!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Beware of ROW_NUMBER without ORDER BY](/beware-of-rownumber-without-order-by)
- [Tidying up WINDOW functions in BigQuery with named windows](/tidying-up-window-functions-in-bigquery-with-named-windows)
- [Computing a cumulative sum in BigQuery](/computing-a-cumulative-sum-in-bigquery)
- [Rolling period calculation in BigQuery](/rolling-period-calculation-in-bigquery)
