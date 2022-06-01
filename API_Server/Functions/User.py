import pymysql as MySQLdb
from API_Server.Functions import Protocols, UserData

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
            db = MySQLdb.connect(host="localhost", user=SQLUSERNAME, password=SQLPASSWORD, database=SQLDATABASE)
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
        self._clearanceLevel = temp[5]
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

    @property
    def clearanceLevel(self):
        # get clearance level
        return self._clearanceLevel

    @property
    def journal(self):
        # get journal
        return self._journal

# ==========================================================================================================

# creating a new user profile
def create(user, password, clearance_level, email="NONE", emailPassword="NONE", discord="NONE"):
    # add parsed entry to database (at least in theory)
    try:
        # open the database
        db = MySQLdb.connect(host="localhost", user=SQLUSERNAME, password=SQLPASSWORD, database=SQLDATABASE)
        cursor = db.cursor()
        # Execute the SQL command
        sql = "INSERT INTO PROFILES(USER, PASSWORD, EMAIL, EMAILPASS, DISCORD) VALUES(%s, %s, %s, %s, %s, %s)"
        val = (user, password, email, emailPassword, discord, clearance_level)
        cursor.execute(sql, val)
        # Commit your changes in the database
        db.commit()
        db.close()
    except:
        # Rollback in case there is any error
        db.rollback()
        db.close()
        # disconnect from server

def isProfile(user):
    # open the database
    db = MySQLdb.connect(host="localhost", user=SQLUSERNAME, password=SQLPASSWORD, database=SQLDATABASE)
    cursor = db.cursor()
    try:
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
    # open the database
    db = MySQLdb.connect(host="localhost", user=SQLUSERNAME, password=SQLPASSWORD, database=SQLDATABASE)
    cursor = db.cursor()
    try:
        # TODO rewrite this to utilize the full potential of SQL query. Could be done in two lines

        # Execute the SQL command
        cursor.execute("SELECT * FROM PROFILES")
        # get all records
        records = cursor.fetchall()
        # temp var
        temp = " "
        # search
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
        db = MySQLdb.connect(host="localhost", user=SQLUSERNAME, password=SQLPASSWORD, database=SQLDATABASE)
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


# returns userID from mysql search
def is_profile_api_key(key):
    try:
        # open the database
        db = MySQLdb.connect(host="localhost", user=SQLUSERNAME, password=SQLPASSWORD, database=SQLDATABASE)
        cursor = db.cursor()
        # see if key exists
        cursor.execute("select * from API_KEYS where API_KEY like '%" + key + "%';")
        # get all records
        records = cursor.fetchall()
        # check
        if records[0][0] == key:
            return records[0][1]
        else:
            return False
    except:
        # Rollback in case there is any error
        db.rollback()
    # disconnect from server
    db.close()
    return False


# returns a user's api key
def get_profile_api_key(profile_id):
    try:
        # open the database
        db = MySQLdb.connect(host="localhost", user=SQLUSERNAME, password=SQLPASSWORD, database=SQLDATABASE)
        cursor = db.cursor()
        # see if key exists
        cursor.execute("select * from API_KEYS where PROFILE_ID like '%" + profile_id + "%';")
        # get all records
        records = cursor.fetchall()
        # check
        return records[0][0]
    except:
        # Rollback in case there is any error
        db.rollback()
    # disconnect from server
    db.close()
    return False