"""The goal of this file is a one and done setup. No buts, cuts, or coconuts."""

import os
import pymysql as MySQLdb

currentDirectory = os.getcwd()
# I would like to assume people aren't dumb enough to run this if it isn't their first time, so no check

# Let's get some decoration and naming!
print(" ________ ________  ________   ________           ________  ________   ________  ___  ________  _________  ________  ________   _________ ")
print("|\  _____\\\   __  \|\   ____\ |\   ____\         |\   __  \|\   ____\ |\   ____\|\  \|\   ____\|\___   ___\\\   __  \|\   ___  \|\___   ___\ ")
print("\ \  \__/\ \  \|\  \ \  \___|_\ \  \___|_        \ \  \|\  \ \  \___|_\ \  \___|\ \  \ \  \___|\|___ \  \_\ \  \|\  \ \  \\\ \  \|___ \  \_| ")
print(" \ \   __\\\ \  \\\\  \ \_____  \\\ \_____  \        \ \   __  \ \_____  \\\ \_____  \ \  \ \_____  \   \ \  \ \ \   __  \ \  \\\ \  \   \ \  \ ")
print("  \ \  \_| \ \  \\\\  \|____|\  \\\|____|\  \        \ \  \ \  \|____|\  \\\|____|\  \ \  \|____|\  \   \ \  \ \ \  \ \  \ \  \\\ \  \   \ \ \ ")
print("   \ \__\   \ \_______\____\_\  \ ____\_\  \        \ \__\ \__\____\_\  \ ____\_\  \ \__\____\_\  \   \ \__\ \ \__\ \__\ \__\\\ \__\   \ \__\ ")
print("    \|__|    \|_______|\_________\\\_________\        \|__|\|__|\_________\\\_________\|__|\_________\   \|__|  \|__|\|__|\|__| \|__|    \|__| ")
print("                      \|_________\|_________|                 \|_________\|_________|   \|_________|                                         ")
# init args
startupParams = []
profileParams = []
# get info from user
startupParams.append(input("= Please Give me a Name: "))
startupParams.append(input("= Enter the full directory path to the folder you keep Music in: "))
startupParams.append(input("= Enter the full directory path to the folder you keep Video in: "))
startupParams.append("fossAssistant")
startupParams.append(input("= Enter mysql Database you want me to use: "))
startupParams.append(input("= Enter mysql username for me to use: "))
startupParams.append(input("= Enter mysql password for me to use: "))
startupParams.append(input("= Enter Discord bot token: "))
startupParams.append(input("= Enter Discord bot prefix: "))
print("=========================================================================")
print("Setup of base functions complete. Enter info for admin profile. ")
profileParams.append(input("= Enter your Username: ").lower().replace(' ', ''))
profileParams.append(input("= Enter your Password: "))
profileParams.append(input("= Enter your Email Address: "))
profileParams.append(input("= Enter your Password for Email Above: "))
profileParams.append(input("= Enter Discord ID (put NONE if no ID): "))

# create startup file
open(currentDirectory + '/Functions/ProgramData/startup.txt', 'x')
with open(currentDirectory + '/Functions/ProgramData/startup.txt', 'w') as f:
    for line in startupParams:
        f.write(line + '\n')

# init database (or try to!)
try:
    # open the database
    db = MySQLdb.connect("localhost", startupParams[5], startupParams[6])
    cursor = db.cursor()
    # Create the database
    cursor.execute("CREATE DATABASE " + startupParams[4] + ";")
except:
    # Rollback in case there is any error
    db.rollback()
    print("ERROR. MYSQL DATABASE INITIATION FAILED. CHECK YOUR USERNAME AND PASSWORD, AND ENSURE MYSQL IS INSTALLED")
# disconnect from server
db.close()

# init all other tables
try:
    # open the database
    db = MySQLdb.connect("localhost", startupParams[5], startupParams[6], startupParams[4])
    cursor = db.cursor()
    # Create Profile Table
    cursor.execute("CREATE TABLE PROFILES(USER VARCHAR(50) NOT NULL, PASSWORD VARCHAR(50) NOT NULL, EMAIL VARCHAR(50), EMAILPASS VARCHAR(50), DISCORD VARCHAR(20));")
    # Create Default User Journal
    cursor.execute("CREATE TABLE " + profileParams[0] + "_JOURNAL(DATE VARCHAR(50) NOT NULL, ENTRY MEDIUMTEXT NOT NULL, UUID VARCHAR(50), STARRED VARCHAR(50), CREATIONDEVICE VARCHAR(50), TIMEZONE VARCHAR(50));")

    # Create Table for saving Daily Briefings. Might be useful someday
    cursor.execute("CREATE TABLE DAILY_BRIEFING(ID INT AUTO_INCREMENT PRIMARY KEY, DATE VARCHAR(50) NOT NULL, NEWS_LINKS MEDIUMTEXT, TECH_LINKS MEDIUMTEXT, TRENDING_SEARCHES MEDIUMTEXT);")

    # \\\\\\\\\\\\\\\\\\\\\\\\\\
    #   Creating Entity Tables
    # //////////////////////////
    # Create Notes Entity Table
    cursor.execute("CREATE TABLE NOTE(ID INT AUTO_INCREMENT PRIMARY KEY, OWNING_USER VARCHAR(200), DATE VARCHAR(50) NOT NULL, TITLE MEDIUMTEXT, BODY MEDIUMTEXT NOT NULL, STARRED VARCHAR(50), CREATION_DEVICE VARCHAR(50), TIMEZONE VARCHAR(50));")
    # Create Contact Entity Table
    cursor.execute("CREATE TABLE CONTACT(ID INT AUTO_INCREMENT PRIMARY KEY, CONTACT_OWNING_USER VARCHAR(200), F_NAME VARCHAR(50) NOT NULL, L_NAME VARCHAR(50) NOT NULL, DISPLAY_NAME VARCHAR(50), NICKNAME VARCHAR(50), EMAIL_ADDRESS VARCHAR(100), EMAIL_ADDRESS2 VARCHAR(100), EMAIL_ADDRESS3 VARCHAR(100), HOME_PHONE VARCHAR(25), BUSINESS_PHONE VARCHAR(25), HOME_FAX VARCHAR(50), BUSINESS_FAX VARCHAR(50), PAGER VARCHAR(100), MOBILE_PHONE VARCHAR(25), HOME_ADDRESS VARCHAR(250), HOME_ADDRESS2 VARCHAR(250), HOME_CITY VARCHAR(250), HOME_STATE VARCHAR(250), HOME_POSTAL_CODE VARCHAR(20), HOME_STREET VARCHAR(250), BUSINESS_ADDRESS VARCHAR(250), BUSINESS_ADDRESS2 VARCHAR(250), BUSINESS_CITY VARCHAR(250), BUSINESS_STATE VARCHAR(150), BUSINESS_POSTAL_CODE VARCHAR(250), BUSINESS_COUNTRY VARCHAR(250), COUNTRY_CODE VARCHAR(250), RELATED_NAMES VARCHAR(250), JOB VARCHAR(250), DEPARTMENT VARCHAR(250), ORGANIZATION VARCHAR(250), NOTES MEDIUMTEXT, BIRTHDAY DATE, ANNIVERSARY DATE, GENDER VARCHAR(1), WEBSITE VARCHAR(250), WEBPAGE2 VARCHAR(250), CATEGORIES MEDIUMTEXT, SOCIOLOGICAL_OPTIONS MEDIUMTEXT, SOCIAL_MEDIA_HANDLE MEDIUMTEXT, DISCORD VARCHAR(100), PERSONALITY_RATING INT, TRUST_SCORE INT);")

    db.commit()
except:
    # Rollback in case there is any error
    db.rollback()
    print("ERROR. MYSQL DATABASE TABLE CREATION FAILED. I GOT NOTHING FOR YOU IF THE CREATION WORKED WY WOULDN'T THIS??")
# disconnect from server
db.close()

# Add user to database
try:
    # open the database
    db = MySQLdb.connect("localhost", startupParams[5], startupParams[6], startupParams[4])
    cursor = db.cursor()
    # Execute the SQL command
    sql = "INSERT INTO PROFILES (USER, PASSWORD, EMAIL, EMAILPASS, DISCORD) VALUES (%s, %s, %s, %s, %s)"
    val = (profileParams[0], profileParams[1], profileParams[2], profileParams[3], profileParams[4])
    cursor.execute(sql, val)

    db.commit()

    print(cursor.rowcount, "record inserted.")
except:
    # Rollback in case there is any error
    db.rollback()
    print("An error occurred and the profile was not saved. Make sure you have ran initial setup.")


# Done! Wrap it up and put a pretty bow on it!
print("Setup successful! Your FOSS Assistant instance is ready to go. To run use the Nodes.")
