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
# import MySQLdb
directory = os.getcwd() + '/Data/profiles.csv'


# ==========================================================================================================
# NOTE: this method should NEVER be called if you are unsure an account exists as there is no error handling
class Profile(object):
    def __init__(self, ID):
        # assign ID
        self.ID = ID
        # open file
        file = open(directory)
        temp = []
        # find profile
        for line in file:
            if line.__contains__(ID):
                # save profile to temp
                temp = line.split(",")
        # assign variables
        self._password = temp[1]
        self._defaultEmail = temp[2]
        self._defaultEmailPassword = temp[3]
        self._discord = temp[4]

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


def getProfile(user):
    file = open(directory)
    for line in file:
        if line.__contains__(user):
            return line
    return "NO USER"


# creating a new user profile
def create(user, password, email, emailPassword, discord):
    file = open(directory, "a")  # open and read file
    newProfile = user + ',' + password + ',' + email + ',' + emailPassword + ',' + discord # create new profile
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
    file = open(directory, "r")
    fileContent = []
    for line in file:
        fileContent.append(line)

    for line in fileContent:
        if line.__contains__(user):
            return True
    return False


def isProfileDiscord(discordtag):
    file = open(directory, "r")
    fileContent = []
    for line in file:
        fileContent.append(line)

    for line in fileContent:
        if line.__contains__(discordtag):
            return True
    return False


def getProfileUsernameDiscord(discordtag):
    file = open(directory, "r")
    fileContent = []
    for line in file:
        fileContent.append(line)

    for line in fileContent:
        if line.__contains__(discordtag):
            return line.split(',')[0]
    return "Anonymous User"


def getProfileDiscord(discordtag):
    file = open(directory, "r")
    fileContent = []
    for line in file:
        fileContent.append(line)

    for line in fileContent:
        if line.__contains__(discordtag):
            return line.split(',')
    return "Dump"