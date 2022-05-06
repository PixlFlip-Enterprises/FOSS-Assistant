"""
Task.py Version 0.2.
Author: PixlFlip
Date: May 5, 2022

All TaskNode operations are methods here
"""
# NOTE: must use pip3 import newspaper3k for it to import correctly
import newspaper
from newspaper import Article
from datetime import datetime
import pymysql as MySQLdb
import os
from API_Server.Functions import Protocols

# Briefing Task
def briefing(date, usr, pwd, db):
    # first check for entry to prevent duplicates
    try:
        # open the database
        db = MySQLdb.connect("localhost", usr, pwd, db)
        cursor = db.cursor()
        # execute the SQL command
        cursor.execute("SELECT * FROM DAILY_BRIEFING WHERE REGEXP_INSTR(date,'" + date + "');")
        # fetch search results
        records = cursor.fetchall()
        # return based on result
        if not records == None:
            # duplicate found
            return

    except:
        # Rollback in case there is any error
        db.rollback()
    # disconnect from server
    db.close()

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
    # Record Briefing to Database
    try:
        # open the database
        db = MySQLdb.connect("localhost", usr, pwd, db)
        cursor = db.cursor()
        # Execute the SQL command
        sql = "INSERT INTO DAILY_BRIEFING (DATE, NEWS_LINKS, TECH_LINKS, TRENDING_SEARCHES) VALUES(%s, %s, %s, %s)"
        val = (date, news_article_urls.__str__(), tech_article_urls.__str__(), google_trending_searches.__str__())
        cursor.execute(sql, val)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    # disconnect from server
    db.close()

# Automatic Backup Task
def full_backup(date, usr, pwd, db):
    # easy as 3.14159265358979323...
    os.system('mysqldump -h localhost -u ' + usr + ' -p ' + pwd + ' ' + db + ' > ' + date + '.sql')

