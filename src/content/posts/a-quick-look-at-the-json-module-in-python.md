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

![Input data: data.json, a users list of three objects with id, name and email: 1 John Doe johndoe@example.com, 2 Jane Smith janesmith@example.com and 3 Bob Johnson bobjohnson@example.com.](/images/a-quick-look-at-the-json-module-in-python/1-input.jpg)

```python
import json

# Loading JSON data

object_from_json_string = json.loads('{"a":1, "b":2, "c":[1,2,3]}')
# <class 'dict'> {'a': 1, 'b': 2, 'c': [1, 2, 3]}

object_from_file = json.load(open('data.json'))
# <class 'dict'> {'users': [{'id': 1, 'name': 'John Doe', 'email': 'johndoe@example.com'},
#                           {'id': 2, 'name': 'Jane Smith', 'email': 'janesmith@example.com'},
#                           {'id': 3, 'name': 'Bob Johnson', 'email': 'bobjohnson@example.com'}]}


# Exporting (dumping) JSON data

a_dict = {'x': 1, 'y': 2, 'z': [1,2,3] }

json_string = json.dumps(a_dict)
# <class 'str'> {"x": 1, "y": 2, "z": [1, 2, 3]}

json.dump(a_dict, open('exported_data.json', 'w'))
```

![Output: the exported\_data.json file written by json.dump contains {"x": 1, "y": 2, "z": \[1, 2, 3\]}.](/images/a-quick-look-at-the-json-module-in-python/1-output.jpg)

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Retrying in Python using tenacity](/retrying-in-python-using-tenacity)
- [Using virtual environments in Python](/using-virtual-environments-in-python)
- [Installing Python packages with pip](/installing-python-packages-with-pip)
- [Using tempfile module in Python](/using-tempfile-module-in-python)
