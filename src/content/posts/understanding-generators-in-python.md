---
title: "Understanding Generators in Python 🐍"
seoTitle: "Python Generators Explained for Data Engineers"
seoDescription: "Understand how Python generators work using yield, why they are memory-efficient for large datasets, and when to use them over lists in data engineering..."
datePublished: 2023-09-25T21:12:57.924Z
dateUpdated: 2026-03-02T10:52:42.929Z
cover: "/images/understanding-generators-in-python/cover.jpg"
coverCredit:
  name: "Jayphen Simpson"
  url: "https://unsplash.com/@jayphen"
series: "python"
hashnodeCuid: "clmzdxmwz000009jwb2eo08a9"
---

Generators are an important concept in Python. They are functions that produce a sequence of values when iterated over.

They provide an iterable (just like lists or tuples) but with a key difference - generators don't store all of their values in memory at once. They produce each value on-the-fly, as you iterate over them, so they're great to use when working with large datasets. And crucial to know about as a Data Engineer.

A generator is defined by using yield instead of return in a function.

In short: generators are:  
\- lazy (items are produced one by one when requested)  
\- stateful between calls (you can pick up where you left off using next() )  
\- immutable (the sequence produced cannot be modified)  
\- single-use (you can iterate through it only once)

![Python comparison: get\_first\_n\_squares\_gen(n) uses yield i \* i to produce squares lazily, consumed by a list comprehension, while get\_first\_n\_squares(n) builds a squares list with append and returns it; both print 0, 1, 4, 9, 16 for n = 5.](/images/understanding-generators-in-python/1.jpg)

TL;DR When handling large, streaming or single-use collections, consider using generators. 💡

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Retrying in Python using tenacity](/retrying-in-python-using-tenacity)
- [Using virtual environments in Python](/using-virtual-environments-in-python)
- [Installing Python packages with pip](/installing-python-packages-with-pip)
- [A quick look at the json module in Python](/a-quick-look-at-the-json-module-in-python)
