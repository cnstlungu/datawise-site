---
title: "Python Showdown: Namedtuple vs SimpleNamespace vs DataClass"
seoTitle: "namedtuple vs SimpleNamespace vs dataclass in Python"
seoDescription: "Compare Python's three lightweight data containers — namedtuple, SimpleNamespace, and dataclass — on mutability, memory, and verbosity to pick the right..."
datePublished: 2023-09-25T21:16:15.095Z
dateUpdated: 2026-03-29T07:34:49.725Z
cover: "/images/python-showdown-namedtuple-vs-simplenamespace-vs-dataclass/cover.jpg"
coverCredit:
  name: "Hisham Zayadneh"
  url: "https://unsplash.com/@hisham_zayadneh"
series: "python"
hashnodeCuid: "clmze1v1z000209mhhm812gzs"
---

Python users, ever needed a light data container (like a dictionary) but wanted to access members using the dot (.) notation?

There are a couple of options to choose from: namedtuple, SimpleNamespace  
and dataclass.

Here's how they all differ:

1️⃣ namedtuple: immutable, memory efficient, iterable and members can be accessed by index as well. Static and somewhat verbose.

2️⃣ simple\_namespace: mutable, uses more memory than namedtuple, not iterable nor indexable. Flexible and less verbose.

3️⃣ dataclass: can be mutable or not (controlled by `frozen` parameter), can set default attributes, has special methods like **repr** (how it's displayed) and **eq** (check if it's equal to another instance). Uses more memory and is relatively newly-introduced (Python 3.7).

![](/images/python-showdown-namedtuple-vs-simplenamespace-vs-dataclass/1.jpg)

When to use which?  
➡ namedtuple: You need something light on memory and immutable

➡ simple\_namespace: You need flexibility to change the attributes or even  
add them dynamically with little boilerplate.

➡ dataclass: You want more flexibility and control.

🔔 Follow me for more insights on Python and Analytics. Thanks for reading!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Structural Pattern Matching in Python](/structural-pattern-matching-in-python)
