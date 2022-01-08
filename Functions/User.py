# profile file syntax:
# contact ID (for retrieval in Contact.csv)
# password for ID
# primary email
# email password
# discord ID
# Sequence of events on startup coded as three char IDs. Example: SLK (sherlock username), RIC (rickroll),
# DTE (date and time), etc.

# TODO restructure this to accomodate tons of new fields, settings for users, and make it easier to get info from (no more stupid array returns and knowing the spot to call)
import os
import MySQLdb

from Functions import Protocols, UserData

directory = os.getcwd() + '/Data/profiles.csv'
# All key (read top level) variables here
SETTINGS = Protocols.Settings()
SQLDATABASE = SETTINGS.sqlDatabase
SQLUSERNAME = SETTINGS.sqlUsername
SQLPASSWORD = SETTINGS.sqlPassword
currentDirectory = SETTINGS.currentDirectory
# End Key Variables =======================


# ==========================================================================================================
# NOTE: this method should NEVER be called if you are unsure an account exists as there is no error handling
class Profile(object):
    def __init__(self, ID):
        self._ID = ID
        # temp var
        temp = []
        holding = []
        try:
            # open the database
            db = MySQLdb.connect("localhost", SQLUSERNAME, SQLPASSWORD, SQLDATABASE)
            cursor = db.cursor()
            # Execute the SQL command
            cursor.execute("SELECT * FROM PROFILES")
            # get all records
            records = cursor.fetchall()
            # add all to array
            for row in records:
                holding.append(row)
                # search for profile
                for i in holding:
                    if i[0].__contains__(self._ID):
                        # save profile to temp
                        for j in i:
                            temp.append(j)

        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        # assign variables
        self._password = temp[1]
        self._defaultEmail = temp[2]
        self._defaultEmailPassword = temp[3]
        self._discord = temp[4]
        # setup other variables
        self._journal = UserData.Journal(self._ID)


    @property
    def password(self):
        # get password
        return self._password

    @property
    def defaultEmail(self):
        # get default email
        return self._defaultEmail

    @property
    def defaultEmailPassword(self):
        # get default email password
        return self._defaultEmailPassword

    @property
    def discord(self):
        # get discord
        return self._discord

# ==========================================================================================================

# creating a new user profile
def create(user, password, email, emailPassword, discord):
    file = open(directory, "a")  # open and read file
    newProfile = user + ',' + password + ',' + email + ',' + emailPassword + ',' + discord  # create new profile
    file.writelines(newProfile)  # save to file
    file.close()

    '''
    # NOW FOR SQL!
    db = MySQLdb.connect("localhost", PrimaryNode.startupParams[3], PrimaryNode.startupParams[4], "FOSS_ASSISTANT")
    cursor = db.cursor()


    try:
        # Execute the SQL command
        cursor.execute("INSERT INTO PROFILES(USER, PASSWORD, EMAIL, EMAILPASS) VALUES(" + user + ", " + password + ", " + email + ", " + emailPassword + " );")
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    # disconnect from server
    db.close()'''

def isProfile(user):
    try:
        # open the database
        db = MySQLdb.connect("localhost", SQLUSERNAME, SQLPASSWORD, SQLDATABASE)
        cursor = db.cursor()
        # Execute the SQL command
        cursor.execute("SELECT * FROM PROFILES")
        # get all records
        records = cursor.fetchall()
        # temp var
        temp = " "
        # add all to array
        for row in records:
            if row.__contains__(user):
                return True
    except:
        # Rollback in case there is any error
        db.rollback()
        # disconnect from server
    db.close()
    return False

# returns boolean from mysql search
def isProfileDiscord(discordtag):
    try:
        # open the database
        db = MySQLdb.connect("localhost", SQLUSERNAME, SQLPASSWORD, SQLDATABASE)
        cursor = db.cursor()
        # Execute the SQL command
        cursor.execute("SELECT * FROM PROFILES")
        # get all records
        records = cursor.fetchall()
        # temp var
        temp = " "
        # add all to array
        for row in records:
            if row.__contains__(discordtag):
                return True
    except:
        # Rollback in case there is any error
        db.rollback()
    # disconnect from server
    db.close()
    return False

# returns userID from mysql search
def getProfileUsernameDiscord(discordtag):
    # temp var
    temp = []
    holding = []
    try:
        # open the database
        db = MySQLdb.connect("localhost", SQLUSERNAME, SQLPASSWORD, SQLDATABASE)
        cursor = db.cursor()
        # Execute the SQL command
        cursor.execute("SELECT * FROM PROFILES")
        # get all records
        records = cursor.fetchall()
        # add all to array
        for row in records:
            holding.append(row)
            # search for profile
            for i in holding:
                if i[4].__contains__(discordtag):
                    # save profile to temp
                    for j in i:
                        temp.append(j)
        return temp[0]
    except:
        # Rollback in case there is any error
        db.rollback()
    # disconnect from server
    db.close()
    return "Anonymous User"