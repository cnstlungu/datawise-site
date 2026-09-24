---
title: "Dunder / magic functions in Python"
seoTitle: "Python Dunder Methods: A Practical Guide with Examples"
seoDescription: "Explains Python dunder (magic) methods like __init__, __repr__, __eq__, and __lt__ with a hands-on class example."
datePublished: 2023-11-28T11:41:27.503Z
dateUpdated: 2026-03-02T10:52:23.983Z
cover: "/images/dunder-magic-functions-in-python/cover.jpg"
coverCredit:
  name: "Cristian Escobar"
  url: "https://unsplash.com/@cristian1"
series: "python"
hashnodeCuid: "clpi9p6xb000n09lbepif6c5f"
---

One thing you might encounter in Python are the "dunder" (because of the double underscore before and after their name) or "magic" methods, because they're special. You should have surely seen the '\_\_init\_\_' method in Python code.

Now, 'dunder' methods are special methods that allow classes to interact with the built-in functions or operators.

We need them because a Python built-in, e.g. the 'greater than' sign (&gt;), does not know how to perform a comparison between two instances of a class we define.

The same would go for many other behaviors such as looping through the object, representing it as a string or finding out its length. There are dozens of dunder/magic methods, but I'll illustrate a few below in a short example.

Let's build a Skyscraper class and implement some magic functions that will allow for comparison, ordering and representation of such classes.

```python
class Skyscraper:
    def __init__(self, name, height):
        self.name = name
        self.height = height

    def __repr__(self):
        return f"Skyscraper({self.name},{self.height})"
    
    def __str__(self):
        return f"{self.name} @ {self.height} "

    def __eq__(self, other):
        if not isinstance(other, Skyscraper):
            return NotImplemented
        return self.height == other.height

    def __ge__(self, other):
        if not isinstance(other, Skyscraper):
            return NotImplemented
        return self.height >= other.height
    
    def __lt__(self, other):
        if not isinstance(other, Skyscraper):
            return NotImplemented
        return self.height < other.height
```

Now, let's see them in action:

```python
# Creating 3 Skyscraper objects
burj_khalifa = Skyscraper('Burj Khalifa', 818)  # Height = 818
taipei_101 = Skyscraper('Taipei 101', 508)  # Height = 508
one_wtc = Skyscraper('One WTC', 541)    # Height = 541

# String representation
print(str(burj_khalifa)) #Output Burj Khalifa @ 818 

# Checking equality
print(burj_khalifa == taipei_101)  # Output: False (because heights are not equal)

# Checking greater than or equal
print(burj_khalifa >= taipei_101)  # Output: True (818 >= 508)
print(taipei_101 >= one_wtc)  # Output: False

# Checking less than
print(one_wtc < taipei_101)  # Output: False
print(one_wtc < burj_khalifa)  # Output: True

# Sorting an array of skyscrapers ascendingly
print(sorted([burj_khalifa, taipei_101, one_wtc])) 
# Output [Skyscraper(Taipei 101,508), Skyscraper(One WTC,541), Skyscraper(Burj Khalifa,818)]
```

Thanks for reading!
