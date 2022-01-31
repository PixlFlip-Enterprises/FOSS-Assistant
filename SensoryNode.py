"""
SensoryNode.py Version 0.1.
Author: PixlFlip
Date: Jan 26, 2022

First Version! Featuring absolutely nothing
noteworthy or interesting. In fact why am
I taking the time to write this???
"""
# Imports
# NOTE: must use pip3 import newspaper3k for it to import correctly
import newspaper
from newspaper import Article
import datetime
# End Condition
should_end = False
# Start Infinite Loop
while should_end:
    # Start by getting the date and time of day
    raw_date = datetime.now()
    # Format date and time
    date = raw_date.__str__().replace(" ", "")
    # Now have independent if statements check date time and preform actions accordingly

# # Daily Briefing Builder
# Get Tech News
tech_site = newspaper.build("https://news.ycombinator.com/news", memoize_articles=False)
tech_article_urls = tech_site.article_urls()
# Get World News
news_site = newspaper.build("https://www.wnd.com/", memoize_articles=False)
news_article_urls = news_site.article_urls()
# Get Trending Searches
google_trending_searches = newspaper.hot()
# Add it all to a single string
newsletter = "Good Morning!\nHere's what you need to know today.\nTop Tech News: \n" + tech_article_urls[0] + "\n" + tech_article_urls[1] + "\n" + tech_article_urls[2] + "\n" + tech_article_urls[3] + "\n" + tech_article_urls[4] + "\nTop World News: \n" + news_article_urls[0] + "\n" + news_article_urls[1] + "\n" + news_article_urls[2] + "\n" + news_article_urls[3] + "\n" + news_article_urls[4] + "\nTrending Searches: \n" + google_trending_searches[0] + "\n" + google_trending_searches[1] + "\n" + google_trending_searches[2] + "\n" + google_trending_searches[3] + "\n" + google_trending_searches[4] + "\nThat is the daily briefing for today <name here>."
print(newsletter)










# Shelved Ideas in comments for a later date
# import Adafruit_DHT
# sensor = Adafruit_DHT.DHT22
# pin = 4
# while True:
#      humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
#      print("Temperature")
#      print(temperature)
#      print("Humidity")
#      print(humidity)

# top_articles = []
# sort data into array
# for index in range(10):
#     article = tech_site.articles[index]
#     article.download()
#     article.parse()
#     top_articles.append(article)
#     print(tech_article_urls[index])

