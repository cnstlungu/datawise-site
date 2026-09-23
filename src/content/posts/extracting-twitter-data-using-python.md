---
title: "Extracting Twitter data using Python"
seoTitle: "Extracting Twitter Data using Python"
seoDescription: "Pull tweets with Python: set up Twitter developer credentials, search tweets with the TwitterSearch package and flatten the JSON into a pandas DataFrame."
datePublished: 2019-08-19T21:17:27.284Z
dateUpdated: 2026-03-02T10:51:33.587Z
cover: "/images/extracting-twitter-data-using-python/cover.jpg"
coverCredit:
  name: "Markus Spiske"
  url: "https://unsplash.com/@markusspiske"
series: "python"
hashnodeCuid: "clfn50hh2000809mg50geg9hh"
---

Twitter is currently one of the most widely used social networks — 330 million people were using it monthly in Q1 2019. It may not have the explosive growth it had a couple of years ago, but it’s certainly a place where businesses and public persons engage with their audiences, important messages are shared in near-real time and, as recent events show, even politics is done.

Businesses and other actors have long understood the power that data from Twitter has. A typical example we could think of is trading firms. Given the fast-paced and concise format of messages shared, it is a nice tool that could be used to gather signals that could impact the stock market. A CEO commending a product or service? A partnership could be in the making. Multiple complaints from users about building issues in a new device? Bad news for the hardware vendor. So Twitter data does have a business use case.

In this three-part series, we’ll look into a Proof of Concept for extracting, transforming and understanding Twitter data relevant to a specific topic.

If you wish to follow along, please refer to the GitHub repository containing the full [Jupyter notebook for this series](https://github.com/cnstlungu/incubator/tree/master/Python/Exploring%20Twitter%20Data%20using%20Python).

### Setup

We’re going to use Python 3.7 and a few specialized libraries to get this done.

But first, we’ll need to obtain the necessary credentials from Twitter. This is done [here](https://developer.twitter.com/en/apps). After filling in the appropriate information, we should have the following:

![Twitter developer portal Keys and tokens tab for an app, showing Consumer API keys (API key, API secret key) and an access token and secret with Read-only access level, all values scribbled out in red, with Regenerate and Revoke buttons.](/images/extracting-twitter-data-using-python/1.png)

Once we have the *API key*, *API secret key*, *Access token* and *Access token secret*, we can process to extract data from Twitter. We’re going to use the Twitter Search API to get our data.

Before we proceed, there’s another thing we should bear in mind though. This is an interface offered by Twitter that has [multiple tiers](https://web.archive.org/web/20190820135527/https://developer.twitter.com/en/docs/tweets/search/overview), including the (free) Standard one we’re going to use. Its limitations are, as of writing this article, described as follows:

> This search API searches against a sampling of recent Tweets published in the past 7 days. Part of the ‘public’ set of APIs.

Nevertheless, this should be enough for our purposes.

### Getting Twitter data

Moving forward, we could either decide between making the API calls directly or using a library that will do so for us. Given the vast choice the Python ecosystem gives us, we’re going to use [TwitterSearch](https://pypi.org/project/TwitterSearch/), which should help us get moving quicker.

After installing TwitterSearch, we’re ready to go.

```bash
pip install TwitterSearch
```

Let’s import the necessary objects and instantiate the TwitterSearch object using the credentials Twitter has set up for us. In this case, I’ve set up a file that will store them.

We’ll now need to create a Search Order against the Search object we’ve defined above.

In this case, we’ve decided to analyze the messages concerning UK’s upcoming exit from the European Union, colloquially known as Brexit. We’re going to analyze tweets in English.

Now we have a list of tweets, which look like the one below.

![Jupyter output of the first element of results: one tweet as a nested Python dictionary with keys such as created\_at, id, id\_str, text (a retweet of @PaulBrandITV about a No Deal Brexit), truncated, metadata, source and a nested user dictionary.](/images/extracting-twitter-data-using-python/2.png)

We could see that we have a nested dictionary-like structure containing other dictionaries and lists. This needs to be flattened out so we could analyze data more efficiently. The [pandas](https://pandas.pydata.org/) library will facilitate this.

Here we’ve imported pandas and used the *json\_normalize* method to transform our list of results into a pandas *DataFrame — a two-dimensional tabular data structure.*

Also, here’s a quick view of our data:

![Jupyter output of df.head() on the flattened tweets DataFrame: 5 rows by 307 columns, including contributors, coordinates, created\_at, favorite\_count, favorited, geo, id, id\_str and in\_reply\_to\_screen\_name.](/images/extracting-twitter-data-using-python/3.png)

To give a more meaningful identifier to each row than the currently used automatically generated row number, we’re going to use the unique tweet id column. We’re also going to drop the *id\_str* column since it’s the string representation of the same tweet id and is thus redundant.

Also, let’s look at how much data we’ve got. This will return (no\_of\_rows (tweets), no\_of\_columns (features/variables) ). So we’re currently looking at 18000 tweets with 326 attributes we could analyze.

![Python pandas df.shape output in Jupyter for the flattened tweets DataFrame: (18000, 326), meaning 18,000 tweets as rows and 326 attributes as columns.](/images/extracting-twitter-data-using-python/4.png)

A view of a subset of columns would be useful here. Let’s look at the date the tweet was created, the user screen name and the text of the tweet. These are only 3 of the several hundred columns available.

![Python pandas df.columns output: an Index of flattened tweet fields such as coordinates.coordinates, created\_at, favorite\_count, geo.type, user.screen\_name, user.statuses\_count and withheld\_in\_countries, abbreviated, with dtype object and length 328.](/images/extracting-twitter-data-using-python/5.png)

![Python pandas selecting the created\_at, user.screen\_name and text columns with head(): five tweets indexed by id, all created Mon Aug 19 2019 around 19:45 UTC, with screen names and truncated retweet texts about Brexit.](/images/extracting-twitter-data-using-python/6.png)

#### Wrapping up

In this first post of the series we’ve looked at setting up our Twitter developer credentials, used the *TwitterSearch* Python package to extract tweets about Brexit and also used the *pandas* library to flatten (unpack) our results.

In the upcoming articles in this series, we’ll do further transformations of the data we’ve extracted and touch on the notions of Natural Language Processing and Sentiment Analysis.

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
