---
title: "Context Managers in Python"
seoTitle: "Python Context Managers Explained with the with Statement"
seoDescription: "Learn what Python context managers do, why data engineers need them for safe resource handling, and how to implement __enter__ and __exit__ in a custom..."
datePublished: 2023-10-06T23:35:56.576Z
dateUpdated: 2026-03-02T10:51:54.717Z
cover: "/images/context-managers-in-python/cover.jpg"
coverCredit:
  name: "Laura Ockel"
  url: "https://unsplash.com/@viazavier"
series: "python"
hashnodeCuid: "clnf8vvkw00020al6avtoemkv"
---

Ever encountered the `with` statement? I've seen them around lots of times, but once, when asked about Context Managers during an interview, I didn't know what they were! Here's what to know about them, so you won't repeat my mistake.

You might've used it without realizing it, especially while working with files. For instance:

```python
with open('test.txt', 'w') as f:
   f.write('Test')
```

Why do we need a Context Manager in Python anyway?

Managing resources like files, databases, or network connections is very common in programming. Ensuring these resources are appropriately released/closed after usage is *vital* to prevent issues like hanging connections or file access problems.

Context Managers help by:  
1️⃣ Managing resources, ensuring safe usage and disposal.  
2️⃣ Executing clean-up operations, like closing files or connections, even when errors pop up.  
3️⃣ Enhancing code readability and ease of refactoring.

For Data Engineers, why should this matter?

While constructing a data pipeline that involves acquiring and releasing resources (like files or database connections), a context manager ensures proper closure, even after errors.

Wondering how to define a Context Manager?

A class just needs to implement two magical dunder methods: `__enter__()` (which produces the resource) and `__exit__()` (which handles cleanup). See below a simple example illustrating how context managers work behind the scenes.

```python
class ExampleContextManager():

    def __init__(self, host, port):
        print('Initializing Context Manager')
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        print('Setting up the connection')
        self.connection = DatabaseConnection(self.host, self.port)
        return self.connection

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.connection.close()

with ExampleContextManager('example_host', '1000') as manager:
    print('Do something with the connection')
```

![Output: Initializing Context Manager, Setting up the connection, Do something with the connection, Connection closed.](/images/context-managers-in-python/1-output.png)

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Retrying in Python using tenacity](/retrying-in-python-using-tenacity)
- [Using virtual environments in Python](/using-virtual-environments-in-python)
- [Installing Python packages with pip](/installing-python-packages-with-pip)
- [A quick look at the json module in Python](/a-quick-look-at-the-json-module-in-python)
