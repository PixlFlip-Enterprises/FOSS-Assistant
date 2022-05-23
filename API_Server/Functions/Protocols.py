# file for any and all protocols used
import os
import datetime
import pymysql as MySQLdb

# get exact directory
currentDirectory = os.getcwd()
if not currentDirectory.__contains__("FOSS"):
    currentDirectory = currentDirectory + '/FOSS-Assistant'


# Burn it all to the ground. Leave nothing
def vex(path, passes=7):
    with open(path, "ba+") as delfile:
        length = delfile.tell()
        for i in range(passes):
            delfile.seek(0)
            delfile.write(os.urandom(length))
    os.remove(path)

# return num lines in file (useful to assign unique IDs to stuff)
def linesInFile(directory):
    count = 0
    with open(directory) as f:
        count = sum(1 for _ in f)
    return count


def loadStartupParameters():
    # startup
    file = open(currentDirectory + '/Functions/ProgramData/startup.txt')
    returnList = []
    for line in file:
        returnList.append(line)
    return returnList


# Makes logging everything everywhere easier. About freaking time I redid this
def debug_log(console_printout, user, command, method_of_input):
    # Print to console
    print("= User " + user + " has issued the " + command + " command")
    # compile string of data for file
    logStr = user + "," + method_of_input + "," + command
    # open file
    file = open(currentDirectory + '/Functions/ProgramData/log.txt', "a")  # append mode
    # get date and time of command issued
    x = datetime.datetime.now()
    xy = x.__str__().replace(" ", "")
    # print line with date to file
    file.write("\n" + xy + "," + logStr)
    # close file and return
    file.close()


# sync between file and database.
# export all datasheets, settings, etc to another instance. Should save me headaches moving between host devices
def exportAll():
    # get all data from mysql databases
    # reconcile with file data
    # get all data from files
    # create a master file for the export (or a zip)
    # put to directory of choice or default and return
    print("Nothing here yet!")


# get correct ID for a new entry in a datatable
def new_database_entry_id(user, password, database, table):
    # username, password and database
    db = MySQLdb.connect(host="localhost", user=user, password=password, database=database)
    # get cursor object
    cursor = db.cursor()
    # get number of rows in a table and give your table
    # name in the query
    number_of_rows = cursor.execute("SELECT * FROM " + table)
    # return number of rows
    return number_of_rows

# TODO method that merges everything from file to database, and I do mean everything
def establish_parady():
    # first cycle through and compile an array of all usernames from database
    # scan through the data folder for any matching files to a specific user
    # if found scan all the information from the file into the database for that user
    # repeat
    # end
    return "nerd"

# TODO ensure this doesn't add duplicates
# Gets all available file information with userID and adds to the database
def establish_parady_user(userID, sqluser, sqlpass, sqldatabase):
    # journal parady
    file = open(currentDirectory + '/Data/' + userID + '-journal.csv')
    # add every entry to a massive array
    foundEntry = []
    for line in file:
        foundEntry.append(line)

    # now cycle through entire thing
    for entryCycle in foundEntry:
        # split message into parts
        # first part split using quotes
        if len(entryCycle) <= 2:
            break
        entryArrayCenter = [x.strip() for x in entryCycle.split('"')]
        # now split the newly created 0 and 2 spots
        entryArrayLeft = [x.strip() for x in entryArrayCenter[0].split(',')]
        entryArrayRight = [x.strip() for x in entryArrayCenter[2].split(',')]
        # conjoin all three and viola the entry will be correct
        entryArrayRight.remove(entryArrayLeft[1])
        entryArrayLeft.remove(entryArrayLeft[1])
        entryArray = entryArrayLeft
        entryArray.append(entryArrayCenter[1])
        entryArray += entryArrayRight
        # add parsed entry to database (at least in theory)
        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=sqluser, password=sqlpass, database=sqldatabase)
            cursor = db.cursor()
            # Execute the SQL command
            sql = "INSERT INTO " + userID + "_JOURNAL (DATE, ENTRY, UUID, STARRED, CREATIONDEVICE, TIMEZONE) VALUES(%s, %s, %s, %s, %s, %s)"
            val = (entryArray[0], entryArray[1], entryArray[2], entryArray[4], entryArray[8], entryArray[9])
            cursor.execute(sql, val)
            # Commit your changes in the database
            db.commit()
            db.close()
        except:
            # Rollback in case there is any error
            db.rollback()
            db.close()
            # disconnect from server

        print(cursor.rowcount, "records inserted for the date " + entryArray[0])

# ==========================================================================================================
# Class for All Startup Settings
class Settings(object):
    def __init__(self):
        # open file
        # once verified go ahead and startup
        file = open(currentDirectory + '/Functions/ProgramData/startup.txt')
        returnList = []
        for line in file:
            returnList.append(line)
        # assign variables
        self._version = returnList[0]
        self._musicDirectory = returnList[1]
        self._videoDirectory = returnList[2]
        self._assistantName = returnList[3]
        self._sqlDatabase = returnList[4]
        self._sqlUsername = returnList[5]
        self._sqlPassword = returnList[6]
        self._discordBotToken = returnList[7]
        self._discordBotPrefix = returnList[8]
        self._currentDirectory = currentDirectory

    @property
    def version(self):
        # get version
        return self._version.replace("\n", "")

    @property
    def musicDirectory(self):
        # get music directory
        return self._musicDirectory.replace("\n", "")

    @property
    def videoDirectory(self):
        # get video directory
        return self._videoDirectory.replace("\n", "")

    @property
    def assistantName(self):
        # get custom assistant name
        return self._assistantName.replace("\n", "")

    @property
    def sqlDatabase(self):
        # get database name
        return self._sqlDatabase.replace("\n", "")

    @property
    def sqlUsername(self):
        # get sql username
        return self._sqlUsername.replace("\n", "")

    @property
    def sqlPassword(self):
        # get database password
        return self._sqlPassword.replace("\n", "")

    @property
    def discordBotToken(self):
        # get bot token for discord
        return self._discordBotToken.replace("\n", "")

    @property
    def discordBotPrefix(self):
        # get version
        return self._discordBotPrefix.replace("\n", "")

    @property
    def currentDirectory(self):
        # get version
        return self._currentDirectory.replace("\n", "")
# ==========================================================================================================
