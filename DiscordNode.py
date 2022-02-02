"""
DiscordNode.py Version 0.5.
Author: PixlFlip
Date: Jan 6, 2022

This update streamlines Profile lookup, prevents
unauthorized use, and is now robust
enough to be used in any server, public or private.
"""

import wikipedia
import discord
from Functions import User, Protocols, Email, UserData

# All key (read top level) variables here
SETTINGS = Protocols.Settings()
TOKEN = SETTINGS.discordBotToken
PREFIX = '/'
currentDirectory = SETTINGS.currentDirectory
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
        # return if no prefix to command. Saves tons of processing power
        if not message.content.startswith(PREFIX):
            return  # we know its a command now
        # check if user profile exists and return if no profile
        if not User.isProfileDiscord(str(message.author)):
            await message.channel.send('You are not authorized to access my commands. NEW UPDATE LOSER!', delete_after=30)
            return  # we know the profile exists now
        # load the profile of the user into key variable
        PROFILE = User.Profile(User.getProfileUsernameDiscord(str(message.author)))
        # log the command and who did it for diagnosis
        Protocols.debugLog(User.getProfileUsernameDiscord(str(message.author)), (message.content.split(" ")[0]), "Discord")


        # ============================ Basics ============================
        # ping command
        if message.content == (PREFIX + 'ping'):
            await message.channel.send('pong', delete_after=10)
        # TODO figure out why this doesn't work. Should import all from csv file...
        if message.content == (PREFIX + 'parady'):
            Protocols.establish_parady_user(User.getProfileUsernameDiscord(str(message.author)), SETTINGS.sqlUsername, SETTINGS.sqlPassword, SETTINGS.sqlDatabase)
            await message.channel.send('parady achieved', delete_after=10)
        # help command
        if message.content == (PREFIX + 'help'):
            # delete user message
            await client.delete_message(message)
            # open discord help file
            file = open(currentDirectory + '/Data/discordhelp.txt')
            returnList = ""
            for line in file:
                returnList += line
            await message.channel.send(returnList)

        # ============================       Email      ==============================
        if message.content.startswith(PREFIX + 'email'):
            # set channel to same as one command issued in
            channel = message.channel
            # warn them about security but send it anyway
            await message.channel.send('This is a Level 2 Command meaning potentially sensitive data is involved.\n For your security this message will be deleted shortly after send.\n Also for security it is recommended you do this in DM.',delete_after=120)
            # ask for and interpret sub command
            await message.channel.send('What would you like to do with email?')
            subCommand1 = await client.wait_for('message')
            subCommand2 = subCommand1.content + " email "
            intentCommand = Protocols.findIntentFromText(subCommand2)
            # 12 meaning they want to view inbox.
            if intentCommand == 12:
                # verify permissions and get email + password
                if User.isProfileDiscord(str(message.author)):
                    # ask user for password for security
                    await message.channel.send('Please Enter Your Password: ', delete_after=120)
                    userSubmittedPassword = await client.wait_for('message')
                    if userSubmittedPassword.content == PROFILE.password:
                        # with that out of the way we can get the inbox
                        # get inbox
                        inbox = str(Email.userViewGetInbox(PROFILE.defaultEmail, PROFILE.defaultEmailPassword))
                        # Return the entry and related information and delete after 120 seconds for security
                        await channel.send(" " + inbox, delete_after=120)
                    else:
                        await channel.send("Invalid Password for account. Access Denied.", delete_after=120)
                else:
                    # Failed to find profile
                    await channel.send('Profile for Discord Tag ' + (str(message.author)) + ' not found. You must be authorized to use this command.', delete_after=120)

            # 1 entered meaning they want to send an email.
            elif intentCommand == 1:
                # verify permissions and get email + password
                if User.isProfileDiscord(str(message.author)):
                    # get profile
                    PROFILE = User.Profile(User.getProfileUsernameDiscord(str(message.author)))
                    # ask user for password for security
                    await message.channel.send('Please Enter Your Password: ', delete_after=120)
                    userSubmittedPassword = await client.wait_for('message')
                    if userSubmittedPassword.content == PROFILE.password:

                        # ask user for what information we want
                        await channel.send("Please Enter the Email You Are Sending To: ", delete_after=120)
                        recieverEmail = await client.wait_for('message')
                        await channel.send("Please Enter the Email Subject: ", delete_after=120)
                        emailSubject = await client.wait_for('message')
                        await channel.send("Please Enter the Email Body: ", delete_after=120)
                        body = await client.wait_for('message')

                        # finally send the email
                        Email.sendEmail(PROFILE.defaultEmail, PROFILE.defaultEmailPassword, PROFILE.defaultEmail, recieverEmail.content, emailSubject.content, body.content)
                        # tell the user we managed to somehow do our job
                        await channel.send("Email sent. Consider deleting your message to preserve your privacy and keep it off Discord's servers.", delete_after=120)
                    else:
                        await channel.send("Invalid Password for account. Access Denied.", delete_after=120)
                else:
                    # Failed to find profile
                    await channel.send('Profile for Discord Tag ' + (str(message.author)) + ' not found. You must be authorized to use this command.', delete_after=120)
            else:
                # no valid option chosen
                await channel.send('Invalid Option. Please Specify Sub Command:\n 1 | View Inbox\n 2 | Send Email', delete_after=120)

        # ============================      Journal     ==============================
        if message.content.startswith(PREFIX + 'journal'):
            # set channel to same as one command issued in
            channel = message.channel
            # ask for and interpret sub command
            await message.channel.send('What would you like to do with your journal?')
            subCommand1 = await client.wait_for('message')
            subCommand2 = subCommand1.content + " journal "
            # send to parser with a little extra journal just to ensure it marks it as a journal command
            intentCommand = Protocols.findIntentFromText(subCommand2)
            # import journal object for use
            userJournal = PROFILE.journal
            # 3 entered meaning they want to view entry
            if intentCommand == 3:
                # parse next part for a date
                await channel.send('Input Date Of Entry You Want to View Using the Format YYYY-MM-DD (include the - )')
                getDate = await client.wait_for('message')
                date = getDate.content
                # check if the entry exists
                if userJournal.is_entry(date):
                    # Get the entry
                    entry = userJournal.get_entry(date)
                    # Return the entry and related information and delete after 120 seconds for security
                    await channel.send('Entry for the Date ' + date + ': \n' + entry.entry, delete_after=120)
                else:
                    # return error to user
                    await channel.send('Invalid Date. Try again using the format YYYY-MM-DD (include the - )')
            # 2 entered meaning new entry
            if intentCommand == 31:
                # format all remaining information in the message and store in variable
                getEntry = await client.wait_for('message')
                entry = getEntry.content
                # add the entry
                userJournal.add_entry(entry.replace("\n", ""), "DiscordClient")
                # tell the user the entry was recorded
                await channel.send('Entry Recorded.')
            # send message to channel if no other data given
            else:
                await channel.send('Invalid Option. Please Specify Sub Command:\n 1 | View Entry\n 2 | Add Entry')

        # ============================       Notes      ==============================
        # TODO integrate new note functionality here

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

        # ===================== Dynamic Command =====================
        # reads intent from message provided to it using intent manager or neural network.


client = MyClient()

client.run(TOKEN)
