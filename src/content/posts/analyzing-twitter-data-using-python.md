---
title: "Analyzing Twitter data using Python"
seoTitle: "Explore Twitter Data Using Python"
seoDescription: "Learn to explore Twitter Data Using Python tools including nltk, matplotlib and pandas"
datePublished: 2019-10-05T10:18:50.023Z
dateUpdated: 2026-03-02T10:51:53.597Z
cover: "/images/analyzing-twitter-data-using-python/cover.jpg"
coverCredit:
  name: "Pascal Müller"
  url: "https://unsplash.com/@millerthachiller"
series: "python"
hashnodeCuid: "clfn4d89s000509mbb86a1ztl"
---

[Previously in this series](/intro-nlp-sentiment-analysis-python), we’ve focused on processing the obtained data and extracting features. We’ve also briefly touched on topics related to Natural Language Processing and tried to derive sentiments from tweets.

We’re now going to look at ways to analyze and present the data we’ve extracted. This post will conclude our series regarding Twitter data exploration using Python.

### Geo-locating tweets using location

The first interesting way to look at tweets is to better understand the audience that produced them. One step in that direction is to identify what places where they originate from. Now, one of the columns from the dataset we can use is the user’s declared location. Let’s review what it contains.

We’re looking at the 50 most common declared user locations for our dataset. It needs a little mapping exercise first.

```python
locs = df['user.location'].value_counts()
locs[locs>=10]
```

![Output: user locations with at least 10 tweets, led by London 198, London, England 187, United Kingdom 184, England, United Kingdom 173 and UK 145, with many variants of the same places further down, ending with Leeds 10.](/images/analyzing-twitter-data-using-python/1-output.png)

*Locations occurring at least 10 times in our dataset*

We’re going to map these entries so we can group similar entries.

```python
mapping = {'London' : 'London, UK',
 'London, England': 'London, UK'  ,
 'United Kingdom' : 'United Kingdom',
 'England, United Kingdom': 'England' ,
 'UK': 'United Kingdom',
 'England': 'England',
 'Europe' : 'Europe' ,
 'South East, England': 'South East England',
 'Scotland, United Kingdom' : 'Scotland',
 'Scotland': 'Scotland',
 'Ireland' : 'Ireland',
 'North West, England' : 'North West England',
 'London, UK': 'London, UK',
 'Manchester, England': 'Manchester, UK',
 'European Union': 'European Union',
 'North East, England': 'North East England',
 'Glasgow, Scotland': 'Glasgow, UK',
 'London ': 'London',
 'European Union 🇪🇺' : 'European Union',
 'Wales, United Kingdom': 'Wales',
 'Rutland': 'Rutland, UK',
```

The mapping dictionary that we created

We’re going to replace locations with the mapped entries:

```python
df['user.location'] =  df['user.location'].apply(lambda x: mapping[x] if x in mapping.keys() else x )
```

Here’s how the locations will look now.

```python
locs = df['user.location'].value_counts()
locs = locs[locs >= 10]
```

```python
locs
```

![Output: locations after the mapping, led by London, UK 465, United Kingdom 329, England 246, Scotland 67 and Europe 40, down to Spain 10.](/images/analyzing-twitter-data-using-python/3-output.png)

*Locations after processing*

Here’s where the *Geolocator* comes in. *Geolocator*? Yes. That’s the tool that given a location (be it the full address or just the city name) can identify a real-world location and provide some extra details such as latitude and longitude, which we’ll need for our later mapping exercise. We’re going to use the Nominatim package which will allow us to get the coordinates of the above cities.

```python
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='twitter-analysis-cl')
#note that user_agent is a random name
locs = list(locs.index) #keep only the city names
```

We’re going to use the geolocate function to return the location of each of the provided place.

```python
geolocated = list(map(lambda x: [x,geolocator.geocode(x)[1] if geolocator.geocode(x) else None],locs))
geolocated = pd.DataFrame(geolocated)
geolocated.columns = ['locat','latlong']
geolocated['lat'] = geolocated.latlong.apply(lambda x: x[0])
geolocated['lon'] = geolocated.latlong.apply(lambda x: x[1])
geolocated.drop('latlong',axis=1, inplace=True)
```

Here’s what the output looks like. We’ll use it as a lookup table.

![Jupyter output of a pandas DataFrame used as a lookup table, with columns locat, lat and lon holding geocoded coordinates for 20 locations, e.g. London, UK at 51.489334, -0.144055 and Europe at 51.0, 10.0.](/images/analyzing-twitter-data-using-python/4.png)

### Plotting on a map

Given we now have a lookup table to use for looking up locations and their coordinates, let’s join it with our data. Let’s also group by location and obtain the count occurrences once again.

```python
mapdata = pd.merge(df,geolocated, how='inner', left_on='user.location', right_on='locat')locations = mapdata.groupby(by=['locat','lat','lon'])\
       .count()['created_at']\
       .sort_values(ascending=False)
```

```python
locations.head(10)
```

![Output: the first 10 tweet counts by locat, lat and lon: London, UK (51.489334, -0.144055) 465, United Kingdom 329, England 246, Scotland 67, South East England 38, North West England 32, Ireland 31, Glasgow, UK 30, Wales 29 and Manchester, UK 28.](/images/analyzing-twitter-data-using-python/5-output.png)

Time for a map. We’ll use [Matplotlib](https://matplotlib.org/) and [Cartopy](https://scitools.org.uk/cartopy/docs/v0.16/) to display our data. In this simple example, we’re going to plot individual locations (can be seen as red dots on the map), as well as blue circles whose radius varies by how many tweets came from that particular place.

We’ve also set a helper function to compute how big the circle should be — the idea is to have the size of the circle increase much slower than the number it wants to represent, otherwise the smaller entries won’t be visible at all.

First, set up general settings for Matplotlib.

```python
import matplotlib.pyplot as pltplt.style.use('fivethirtyeight')
plt.rcParams.update({'font.size': 20})
plt.rcParams['figure.figsize'] = (20, 10)
```

Now, generate the map.

```python
import cartopy.crs as ccrs
from matplotlib.patches import Circleax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()# plot individual locations                                                                                                       
ax.plot(mapdata.lon, mapdata.lat, 'ro', transform=ccrs.PlateCarree())# add coastlines for reference                                                                                                
ax.coastlines(resolution='50m')
ax.set_global()
ax.set_extent([20, -20, 45,60])def get_radius(freq):
    if freq < 50:
        return 0.5
    elif freq < 200:
        return 1.2
    elif freq < 1000:
        return 1.8# plot count of tweets per location
for i,x in locations.iteritems():
    ax.add_patch(Circle(xy=[i[2], i[1]], radius=get_radius(x), color='blue', alpha=0.6, transform=ccrs.PlateCarree()))
plt.show()
```

![Map of north-western Europe drawn with Matplotlib and Cartopy: red dots mark geocoded tweet locations and blue circles sized by tweet count, clustered heavily over England, especially London, with a few over Scotland, Wales, Ireland and France.](/images/analyzing-twitter-data-using-python/6.png)

*The output of our code. Brexit is a very UK-centered issue.*

### Further analysis using charts

Let’s continue exploring our data using the power of [Matplotlib](https://matplotlib.org/). Remember the sentiment score we computed? Let’s plot it.

![Matplotlib histogram of tweet sentiment\_score values ranging roughly from -1.6 to 1.8; the tallest bin, about 3,200 tweets, sits just below zero, followed by about 1,550 just above zero and about 950 between -1 and -0.5.](/images/analyzing-twitter-data-using-python/7.png)

*The sentiment in the tweets we’re looking at is skewed towards negative*

Let’s say we want to display this in a friendlier way. We’ll now transform it into a categorical variable. This will cut our data into four bins of data, with more friendly values (being levels of a categorical variable).

```python
sent_clasification = pd.cut(df['sentiment_score'],\
          [-3,-1.2, 0, 1.2 , 3],\
          right=True,\
          include_lowest=True,\
          labels=['strongly negative', 'negative', 'positive', 'strongly positive'])
```

```python
sent_clasification.value_counts()
```

![Output: negative 3958, positive 2250, strongly negative 105 and strongly positive 75 (Name: sentiment\_score, dtype: int64).](/images/analyzing-twitter-data-using-python/8-output.png)

Results

![Matplotlib bar chart of tweet counts per sentiment category: negative about 3,950, positive about 2,250, and strongly negative and strongly positive both around 100 or fewer.](/images/analyzing-twitter-data-using-python/9.png)

*Let’s try plotting them one more time — same information but from a different perspective.*

Another way to look at this data is one of the most recognizable (and hated) ways to represent data: pie charts. Not a big fan of it myself, but let’s give it a try.

```python
plt.figure(figsize=(10,7)) #make it smaller this time
sent_clasification.value_counts().plot(kind='pie')
plt.grid(False)
plt.tight_layout()
```

![Matplotlib pie chart of the sentiment\_score categories: negative takes roughly 60 percent, positive about a third, and strongly negative and strongly positive are thin slivers.](/images/analyzing-twitter-data-using-python/10.png)

#### Word Cloud

What about a word cloud? Can it depict the chaos of Brexit in a single image?

```python
from wordcloud import WordCloud, STOPWORDS
bigstring = df['processed_text'].apply(lambda x: ' '.join(x)).str.cat(sep=' ')plt.figure(figsize=(12,12))
wordcloud = WordCloud(stopwords=STOPWORDS,
                          background_color='white',
                          collocations=False,
                          width=1200,
                          height=1000
                         ).generate(bigstring)
plt.axis('off')
plt.imshow(wordcloud)
```

![Word cloud of processed Brexit tweet text, dominated by brexit, deal, johnson, boris, parliament, eu, uk, people, say and stop, with smaller words such as corbyn, labour, vote, trump, government and british.](/images/analyzing-twitter-data-using-python/11.png)

*The output of our Word Cloud efforts*

#### Hash Tags

Interested in the Top 10 hashtags? We’re going to use regular expressions to extract them and then count occurrences.

```python
import re
hashtags = df['text'].apply(lambda x: pd.value_counts(re.findall('(#\w+)', x.lower() )))\
                     .sum(axis=0)\
                     .to_frame()
                     .reset_index()\
                     .sort_values(by=0,ascending=False)
hashtags.columns = ['hashtag','occurences']
```

```python
hashtags.head(10)
```

![Output: the top 10 hashtags with their counts (occurences column): #brexit 639.0, #blockthecoup 84.0, #eu 64.0, #revokea50 54.0, #stopbrexit 40.0, #liarjohnson 35.0, #peoplesvote 32.0, #borisjohnson 30.0, #fbpe 26.0 and #nodeal 24.0.](/images/analyzing-twitter-data-using-python/12-output.png)

```python
hashtags[:10].plot(kind='bar',y='occurences',x='hashtag')
plt.tight_layout()
plt.grid(False)
plt.suptitle('Top 10 Hashtags for keyword: Brexit, language: English', fontsize=14)
```

![Matplotlib bar chart titled Top 10 Hashtags for keyword: BREXIT, locale: EN, where #brexit at about 640 occurrences dwarfs #blockthecoup, #eu, #revokea50, #stopbrexit and the rest, all under 100.](/images/analyzing-twitter-data-using-python/13.png)

#### Users Mentioned

Let’s do the same for users mentioned in tweets. They’re easy to be spotted by the @ sign.

```python
plt.grid(False)
plt.tight_layout()
plt.suptitle('Top 10 Users for keyword: BREXIT, locale: EN', fontsize=14)df['text'].str\
          .findall('(@[A-Za-z0-9]+)')\
          .apply(lambda x: pd.value_counts(x))\
          .sum(axis=0)\
          .sort_values(ascending=False)[:10]\
          .plot(kind='bar')
```

![Matplotlib bar chart titled Top 10 Users for keyword: BREXIT, locale: EN: @BorisJohnson is mentioned about 315 times and @joswinson about 190, followed by @Femi, @jeremycorbyn, @Doozy, @Peston, @SkyNews, @PaulBrandITV, @DavidLammy and @brexit, each under 80.](/images/analyzing-twitter-data-using-python/14.png)

No surprises here really

#### Top Words

Let’s now look at the top 10 most used words. The order of action is as follows:

* drop rows with no data
    
* use regular expressions to extract words
    
* count word usage and sum them app
    
* sort
    

```python
import re
words = df['processed_text'].dropna()\
                            .apply(lambda y: pd.value_counts(re.findall('([\s]\w+[\s])',' '.join(y))))\
                            .sum(axis=0)\
                            .to_frame()\
                            .reset_index()\
                            .sort_values(by=0,ascending=False)
words.columns = ['word','occurences']
```

```python
words.head(10)
```

![Output: the top 10 words with their counts (occurences column): brexit 1490.0, deal 483.0, johnson 354.0, eu 272.0, uk 186.0, boris 184.0, get 166.0, people 154.0, mps 138.0 and would 133.0.](/images/analyzing-twitter-data-using-python/15-output.png)

![Matplotlib bar chart titled Top 10 Words for keyword: BREXIT, locale: EN: brexit leads with about 1,490 occurrences, then deal about 480, johnson 350 and eu 270, with uk, boris, get, people, mps and would between roughly 130 and 190.](/images/analyzing-twitter-data-using-python/16.png)

*Top 10 words used*

#### Bigrams

Another thing we should look at are bigrams — a sequence of two words, commonly found together. There’s also trigrams (for three-word sequences) if you’re asking.

```python
from nltk import bigrams
bigramseries = pd.Series([word for sublist in df['processed_text'].dropna()\
                    .apply(lambda x: [i for i in bigrams(x)])\
                    .tolist() for word in sublist])\
                    .value_counts()
```

```python
bigrams.head(10)
```

![Output: the 10 most common bigrams: (deal, brexit) 532, (boris, johnson) 364, (brexit, deal) 102, (abuse, power) 96, (gravest, abuse) 96, (shutting, parliament) 94, (stop, brexit) 91, (brexit, party) 86, (living, memory) 86 and (power, living) 80.](/images/analyzing-twitter-data-using-python/17-output.png)

```python
plt.suptitle('Top 10 Bigrams for keyword: BREXIT, locale: EN', fontsize=18)
bigramseries[:10].plot(kind='bar')
```

![Matplotlib bar chart titled Top 10 Bigrams for keyword: BREXIT, locale: EN: (deal, brexit) at about 530 and (boris, johnson) at about 365 far exceed the rest, such as (brexit, deal), (abuse, power) and (shutting, parliament), all between 80 and 100.](/images/analyzing-twitter-data-using-python/18.png)

### Conclusion

This post concludes our series about exploring Twitter data with Python. While it wasn’t supposed to be an exhaustive list of what you can do with it, it was meant to give the reader a glimpse into the sheer possibilities the Python toolkit gives about extracting, processing and presenting data. It’s straightforward, well-documented and downright fun. The full Jupyter Notebook for this series is available [here](https://github.com/cnstlungu/incubator/tree/master/Python/Exploring%20Twitter%20Data%20using%20Python).

Thank you for reading and feel free to share some examples of your own.

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
