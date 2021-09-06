import datetime


# TODO this is really basic and just returns an array of the entire entry. Maybe spice it up some
def viewEntry(date):
    file = open('Data/Journal/Journal.csv')
    foundEntry = []
    for line in file:
        if line.__contains__(date):
            foundEntry = line
    # split message into parts
    entryArray = [x.strip() for x in foundEntry.split(',')]

    return entryArray


def addBasicEntry(entry, creationDevice):
    file = open('Data/Journal/Journal.csv', "a")  # append mode
    x = datetime.datetime.now()
    xy = x.__str__().replace(" ", "")
    # TODO the date is messed up and is therefore unreadable by DayOne App. Fix
    file.write("\n" + xy + ',"' + entry + '",UUID Unspecified,0,,,,'+creationDevice+',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,')
    file.close()


def addEntry(entry, starred, creationDevice, timeZone):
    file = open('Data/Journal/Journal.csv', "a")  # append mode
    x = datetime.datetime.now()
    xy = x.__str__().replace(" ", "")
    # TODO the date is messed up and is therefore unreadable by DayOne App. Fix
    file.write("\n" + xy + ',"' + entry + '",UUID Unspecified,0,'+starred+',,,'+creationDevice+','+timeZone+',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,')
    file.close()


def appendEntry(month, day, year, entry, starred, creationDevice, timeZone):
    filename = 'Data/Journal/Journal.csv'
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
    contents.insert(indexNum, lookup + ',"' + entry + '",UUID specified,0,'+starred+',,,'+creationDevice+','+timeZone+',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,')
    # write file with changes to memory again
    with open(filename, "w") as f:
        contents = "".join(contents)
        f.write(contents)