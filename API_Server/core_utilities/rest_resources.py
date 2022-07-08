from flask_restful import Resource, reqparse
from datetime import datetime
import pymysql as MySQLdb
# todo this should be gone and be fully functional as a package.
from API_Server.Functions import Protocols, User, Email

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
journal_get_args.add_argument("session_token", type=str, help="Token from valid session. Expired token?", required=True)
journal_put_args.add_argument("date", type=str, help="Date of journal entry", required=False)
journal_put_args.add_argument("entry", type=str, help="Journal entry", required=True)
journal_put_args.add_argument("creation_device", type=str, help="Device created on", required=True)
journal_put_args.add_argument("starred", type=bool, help="Favorited or not", required=True)
journal_put_args.add_argument("timezone", type=str, help="Timezone created in", required=True)


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
            return {"status": "failed. Invalid session token"}
        # load profile from session token
        PROFILE = User.Profile(User.is_profile_api_key(args['session_token']))
        # log
        Protocols.debug_log(console_printout="Journal View Entry", user=User.is_profile_api_key(args['session_token']), command="000020", method_of_input="REST API")
        # save journal entry to database
        PROFILE.journal.add_entry(args['entry'], args['creation_device'], args['starred'], args['timezone'])
        # note, you can put a comma and then follow it with a status code of your choice. Handy for some stuff
        return {"status": "Completed"}, 201