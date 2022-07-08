from flask_restful import Resource, reqparse

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
        # load profile from session token
        PROFILE = User.Profile(User.is_profile_api_key(args['session_token']))
        # log
        Protocols.debug_log(console_printout="Journal View Entry", user=User.is_profile_api_key(args['session_token']), command="000020", method_of_input="REST API")

        # Get the entry
        entry = PROFILE.journal.get_entry(args['date'])
        # build json to return
        return {"date": entry.date, "entry": entry.entry, "starred": entry.starred,
                "creation_device": entry.creationDevice, "timezone": entry.timeZone}, 201

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