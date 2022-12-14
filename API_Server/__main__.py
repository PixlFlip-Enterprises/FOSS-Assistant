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
from core_utilities.rest_resources import *
from core_utilities import journal, notes, finance
import json

'''
aniso8601==8.0.0
click==7.1.2
Flask==1.1.2
Flask-RESTful==0.3.8
Flask-SQLAlchemy==2.4.3
itsdangerous==1.1.0
Jinja2==2.11.2
MarkupSafe==1.1.1
pytz==2020.1
six==1.15.0
SQLAlchemy==1.3.18
Werkzeug==1.0.1
'''

# load config
config = json.load(open('config.json',))

print(" ________ ________  ________   ________           ________  ________   ________  ___  ________  _________  ________  ________   _________ ")
print("|\  _____\\\   __  \|\   ____\ |\   ____\         |\   __  \|\   ____\ |\   ____\|\  \|\   ____\|\___   ___\\\   __  \|\   ___  \|\___   ___\ ")
print("\ \  \__/\ \  \|\  \ \  \___|_\ \  \___|_        \ \  \|\  \ \  \___|_\ \  \___|\ \  \ \  \___|\|___ \  \_\ \  \|\  \ \  \\\ \  \|___ \  \_| ")
print(" \ \   __\\\ \  \\/\\  \ \_____  \\\ \_____  \        \ \   __  \ \_____  \\\ \_____  \ \  \ \_____  \   \ \  \ \ \   __  \ \  \\\ \  \   \ \  \ ")
print("  \ \  \_| \ \  \\/\\  \|____|\  \\\|____|\  \        \ \  \ \  \|____|\  \\\|____|\  \ \  \|____|\  \   \ \  \ \ \  \ \  \ \  \\\ \  \   \ \ \ ")
print("   \ \__\   \ \_______\____\_\  \ ____\_\  \        \ \__\ \__\____\_\  \ ____\_\  \ \__\____\_\  \   \ \__\ \ \__\ \__\ \__\\\ \__\   \ \__\ ")
print("    \|__|    \|_______|\_________\\\_________\        \|__|\|__|\_________\\\_________\|__|\_________\   \|__|  \|__|\|__|\|__| \|__|    \|__| ")
print("                      \|_________\|_________|                 \|_________\|_________|   \|_________|                                         ")
print()
print("Running Version: 1.0.2")

# init flask restful api server
app = Flask(__name__)
api = Api(app)




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

api.add_resource(journal.Journal, "/journal/<string:profile_id>/")
api.add_resource(notes.Notes, "/notes/<string:profile_id>/")
api.add_resource(finance.Finance, "/finance/<string:profile_id>/")
api.add_resource(Profile, "/profile/")
# run program with debug, something you want to disable for production builds
app.run(debug=config['api_server_debug_mode'])

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
