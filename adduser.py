""" Until Database function is immplimented properly this is a command line script to add a user by hand. """
import MySQLdb
from Functions import Protocols

# All key (read top level) variables here
SETTINGS = Protocols.Settings()
SQLDATABASE = SETTINGS.sqlDatabase
SQLUSERNAME = SETTINGS.sqlUsername
SQLPASSWORD = SETTINGS.sqlPassword
currentDirectory = SETTINGS.currentDirectory
# End Key Variables =======================

profileParams = []
print("FOSS ASSISTANT ADD PROFILE SCRIPT ")
profileParams.append(input("= Enter your Username: ").lower().replace(' ', ''))
profileParams.append(input("= Enter your Password: "))
profileParams.append(input("= Enter your Email Address: "))
profileParams.append(input("= Enter your Password for Email Above: "))
profileParams.append(input("= Enter Discord ID (put NONE if no ID): "))
# Add user to database
try:
    # open the database
    db = MySQLdb.connect("localhost", SQLUSERNAME, SQLPASSWORD, SQLDATABASE)
    cursor = db.cursor()
    # Execute the SQL command
    cursor.execute(
        "INSERT INTO PROFILES(USER, PASSWORD, EMAIL, EMAILPASS, DISCORD) VALUES(" + profileParams[0] + ", " + profileParams[1] + "," + profileParams[2] + "," + profileParams[3] + ", " + profileParams[4] + " );")
    # Commit your changes in the database
    db.commit()
except:
    # Rollback in case there is any error
    db.rollback()
    print("An error occurred and the profile was not saved. Make sure you have ran initial setup.")

# disconnect from server
db.close()
# print and end
print("Profile created successfully.")