import os, shutil, socket, wikipedia, json
from API_Server.Functions import Protocols, Music, User, Email

# Top level variables
Protocols.loadStartupParameters()
SETTINGS = Protocols.Settings()
currentDirectory = SETTINGS.currentDirectory

"""All of the code in this entire file has to be reworked and I do mean all. Integrate database use, add new
method for getting user input before running, move to a json format(?), streamline the error handling, 
modify the variable calls, and makeall of it use multitasking like discord node.

Added note May 3: Moving to a JSON message format, document that new API, and make this the api server that
all others call. Simple, sleek, and uniform. """

# Music.playVoice("/Functions/ProgramData/Voice/startup.wav")
print("============================================================================")
print("                          FOSS Assistant V" + SETTINGS.version)
print("============================================================================")

port = 8008
# create a server at ip and port listed
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('0.0.0.0', port))

serv.listen()
# TODO make this display the proper IP being used by the device
print("= Startup Complete. Listening on port " + str(port) + " at IP 0.0.0.0")
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
        # format data
        # V2 Format     usr,pass,device:commandID:commandArg1,commandArg2,etc.
        request = Protocols.byteToStr(data)

        requestingDevice = request[0][2]
        # log to console for ease of seeing what's going on
        Protocols.debugLog(request[0][0], request[1][0], request[0][2])

        # User Login
        if not User.isProfile(request[0][0]): break

        # profile
        profile = User.Profile(request[0][0])

        # Process Request
        # TODO add arg to base command to basically let it tell if the command num is already there
        command = Protocols.findIntentFromText(request[1][0])
        # yeah... i kinda cut corners here but it all still works so whatever
        commandAndArgs = [""] + request[2]

        if command == 1:
            sendAddress = commandAndArgs[1]
            emailTitle = commandAndArgs[2]
            emailBody = commandAndArgs[3]
            Email.sendEmail(profile.defaultEmail, profile.defaultEmailPassword, profile.defaultEmail, sendAddress, emailTitle, emailBody)
            returnToClient = "Message sent."

            # return simplified version of topic from wikipedia
        elif command == 2:
            returnToClient = wikipedia.summary(commandAndArgs[1])

            # add entry to Journal
        elif command == 3:
            returnToClient = "Journal Entry Recorded."

        elif command == 4:
            # os.system('python3 hello.py')
            returnToClient = "bomb indeed"

            # download youtube link to memory
        elif command == 5:
            commandAndArgs.pop(0)
            # download the videos
            # Protocols.youtubeVideoDownload(commandAndArgs)
            # return message
            returnToClient = "Youtube Video(s) Downloaded"

        elif command == 6:
            # the heck was this even meant to do??
            returnToClient = "Uh, test of help on a line, by line basis., I've got nothing here figure it out."

        elif command == 7:
            # rickroll
            returnToClient = "Get Rickrolled!"
            res = bytes(returnToClient, 'utf-8')
            conn.send(res)
            conn.close()
            # removed for copyright reasons
            break

        elif command == 8:
            # play all music
            returnToClient = "Playing All Music In Database"
            res = bytes(returnToClient, 'utf-8')
            conn.send(res)
            conn.close()
            queue = Music.queueAll(SETTINGS.musicDirectory)
            Music.playQueue(queue)
            break

        elif command == 9:
            # create backup at destination folder
            returnToClient = "Backing Up Database"
            res = bytes(returnToClient, 'utf-8')
            conn.send(res)
            conn.close()

            # path to source directory
            src_dir = 'Data'
            # path to destination directory
            dest_dir = commandAndArgs[1] + '/backup'
            # getting all the files in the source directory
            files = os.listdir(src_dir)
            shutil.copytree(src_dir, dest_dir)
            break

        elif command == 10:
            break

        else:
            returnToClient = "Invalid Format or Error in Command."

        res = bytes(returnToClient, 'utf-8')
        conn.send(res)
    conn.close()
    print("= Client Successfully Disconnected")