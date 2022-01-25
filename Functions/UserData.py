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
                for j in holding:
                    # sort tuple to array and append
                    tempEntries.append(Entry(j[0], j[1], j[2], j[3], j[4], j[5]))
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        self._entries = tempEntries

    # date, entry, UUID Unspecified, starred, creationDevice, timeZone
    def add_entry(self, entry=" ", creationDevice="Generic", starred="false", timeZone="EST"):

        x = datetime.now()
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

    # returns boolean based on if a matching date is found
    def is_entry(self, date):
        sort = self._entries
        for entry in sort:
            if entry.date.__contains__(date):
                return True
        return False

    # exports all journal entries of user to file
    def export_all(self):
        # create export file
        open(currentDirectory + '/Data/' + self._ID + '-journal.csv', 'x')
        for entry in self._entries:
            file = open(currentDirectory + '/Data/' + self._ID + '-journal.csv', "a")  # append mode
            file.write(entry.date + ',"' + entry.entry + '",' + entry.starred + ',' + entry.creationDevice + ',' + entry.timeZone + "\n")
            file.close()
        print("User " + self._ID + " Has Exported Their Journal To File.")

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


# ContactBook Class
# ==========================================================================================================
class ContactBook(object):
    def __init__(self, userID):
        self._ID = userID
        tempEntries = []
        holding = []
        try:
            # open the database
            db = MySQLdb.connect("localhost", SQLUSERNAME, SQLPASSWORD, SQLDATABASE)
            cursor = db.cursor()
            # Execute the SQL command
            cursor.execute("SELECT * FROM " + userID + "_CONTACTS")
            # get all records
            records = cursor.fetchall()
            # add all to array
            for row in records:
                holding.append(row)
                # add entry to holding variables
                for j in holding:
                    # sort tuple to array and append
                    tempEntries.append(Contact(j[0], j[1], j[2], j[3], j[4], j[5], j[6], j[7], j[8], homeFax, businessFax, pager, mobilePhone, homeStreet, homeAddress2, homeCity, homeState, homePostalCode, homeCountry, businessAddress, businessAddress2, businessCity, businessState, businessPostalCode, businessCountry, countryCode, relatedName, jobTitle, department, organization, notes, birthday, anniversary, gender, webPage, webPage2, categories, sociologicalOptions, genericSocialMediaHandle, discord, personalityRating, trustScore, blank1, blank2, blank3, blank4, blank5, blank6, blank7, blank8, blank9, blank10, blank11, blank12, blank13, blank14, blank15, blank16, blank17, blank18, blank19, blank20, blank21, blank22, blank23, blank24))
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        self._entries = tempEntries

    # date, entry, UUID Unspecified, starred, creationDevice, timeZone
    def add_entry(self, entry=" ", creationDevice="Generic", starred="false", timeZone="EST"):

        x = datetime.now()
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

    # returns boolean based on if a matching date is found
    def is_entry(self, date):
        sort = self._entries
        for entry in sort:
            if entry.date.__contains__(date):
                return True
        return False

    # exports all journal entries of user to file
    def export_all(self):
        print("User " + self._ID + " Has Exported Their Journal To File.")
        # create export file
        open(currentDirectory + '/Data/' + self._ID + '-journal.csv', 'x')
        with open(currentDirectory + '/Data/' + self._ID + '-journal.csv', 'w') as file:
            for entry in self._entries:
                file.write(entry.date + ',"' + entry.entry + '",' + entry.starred + ',' + entry.creationDevice + ',' + entry.timeZone + "\n")
        return "Export Complete"

# Sub Class Contact (only should be called inside ContactBook!)
class Contact(object):
    def __init__(self, firstName, lastName, displayName, nickname, emailAddress, email2address, email3address, homePhone, businessPhone, homeFax, businessFax, pager, mobilePhone, homeStreet, homeAddress2, homeCity, homeState, homePostalCode, homeCountry, businessAddress, businessAddress2, businessCity, businessState, businessPostalCode, businessCountry, countryCode, relatedName, jobTitle, department, organization, notes, birthday, anniversary, gender, webPage, webPage2, categories, sociologicalOptions, genericSocialMediaHandle, discord, personalityRating, trustScore, blank1, blank2, blank3, blank4, blank5, blank6, blank7, blank8, blank9, blank10, blank11, blank12, blank13, blank14, blank15, blank16, blank17, blank18, blank19, blank20, blank21, blank22, blank23, blank24):
        self._firstName = firstName
        self._lastName = lastName
        self._displayName = displayName
        self._nickname = nickname
        self._emailAddress = emailAddress
        self._email2address = email2address
        self._email3address = email3address
        self._lastName = lastName
        self._displayName = displayName
        self._homePhone = homePhone
        self._businessPhone = businessPhone
        self._homeFax = homeFax
        self._businessFax = businessFax
        self._pager = pager
        self._mobilePhone = mobilePhone
        self._homeStreet = homeStreet
        self._homeAddress2 = homeAddress2
        self._homeCity = homeCity
        self._homeState = homeState
        self._homePostalCode = homePostalCode
        self._homeCountry = homeCountry
        self._businessAddress = businessAddress
        self._businessAddress2 = businessAddress2
        self._businessCity = businessCity
        self._businessState = businessState
        self._businessPostalCode = businessPostalCode
        self._businessCountry = businessCountry
        self._countryCode = countryCode
        self._relatedName = relatedName
        self._jobTitle = jobTitle
        self._department = department
        self._organization = organization
        self._notes = notes
        self._birthday = birthday
        self._anniversary = anniversary
        self._gender = gender
        self._webPage = webPage
        self._webPage2 = webPage2
        self._categories = categories
        self._sociologicalOptions = sociologicalOptions
        self._genericSocialMediaHandle = genericSocialMediaHandle
        self._discord = discord
        self._personalityRating = personalityRating
        self._trustScore = trustScore
        # these variables exist for future expansion of the contact class without having to rewrite the entire database
        # note that these SHOULD NOT be called or used as they are, rather they should be renamed and then used.
        self._blank1 = blank1
        self._blank2 = blank2
        self._blank3 = blank3
        self._blank4 = blank4
        self._blank5 = blank5
        self._blank6 = blank6
        self._blank7 = blank7
        self._blank8 = blank8
        self._blank9 = blank9
        self._blank10 = blank10
        self._blank11 = blank11
        self._blank12 = blank12
        self._blank13 = blank13
        self._blank14 = blank14
        self._blank15 = blank15
        self._blank16 = blank16
        self._blank17 = blank17
        self._blank18 = blank18
        self._blank19 = blank19
        self._blank20 = blank20

    @property
    def firstName(self):
        return self._firstName

    @property
    def lastName(self):
        return self._lastName

    @property
    def displayName(self):
        return self._displayName

    @property
    def nickname(self):
        return self._nickname

    @property
    def emailAddress(self):
        return self._emailAddress

    @property
    def email2address(self):
        return self._email2address

    @property
    def email3address(self):
        return self._email3address

    @property
    def homePhone(self):
        return self._homePhone

    @property
    def businessPhone(self):
        return self._businessPhone

    @property
    def homeFax(self):
        return self._homeFax

    @property
    def businessFax(self):
        # get version
        return self._businessFax

    @property
    def pager(self):
        return self._pager

    @property
    def mobilePhone(self):
        return self._mobilePhone

    @property
    def homeStreet(self):
        return self._homeStreet

    @property
    def homeAddress2(self):
        return self._homeAddress2

    @property
    def homeCity(self):
        return self._homeCity

    @property
    def homeState(self):
        return self._homeState

    @property
    def homePostalCode(self):
        return self._homePostalCode

    @property
    def homeCountry(self):
        return self._homeCountry

    @property
    def homeCity(self):
        return self._homeCity

    @property
    def businessAddress(self):
        return self._businessAddress

    @property
    def businessAddress2(self):
        return self._businessAddress2

    @property
    def businessCity(self):
        return self._businessCity

    @property
    def businessState(self):
        return self._businessState

    @property
    def businessPostalCode(self):
        return self._businessPostalCode

    @property
    def businessCountry(self):
        return self._businessCountry

    @property
    def businessCountry(self):
        return self._businessCountry

    @property
    def countryCode(self):
        return self._countryCode

    @property
    def relatedName(self):
        return self._relatedName

    @property
    def jobTitle(self):
        return self._jobTitle

    @property
    def department(self):
        return self._department

    @property
    def organization(self):
        return self._organization

    @property
    def notes(self):
        return self._notes

    @property
    def birthday(self):
        return self._birthday

    @property
    def anniversary(self):
        return self._anniversary

    @property
    def gender(self):
        return self._gender

    @property
    def webPage(self):
        return self._webPage

    @property
    def webPage2(self):
        return self._webPage2

    @property
    def categories(self):
        return self._categories

    @property
    def sociologicalOptions(self):
        return self._sociologicalOptions

    @property
    def genericSocialMediaHandle(self):
        return self._genericSocialMediaHandle

    @property
    def discord(self):
        return self._discord

    @property
    def personalityRating(self):
        return self._personalityRating

    @property
    def trustScore(self):
        return self._trustScore

