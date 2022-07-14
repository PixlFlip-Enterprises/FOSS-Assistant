from flask_restful import Resource, reqparse
from datetime import datetime
import pymysql as MySQLdb
# todo this should be gone and be fully functional as a package.
from API_Server.Functions import Protocols, User

# Top variables
SETTINGS = Protocols.Settings()
SQLDATABASE = SETTINGS.sqlDatabase
SQLUSERNAME = SETTINGS.sqlUsername
SQLPASSWORD = SETTINGS.sqlPassword
currentDirectory = SETTINGS.currentDirectory

########################################################################################################################
#                                                   JOURNAL RESOURCE
########################################################################################################################
# journal get args
journal_get_args = reqparse.RequestParser()
journal_get_args.add_argument("session_token", type=str, help="Token from valid session. Expired token?", required=True)
journal_get_args.add_argument("date", type=str, help="Date of journal entry", required=True)
# journal put args
journal_put_args = reqparse.RequestParser()
journal_put_args.add_argument("session_token", type=str, help="Token from valid session. Expired token?", required=True)
journal_put_args.add_argument("date", type=str, help="Date of journal entry", required=False)
journal_put_args.add_argument("entry", type=str, help="Journal entry", required=True)
journal_put_args.add_argument("creation_device", type=str, help="Device created on", required=True)
journal_put_args.add_argument("starred", type=str, help="Favorited or not", required=True)
journal_put_args.add_argument("time_zone", type=str, help="Timezone created in", required=True)
# journal del args
journal_del_args = reqparse.RequestParser()
journal_del_args.add_argument("session_token", type=str, help="Token from valid session. Expired token?", required=True)
journal_del_args.add_argument("date", type=str, help="Date of journal entry to be deleted", required=True)


# create journal resource
class Journal(Resource):

    def get(self):
        # verify fields
        args = journal_get_args.parse_args()
        # verify session
        if User.is_profile_api_key(args['session_token']) == False:
            return {"status": "failed. Invalid session token"}
        # log
        Protocols.debug_log(console_printout="Journal View Entry", user=User.is_profile_api_key(args['session_token']), command="000020", method_of_input="REST API")
        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=SQLUSERNAME, password=SQLPASSWORD, database=SQLDATABASE)
            cursor = db.cursor()
            # Execute the SQL command
            cursor.execute("select * from JOURNAL where PROFILE_ID LIKE '" + User.is_profile_api_key(args['session_token']) + "' AND DATE LIKE '" + args['date'] + "%';")
            # get all records
            records = cursor.fetchall()
            # first is entry
            try:
                entry = records[0]
                return {"date": entry[2], "entry": entry[3], "starred": entry[5],"creation_device": entry[6], "timezone": entry[7]}, 201
            except:
                return {"status": "Failed. Entry does not exist"}
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        # return since entry doesn't exist
        return {"status": "Failed. Entry does not exist"}


    def put(self):
        # verify fields
        args = journal_put_args.parse_args()
        # verify session
        if User.is_profile_api_key(args['session_token']) == False:
            return {"status": "Failed. Invalid session token"}

        username = User.is_profile_api_key(args['session_token'])
        # log
        Protocols.debug_log(console_printout="Journal View Entry", user=username, command="000021", method_of_input="REST API")
        # todo add a thing in here to allow for arbitrary dates to be added instead of just the second the put is received
        x = datetime.now().__str__().replace(" ", "")
        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=SQLUSERNAME, password=SQLPASSWORD, database=SQLDATABASE)
            cursor = db.cursor()
            # Execute the SQL command
            sql = "INSERT INTO JOURNAL (PROFILE_ID, DATE, ENTRY, UUID, STARRED, CREATIONDEVICE, TIMEZONE) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            val = (username, x, args['entry'], "UPDATED SO THIS IS AN UNUSED FIELD FOR NOW", args['starred'], args['creation_device'], args['time_zone'])
            print(val)
            cursor.execute(sql, val)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
            return {"status": "Failed. Is the data provided correct?"}

        # disconnect from server
        db.close()
        # note, you can put a comma and then follow it with a status code of your choice. Handy for some stuff
        return {"status": "Completed"}, 201


    def delete(self):
        # verify fields
        args = journal_del_args.parse_args()
        # verify session
        if User.is_profile_api_key(args['session_token']) == False:
            return {"status": "failed. Invalid session token"}
        # log
        Protocols.debug_log(console_printout="Journal Delete Entry", user=User.is_profile_api_key(args['session_token']), command="000022", method_of_input="REST API")
        username = User.is_profile_api_key(args['session_token'])

        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=SQLUSERNAME, password=SQLPASSWORD, database=SQLDATABASE)
            cursor = db.cursor()
            # Execute the SQL command
            sql = "DELETE FROM JOURNAL WHERE PROFILE_ID = '" + username + "' AND DATE = '" + args['date'] + "%'"
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
            return {"status": "Failed. Most likely means the entry does not exist or bad input."}
        return {"status": "Completed"}


    def patch(self):
        # verify fields
        args = journal_get_args.parse_args()
        # verify session
        if User.is_profile_api_key(args['session_token']) == False:
            return {"status": "failed. Invalid session token"}

        # log
        Protocols.debug_log(console_printout="Journal Delete Entry", user=User.is_profile_api_key(args['session_token']), command="000023", method_of_input="REST API")
        return {"status": "Code will go here, but this returned correctly?"}

########################################################################################################################
#                                                   PROFILE RESOURCE
########################################################################################################################
# profile get args
profile_get_args = reqparse.RequestParser()
profile_get_args.add_argument("session_token", type=str, help="Token from valid session. Expired token?", required=True)
profile_get_args.add_argument("username", type=str, help="Name of the user profile", required=True)
# profile put args
profile_put_args = reqparse.RequestParser()
profile_put_args.add_argument("session_token", type=str, help="Token from valid session. Expired token?", required=True)
profile_put_args.add_argument("date", type=str, help="Date of journal entry", required=False)
profile_put_args.add_argument("entry", type=str, help="Journal entry", required=True)
profile_put_args.add_argument("creation_device", type=str, help="Device created on", required=True)
profile_put_args.add_argument("starred", type=str, help="Favorited or not", required=True)
profile_put_args.add_argument("time_zone", type=str, help="Timezone created in", required=True)
# profile del args
profile_del_args = reqparse.RequestParser()
profile_del_args.add_argument("session_token", type=str, help="Token from valid session. Expired token?", required=True)
profile_del_args.add_argument("username", type=str, help="Username of profile to be deleted", required=True)
profile_del_args.add_argument("user_password", type=str, help="Password of user being deleted", required=True)


# create profile resource
class Profile(Resource):

    # GET provides information on a profile based on the clearance level of the account
    def get(self):
        # verify fields
        args = profile_get_args.parse_args()
        # verify session
        if User.is_profile_api_key(args['session_token']) == False:
            return {"status": "failed. Invalid session token"}
        # log
        Protocols.debug_log(console_printout="View Profile", user=User.is_profile_api_key(args['session_token']), command="000030", method_of_input="REST API")
        # check clearance level of user
        clearance_level = 3
        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=SQLUSERNAME, password=SQLPASSWORD, database=SQLDATABASE)
            cursor = db.cursor()
            # Execute the SQL command
            cursor.execute("select CLEARANCE_LEVEL from PROFILES where USER LIKE '" + User.is_profile_api_key(args['session_token']) + "';")
            # get all records
            record = cursor.fetchone()
            # first is entry
            clearance_level = record[0]
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        # get all data on username
        requested_profile = ()
        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=SQLUSERNAME, password=SQLPASSWORD, database=SQLDATABASE)
            cursor = db.cursor()
            # Execute the SQL command
            cursor.execute("select * from PROFILES where USER LIKE '" + args['username'] + "';")
            # get all records
            records = cursor.fetchall()
            # first is entry
            try:
                requested_profile = records[0]
            except:
                return {"status": "Failed. Server error not your fault though"}
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        # return data permitted for clearance level
        if clearance_level == 3:
            # basically show them the profile exists and that's about it
            return {"status": "Completed.", "data": {"username": requested_profile[0]}}, 201
        if clearance_level == 2:
            # basically show them the profile exists and that's about it
            return {"status": "Completed.", "data": {"username": requested_profile[0], "discord": requested_profile[4]}}, 201
        if clearance_level == 1:
            # basically show them the profile exists and that's about it
            return {"status": "Completed.", "data": {"username": requested_profile[0], "discord": requested_profile[4], "email": requested_profile[2]}}, 201
        return {"status": "Failed.", "error_msg": "...Yeah I've got nothing for you this should be impossible"}, 201


    # PUT allows for new user accounts to be created
    def put(self):
        # verify fields
        args = profile_put_args.parse_args()
        # verify session
        if User.is_profile_api_key(args['session_token']) == False:
            return {"status": "Failed. Invalid session token"}

        username = User.is_profile_api_key(args['session_token'])
        # log
        Protocols.debug_log(console_printout="Journal View Entry", user=username, command="000021", method_of_input="REST API")
        # todo add a thing in here to allow for arbitrary dates to be added instead of just the second the put is received
        x = datetime.now().__str__().replace(" ", "")
        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=SQLUSERNAME, password=SQLPASSWORD, database=SQLDATABASE)
            cursor = db.cursor()
            # Execute the SQL command
            sql = "INSERT INTO JOURNAL (PROFILE_ID, DATE, ENTRY, UUID, STARRED, CREATIONDEVICE, TIMEZONE) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            val = (username, x, args['entry'], "UPDATED SO THIS IS AN UNUSED FIELD FOR NOW", args['starred'], args['creation_device'], args['time_zone'])
            print(val)
            cursor.execute(sql, val)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
            return {"status": "Failed. Is the data provided correct?"}

        # disconnect from server
        db.close()
        # note, you can put a comma and then follow it with a status code of your choice. Handy for some stuff
        return {"status": "Completed"}, 201


    # DELETE can be used by someone to delete their own account or specific details, or for a level 1 person to delete them
    def delete(self):
        # verify fields
        args = journal_del_args.parse_args()
        # verify session
        if User.is_profile_api_key(args['session_token']) == False:
            return {"status": "failed. Invalid session token"}
        # log
        Protocols.debug_log(console_printout="Journal Delete Entry", user=User.is_profile_api_key(args['session_token']), command="000022", method_of_input="REST API")
        username = User.is_profile_api_key(args['session_token'])

        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=SQLUSERNAME, password=SQLPASSWORD, database=SQLDATABASE)
            cursor = db.cursor()
            # Execute the SQL command
            sql = "DELETE FROM JOURNAL WHERE PROFILE_ID = '" + username + "' AND DATE = '" + args['date'] + "%'"
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
            return {"status": "Failed. Most likely means the entry does not exist or bad input."}
        return {"status": "Completed"}


    # PATCH can update any user field and allows level 1 updating of any user information
    def patch(self):
        # verify fields
        args = journal_get_args.parse_args()
        # verify session
        if User.is_profile_api_key(args['session_token']) == False:
            return {"status": "failed. Invalid session token"}

        # log
        Protocols.debug_log(console_printout="Update Profile", user=User.is_profile_api_key(args['session_token']), command="000034", method_of_input="REST API")
        return {"status": "Code will go here, but this returned correctly?"}