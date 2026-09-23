---
title: "Generating a Random Number in BigQuery"
seoTitle: "BigQuery RAND(): Random Numbers and Random Array Elements"
seoDescription: "RAND() in BigQuery returns a pseudo-random float between 0 and 1. Scale it for integers or use with ARRAY_LENGTH to pick a random element from an array."
datePublished: 2024-05-16T09:40:21.308Z
dateUpdated: 2026-03-02T10:22:48.975Z
cover: "/images/generating-a-random-number-in-bigquery/cover.jpg"
coverCredit:
  name: "Steve Smith"
  url: "https://unsplash.com/@varrak"
series: "practical-sql"
hashnodeCuid: "clw9289mk00170ajo84cx2b0s"
---

If you're looking to generate a random number in BigQuery, check out the RAND() function.

It's a pseudo-random number generator, generating a float in the interval \[0, 1).

I've used it a few times before, but for the today's exercise, I've decide to try something akin to Python's random.pick(). So, let's pick a random value from an ARRAY.

Inspired by one of [Mikhail Berlyant's SO answers](https://stackoverflow.com/questions/56780571/generate-a-random-value-from-an-array-in-google-bigquery-standard-sql) (which are some of the best answers on BigQuery on SO, linked in comments), I wanted to randomly assign one of 20 options to 100 participants.

As seen in [one of my previous posts](/accessing-array-elements-in-bigquery) about accessing array elements, we're going to generate a random 0-based index to retrieve the random array element in each case.

`OFFSET(CAST(ARRAY_LENGTH(available_options)*RAND()-0.5 AS INT64))`

![BigQuery SQL that builds an available\_options array of Option 1 to Option 20 with ARRAY\_AGG, CONCAT and GENERATE\_ARRAY, cross joins 100 participants and picks one per row with OFFSET(CAST(ARRAY\_LENGTH(available\_options)\*RAND()-0.5 AS INT64)); results list each participant\_id with a random selected\_option.](/images/generating-a-random-number-in-bigquery/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at*[*notjustsql.com*](https://www.notjustsql.com)*.*
