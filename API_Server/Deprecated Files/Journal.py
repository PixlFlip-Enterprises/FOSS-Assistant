import datetime
from API_Server.Functions import Protocols

# import MySQLdb
SETTINGS = Protocols.Settings()
workingDirectory = SETTINGS.currentDirectory + '/Data/Journal/'

# TODO we can make this into a class for calling, getting, and setting all in one organized format
def getFullEntry(date, user):
    file = open(workingDirectory + user + '-journal.csv')
    foundEntry = []
    for line in file:
        if line.__contains__(date):
            foundEntry = line
    # split message into parts
    # first part split using quotes
    entryArrayCenter = [x.strip() for x in foundEntry.split('"')]
    # now split the newly created 0 and 2 spots
    entryArrayLeft = [x.strip() for x in entryArrayCenter[0].split(',')]
    entryArrayRight = [x.strip() for x in entryArrayCenter[2].split(',')]
    # conjoin all three and viola the entry will be correct
    entryArrayRight.remove(entryArrayLeft[1])
    entryArrayLeft.remove(entryArrayLeft[1])
    entryArray = entryArrayLeft
    entryArray.append(entryArrayCenter[1])
    entryArray += entryArrayRight
    # entryArray can be returned to user
    return entryArray

# TODO for some reason this is adding a blank line in the file before recording the entry. Could be DiscordNode
def add_entry(entry=" ", creationDevice="Generic", user="test", starred="false", timeZone="EST"):
    file = open(workingDirectory + user + '-journal.csv', "a")  # append mode
    x = datetime.datetime.now()
    xy = x.__str__().replace(" ", "")
    file.write(
        "\n" + xy + ',"' + entry + '",UUID Unspecified,0,' + starred + ',,,' + creationDevice + ',' + timeZone + ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,')
    file.close()

    '''
    try:
        db = MySQLdb.connect("localhost", PrimaryNode.startupParams[3], PrimaryNode.startupParams[4], "FOSS_ASSISTANT")
        cursor = db.cursor()
        # Execute the SQL command
        cursor.execute(
            "INSERT INTO JOURNAL(DATE, ENTRY, UUID, STARRED, CREATIONDEVICE, TIMEZONE) VALUES(" + xy + ", " + entry + ",UUID Unspecified ," + starred + ", " + creationDevice + ", " + timeZone + " );")
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    # disconnect from server
    db.close()'''


def appendEntry(user, month, day, year, entry, starred, creationDevice, timeZone):
    filename = workingDirectory + user + '-journal.csv'
    indexNum = 0
    day = day - 1

    # format of dates: 2019-10-17T14:37:13.619Z
    lookup = str(year) + '-' + str(month) + '-' + str(day)

    # find index of entry to append
    with open(filename) as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup in line:
                indexNum = num

    # save current file state
    with open(filename, "r") as f:
        contents = f.readlines()
    # add new part to the file
    contents.insert(indexNum,
                    lookup + ',"' + entry + '",UUID specified,0,' + starred + ',,,' + creationDevice + ',' + timeZone + ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,')
    # write file with changes to memory again
    with open(filename, "w") as f:
        contents = "".join(contents)
        f.write(contents)


def importEntriesToDatabase(user):
    # Open file
    file = open(workingDirectory + user + '-journal.csv')
    # get all entries and store in array
    i = 0
    foundEntry = []
    for line in file:
        foundEntry[i] = line
        i = i + 1

        '''
        try:
            db = MySQLdb.connect("localhost", PrimaryNode.startupParams[3], PrimaryNode.startupParams[4], "FOSS_ASSISTANT")
            cursor = db.cursor()
            # Execute the SQL command
            cursor.execute("INSERT INTO JOURNAL(DATE, ENTRY, UUID, STARRED, CREATIONDEVICE, TIMEZONE) VALUES(" + entryArray[0] + ", " + entryArray[1] + ", " + entryArray[2] + ", " + entryArray[4] + ", " + entryArray[8] + ", " + entryArray[9] + " );")
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()

        # disconnect from server
        db.close()'''


def isEntry(date, user):
    file = open(workingDirectory + user + '-journal.csv')
    for line in file:
        if line.__contains__(date):
            return True
    return False


# ==========================================================================================================
# Entry Class
class Entry(object):
    def __init__(self, date, user):
        file = open(workingDirectory + user + '-journal.csv')
        foundEntry = []
        for line in file:
            if line.__contains__(date):
                foundEntry = line
        # split message into parts
        # first part split using quotes
        entryArrayCenter = [x.strip() for x in foundEntry.split('"')]
        # now split the newly created 0 and 2 spots
        entryArrayLeft = [x.strip() for x in entryArrayCenter[0].split(',')]
        entryArrayRight = [x.strip() for x in entryArrayCenter[2].split(',')]
        # conjoin all three and viola the entry will be correct
        entryArrayRight.remove(entryArrayLeft[1])
        entryArrayLeft.remove(entryArrayLeft[1])
        entryArray = entryArrayLeft
        entryArray.append(entryArrayCenter[1])
        entryArray += entryArrayRight
        # entryArray can be now sorted into its respective variables
        self._date = entryArray[0]
        self._entry = entryArray[1]
        self._UUID = entryArray[2]
        self._starred = entryArray[3]
        self._creationDevice = entryArray[4]
        self._timeZone = entryArray[5]

    @property
    def date(self):
        # get version
        return self._date

    @property
    def entry(self):
        # get music directory
        return self._entry

    @property
    def starred(self):
        # get video directory
        return self._starred

    @property
    def creationDevice(self):
        # get custom assistant name
        return self._creationDevice

    @property
    def timeZone(self):
        # get database name
        return self._timeZone
# ==========================================================================================================

