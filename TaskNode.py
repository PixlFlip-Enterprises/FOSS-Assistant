"""
TaskNode.py Version 0.1.
Author: PixlFlip
Date: Jan 26, 2022

First Version!
"""
# Imports
import time
from datetime import datetime
import MySQLdb
from Functions import Protocols
import Task
# Top Variables
SETTINGS = Protocols.Settings()
SQLDATABASE = SETTINGS.sqlDatabase
SQLUSERNAME = SETTINGS.sqlUsername
SQLPASSWORD = SETTINGS.sqlPassword
currentDirectory = SETTINGS.currentDirectory
# End Condition
should_end = False
# holding date
holding_date = datetime.now().__str__().replace(" ", "")[0:10]

'''
taking a moment to comment here, when the program is first run everything should be done. Then we yield to a while
loop that will tick at 5 min intervals, if something matches a tick then it will execute and move on.
'''
Task.briefing(holding_date, SQLUSERNAME, SQLPASSWORD, SQLDATABASE)

# Start Infinite Loop
while not should_end:
    # Start by getting the date and time of day
    date = datetime.now().__str__().replace(" ", "")[0:10]
    # check if new day
    if not holding_date.__contains__(date):
        # New day from start of operation, so run daily tasks
        print("Daily Task Protocol Initiated")
        Task.briefing(date, SQLUSERNAME, SQLPASSWORD, SQLDATABASE)

    print("Tick Based Tasks Run")
    # 5 min or 300 sec sleep which makes up one "tick"
    time.sleep(300)




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

