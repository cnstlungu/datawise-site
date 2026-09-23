---
title: "Beware of ROW_NUMBER without ORDER BY"
seoTitle: "Avoid ROW_NUMBER Chaos: Use ORDER BY"
seoDescription: "Avoid using ROW_NUMBER() without ORDER BY to prevent random changes in reports. Understand its pitfalls and ensure data accuracy"
datePublished: 2025-09-30T05:20:48.829Z
dateUpdated: 2026-03-02T10:52:55.065Z
cover: "/images/beware-of-rownumber-without-order-by/cover.jpg"
coverCredit:
  name: "Free Walking Tour Salzburg"
  url: "https://unsplash.com/@freewalkingtoursalzburg"
series: "bigquery-window-functions"
hashnodeCuid: "cmg6404ho000002jr77x13ow5"
---

Haven’t posted all summer, but this bug pulled me straight out of the shadows.

I recently faced a mystery that pushed me to the edge of despair.

It seemed like a simple issue at first glance. A report kept changing completely at random.

I spent a good few days chasing it across multiple weeks . Imagine juggling several tables with time travel, all joined together. Trying to catch the bug.

I started to wonder if time travel even worked correctly. I wasn’t able to reproduce previous states, even when all the inputs had data from that exact point in time.

I began to question if I’d make it. The culprit?

Take this as a cautionary tale against using ROW\_NUMBER() OVER(PARTITION BY …) without an accompanying ORDER BY.

Tucked into a table somewhere, it haunted me and wreaked havoc. I don’t know if there’s a real use case for it like that — but expect surprises.

![Scooby-Doo unmasking meme: Fred asks why the report keeps changing at random, then pulls the mask off the ghost to reveal the villain, labelled ROW\_NUMBER with stochastic vibes.](/images/beware-of-rownumber-without-order-by/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [***notjustsql.com***](https://www.notjustsql.com/)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Tidying up WINDOW functions in BigQuery with named windows](/tidying-up-window-functions-in-bigquery-with-named-windows)
- [Using RANGE in Window Functions in BigQuery](/using-range-in-window-functions-in-bigquery)
- [Computing a cumulative sum in BigQuery](/computing-a-cumulative-sum-in-bigquery)
- [Rolling period calculation in BigQuery](/rolling-period-calculation-in-bigquery)
