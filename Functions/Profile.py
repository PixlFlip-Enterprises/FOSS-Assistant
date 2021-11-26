# profile file syntax:
# contact ID (for retrieval in Contact.csv
# primary email password
# secondary email password
# third email password
# Sequence of events on startup coded as three char IDs. Example: SLK (sherlock username), RIC (rickroll),
# DTE (date and time), etc.
import os
# import MySQLdb
currentDirectory = os.getcwd()


def getProfile(user):
    file = open(currentDirectory + '/Functions/Profiles/profiles.csv')
    for line in file:
        if line.__contains__(user):
            return line
    return "NO USER"


# creating a new user profile
def create(user, password, email, emailPassword, discord):
    file = open(currentDirectory + '/Functions/Profiles/profiles.csv', "a")  # open and read file
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
    file = open(currentDirectory + '/Functions/Profiles/profiles.csv', "r")
    fileContent = []
    for line in file:
        fileContent.append(line)

    for line in fileContent:
        if line.__contains__(user):
            return True
    return False


def isProfileDiscord(discordtag):
    file = open(currentDirectory + '/Functions/Profiles/profiles.csv', "r")
    fileContent = []
    for line in file:
        fileContent.append(line)

    for line in fileContent:
        if line.__contains__(discordtag):
            return True
    return False

def getProfileDiscord(discordtag):
    file = open(currentDirectory + '/Functions/Profiles/profiles.csv', "r")
    fileContent = []
    for line in file:
        fileContent.append(line)

    for line in fileContent:
        if line.__contains__(discordtag):
            return line.split(',')[0]
    return "Dump"
