---
title: "Using tempfile module in Python"
seoTitle: "Python Tempfile Module Guide"
seoDescription: "Use Python's tempfile module for creating and managing temporary files and directories with context managers for automatic cleanup"
datePublished: 2024-08-08T09:00:06.614Z
dateUpdated: 2026-03-02T10:51:10.743Z
cover: "/images/using-tempfile-module-in-python/cover.jpg"
coverCredit:
  name: "Khadeeja Yasser"
  url: "https://unsplash.com/@k_yasser"
series: "python"
hashnodeCuid: "clzl1s2fq000709joel2983p5"
---

In this world, everything is ephemeral. If you need to create temporary files or directories in Python, check out the **tempfile** module.

Whether you want to store intermediate results, manage temp data during execution or just test things out, it can help you by abstracting file creation and cleaning-up operations.

In the a quick walk-through below, we're looking at the following functions:  
\- TemporaryFile : creates an anonymous temporary file  
\- NameTemporaryFile: creates a named temp file which we can use in multiple contexts  
\- TemporaryDirectory: creates a temporary directory (in which we also can create temp files).

Notice how we're using the inside context managers (the 'with' block , check out the comments for a quick intro on them). This means the file will be automatically cleaned up upon exiting (default behavior), unless we specify delete=False at creation.

```python
import tempfile
import os

with tempfile.NamedTemporaryFile(mode='w+t') as temp_file:
    temp_file.write('Hello world!')
    print(f"Temporary file created at {temp_file.name}")
# Temporary file created at /var/folders/0_/00hs4my104l9tl0x2y386b3c0000gn/T/tmp8nqm3qa1


with tempfile.TemporaryFile(mode='w+t') as temp_file:
    temp_file.write('Hello world!')
    temp_file.seek(0)
    content = temp_file.read()
    print(f'Content of the file: {content}')
# Content of the file: Hello world!


with tempfile.TemporaryDirectory() as temp_dir:
    print(f"Temporary directory created at: {temp_dir}")
    temp_file_path = os.path.join(temp_dir, 'tempfile.txt')
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write("Hello, World!")
        print(temp_file.name)
        print(f"Temporary file created at {temp_file.name}")
# Temporary directory created at: /var/folders/0_/00hs4my104l9tl0x2y386b3c0000gn/T/tmp4yh5u33m
# Temporary file created at /var/folders/0_/00hs4my104l9tl0x2y386b3c0000gn/T/tmprgxjwmsj/tempfile.txt
```

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Retrying in Python using tenacity](/retrying-in-python-using-tenacity)
- [Using virtual environments in Python](/using-virtual-environments-in-python)
- [Installing Python packages with pip](/installing-python-packages-with-pip)
- [A quick look at the json module in Python](/a-quick-look-at-the-json-module-in-python)
