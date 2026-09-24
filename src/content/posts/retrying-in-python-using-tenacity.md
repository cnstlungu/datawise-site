---
title: "Retrying in Python using tenacity"
seoTitle: "Python Retry Logic with Tenacity"
seoDescription: "Learn how to simplify retry logic in Python using the tenacity package for handling exceptions and implementing back-off strategies"
datePublished: 2024-08-06T20:59:59.462Z
dateUpdated: 2026-03-02T15:57:41.130Z
cover: "/images/retrying-in-python-using-tenacity/cover.jpg"
coverCredit:
  name: "Tomas Martinez"
  url: "https://unsplash.com/@tomasmartinez"
series: "python"
hashnodeCuid: "clziwm4x1000108l9bq2c3r32"
---

*tenacity - (noun) the quality or fact of continuing to exist; persistence.*

If you ever need to retry something that might fail in Python, take a look at a specialized package like tenacity.

It helps you properly cover common scenarios like retrying only a particular type of exception, exponential back-off or even jitter (adding random variance in the retrying cadence so clients don't all retry at the same time).

Otherwise it's important to leverage great packages like these in our workflows and not reinvent the wheel when faced with problems many other people face day to day.

Check out a quick example of it in action below.

```python
import random
from datetime import datetime, timezone
from tenacity import retry, retry_if_exception_type, wait_exponential


@retry(retry=retry_if_exception_type(IOError),
       wait=wait_exponential(multiplier=2, min=4, max=12))
def retrieve_data():
    print(f"{datetime.now(timezone.utc)}: running ...")
    if random.randint(0, 10) > 1:
        print("An error has occurred.")
        raise IOError("Something went wrong.")
    else:
        print("All good!")

retrieve_data()
```

![Terminal output: retrieve\_data runs on 2024-07-27 at 12:42:16, 12:42:20, 12:42:24, 12:42:32, 12:42:44, 12:42:56 and 12:43:08, waiting 4, 4, 8, 12, 12 and 12 seconds; the first six runs print An error has occurred. and the last prints All good!](/images/retrying-in-python-using-tenacity/1-output.jpg)

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using virtual environments in Python](/using-virtual-environments-in-python)
- [Installing Python packages with pip](/installing-python-packages-with-pip)
- [A quick look at the json module in Python](/a-quick-look-at-the-json-module-in-python)
- [Using tempfile module in Python](/using-tempfile-module-in-python)
- [A few thoughts about recent Python integration into Excel](/a-few-thoughts-about-recent-python-integration-into-excel)
