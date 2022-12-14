from random import randint

from flask_restful import Resource, reqparse
from datetime import datetime
import pymysql as MySQLdb
import json
from API_Server.core_utilities import core_functions

# load config
config = json.load(open('config.json',))

########################################################################################################################
#                                                   PROFILE RESOURCE
########################################################################################################################
# profile get args
profile_get_args = reqparse.RequestParser()
profile_get_args.add_argument("session_token", type=str, help="Token from valid session. Expired token?", required=True)
profile_get_args.add_argument("username", type=str, help="Name of the user profile", required=False)
profile_get_args.add_argument("discord", type=str, help="Discord of user", required=False)
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
        if core_functions.is_profile_api_key(args['session_token']) == False:
            return {"status": "failed. Invalid session token"}
        # if discord id given, see if exists and return data based on clearance level
        usr = core_functions.is_profile_api_key(args['session_token'])  # starting value
        for identifier in args.keys():
            if identifier == 'username':
                # we know a username was provided
                usr = args['username']
            elif identifier == 'discord':
                # we know a discord id was provided, so a little more legwork is involved
                usr = core_functions.getProfileUsernameDiscord(args['discord'])

        # check clearance level of user
        clearance_level = 3
        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=config['sql_username'], password=config['sql_password'], database=config['sql_database'])
            cursor = db.cursor()
            # Execute the SQL command
            cursor.execute("select CLEARANCE_LEVEL from PROFILES where USER LIKE '" + core_functions.is_profile_api_key(args['session_token']) + "';")
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
            db = MySQLdb.connect(host="localhost", user=config['sql_username'], password=config['sql_password'], database=config['sql_database'])
            cursor = db.cursor()
            # Execute the SQL command
            cursor.execute("select * from PROFILES where USER LIKE '" + usr + "';")
            # get all records
            records = cursor.fetchall()
            # first is entry
            try:
                requested_profile = records[0]
            except:
                return {"status": "Failed.", "error_msg": "The profile does not exist."}, 404
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
        if core_functions.is_profile_api_key(args['session_token']) == False:
            return {"status": "Failed. Invalid session token"}

        username = core_functions.is_profile_api_key(args['session_token'])
        # todo edit for actual profile data
        x = datetime.now().__str__().replace(" ", "")
        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=config['sql_username'], password=config['sql_password'], database=config['sql_database'])
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
        if core_functions.is_profile_api_key(args['session_token']) == False:
            return {"status": "failed. Invalid session token"}
        username = core_functions.is_profile_api_key(args['session_token'])

        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=config['sql_username'], password=config['sql_password'], database=config['sql_database'])
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
        if core_functions.is_profile_api_key(args['session_token']) == False:
            return {"status": "failed. Invalid session token"}

        return {"status": "Code will go here, but this returned correctly?"}

########################################################################################################################
#                                                   LOGIN RESOURCE
########################################################################################################################
# profile get args
login_get_args = reqparse.RequestParser()
login_get_args.add_argument("username", type=str, help="Username of your account.", required=True)
login_get_args.add_argument("password", type=str, help="Password of your account.", required=True)


# create login resource
class Login(Resource):

    # GET provides session key if username and password are correct
    def get(self):
        # verify fields
        args = profile_get_args.parse_args()
        profile = ''
        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=config['sql_username'], password=config['sql_password'], database=config['sql_database'])
            cursor = db.cursor()
            # Execute the SQL command
            cursor.execute("select * from PROFILES where USER LIKE '" + args['username'] + "' AND PASSWORD = '" + args['password'] + "';")
            # get record
            profile = cursor.fetchone()
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        print(profile)
        if not profile[2] == args['password']:
            return {"status": "Failed", "error_msg": "Incorrect password. Are you a dirty hacker?"}, 201
        # correct password so return data
        # todo this needs to be better
        session_token = 0
        for i in 50:
            session_token += randint(1, 100)
        # update session token list in database and set to expire in 24 hours

        return {"status": "Completed", "session_token": session_token }


########################################################################################################################
#                                                   FINANCE RESOURCE
########################################################################################################################
# finance get args
finance_get_args = reqparse.RequestParser()
finance_get_args.add_argument("session_token", type=str, help="Token from valid session. Expired token?", required=True)
finance_get_args.add_argument("date", type=str, help="Date of finance entry", required=True)
finance_get_args.add_argument("device_id", type=str, help="Device created on", required=False)

# finance put args
finance_put_args = reqparse.RequestParser()
finance_put_args.add_argument("session_token", type=str, help="Token from valid session. Expired token?", required=True)
finance_put_args.add_argument("date", type=str, help="Date of finance entry", required=False)
finance_put_args.add_argument("title", type=str, help="finance entry", required=True)
finance_put_args.add_argument("memo", type=str, help="Device created on", required=False)
finance_put_args.add_argument("starred", type=str, help="Favorited or not", required=True)
# finance del args
finance_del_args = reqparse.RequestParser()
finance_del_args.add_argument("session_token", type=str, help="Token from valid session. Expired token?", required=True)
finance_del_args.add_argument("date", type=str, help="Date of finance entry to be deleted", required=True)


# create finance resource
class Finance(Resource):

    def get(self):
        # verify fields
        args = finance_get_args.parse_args()
        # verify session
        if core_functions.is_profile_api_key(args['session_token']) == False:
            return {"status": "failed. Invalid session token"}
        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=config['sql_username'], password=config['sql_password'], database=config['sql_database'])
            cursor = db.cursor()
            # Execute the SQL command
            cursor.execute("select * from FINANCE where PROFILE_ID LIKE '" + core_functions.is_profile_api_key(args['session_token']) + "' AND DATE LIKE '" + args['date'] + "%';")
            # get all records
            records = cursor.fetchall()
            # first is entry
            try:
                entry = records[0]
                # log
                core_functions.debug_log(user=core_functions.is_profile_api_key(args['session_token']), command_run="Finance View Entry", device_id=args['device_id'], command_id="000040", return_code="201")
                return {"status": "Completed.", "date": entry[2], "entry": entry[3], "starred": entry[5], "creation_device": entry[6], "timezone": entry[7]}, 201
            except:
                # log
                core_functions.debug_log(user=core_functions.is_profile_api_key(args['session_token']), command_run="Finance View Entry", device_id=args['device_id'], command_id="000040", return_code="404", debug_msg="Error while retrieving the entry")
                return {"status": "Failed. Entry does not exist"}
        except:
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        # return since entry doesn't exist
        core_functions.debug_log(user=core_functions.is_profile_api_key(args['session_token']), command_run="Finance View Entry", device_id=args['device_id'], command_id="000040", return_code="404", debug_msg="Entry was not found in the database")
        return {"status": "Failed. Entry does not exist"}


    def put(self):
        # verify fields
        args = finance_put_args.parse_args()
        # verify session
        if core_functions.is_profile_api_key(args['session_token']) == False:
            return {"status": "Failed.", 'error_msg': " Invalid session token"}

        username = core_functions.is_profile_api_key(args['session_token'])
        # log
        # todo add a thing in here to allow for arbitrary dates to be added instead of just the second the put is received
        x = datetime.now().__str__().replace(" ", "")
        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=config['sql_username'], password=config['sql_password'], database=config['sql_database'])
            cursor = db.cursor()
            # Execute the SQL command
            sql = "INSERT INTO FINANCE (OWNING_USER, DATE, TITLE, MEMO, DEPOSIT, AMOUNT, ACCOUNT_BALANCE) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            # TODO maths here
            val = (username, x, args['title'], args['memo'], args['deposit'], args['amount'], (int(args['amount']))-9)
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
        args = finance_del_args.parse_args()
        # verify session
        if core_functions.is_profile_api_key(args['session_token']) == False:
            return {"status": "failed. Invalid session token"}
        # log
        username = core_functions.is_profile_api_key(args['session_token'])

        try:
            # open the database
            db = MySQLdb.connect(host="localhost", user=config['sql_username'], password=config['sql_password'], database=config['sql_database'])
            cursor = db.cursor()
            # Execute the SQL command
            sql = "DELETE FROM finance WHERE PROFILE_ID = '" + username + "' AND DATE = '" + args['date'] + "%'"
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
            core_functions.debug_log(user=core_functions.is_profile_api_key(args['session_token']),
                                     command_run="finance Delete Entry", device_id=args['device_id'], command_id="000023",
                                     return_code="404", debug_msg="Failed to delete entry.")
            return {"status": "Failed. Most likely means the entry does not exist or bad input."}
        return {"status": "Completed"}


    def patch(self):
        # verify fields
        args = finance_get_args.parse_args()
        # verify session
        if core_functions.is_profile_api_key(args['session_token']) == False:
            return {"status": "failed. Invalid session token"}

        # log
        core_functions.debug_log(user=core_functions.is_profile_api_key(args['session_token']), command_run="finance Delete Entry", device_id=args['device_id'], command_id="000023", return_code="201", debug_msg="Entry was deleted.")
        return {"status": "Code will go here, but this returned correctly?"}