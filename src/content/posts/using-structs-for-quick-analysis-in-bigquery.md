---
title: "Using STRUCTS for quick analysis in BigQuery"
seoTitle: "Use BigQuery STRUCTs to Filter Multiple Test Cases at Once"
seoDescription: "Wrap multiple filter conditions into an array of STRUCTs in BigQuery to check several test cases in a single query pass."
datePublished: 2024-04-19T13:59:14.029Z
dateUpdated: 2026-03-02T10:52:09.406Z
cover: "/images/using-structs-for-quick-analysis-in-bigquery/cover.jpg"
coverCredit:
  name: "Marc Sendra Martorell"
  url: "https://unsplash.com/@marcsm"
series: "bigquery-arrays-and-structs"
hashnodeCuid: "clv6ql6r1000m0ald2mym54eu"
---

I've posted earlier [about STRUCTS in BigQuery](/understanding-structs-in-bigquery), here's how I use it from time to time to help me debug and analyze data a bit faster.

Since changing filter values for different test cases / observations you are interested about can be a headache (especially if you have a lot of columns), you could put them in a tuple of STRUCTS and check the matching records at once.

Not a game changer but makes life a bit easier 😁

![BigQuery SQL filtering customers with WHERE STRUCT(country, has\_paid, plan, service) IN (STRUCT('UK', FALSE, 'Premium', 'TV'), STRUCT('FR', FALSE, 'Basic', 'Internet')) as a shorter alternative to chained AND/OR conditions; it returns Catie Doe (UK) and Francesca Duchamp (FR).](/images/using-structs-for-quick-analysis-in-bigquery/1.jpg)

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Understanding STRUCTS in BigQuery](/understanding-structs-in-bigquery)
- [Constructing STRUCTS in BigQuery](/constructing-structs-in-bigquery)
- [Using STRUCTS for Audit Fields in BigQuery](/using-structs-for-audit-fields-in-bigquery)
- [Using LAST_VALUE with STRUCTS](/using-lastvalue-with-structs)
