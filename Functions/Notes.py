import datetime
from Functions import Protocols, User

SETTINGS = Protocols.Settings()
currentDirectory = SETTINGS.currentDirectory


# note .csv format in order with comas

def get_note(date, user):
    file = open(currentDirectory + '/Data/Notes/' + user + '-notes.csv')
    foundNote = []
    for line in file:
        if line.__contains__(date):
            foundNote = line
    # split message into parts
    # first part split using quotes
    noteArray = [x.strip() for x in foundNote.split('"')]

    return noteArray


def add_note(user, noteTitle="NO TITLE", noteBody="I MADE A NOTE WITHOUT ANY TEXT", noteCreationDevice="Generic", noteStarred="false", noteLocked="false"):
    # directory
    directory = currentDirectory + '/Data/Notes/' + user + '-notes.csv'
    # create ID of note for file
    noteID = Protocols.linesInFile(directory) + 1
    # open file
    file = open(directory, "a")  # append mode
    # get date + format
    x = datetime.datetime.now()
    xy = x.__str__().replace(" ", "")
    # write the note to file
    # noteID, noteDateCreated, noteDateLastModified, noteTitle, noteBody, noteCreationDevice, noteStarred, noteLocked
    file.write("\n" + noteID + "," + xy + "," + xy + ',"' + noteTitle + '","' + noteBody + '",' + noteCreationDevice + ',' + noteStarred + ',' + noteLocked)
    file.close()


def delete_note(date, user):
    file = open(currentDirectory + '/Data/Notes/' + user + '-notes.csv')
    foundNote = []
    for line in file:
        if line.__contains__(date):
            foundNote = line
    # split message into parts
    # first part split using quotes
    noteArray = [x.strip() for x in foundNote.split('"')]

    return noteArray


def create_note():
    file = open(currentDirectory + '/Data/Notes/' + user + '-notes.csv')
    foundNote = []
    for line in file:
        if line.__contains__(date):
            foundNote = line
    # split message into parts
    # first part split using quotes
    noteArray = [x.strip() for x in foundNote.split('"')]

    return noteArray
