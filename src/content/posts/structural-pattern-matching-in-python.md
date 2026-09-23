---
title: "Structural Pattern Matching in Python"
seoTitle: "Python match Statement: Structural Pattern Matching Guide"
seoDescription: "Explore the Python 3.10 match statement for structural pattern matching, how it compares to if-elif-else chains, and where it handles complex conditions..."
datePublished: 2023-09-16T14:49:46.894Z
dateUpdated: 2026-03-02T10:53:16.401Z
cover: "/images/structural-pattern-matching-in-python/cover.jpg"
coverCredit:
  name: "Andrew Ridley"
  url: "https://unsplash.com/@aridley88"
series: "python"
hashnodeCuid: "clmm5a6x9000008l556gb5w8t"
---

Have you had the opportunity to dive into the match statement introduced in Python 3.10? This feature brings structural pattern matching to Python, reminiscent of the pattern matching in Scala that I've always admired.

What makes the match statement stand out? It's not just a streamlined alternative to the traditional if-elif-else block. It offers a more structured and concise way to handle multiple conditions, making your code easier to read, especially when juggling numerous cases.

Additionally, it can gracefully handle complex patterns like sequence unpacking and can match against multiple values simultaneously—something not so straightforward with if-elif-else.

```python
# Classical if-elif-else
def get_day_name(day_number: int) -> str:

	if day_number == 1:
		return "Monday"
	elif day_number == 2:
		return "Tuesday"
	elif day_number == 3:
		return "Wednesday"
	elif day_number == 4:
		return "Thursday"
	elif day_number == 5:
		return "Friday"
	elif day_number == 6:
		return "Saturday"
	elif day_number == 7:
		return "Sunday"
	else:
		return "Invalid day number"
```

```python
# using match for pattern matching
def get_day_name(day_number: int) -> str:

	match day_number:
		case 1:
			return "Monday"
		case 2:
			return "Tuesday"
		case 3:
			return "Wednesday"
		case 4:
			return "Thursday"
		case 5:
			return "Friday"
		case 6:
			return "Saturday"
		case 7:
			return "Sunday"
		case _:
			return "Invalid day number"
```

While the classic if-elif-else approach has its place and is compatible with older Python versions, the match statement ushers in a fresh, concise, and expressive method to manage multiple conditions. If you haven't tried it yet, I highly recommend giving it a spin!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
