import wikipedia
import discord
import os
from Functions import User, Journal, Protocols, Email

# All key (read top level) variables here
TOKEN = ""
PREFIX = '/'
currentDirectory = os.getcwd()
# End Key Variables ======================


class MyClient(discord.Client):
    # Startup Bot
    async def on_ready(self):
        print('Logged on as', self.user)

    # Runs When Message is Sent that is Visible to Bot
    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        # log the command and who did it for diagnosis
        if message.content.startswith(PREFIX):
            Protocols.debugLog(User.getProfileUsernameDiscord(str(message.author)), (message.content.split(" ")[0]), "Discord")

        # ============================ Basics ============================
        # ping command
        if message.content == (PREFIX + 'ping'):
            await message.channel.send('pong', delete_after=10)

        # help command
        if message.content == (PREFIX + 'help'):
            # open discord help file
            file = open(currentDirectory + '/Data/discordhelp.txt')
            returnList = ""
            for line in file:
                returnList += line
            await message.channel.send(returnList)

        # timer command


        # ============================  Troll Commands  ============================
        if message.content == (PREFIX + 'submit'):
            await message.channel.send('I will not comply. Don\'t try /forcesubmit')

        if message.content == (PREFIX + 'forcesubmit'):
            await message.channel.send('You\'re an idiot.')

        # ============================      Email     ==============================
        if message.content.startswith(PREFIX + 'email'):
            # set channel to same as one command issued in
            channel = message.channel
            # warn them about security but send it anyway
            await message.channel.send('This is a Level 2 Command meaning potentially sensitive data is involved.\n For your security this message will be deleted shorlty after send.\n Also for security it is recommended you do this in DM.', delete_after=120)
            # sub command value at 7

            # TODO Fix error handling for no variable at char 7 and fix inbox issue as a whole
            # 1 entered meaning they want to view inbox.
            if (message.content[7]) == '1':
                # verify permissions and get email + password
                if User.isProfileDiscord(str(message.author)):
                     # get profile
                     profile = User.Profile(User.getProfileUsernameDiscord(str(message.author)))
                     # get inbox
                     inbox = str(Email.userViewGetInbox(profile.defaultEmail, profile.defaultEmailPassword))
                     # Return the entry and related information and delete after 120 seconds for security
                     await channel.send(" " + inbox, delete_after=120)
                else:
                    # Failed to find profile
                    await channel.send('Profile for Discord Tag ' + (str(message.author)) + ' not found. You must be authorized to use this command.')

            # 2 entered meaning they want to send an email.
            elif (message.content[7]) == '2':
                # verify permissions and get email + password
                if User.isProfileDiscord(str(message.author)):
                    # get profile
                    profile = User.Profile(User.getProfileUsernameDiscord(str(message.author)))
                    # split the entire freaking thing to get what we want
                    stuffWeNeed = message.content.split(" ")
                    # format should be receiver email, subject, then body
                    recieverEmail = stuffWeNeed[2]
                    emailSubject = stuffWeNeed[3]
                    # the rest is body so we can just stitch it back together. What a mess
                    body = ""
                    # pop out the junk
                    stuffWeNeed.pop(0)
                    stuffWeNeed.pop(0)
                    stuffWeNeed.pop(0)
                    stuffWeNeed.pop(0)
                    # combine the rest with spaces
                    for uselessAlone in stuffWeNeed:
                        body += (uselessAlone + " ")
                    # finally send the email
                    Email.sendEmail(profile.defaultEmail, profile.defaultEmailPassword, profile.defaultEmail, recieverEmail, emailSubject, body)
                    # tell the user we managed to somehow do our job
                    await channel.send("Email sent. Consider deleting your message to preserve your privacy and keep it off Discord's servers.", delete_after=120)
                else:
                    # Failed to find profile
                    await channel.send('Profile for Discord Tag ' + (str(message.author)) + ' not found. You must be authorized to use this command.')
            else:
                # no valid option chosen
                await channel.send('Invalid Option. Please Specify Sub Command:\n 1 | View Inbox\n 2 | Send Email')



        # ============================      Journal     ==============================
        if message.content.startswith(PREFIX + 'journal'):
            # set channel to same as one command issued in
            channel = message.channel
            # we know the command now parse sub command always at char value 9

            # 1 entered meaning they want to view entry
            if (message.content[9]) == '1':
                # parse next part for a date
                # return entry of matching user and date
                date = message.content[11:]
                # check if a profile exists
                if User.isProfileDiscord(str(message.author)):
                    # check if the entry exists
                    if Journal.isEntry(date, User.getProfileUsernameDiscord(str(message.author))):
                        # Get the entry
                        entry = Journal.getFullEntry(date, User.getProfileUsernameDiscord(str(message.author)))
                        # Return the entry and related information and delete after 120 seconds for security
                        await channel.send('Entry for the Date ' + date + ': \n' + entry[1], delete_after=120)
                    else:
                        # return error to user
                        await channel.send('Invalid Date. Try again using the format YYYY-MM-DD (include the - )')
                else:
                    # Failed to find profile
                    await channel.send('Profile for Discord Tag ' + (str(message.author)) + ' not found. You must be authorized to use this command.')

            # 2 entered meaning new entry
            elif (message.content[9]) == '2':
                # format all remaining information in the message and store in variable
                entry = message.content[11:]
                # check if a profile exists
                if User.isProfileDiscord(str(message.author)):
                    # add the entry
                    Journal.addBasicEntry(entry, "DiscordClient", User.getProfileUsernameDiscord(str(message.author)))
                    # tell the user the entry was recorded
                    await channel.send('Entry Recorded.')
                else:
                    # Failed to find profile
                    await channel.send('Profile for Discord Tag ' + (str(message.author)) + ' not found. You must be authorized to use this command.')

            # send message to channel if no other data given
            else:
                await channel.send('Invalid Option. Please Specify Sub Command:\n 1 | View Entry\n 2 | Add Entry')

        # ===================== Greet =====================
        if message.content.startswith('/greet'):
            channel = message.channel
            await channel.send('Say hello!')

            def check(m):
                return m.content == 'hello' and m.channel == channel

            msg = await client.wait_for('message', check=check)
            await channel.send('Hello {.author}!'.format(msg))

        # ===================== Wikipedia =====================
        # takes message, looks for a match on wikipedia, and returns article summary
        if message.content.startswith(PREFIX + 'wiki'):
            # substring extract user query, pass to wikipedia, and return summary
            try:
                summary = wikipedia.summary(message.content[6:], 7)
                await message.channel.send('Wikipedia Top Result: ' + summary)
            except:
                await message.channel.send('No Data Found From Wikipedia')

        # DYNAMIC COMMANDS (READING INTENT WITH NEUTRAL NET AND/OR KEYWORDS)


client = MyClient()

client.run(TOKEN)
