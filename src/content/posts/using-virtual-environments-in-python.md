---
title: "Using virtual environments in Python"
seoTitle: "Python Virtual Environments: A Guide"
seoDescription: "Learn how to use Python virtual environments to manage project dependencies effectively and avoid conflicts with this comprehensive guide"
datePublished: 2024-07-28T20:14:25.717Z
dateUpdated: 2026-03-02T15:57:39.506Z
cover: "/images/using-virtual-environments-in-python/cover.jpg"
coverCredit:
  name: "Vedrana Filipović"
  url: "https://unsplash.com/@vedranafilipovic"
series: "python"
hashnodeCuid: "clz600vjp000909l8dbk8e9i2"
---

In my yesterday's post, we looked at the basics of installing packages in Python using pip.

The next immediate step is to learn about virtual environments. When you install packages with pip, they are added to your 'global' library.

However, if you have multiple Python projects on your machine, each with different package requirements and dependencies, managing these packages globally can become a complex task.

A solution to this problem is to use virtual environments. A virtual environment is a lightweight, isolated Python installation specific to each project (read: folder), with its own list of installed packages.

This way, Project A can use version 1.0 of CoolPythonModule while Project B uses version 2.0, without conflicts.

There are multiple tools for managing environments: conda or poetry also do that, but one of the simplest options is venv.

To create a virtual environment, use the following command:

`python3 -m venv .venv`

`# This creates a virtual environment in the '.venv' folder inside the current working directory`

You can now activate the virtual environment:

`source .venv/bin/activate`

The name of the virtual env is displayed next to your user name. You can now install and do everything you need in terms of packages - they will after only this virtual env.

If you'd like to deactivate it, you do:

`deactivate`

Don't know which Python interpreter you're using?

`which python`

This will show you the path of the active interpreter.

P.S. Activate/deactivate scripts can do interesting things like assigning an environment variable upon activation.

![Terminal session in \~/repos/test: source .venv/bin/activate adds a (test) prompt prefix, Python 3.10.12 imports pandas and builds a DataFrame, which python points to /repos/test/.venv/bin/python, and deactivate returns to the normal prompt.](/images/using-virtual-environments-in-python/1.webp)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Retrying in Python using tenacity](/retrying-in-python-using-tenacity)
- [Installing Python packages with pip](/installing-python-packages-with-pip)
- [A quick look at the json module in Python](/a-quick-look-at-the-json-module-in-python)
- [Using tempfile module in Python](/using-tempfile-module-in-python)
- [A few thoughts about recent Python integration into Excel](/a-few-thoughts-about-recent-python-integration-into-excel)
