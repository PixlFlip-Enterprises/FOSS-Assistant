import datetime
import os

# import MySQLdb


currentDirectory = os.getcwd()


def getFullEntry(date, user):
    file = open(currentDirectory + '/Data/Journal/' + user + '-journal.csv')
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


def add_entry(entry=" ", creationDevice="Generic", user="test", starred="false", timeZone="EST"):
    file = open(currentDirectory + '/Data/Journal/' + user + '-journal.csv', "a")  # append mode
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
    filename = currentDirectory + '/Data/Journal/' + user + '-journal.csv'
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
    file = open(currentDirectory + '/Data/Journal/' + user + '-journal.csv')
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
    file = open(currentDirectory + '/Data/Journal/' + user + '-journal.csv')
    for line in file:
        if line.__contains__(date):
            return True
    return False
