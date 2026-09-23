---
title: "Decorators in Python"
seoTitle: "Python Decorators Explained with a Practical Example"
seoDescription: "Learn how Python decorators work using the @ pie notation to modify function behavior without changing function structure."
datePublished: 2023-12-19T22:38:33.653Z
dateUpdated: 2026-03-02T10:53:15.286Z
cover: "/images/decorators-in-python/cover.jpg"
coverCredit:
  name: "Thalia Ruiz"
  url: "https://unsplash.com/@thalia_s_ruiz"
series: "python"
hashnodeCuid: "clqcxf4c5000208jng5jd3kzd"
---

One of the important programming patterns is the decorator pattern.

What do decorators do? They modify a function's behavior, allowing us to enhance to add functionality without changing its structure. But how does it work in Python?

You might have noticed the syntactic sugar notation for the decorator - the so-called 'pie' notation: @.

```python
@decorator
def my_function():
    do something
```

Let's look at a quick practical example. We're going to define a 'polite' decorator that will modify announcements issued in a train station.

We will then decorate a function issuing such an announcement.

Here's how it would look like:

```python
def polite(function):
    def wrapper():
            print('Dear passengers!')
            original_output = function()
            print(f'Please {original_output}')
            print('Thank you for traveling with us!')
    return wrapper

@polite
def issue_offboarding_warning():
    return "mind the gap between the train and the platform."

@polite
def issue_platform_warning():
    return "maintain a safe distance from the edge of the platform."


issue_offboarding_warning()
# Dear passengers!
# Please mind the gap between the train and the platform.
# Thank you for traveling with us!

issue_platform_warning()
# Dear passengers!
# Please maintain a safe distance from the edge of the platform.
# Thank you for traveling with us!
```

Thanks for reading!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
