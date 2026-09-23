---
title: "Why you should use UNION DISTINCT sparingly"
seoTitle: "UNION ALL vs UNION DISTINCT in BigQuery: Avoid Wasted Slots"
seoDescription: "Using UNION DISTINCT on already-distinct sources wastes slot time on unnecessary deduplication in BigQuery. Switch to UNION ALL when sources are known to..."
datePublished: 2024-04-02T23:12:39.465Z
dateUpdated: 2026-03-02T10:52:11.695Z
cover: "/images/why-you-should-use-union-distinct-sparingly/cover.jpg"
coverCredit:
  name: "Randy Fath"
  url: "https://unsplash.com/@randyfath"
series: "practical-sql"
hashnodeCuid: "cluizvew9000008i88ygd6rxj"
---

Let's help BigQuery do less unneeded work!

If you're UNIONING two sources known to have distinct values (and they don't have duplicates), go for UNION ALL instead of UNION DISTINCT (UNION for some other sql dialects) to avoid redundant de-duplication.

In the example below, I've unioned two Google Trends tables - one that is only for US terms and another one for the rest of the world. Since one table only contains US and the other everything except the US, we know the union of the two tables to be distinct from the start, thus not needing the UNION DISTINCT.

![](/images/why-you-should-use-union-distinct-sparingly/1.jpg)

There's no difference indeed for on-demand pricing (same amount of data scanned), but quite a difference for capacity pricing users ( 1/2 of slot usage).

So use UNION DISTINCT (and any other DISTINCT) sparingly and when you actually need it.

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [9 tips on writing cleaner SQL](/9-tips-on-writing-cleaner-sql)
- [Order of precedence in SQL: WHERE vs HAVING](/order-of-precedence-in-sql-where-vs-having)
- [Easy with that SELECT DISTINCT!](/easy-with-that-select-distinct)
- [Why you should use parentheses with AND & OR in SQL](/why-you-should-use-parentheses-with-and-or-in-sql)
