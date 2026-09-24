---
title: "Using LAST_VALUE with STRUCTS"
seoTitle: "Mastering LAST_VALUE Function with STRUCTS"
seoDescription: "Learn how to correctly use LAST_VALUE with STRUCTs in SQL and handle non-null structures with practical examples and solutions"
datePublished: 2025-10-05T16:27:43.240Z
dateUpdated: 2026-03-02T10:52:52.854Z
cover: "/images/using-lastvalue-with-structs/cover.jpg"
coverCredit:
  name: "Tanja Tepavac"
  url: "https://unsplash.com/@ttepavac"
series: "bigquery-window-functions"
hashnodeCuid: "cmgdx1154000002l962hqaixy"
---

Even an “empty” STRUCT is still technically something. Not the same as a standalone NULL value.

This is why, if you work with STRUCTs in SQL and try to find the latest non-empty struct using LAST\_VALUE(...) IGNORE NULLS, you’ll notice it doesn’t help — because the struct, even when all fields are null, is still considered non-null.

LAST\_VALUE only skips rows where the entire expression itself is NULL.

To fix this, we can adjust the logic in one of the following ways:  
➡️ Setting the value to NULL when all fields are NULL  
➡️ Using TO\_JSON\_STRING + NULLIF to treat such entries as “null”  
➡️ Using REGEXP\_CONTAINS (thanks ChatGPT) for more dynamic checks

Alternatively, we can just apply LAST\_VALUE separately to each individual field in the struct.

If you're new to STRUCTs, see [one of my previous posts](/understanding-structs-in-bigquery).

![Input data: event\_date with a struct event of fields a and b, three rows: 2025-01-10 with a and b null, 2025-01-07 with a 123 and b 235, 2025-01-02 with a and b null.](/images/using-lastvalue-with-structs/1-input.jpg)

```sql
SELECT
  event_date,
  LAST_VALUE(event IGNORE NULLS) OVER (ORDER BY event_date
                                       ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS last_known_event
FROM cte

ORDER BY event_date
```

![BigQuery results: 2025-01-02 null, 2025-01-07 a 123 and b 235, and 2025-01-10 null again, because the all-null struct is not skipped.](/images/using-lastvalue-with-structs/1-result.jpg)

```sql
SELECT event_date,
    LAST_VALUE(CASE WHEN event.a IS NULL AND event.b IS NULL THEN NULL ELSE event END IGNORE NULLS)
          OVER (ORDER BY event_date
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS last_known_event_struct,

    LAST_VALUE(NULLIF(TO_JSON_STRING(event),'{"a":null,"b":null}') IGNORE NULLS)
          OVER (ORDER BY event_date
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS last_known_event_json,

    LAST_VALUE(CASE WHEN NOT REGEXP_CONTAINS(TO_JSON_STRING(event), r':(true|false|"|[0-9\-]|\[|\{)') THEN NULL ELSE event END IGNORE NULLS)
          OVER (ORDER BY event_date
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW ) AS last_known_event_regex

FROM cte
```

![BigQuery results: with all three fixes, 2025-01-02 stays null while 2025-01-07 and 2025-01-10 both carry 123 and 235 forward in the struct, JSON-string and regex columns.](/images/using-lastvalue-with-structs/1-result-2.jpg)

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Beware of ROW_NUMBER without ORDER BY](/beware-of-rownumber-without-order-by)
- [Tidying up WINDOW functions in BigQuery with named windows](/tidying-up-window-functions-in-bigquery-with-named-windows)
- [Using RANGE in Window Functions in BigQuery](/using-range-in-window-functions-in-bigquery)
- [Computing a cumulative sum in BigQuery](/computing-a-cumulative-sum-in-bigquery)
