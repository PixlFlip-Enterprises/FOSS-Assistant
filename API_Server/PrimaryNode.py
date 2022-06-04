"""
DiscordNode.py Version 0.8.1
Author: PixlFlip
Date: June 2, 2022

Getting very close to a full on Alpha.
"""
import os, shutil, socket, wikipedia, json, ssl
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
        # data = conn.recv(4096)
        data = conn.recv(1024)
        # verify data
        if not data: break
        # todo current version is vulnerable to sql injection attacks. Can be easily fixed so do it here before data is used
        # parse json
        query = json.loads(data.decode())
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


    # encode, send, close connection, reset
    res = bytes(return_json, 'utf-8')
    conn.send(res)
    conn.close()
    return_json = '{"status": "Error", "error_info": "Not Specified"}'
    print("API Call Completed")

