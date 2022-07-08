"""
__main__.py Version 1.0.0
Author: PixlFlip
Date: July 07, 2022

An Alpha, and one Chad coder to boot!
"""
# flask for rest server init
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
# other imports
import os, shutil, socket, json, ssl
from Functions import Protocols, User, Email

# Top variables
SETTINGS = Protocols.Settings()
SQLDATABASE = SETTINGS.sqlDatabase
SQLUSERNAME = SETTINGS.sqlUsername
SQLPASSWORD = SETTINGS.sqlPassword
currentDirectory = SETTINGS.currentDirectory
# Let's get some decoration and naming!
print(" ________ ________  ________   ________           ________  ________   ________  ___  ________  _________  ________  ________   _________ ")
print("|\  _____\\\   __  \|\   ____\ |\   ____\         |\   __  \|\   ____\ |\   ____\|\  \|\   ____\|\___   ___\\\   __  \|\   ___  \|\___   ___\ ")
print("\ \  \__/\ \  \|\  \ \  \___|_\ \  \___|_        \ \  \|\  \ \  \___|_\ \  \___|\ \  \ \  \___|\|___ \  \_\ \  \|\  \ \  \\\ \  \|___ \  \_| ")
print(" \ \   __\\\ \  \\/\\  \ \_____  \\\ \_____  \        \ \   __  \ \_____  \\\ \_____  \ \  \ \_____  \   \ \  \ \ \   __  \ \  \\\ \  \   \ \  \ ")
print("  \ \  \_| \ \  \\/\\  \|____|\  \\\|____|\  \        \ \  \ \  \|____|\  \\\|____|\  \ \  \|____|\  \   \ \  \ \ \  \ \  \ \  \\\ \  \   \ \ \ ")
print("   \ \__\   \ \_______\____\_\  \ ____\_\  \        \ \__\ \__\____\_\  \ ____\_\  \ \__\____\_\  \   \ \__\ \ \__\ \__\ \__\\\ \__\   \ \__\ ")
print("    \|__|    \|_______|\_________\\\_________\        \|__|\|__|\_________\\\_________\|__|\_________\   \|__|  \|__|\|__|\|__| \|__|    \|__| ")
print("                      \|_________\|_________|                 \|_________\|_________|   \|_________|                                         ")
print()
print("Running Version: " + SETTINGS.version)

# init flask restful api server
app = Flask(__name__)
api = Api(app)

########################################################################################################################
#                                                   JOURNAL RESOURCE
########################################################################################################################
# journal get args
journal_get_args = reqparse.RequestParser()
journal_get_args.add_argument("username", type=str, help="Username", required=True)
journal_get_args.add_argument("password", type=str, help="Password. Man I hope this is secure enough...", required=True)
journal_get_args.add_argument("date", type=str, help="Date of journal entry", required=True)
# journal put args
journal_put_args = reqparse.RequestParser()
journal_put_args.add_argument("username", type=str, help="Username", required=True)
journal_put_args.add_argument("password", type=str, help="Password. Man I hope this is secure enough...", required=True)
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
        # log
        Protocols.debug_log(console_printout="Journal View Entry", user=args['username'], command="000020",
                            method_of_input="REST API")
        # todo add a password check for what should be obvious reasons
        PROFILE = User.Profile(args['username'])
        # Get the entry
        entry = PROFILE.journal.get_entry(args['date'])
        # build json to return
        return {"date": entry.date, "entry": entry.entry, "starred": entry.starred,
                "creation_device": entry.creationDevice, "timezone": entry.timeZone}, 201

    def put(self):
        args = journal_put_args.parse_args()
        # log
        Protocols.debug_log(console_printout="Journal Create Entry", user=args['username'], command="000021",
                            method_of_input="REST API")
        # todo add a password check for what should be obvious reasons
        PROFILE = User.Profile(args['username'])
        # save journal entry to database
        PROFILE.journal.add_entry(args['entry'], args['creation_device'], args['starred'], args['timezone'])
        # note, you can put a comma and then follow it with a status code of your choice. Handy for some stuff
        return {"status": "Completed"}, 201


# create a resource for our web server to utilize
class HelloWorld(Resource):
    def get(self, name, age):
        return {"data": "Hello " + name + "!!!", "testingsecondvar": age}

    def put(self):
        return {"data": "Hello!!!", "testingsecondvar": "9"}

    def delete(self):
        return {"data": "Hello!!!", "testingsecondvar": "9"}


# add resources to api
api.add_resource(HelloWorld, "/hello/hello2/<string:name>/<int:age>")
api.add_resource(Journal, "/journal/")
# run program with debug, something you want to disable for production builds
app.run(debug=True)

#     # All commands. Literally all of them
#
#     # hello world/testing api command
#     if query['command_id'] == '000010':
#         Protocols.debug_log(console_printout="API Test", user=username, command="000001", method_of_input="API")
#         return_json = '{"status": "Completed"}'
#         break
#
#     # verify identity from discord application
#     elif query['command_id'] == '000011':
#         # log
#         Protocols.debug_log(console_printout="ID Check", user=username, command="000011", method_of_input="API")
#         # verify fields
#         if not 'discord_id' in query:
#             print("Invalid Data in Query")
#             break
#         # check discord id
#         if not User.isProfileDiscord(query['discord_id']):
#             return_json = '{"status": "Completed", "is_valid_id": "False"}'
#             break
#         # valid id so return relevant information
#         user_key = User.get_profile_api_key(User.getProfileUsernameDiscord(query['discord_id']))
#         # returned json
#         return_json = '{"status": "Completed", "is_valid_id": "True", "api_key": "' + user_key + '", "user": "' + User.getProfileUsernameDiscord(query['discord_id']) + '"}'
#         break
#
#     # simple wikipedia information grab
#     elif query['command_id'] == '000012':
#         # log
#         Protocols.debug_log(console_printout="Wikipedia Search", user=username, command="000011", method_of_input="API")
#         # todo finish this code
#
#     # add base contact information
#     elif query['command_id'] == '000030':
#         # log
#         Protocols.debug_log(console_printout="Add Base Contact", user=username, command="000030", method_of_input="API")
#         # verify fields (all of them)
#         verifable_fields = ['f_name', 'l_name', 'display_name', 'nickname', 'email_address', 'email_address2',
#                             'email_address3', 'home_phone', 'business_phone', 'home_fax', 'business_fax',
#                             'pager', 'mobile_phone', 'home_address', 'home_address2', 'home_city', 'home_state',
#                             'home_postal_code', 'home_street', 'business_address', 'business_address2',
#                             'business_city', 'business_state', 'business_postal', 'business_country', 'country_code',
#                             'related_names', 'job', 'department', 'organization', 'notes', 'birthday', 'anniversary',
#                             'gender', 'website', 'website2', 'categories', 'sociological_options', 'social_media',
#                             'discord', 'personality_rating', 'trust_score', 'known_since']
#         no_field_kill = False
#         for field in verifable_fields:
#             if not field in query:
#                 print("Invalid Data in Query")
#                 no_field_kill = True
#         if no_field_kill:
#             break
#         # save contact to database
#         PROFILE.contacts.create_contact(query['f_name'], query['l_name'], query['display_name'], query['nickname'], query['email_address'],
#                                         query['email_address2'], query['email_address3'], query['home_phone'], query['business_phone'],
#                                         query['home_fax'], query['business_fax'], query['pager'], query['mobile_phone'], query['home_address'],
#                                         query['home_address2'], query['home_city'], query['home_state'], query['home_postal_code'],
#                                         query['home_street'], query['business_address'], query['business_address2'], query['business_city'],
#                                         query['business_state'], query['business_postal'], query['business_country'], query['country_code'],
#                                         query['related_names'], query['job'], query['department'], query['organization'], query['notes'],
#                                         query['birthday'], query['anniversary'], query['gender'], query['website'], query['website2'],
#                                         query['categories'], query['sociological_options'], query['social_media'], query['discord'],
#                                         query['personality_rating'], query['trust_score'], query['known_since'])
#         # build json to return
#         return_json = '{"status": "Completed"}'
#         break
#
#     # get news from database
#     elif query['command_id'] == '000040':
#         print("will get news someday")
#
# # encode, send, close connection, reset
# res = bytes(return_json, 'utf-8')
# conn.send(res)
# conn.close()
# return_json = '{"status": "Error", "error_info": "Not Specified"}'
# print("API Call Completed")
