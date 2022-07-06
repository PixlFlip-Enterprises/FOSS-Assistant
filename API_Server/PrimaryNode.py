"""
DiscordNode.py Version 0.8.2
Author: PixlFlip
Date: June 26, 2022

Getting very close to a full on Alpha.
Contacts, Journals, and SQL oh my.
"""
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

h_name = socket.gethostname()
IP_addres = socket.gethostbyname(h_name)

# todo have the port be one of the configurable settings?
port = 8008
# create a server at ip and port listed
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('0.0.0.0', port))

serv.listen()
print("Host Name is:   " + h_name)
print("Hosting At Address:   " + IP_addres + ":" + str(port))

# holding variable for returned json
return_json = '{"status": "Error", "error_info": "Not Specified"}'

# run this code forever
while True:
    # I have no idea what this code does
    conn, addr = serv.accept()
    while True:
        # receive data from client on connect
        data = conn.recv(4096)
        # data = conn.recv(1024)
        # verify data
        if not data: break
        # protect against sql injection
        query = query.__replace__()
        # parse json
        try:
            query = json.loads(data.decode())
        except:
            return_json = '{"status": "Error", "error_info": "Invalid JSON Unable To Parse"}'
            break
        # verify api_key exists
        if not 'api_key' in query:
            print("No API Key Provided in Query")
            break
        # verify command_id exists
        if not 'command_id' in query:
            print("No API Key Provided in Query")
            break
        # both exist so now verify valid api key
        if User.is_profile_api_key(query['api_key']) == False:
            print("Invalid API Key Provided in Query")
            break
        # valid api key so grab user profile
        username = User.is_profile_api_key(query['api_key'])
        PROFILE = User.Profile(username)

        # All commands. Literally all of them

        # hello world/testing api command
        if query['command_id'] == '000010':
            Protocols.debug_log(console_printout="API Test", user=username, command="000001", method_of_input="API")
            return_json = '{"status": "Completed"}'
            break

        # verify identity from discord application
        elif query['command_id'] == '000011':
            # log
            Protocols.debug_log(console_printout="ID Check", user=username, command="000011", method_of_input="API")
            # verify fields
            if not 'discord_id' in query:
                print("Invalid Data in Query")
                break
            # check discord id
            if not User.isProfileDiscord(query['discord_id']):
                return_json = '{"status": "Completed", "is_valid_id": "False"}'
                break
            # valid id so return relevant information
            user_key = User.get_profile_api_key(User.getProfileUsernameDiscord(query['discord_id']))
            # returned json
            return_json = '{"status": "Completed", "is_valid_id": "True", "api_key": "' + user_key + '", "user": "' + User.getProfileUsernameDiscord(query['discord_id']) + '"}'
            break

        # simple wikipedia information grab
        elif query['command_id'] == '000012':
            # log
            Protocols.debug_log(console_printout="Wikipedia Search", user=username, command="000011", method_of_input="API")
            # todo finish this code

        # journal view entry
        elif query['command_id'] == '000020':
            # log
            Protocols.debug_log(console_printout="Journal View Entry", user=username, command="000020", method_of_input="API")
            # verify fields
            if not 'date' in query:
                print("Invalid Data in Query")
                break
            # ensure exists
            if not PROFILE.journal.is_entry(query['date']):
                print("Incorrect Date or Format for Command ID 000020")
                break
            # Get the entry
            entry = PROFILE.journal.get_entry(query['date'])
            # build json to return
            return_json = '{"date": "' + entry.date + '", "entry": "' + entry.entry + '", "starred":"' + entry.starred + '", "creation_device":"' + entry.creationDevice + '", "timezone":"' + entry.timeZone + '"}'
            break

        # journal view entry
        elif query['command_id'] == '000021':
            # log
            Protocols.debug_log(console_printout="Journal Create Entry", user=username, command="000021", method_of_input="API")
            # verify fields
            # todo for now date is unused, but should be someday preferably
            verifable_fields = ['date', 'entry', 'creation_device', 'starred', 'timezone']
            no_field_kill = False
            for field in verifable_fields:
                if not field in query:
                    print("Invalid Data in Query")
                    no_field_kill = True
            if no_field_kill:
                break
            # save journal entry to database
            PROFILE.journal.add_entry(query['entry'], query['creation_device'], query['starred'], query['timezone'])
            # build json to return
            return_json = '{"status": "Completed"}'
            break

        # add base contact information
        elif query['command_id'] == '000030':
            # log
            Protocols.debug_log(console_printout="Add Base Contact", user=username, command="000030", method_of_input="API")
            # verify fields (all of them)
            verifable_fields = ['f_name', 'l_name', 'display_name', 'nickname', 'email_address', 'email_address2',
                                'email_address3', 'home_phone', 'business_phone', 'home_fax', 'business_fax',
                                'pager', 'mobile_phone', 'home_address', 'home_address2', 'home_city', 'home_state',
                                'home_postal_code', 'home_street', 'business_address', 'business_address2',
                                'business_city', 'business_state', 'business_postal', 'business_country', 'country_code',
                                'related_names', 'job', 'department', 'organization', 'notes', 'birthday', 'anniversary',
                                'gender', 'website', 'website2', 'categories', 'sociological_options', 'social_media',
                                'discord', 'personality_rating', 'trust_score', 'known_since']
            no_field_kill = False
            for field in verifable_fields:
                if not field in query:
                    print("Invalid Data in Query")
                    no_field_kill = True
            if no_field_kill:
                break
            # save contact to database
            PROFILE.contacts.create_contact(query['f_name'], query['l_name'], query['display_name'], query['nickname'], query['email_address'],
                                            query['email_address2'], query['email_address3'], query['home_phone'], query['business_phone'],
                                            query['home_fax'], query['business_fax'], query['pager'], query['mobile_phone'], query['home_address'],
                                            query['home_address2'], query['home_city'], query['home_state'], query['home_postal_code'],
                                            query['home_street'], query['business_address'], query['business_address2'], query['business_city'],
                                            query['business_state'], query['business_postal'], query['business_country'], query['country_code'],
                                            query['related_names'], query['job'], query['department'], query['organization'], query['notes'],
                                            query['birthday'], query['anniversary'], query['gender'], query['website'], query['website2'],
                                            query['categories'], query['sociological_options'], query['social_media'], query['discord'],
                                            query['personality_rating'], query['trust_score'], query['known_since'])
            # build json to return
            return_json = '{"status": "Completed"}'
            break

        # get news from database
        elif query['command_id'] == '000040':
            print("will get news someday")

    # encode, send, close connection, reset
    res = bytes(return_json, 'utf-8')
    conn.send(res)
    conn.close()
    return_json = '{"status": "Error", "error_info": "Not Specified"}'
    print("API Call Completed")

