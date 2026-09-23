---
title: "Using zip in Python"
seoTitle: "Python zip() Function: Iterate Multiple Lists at Once"
seoDescription: "Python's zip() lets you iterate over multiple iterables simultaneously, pairing elements into tuples. It stops at the shortest iterable, making it a..."
datePublished: 2024-02-23T15:27:11.298Z
dateUpdated: 2026-03-02T10:53:14.164Z
cover: "/images/using-zip-in-python/cover.jpg"
coverCredit:
  name: "Tomas Sobek"
  url: "https://unsplash.com/@tomas_nz"
series: "python"
hashnodeCuid: "clsyt2ldu000008ladlc87244"
---

If you haven't encountered it already, note that zip is quite handy in Python.

It allows you to go through multiple iterables (such as lists, sets, tuples etc) at the same time, effectively "zipping" them into an iterator that will produce tuples of elements from each initial collection.

Worth keeping in mind that if the provided iterables' length differs, zip will stop when the shortest of them has reached its end.

Happy coding!

```python
integers = [1,2,3,4,5]

letters = ['a','b', 'c', 'd']

for pair in zip(integers, letters):
    print(pair)

# Prints:
# (1, 'a')
# (2, 'b')
# (3, 'c')
# (4, 'd')
```

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Retrying in Python using tenacity](/retrying-in-python-using-tenacity)
- [Using virtual environments in Python](/using-virtual-environments-in-python)
- [Installing Python packages with pip](/installing-python-packages-with-pip)
- [A quick look at the json module in Python](/a-quick-look-at-the-json-module-in-python)
