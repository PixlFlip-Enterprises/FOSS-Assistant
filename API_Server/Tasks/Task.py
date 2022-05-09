"""
Task.py Version 0.2.
Author: PixlFlip
Date: May 5, 2022

All TaskNode operations are methods here
"""
import newspaper
from newspaper import Article
from datetime import datetime
import pymysql
import os
import csv

# Briefing Task
def briefing(date, usr, pwd, db):
    # first check for entry to prevent duplicates
    try:
        # open the database
        db = pymysql.connect(host="localhost", user=usr, password=pwd, database=db)
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
        db = pymysql.connect(host="localhost", user=usr, password=pwd, database=db)
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
def full_backup(usr, pwd, db, currentDirectory):
    # easy as 3.14159265358979323...

    # File path and name.
    filePath = currentDirectory
    fileName = '_JOURNAL.csv'

    # Database connection variable.
    connect = None

    # Check if the file path exists.
    if os.path.exists(filePath):

        try:

            # Connect to database.
            connect = pymysql.connect(host="localhost", user=usr, password=pwd, database=db)

        except pymysql.DatabaseError as e:

            # Confirm unsuccessful connection and stop program execution.
            print("Database connection unsuccessful.")
            quit()

        # Cursor to execute query.
        cursor = connect.cursor()

        # TODO this is hard coded to my journal since I dont want to lose it again. This will need to be fixed though
        # SQL to select data from the person table.
        sqlSelect = \
            "SELECT * FROM pixl_JOURNAL"

        try:

            # Execute query.
            cursor.execute(sqlSelect)

            # Fetch the data returned.
            results = cursor.fetchall()

            # Extract the table headers.
            headers = [i[0] for i in cursor.description]

            # Add the table headers to the data returned.
            results = (tuple(headers),) + results

            # Open CSV file for writing.
            csvFile = csv.writer(open(filePath + fileName, 'w', newline=''),
                                 delimiter=',', lineterminator='\r\n',
                                 quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the headers and data to the CSV file.
            csvFile.writerows(results)

            # Message stating export successful.
            print("Data export successful.")

        except pymysql.DatabaseError as e:

            # Message stating export unsuccessful.
            print("Data export unsuccessful.")
            quit()

        finally:

            # Close database connection.
            connect.close()

    else:

        # Message stating file path does not exist.
        print("File path does not exist.")

    # DAILY BREIFING BACKUP
    filePath = currentDirectory
    fileName = '_DAILYBRIEFING.csv'

    # Database connection variable.
    connect = None

    # Check if the file path exists.
    if os.path.exists(filePath):

        try:

            # Connect to database.
            connect = pymysql.connect(host="localhost", user=usr, password=pwd, database=db)

        except pymysql.DatabaseError as e:

            # Confirm unsuccessful connection and stop program execution.
            print("Database connection unsuccessful.")
            quit()

        # Cursor to execute query.
        cursor = connect.cursor()

        # SQL to select data from the person table.
        sqlSelect = \
            "SELECT * FROM DAILY_BRIEFING"

        try:

            # Execute query.
            cursor.execute(sqlSelect)

            # Fetch the data returned.
            results = cursor.fetchall()

            # Extract the table headers.
            headers = [i[0] for i in cursor.description]

            # Add the table headers to the data returned.
            results = (tuple(headers),) + results

            # Open CSV file for writing.
            csvFile = csv.writer(open(filePath + fileName, 'w', newline=''),
                                 delimiter=',', lineterminator='\r\n',
                                 quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the headers and data to the CSV file.
            csvFile.writerows(results)

            # Message stating export successful.
            print("Data export successful.")

        except pymysql.DatabaseError as e:

            # Message stating export unsuccessful.
            print("Data export unsuccessful.")
            quit()

        finally:

            # Close database connection.
            connect.close()

    else:

        # Message stating file path does not exist.
        print("File path does not exist.")

