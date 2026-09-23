---
title: "LIKE ALL and LIKE ANY in BigQuery"
seoTitle: "BigQuery LIKE ALL and LIKE ANY: Multi-Pattern Matching"
seoDescription: "LIKE ANY matches if any pattern matches; LIKE ALL requires all to match. Learn BigQuery's quantified LIKE operators with practical SQL examples and edge cases."
datePublished: 2023-12-05T23:01:17.352Z
dateUpdated: 2026-03-02T10:16:36.542Z
cover: "/images/like-all-and-like-any-in-bigquery/cover.jpg"
coverCredit:
  name: "JJ Ying"
  url: "https://unsplash.com/@jjying"
series: "practical-sql"
hashnodeCuid: "clpsy2f8o000108l243wxftf3"
---

Let's look at the quantified LIKE operator in BigQuery. Why quantified? , you'll ask.

So while the normal LIKE operator can be used to check just for one pattern, the quantified one (still in preview btw) can check the presence of one or all patterns from a sequence we provide. Here's how the syntax looks.

`WHERE text LIKE ALL ('%dog%', '%fox%')` - this will check if ALL the patterns are present in the text

```sql
WITH input_data AS 

(
  SELECT 'The quick brown fox jumps over the lazy dog' AS text
  UNION ALL
  SELECT 'My favorite dog is a Labrador' AS text
)

SELECT text FROM input_data

WHERE text LIKE ALL ('%dog%', '%fox%')

-- returns only the first row, since only that one has both dog and fox
```

`WHERE text LIKE SOME ('%dog%', '%fox%')` and  
`WHERE text LIKE ANY ('%dog%', '%fox%')` - these two are synonyms and will check if AT LEAST ONE of the listed patterns is present in the text

```sql
WITH input_data AS 

(
  SELECT 'The quick brown fox jumps over the lazy dog' AS text
  UNION ALL
  SELECT 'My favorite dog is a Labrador' AS text
)

SELECT text FROM input_data

WHERE text LIKE ALL ('%dog%', '%fox%')
-- returns both rows, since both match at least one pattern
```

Pair them with the NOT keyword to achieve the opposite effect, so NOT LIKE ANY/SOME means not even a partial match and NOT LIKE ALL means no full match.

Thanks for reading!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
