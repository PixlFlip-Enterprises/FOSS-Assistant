"""The goal of this file is a one and done setup. No buts, cuts, or coconuts."""
import os
import MySQLdb

currentDirectory = os.getcwd()
# I would like to assume people aren't dumb enough to run this if it isn't their first time, so no check
print("===================== FOSS Assistant Server Setup ======================")
startupParams = []
profileParams = []
# get info from user
startupParams.append(input("= Please Give me a Name: "))
startupParams.append(input("= Enter the full directory path to the folder you keep Music in: "))
startupParams.append(input("= Enter the full directory path to the folder you keep Video in: "))
startupParams.append(input("= Enter name of your instance of FOSS Assistant: "))
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
        f.write(line)

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
    # Create Default User Notes
    cursor.execute("CREATE TABLE " + profileParams[0] + "_NOTES(DATE VARCHAR(50) NOT NULL, TITLE MEDIUMTEXT, BODY MEDIUMTEXT NOT NULL, UUID VARCHAR(50), STARRED VARCHAR(50), CREATIONDEVICE VARCHAR(50), TIMEZONE VARCHAR(50));")
    db.commit()
except:
    # Rollback in case there is any error
    db.rollback()
    print("ERROR. MYSQL DATABASE TABLE CREATION FAILED. I GOT NOTHING FOR YOU IF THE CREATION WORKED WY WOULDNT THIS??")
# disconnect from server
db.close()

# Add user to database
try:
    # open the database
    db = MySQLdb.connect("localhost", startupParams[5], startupParams[6], startupParams[4])
    cursor = db.cursor()
    # Execute the SQL command
    cursor.execute(
        "INSERT INTO PROFILES(USER, PASSWORD, EMAIL, EMAILPASS, DISCORD) VALUES(" + profileParams[0] + ", " + profileParams[1] + "," + profileParams[2] + "," + profileParams[3] + ", " + profileParams[4] + " );")
    # Commit your changes in the database
    db.commit()
except:
    # Rollback in case there is any error
    db.rollback()

    # disconnect from server
db.close()

# Done! Wrap it up and put a pretty bow on it!
print("Setup successful! Your FOSS Assistant instance is ready to go. To run use the Nodes.")
