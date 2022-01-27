"""
SensoryNode.py Version 0.1.
Author: PixlFlip
Date: Jan 26, 2022

First Version! Featuring absolutely nothing
noteworthy or interesting. In fact why am
I taking the time to write this???
"""
# import Adafruit_DHT
# sensor = Adafruit_DHT.DHT22
# pin = 4
# while True:
#      humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
#      print("Temperature")
#      print(temperature)
#      print("Humidity")
#      print(humidity)


"""Everything in this file is based on timing or preforming an action after or on a specific date/time"""
import pandas as pd
import numpy
from pytrends.request import TrendReq
# NOTE: must use pip3 import newspaper3k for it to import correctly
import newspaper
from newspaper import Article

# # Daily Briefing Builder
# # setup object
# pytrend = TrendReq()
# # Get Google Hot Trends data
# df = pytrend.trending_searches(pn='united_states')
# # turn that into array
# temp_trending = df.values
# # format array into string so we can actually use it
# google_trending_searches = []
# for trend in temp_trending:
#     google_trending_searches.append(trend.__str__().replace("'", "").replace("[", "").replace("]", ""))
#     print(trend.__str__().replace("'", "").replace("[", "").replace("]", ""))
# # Google Trend Data Retrieved

site = newspaper.build("https://news.ycombinator.com/news", memoize_articles=False)
# site = newspaper.build("https://www.wnd.com/", memoize_articles=False)
# get list of article URLs
article_urls = site.article_urls()
top_articles = []
# sort data into array
for index in range(10):
    article = site.articles[index]
    article.download()
    article.parse()
    top_articles.append(article)
    print(article_urls[index])
# Get Trending Searches
print(newspaper.hot())
