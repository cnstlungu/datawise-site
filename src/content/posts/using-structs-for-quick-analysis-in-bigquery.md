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

```sql
WITH input_data AS (
  SELECT 'Catie Doe' AS name, 'UK' AS country, false AS has_paid, 'Premium' AS plan, 'TV' AS service
  UNION ALL
  SELECT 'Martin Bekker' AS name, 'DE' AS country, true AS has_paid, 'Premium' AS plan, 'TV' AS service
  UNION ALL
  SELECT 'Jerry Taylor' AS name, 'US' AS country, true AS has_paid, 'Basic' AS plan, 'Internet' AS service
  UNION ALL
  SELECT 'Francesca Duchamp' AS name, 'FR' AS country, false AS has_paid, 'Basic' AS plan, 'Internet' AS service
  UNION ALL
  SELECT 'Paolo Rossi' AS name, 'IT' AS country, true AS has_paid, 'Premium' AS plan, 'Internet' AS service
)

SELECT name, country, has_paid, plan, service FROM input_data

-- Retrive UK customers on a TV Premium Plan or FR customers on Internet Basic plan that haven't paid yet

WHERE STRUCT(country, has_paid, plan, service) IN (STRUCT('UK', FALSE, 'Premium', 'TV'),
                                                   STRUCT('FR', FALSE, 'Basic', 'Internet'))

--- alternative to:
-- WHERE

-- (country = 'FR' AND plan='Basic' AND NOT has_paid AND service = 'Internet') OR
-- (country = 'UK' AND plan='Premium' AND NOT has_paid AND service = 'TV')
```

![BigQuery results: two rows, Catie Doe (UK, has\_paid false, Premium, TV) and Francesca Duchamp (FR, has\_paid false, Basic, Internet).](/images/using-structs-for-quick-analysis-in-bigquery/1-result.jpg)

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Understanding STRUCTS in BigQuery](/understanding-structs-in-bigquery)
- [Constructing STRUCTS in BigQuery](/constructing-structs-in-bigquery)
- [Using STRUCTS for Audit Fields in BigQuery](/using-structs-for-audit-fields-in-bigquery)
- [Using LAST_VALUE with STRUCTS](/using-lastvalue-with-structs)
