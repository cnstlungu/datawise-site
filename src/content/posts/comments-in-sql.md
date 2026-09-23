---
title: "Comments in SQL"
seoTitle: "SQL Comments in BigQuery: --, #, and /* */ Syntax"
seoDescription: "BigQuery supports single-line comments with -- or #, and multi-line block comments with /* */. Learn the differences between inline and block comments to..."
datePublished: 2024-06-26T22:17:04.171Z
dateUpdated: 2026-03-02T10:52:19.487Z
cover: "/images/comments-in-sql/cover.jpg"
coverCredit:
  name: "Raphael Schaller"
  url: "https://unsplash.com/@raphaelphotoch"
series: "practical-sql"
hashnodeCuid: "clxwebc17000009jx954kh53g"
---

Let's look at the available options in terms of SQL comments in BigQuery.

If you ever need to pass on a note to the future you or a fellow developers about the reasoning behind a particular approach or something to watch out for in a query, you can write a comment.

Based on where we put them, we can distinguish between:  
\- single line, taking the entire line  
\- in-line, comments intertwined with code  
\- multi-line, comments spanning across lines

With regards to the notation, we have:  
\- the '--' will turn everything after it on the same line into a comment  
\- the '#' which you might recognize from say Python, and works like '--'  
\- the '/\* \*/' block which clearly marks it start and end, making possible the insertions of a comment inside a code line and multi-line comments

How much are you using comments in your SQL code and in what situations?

![](/images/comments-in-sql/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
