"""
Instead of many files for each function related to user data, why not merge them into a single file with tons of
classes? That is what this is: Each class can be called and used as needed for what it is meant to do, which saves
space in the long run, is more readable for coding, and just will be easier to manage for tying into mysql database.

"""
from datetime import datetime
import MySQLdb
from Functions import Protocols

# All key (read top level) variables here
SETTINGS = Protocols.Settings()
SQLDATABASE = SETTINGS.sqlDatabase
SQLUSERNAME = SETTINGS.sqlUsername
SQLPASSWORD = SETTINGS.sqlPassword
currentDirectory = SETTINGS.currentDirectory
# End Key Variables =======================


# Notebook Class
# ==========================================================================================================
class Notes(object):
    def __init__(self, userID):
        self._ID = userID
        tempEntries = []
        try:
            # open the database
            db = MySQLdb.connect("localhost", SQLUSERNAME, SQLPASSWORD, SQLDATABASE)
            cursor = db.cursor()
            # Execute the SQL command
            cursor.execute("SELECT * FROM " + userID + "_NOTES")
            # get all records
            records = cursor.fetchall()
            # add all to array
            for row in records:
                # date, entry, UUID, starred, creationDevice, timeZone
                tempEntries.append(Entry(row[0], row[1], row[2], row[3], row[4], row[5]))
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        self._entries = tempEntries

    # noteID, noteDateCreated, noteDateLastModified, noteTitle, noteBody, noteCreationDevice, noteStarred, noteLocked
    def add_note(self, entry=" ", creationDevice="Generic", starred="false", timeZone="EST"):

        x = datetime.datetime.now()
        xy = x.__str__().replace(" ", "")
        entryID = Protocols.new_database_entry_id(SQLUSERNAME, SQLPASSWORD, SQLDATABASE, self._ID + "-JOURNAL")
        try:
            # open the database
            db = MySQLdb.connect("localhost", SQLUSERNAME, SQLPASSWORD, SQLDATABASE)
            cursor = db.cursor()
            # Execute the SQL command
            cursor.execute(
                "INSERT INTO " + self._ID + "_JOURNAL(DATE, ENTRY, UUID, STARRED, CREATIONDEVICE, TIMEZONE) VALUES(" + xy + ", " + entry + "," + entryID + "," + starred + ", " + creationDevice + ", " + timeZone + " );")
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()

            # disconnect from server
        db.close()

    # returns Entry object of entry from date
    def get_entry(self, date):
        foundEntry = self._entries
        returnedEntry = Entry
        for entry in foundEntry:
            if entry.date.__contains__(date):
                returnedEntry = entry
        return returnedEntry

    # TODO implement logic
    def find_entry(self):

        return ""

    # TODO implement logic
    def remove_entry(self):
        return ""

    # returns array of all Entry objects. maybe could make this a string array someday.
    def export_all(self):
        return self._entries
# ==========================================================================================================


# Journal Class
# ==========================================================================================================
class Journal(object):
    def __init__(self, userID):
        self._ID = userID
        tempEntries = []
        holding = []
        try:
            # open the database
            db = MySQLdb.connect("localhost", SQLUSERNAME, SQLPASSWORD, SQLDATABASE)
            cursor = db.cursor()
            # Execute the SQL command
            cursor.execute("SELECT * FROM " + userID + "_JOURNAL")
            # get all records
            records = cursor.fetchall()
            # add all to array
            for row in records:
                holding.append(row)
                # add entry to holding variables
                for i in holding:
                    # sort tuple to array and append
                    for j in i:
                        # date, entry, UUID, starred, creationDevice, timeZone
                        tempEntries.append(Entry(j[0], j[1], j[2], j[3], j[4], j[5]))

        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        self._entries = tempEntries

    # date, entry, UUID Unspecified, starred, creationDevice, timeZone
    def add_entry(self, entry=" ", creationDevice="Generic", starred="false", timeZone="EST"):

        x = datetime.datetime.now()
        xy = x.__str__().replace(" ", "")
        entryID = Protocols.new_database_entry_id(SQLUSERNAME, SQLPASSWORD, SQLDATABASE, self._ID + "_JOURNAL")
        try:
            # open the database
            db = MySQLdb.connect("localhost", SQLUSERNAME, SQLPASSWORD, SQLDATABASE)
            cursor = db.cursor()
            # Execute the SQL command
            sql = "INSERT INTO " + self._ID + "_JOURNAL (DATE, ENTRY, UUID, STARRED, CREATIONDEVICE, TIMEZONE) VALUES(%s, %s, %s, %s, %s, %s)"
            val = (xy, entry, entryID, starred, creationDevice, timeZone)
            cursor.execute(sql, val)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()

            # disconnect from server
        db.close()

    # returns Entry object of entry from date
    def get_entry(self, date):
        foundEntry = self._entries
        returnedEntry = Entry
        for entry in foundEntry:
            if entry.date.__contains__(date):
                returnedEntry = entry
        return returnedEntry

    # TODO implement logic
    def find_entry(self):

        return ""

    # TODO implement logic
    def remove_entry(self):
        return ""

    def is_entry(self, date):
        sort = self._entries
        for entry in sort:
            if entry[1].__contains__(date):
                return True
        return False

    # returns array of all Entry objects. maybe could make this a string array someday.
    def export_all(self):
        return self._entries
# Sub Class Entry (only should be called inside journal!)
class Entry(object):
    def __init__(self, date, entry, UUID, starred, creationDevice, timeZone):
        self._date = date
        self._entry = entry
        self._UUID = UUID  # ID of entry as of this update
        self._starred = starred
        self._creationDevice = creationDevice
        self._timeZone = timeZone

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
