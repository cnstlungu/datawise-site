---
title: "sorted(List) vs List.sorted() in Python"
seoTitle: "Sorted Function vs Method in Python"
seoDescription: "Learn the key differences between sorted() and List.sort() in Python, crucial for effective data handling and management"
datePublished: 2024-08-04T11:03:08.194Z
dateUpdated: 2026-03-02T10:52:38.522Z
cover: "/images/sortedlist-vs-listsorted-in-python/cover.jpg"
coverCredit:
  name: "Aram Ramazyan"
  url: "https://unsplash.com/@alien4you2"
series: "python"
hashnodeCuid: "clzfgevfm000809jq4z1h0u04"
---

When I was just starting out with Python I found the distinction between a function doing something in place and returning the result instead pretty interesting.

Understanding this distinction is pretty important as a beginner! Since sorting in one of the most important operations we do in programming, let's look at an example involving exactly that.

➡ sorted(\[a\_list\]): is a built-in function than returns a new sorted list, without modifying the original  
➡ a\_list.sort(): sorts the list in place and doesn't return anything

```python
numbers = [2,3,1,4,5,5]

print(sorted(numbers))
# returns a new, sorted list
# [1, 2, 3, 4, 5, 5]

print(numbers)
# the original list was not affected
# [2, 3, 1, 4, 5, 5]

numbers.sort()
# sorts the original list in-place

print(numbers)
# check that the original list is sorted
# [1, 2, 3, 4, 5, 5]
```
