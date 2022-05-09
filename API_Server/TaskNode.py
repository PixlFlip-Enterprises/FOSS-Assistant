"""
TaskNode.py Version 0.1.2
Author: PixlFlip
Date: Jan 26, 2022

Now with actual backups
"""
# Imports
import time
from datetime import datetime
from Functions import Protocols
from Tasks import Task

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
        print("Daily Task Protocols Initiated")
        print("Task: compile briefing")
        Task.briefing(date, SQLUSERNAME, SQLPASSWORD, SQLDATABASE)              # compile briefing
        print("Task: full database backup")
        Task.full_backup(SQLUSERNAME, SQLPASSWORD, SQLDATABASE, currentDirectory)           # backup database
        print("Daily Tasks Complete.")
        # reset our base date and move on
        holding_date = date

    print("Tick Based Tasks Run")
    # 5 min or 300 sec sleep which makes up one "tick"
    time.sleep(300)

