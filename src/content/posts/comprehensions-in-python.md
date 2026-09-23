---
title: "Comprehensions in Python"
seoTitle: "Python Comprehensions: List, Dict, Set, and Generator"
seoDescription: "A concise guide to list, dictionary, set, and generator comprehensions in Python with practical examples. Learn when comprehensions improve code..."
datePublished: 2023-12-06T22:18:07.541Z
dateUpdated: 2026-03-02T15:57:37.874Z
cover: "/images/comprehensions-in-python/cover.jpg"
coverCredit:
  name: "Tomas Sobek"
  url: "https://unsplash.com/@tomas_nz"
series: "python"
hashnodeCuid: "clpubyrlh000008jn7u8cdbhd"
---

Do you work with Python comprehensions in your day-to-day?

Comprehensions are a straightforward way to create lists, sets, dictionaries and generators from existing iterables - such as lists or tuples.

They allow for short, concise notation as opposed to loops. As usual, it's important to think about code readability and not overuse them.

See below a quick worksheet with examples of common comprehensions in Python, applied in a simple scenario - computing number squares.

Thanks for reading!

```python
### Number squares - Python comprehensions examples

input_list = [1,2,3,4,5,6,7,8,9,10]

## List comprehension
output_list = []
for i in input_list:
    output_list.append(i**2)

[i**2 for i in input_list]
# both would print out: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# a list comprehension for only squares of even numbers
[i**2 for i in input_list if i%2==0]
# prints: [4, 16, 36, 64, 100]

## Dictionary comprehension
output_dict = {}
for i in input_list:
    output_dict[i] =  i**2

{ k: k**2 for k in input_list}
# both print out:
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 64, 9: 81, 10: 100}


## Set comprehension
input_list_with_dups = [1,2,3,4,5,6,7,8,9,10,10]

output_set = set()

for i in input_list_with_dups:
    output_set.add(i**2)

{i**2 for i in input_list_with_dups}
# both print out something like {64, 1, 4, 36, 100, 9, 16, 49, 81, 25}
# Sets are unordered and have unique members!

## NO TUPLE COMPREHENSIONS

## Generator comprehension
def generate_squares(list_of_numbers):
    for i in list_of_numbers:
        yield i**2

(i**2 for i in input_list)
# both produce a generator that will yield one by one
# [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using SETS in Python](/using-sets-in-python)
