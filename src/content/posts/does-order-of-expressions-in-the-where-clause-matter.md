---
title: "Does order of expressions in the WHERE clause matter?"
seoTitle: "Does WHERE Clause Order Affect BigQuery Performance?"
seoDescription: "Investigates whether the order of filter expressions in a BigQuery WHERE clause impacts query performance, based on a 200M row public dataset test."
datePublished: 2023-12-03T16:46:01.427Z
dateUpdated: 2026-03-02T10:52:22.855Z
cover: "/images/does-order-of-expressions-in-the-where-clause-matter/cover.jpg"
coverCredit:
  name: "Michal Mrozek"
  url: "https://unsplash.com/@miqul"
series: "practical-sql"
hashnodeCuid: "clppps4ib000009l46lf576gk"
---

Does the order of expressions in a WHERE clause matter for performance?

So an interesting point found in a [Google Cloud blog post](https://cloud.google.com/blog/topics/developers-practitioners/bigquery-admin-reference-guide-query-optimization) was the fact that this expression order matters, with BigQuery assuming that the user has provided the best order of expressions in the WHERE clause, so it would not reorder expressions.

The recommendation given is to put the most selective expression first - basically, the one that narrows down the result set the most.

For testing it out, I've picked a ~200 million rows table (the publicly available `google_trends.international_top_terms`) .

The two scenarios to be tested were the ones presented in the same blog post - an exact match on a string and a wildcard lookup, then switching their order in the WHERE clause.

Now, the blog post is already more than 2 years old and some things might have changed, given I wasn't able to replicate the results very well.

The results have shown almost no difference between the two approaches (across several attempts), but another reason might be the table is just not big enough for me to see a difference.

![](/images/does-order-of-expressions-in-the-where-clause-matter/1.jpg)

In any case, I'll keep this in mind next time I'm working with a very big table and check it out again.

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [A couple of fun things about NULL in SQL](/a-couple-of-fun-things-about-null-in-sql)
- [Not all NULLS are the same](/not-all-nulls-are-the-same)
- [COALESCE vs IFNULL vs NULLIF in BigQuery](/coalesce-vs-ifnull-vs-nullif-in-bigquery)
- [Null-safe comparison: IS DISTINCT/NOT DISTINCT FROM](/null-safe-comparison-is-distinctnot-distinct-from)
