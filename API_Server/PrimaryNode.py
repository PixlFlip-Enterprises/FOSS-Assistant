"""
DiscordNode.py Version 0.8
Author: PixlFlip
Date: May 23, 2022

Basically a 2.0 but regardless here it is.
Queries in JSON (finally) and major revamp in general.
"""
import os, shutil, socket, wikipedia, json
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

port = 8008
# create a server at ip and port listed
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('0.0.0.0', port))

serv.listen()
# TODO make this display the proper IP being used by the device
print("Startup Complete. Listening on port " + str(port) + " at IP 0.0.0.0")
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
        '''welcome to the code I haven't done yet. This area needs an api table and a few rapid fire calls to sql. It is
        imperative that the calls be hardened to sql injection so the api cannot be easily exploited. Have fun future me'''
        # valid api key so begin acting on command_id

        # hello world/testing api command
        if query['command_id'] == '1':
            Protocols.debug_log("API is working correctly", "NONE", "1", "API")
        # journal
        elif query['command_id'] == '2':
            print("value 2")

        res = bytes("string json reply here", 'utf-8')
        conn.send(res)
    conn.close()
    print("= Client Successfully Disconnected")

