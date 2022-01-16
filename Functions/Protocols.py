# file for any and all protocols used
import os
import datetime
from os.path import exists

import MySQLdb
# import pytube
# from pytube import YouTube
currentDirectory = os.getcwd()


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

# Returns String array of Byte array provided
def byteToStr(bytesToConvert):
    # Format data into str from byte
    convertedBytes = bytesToConvert.decode()
    # split message into parts
    request = convertedBytes.split(':')
    part1 = request[0].split(',')
    part2 = request[1].split(',')
    part3 = request[2].split(',')
    # return multidimensional array
    return part1, part2, part3


def loadStartupParameters():
    # startup
    file = open(currentDirectory + '/Functions/ProgramData/startup.txt')
    returnList = []
    for line in file:
        returnList.append(line)
    return returnList


# Logs any issued command to file and prints to console
def debugLog(user, command, requestDevice):
    # Print to console
    print("= User " + user + " has issued the following command: " + command)
    # compile string of data for file
    logStr = user + "," + requestDevice + "," + command
    # open file
    file = open(currentDirectory + '/Functions/ProgramData/log.txt', "a")  # append mode
    # get date and time of command issued
    x = datetime.datetime.now()
    xy = x.__str__().replace(" ", "")
    # print line with date to file
    file.write("\n" + xy + "," + logStr)
    # close file and return
    file.close()


""" Eventually this with tie in to a neural network to make it easier. This method just makes it easier to skip the step
of speech intent if a command already has been correctly assigned from client based application """


# Finds intent of query and returns it as a numeric value + rest of array
def findIntentFromText(message):
    command = message
    # massive if statement for now to gather intent. Don't touch the rest of the array in this function
    if command.__contains__("send") and command.__contains__("email"):
        # send email command code 1
        return 1

    elif command.__contains__("view") and command.__contains__("email"):
        # send email command code 12
        return 12

    elif command.__contains__("wiki"):
        # wikipedia search command code 2
        return 2

    elif command.__contains__("journal") and command.__contains__("view"):
        # add entry to Journal command code 3
        return 3

    elif command.__contains__("journal") and command.__contains__("new") and command.__contains__("entry"):
        # add entry to Journal command code 3
        return 31

    elif command.__contains__("bomb"):
        # this will do something dramatic eventually. Code 4
        return 4

    elif command.__contains__("youtube") and command.__contains__("download"):
        # download youtube link to memory. Code 5
        return 5

    elif command.__contains__("help"):
        return 6

    # ========================== MUSIC COMMANDS ==========================
    elif command.__contains__("rickroll"):
        # rickroll. A classic!
        return 7

    elif command.__contains__("music") and command.__contains__("all"):
        # play all music in no order
        return 8

    elif command.__contains__("backup") and command.__contains__("all"):
        # backup
        return 9

    elif command.__contains__("import") and command.__contains__("journal"):
        # imports journal to sql database (in theory)
        return 10

    elif command.__contains__("music") and command.__contains__("playlist"):
        # play playlist
        return 13

    else:
        return 0


# Downloads links provided to Youtube in highest possible resolution... at least in theory
"""def youtubeVideoDownload(links):
    for link in links:
        yt = pytube.YouTube(link)
        stream = yt.streams.first()
        stream.download()"""

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
    db = MySQLdb.connect("localhost", user, password, database)
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
            break;
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
            db = MySQLdb.connect("localhost", sqluser, sqlpass, sqldatabase)
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
        self._currentDirectory = os.getcwd()

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
