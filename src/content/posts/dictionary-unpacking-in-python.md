---
title: "Dictionary Unpacking in Python"
seoTitle: "Python Dictionary Unpacking with ** for Cleaner Code"
seoDescription: "Learn how to use Python's ** operator to unpack dictionaries as function keyword arguments, with a practical API call templating example that keeps config..."
datePublished: 2023-09-08T13:49:15.907Z
dateUpdated: 2026-03-29T07:34:51.053Z
cover: "/images/dictionary-unpacking-in-python/cover.jpg"
coverCredit:
  name: "Kelli McClintock"
  url: "https://unsplash.com/@kelli_mcclintock"
series: "python"
hashnodeCuid: "clmanljwi000e09l68xor9q3o"
---

One of the most versatile aspects of Python dictionaries is the ability to unpack them. Ever wondered how to use dictionary values as function arguments?

Simply employ the \*\* operator\*\*:

```python
def greet(name, age):
    return f"Hello {name}, you're {age} years old!"

data = {'name': 'Jane', 'age': 28}
print(greet(**data)) # This will print: Hello Jane, you're 28 years old!
```

Let's dive deeper into a practical use case:

Imagine making multiple API calls, where every call has a different template with a unique URL, endpoint, and parameters.

You'd need a systematic way to manage this. Here's when dictionary unpacking comes to the rescue.

```python

url_format_templates = {
    'A': '{api_url}/{endpoint_name}',
    'B': '{api_url}/{endpoint_name}?parameter1={parameter1}&parameter2={parameter2}',
    'C': '{api_url}/{endpoint_name}?parameter3={parameter3}'
}

url_configurations = {
    'A': {'api_url': 'siteA.com', 'endpoint_name': 'endpointA'},
    'B': {'api_url': 'siteB.com', 'endpoint_name': 'endpointB', 'parameter1': 100, 'parameter2': '50'},
    'C': {'api_url': 'siteC.com', 'endpoint_name': 'endpointC', 'parameter3': 200}
}

for site, template in url_format_templates.items():
    try:
        print(template.format(**url_configurations[site]))
    except KeyError as e:
        print(f"Error formatting URL for site {site}. Missing key: {e}")


# outputs
#siteA.com/endpointA
#siteB.com/endpointB?parameter1=100&parameter2=50
#siteC.com/endpointC?parameter3=200
```

*[View on GitHub Gist](https://gist.github.com/cnstlungu/4333aa644ee3420f67e0f18716d5f950)* 

We're separating the templates and configuration and then leveraging dictionary unpacking for a flexible yet clean approach.

Stay tuned for more Python insights and best practices!

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using SETS in Python](/using-sets-in-python)
