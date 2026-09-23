---
title: "A quick look at the json module in Python"
seoTitle: "JSON Module in Python: Quick Overview"
seoDescription: "Learn how to handle JSON in Python using the json module for encoding, decoding, and pretty-formatting"
datePublished: 2024-08-07T09:14:14.719Z
dateUpdated: 2026-03-02T10:52:14.963Z
cover: "/images/a-quick-look-at-the-json-module-in-python/cover.jpg"
coverCredit:
  name: "Pankaj Patel"
  url: "https://unsplash.com/@pankajpatel"
series: "python"
hashnodeCuid: "clzjmue67000h0al898ki9qu1"
---

If you ever need to work with JSON files in Python, you're going to encounter the module with the same name.

It help encode to and decode from JSON. Here are the basics:

➡ json.load imports contents from a JSON file to a Python object, based on conversion rules (object -&gt; dict, array -&gt; list/tuple, string-&gt; str etc)

➡ json.dump performs the opposite operation - export to a file-like object

There are also the json.loads and json.dumps functions (notice the extra s) which apply to strings instead of files.

There's also the *json.tool*, which can validate and pretty-format a provided json file.

You can save that prettified json into another file, as follows:

`python -m json.tool ugly_format.json pretty_format.json`

![](/images/a-quick-look-at-the-json-module-in-python/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Retrying in Python using tenacity](/retrying-in-python-using-tenacity)
- [Using virtual environments in Python](/using-virtual-environments-in-python)
- [Installing Python packages with pip](/installing-python-packages-with-pip)
- [Using tempfile module in Python](/using-tempfile-module-in-python)
