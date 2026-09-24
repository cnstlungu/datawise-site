---
title: "Partial functions in Python"
seoTitle: "Python functools.partial: Pre-fill Function Arguments"
seoDescription: "Learn how to use functools.partial in Python to create specialized versions of existing functions by pre-filling one or more arguments."
datePublished: 2023-12-17T09:55:45.083Z
dateUpdated: 2026-03-29T07:34:48.127Z
cover: "/images/partial-functions-in-python/cover.jpg"
coverCredit:
  name: "Rafael Garcin"
  url: "https://unsplash.com/@nimbus_vulpis"
series: "python"
hashnodeCuid: "clq9bafqz000008l3c29n9u4d"
---

Have you ever used partial functions? It's an interesting functionality that can be found in the *functools* package.

It's pretty straightforward - you can take a function that takes multiple arguments and produces a new function that has one or more arguments already set, effectively tailoring your previous function to a specific need.

See below an example of it in action.

```python
from functools import partial

# Raises the number to a power
def power(base, exponent):
    return base ** exponent

# Making specialized versions for squaring and cubing
square = partial(power, exponent = 2)

cube = partial(power, exponent = 3)

print(square(5))  # Output: 25

print(cube(5))    # Output: 125
```

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Decorators in Python](/decorators-in-python)
