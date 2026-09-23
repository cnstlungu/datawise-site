---
title: "Installing Python packages with pip"
seoTitle: "pip Install Guide: Packages, Environments, and Options"
seoDescription: "Learn how to install Python packages with pip, use requirements files, install from GitHub, and upgrade or uninstall packages."
datePublished: 2024-07-27T20:56:09.872Z
dateUpdated: 2026-03-02T10:52:28.498Z
cover: "/images/installing-python-packages-with-pip/cover.jpg"
coverCredit:
  name: "Evan Krause"
  url: "https://unsplash.com/@evankrause_"
series: "python"
hashnodeCuid: "clz4m2p3j000209la91vzgrs6"
---

Here are the basics you need to know about installing Python packages.

Apart from the built-in modules that come by default with the Python installation (the Standard Library), you need to install third-packages packages to be able to use them in your code (and of course import them).

You do so with a package manager. Perhaps the most widely known is **pip**, but there are other options like **poetry** or **uv**.

You can check more information about Python packages at [pypi.org](https://pypi.org)

Here's a quick list of common use cases:

`➡ pip install pandas # installs the package and its dependencies`

`➡ pip uninstall pandas # removes the package`

`➡ pip install --upgrade pandas # upgrades a package`

`➡ pip list # lists installed packages`

`➡ pip freeze > requirements.txt # saves the list of installed packages to a file so you can recreate the environment with the same packages next time you need it`

![VS Code with program.py (import pandas as pd, build a DataFrame from a list of dicts, df.head()) and a requirements.txt pinning numpy==2.0.0, pandas==2.2.2, python-dateutil, pytz, six and tzdata; the terminal shows source .venv/bin/activate and deactivate.](/images/installing-python-packages-with-pip/1.jpg)

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Retrying in Python using tenacity](/retrying-in-python-using-tenacity)
- [Using virtual environments in Python](/using-virtual-environments-in-python)
- [A quick look at the json module in Python](/a-quick-look-at-the-json-module-in-python)
- [Using tempfile module in Python](/using-tempfile-module-in-python)
