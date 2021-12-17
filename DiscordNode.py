import wikipedia
import discord
import os
from Functions import User, Journal, Protocols, Email

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
            await message.channel.send('When will you learn. Nuking Sweden...')

        # ============================      Email     ==============================
        if message.content.startswith(PREFIX + 'email'):
            # set channel to same as one command issued in
            channel = message.channel
            # warn them about security but send it anyway
            await message.channel.send('This is a Level 2 Command meaning potentially sensitive data is involved.\n For your security this message will be deleted shorlty after send.\n Also for security it is recommended you do this in DM.',delete_after=120)
            # ask for and interpret sub command
            await message.channel.send('What would you like to do with email?')
            subCommand1 = await client.wait_for('message')
            subCommand2 = subCommand1.content + " email "
            intentCommand = Protocols.findIntentFromText(subCommand2)
            # 12 meaning they want to view inbox.
            if intentCommand == 12:
                # verify permissions and get email + password
                if User.isProfileDiscord(str(message.author)):
                    # get profile
                    profile = User.Profile(User.getProfileUsernameDiscord(str(message.author)))
                    # ask user for password for security
                    await message.channel.send('Please Enter Your Password: ', delete_after=120)
                    userSubmittedPassword = await client.wait_for('message')
                    if userSubmittedPassword.content == profile.password:
                        # with that out of the way we can get the inbox
                        # get inbox
                        inbox = str(Email.userViewGetInbox(profile.defaultEmail, profile.defaultEmailPassword))
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
                    profile = User.Profile(User.getProfileUsernameDiscord(str(message.author)))
                    # ask user for password for security
                    await message.channel.send('Please Enter Your Password: ', delete_after=120)
                    userSubmittedPassword = await client.wait_for('message')
                    if userSubmittedPassword.content == profile.password:

                        # ask user for what information we want
                        await channel.send("Please Enter the Email You Are Sending To: ", delete_after=120)
                        recieverEmail = await client.wait_for('message')
                        await channel.send("Please Enter the Email Subject: ", delete_after=120)
                        emailSubject = await client.wait_for('message')
                        await channel.send("Please Enter the Email Body: ", delete_after=120)
                        body = await client.wait_for('message')

                        # finally send the email
                        Email.sendEmail(profile.defaultEmail, profile.defaultEmailPassword, profile.defaultEmail, recieverEmail.content, emailSubject.content, body.content)
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
            # warning about high level command
            await message.channel.send('This is a Level 2 Command meaning potentially sensitive data is involved.\n For your security this message will be deleted shorlty after send.\n Also for security it is recommended you do this in DM.', delete_after=120)
            # ask for and interpret sub command
            await message.channel.send('What would you like to do with your journal?')
            subCommand1 = await client.wait_for('message')
            # send to parser with a little extra journal just to ensure it marks it as a journal command
            subCommand2 = subCommand1.content + " journal "
            intentCommand = Protocols.findIntentFromText(subCommand2)
            # 1 entered meaning they want to view entry
            if intentCommand == 3:
                # parse next part for a date
                await channel.send('Input Date Of Entry You Want to View Using the Format YYYY-MM-DD (include the - )')
                date = await client.wait_for('message')
                # check if a profile exists
                if User.isProfileDiscord(str(message.author)):
                    # verify password
                    await message.channel.send('Please Enter Your Password: ', delete_after=120)
                    userSubmittedPassword = await client.wait_for('message')
                    if userSubmittedPassword.content == profile.password:
                        getDate = await client.wait_for('message')
                        date = getDate.content
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
                        # Failed Login
                        await channel.send("Invalid Password for account. Access Denied.", delete_after=120)
                else:
                    # Failed to find profile
                    await channel.send('Profile for Discord Tag ' + (str(message.author)) + ' not found. You must be authorized to use this command.')

            # 2 entered meaning new entry
            if intentCommand == 31:
                # format all remaining information in the message and store in variable
                getEntry = await client.wait_for('message')
                entry = getEntry.content
                # check if a profile exists
                if User.isProfileDiscord(str(message.author)):
                    # add the entry
                    Journal.add_entry(entry, "DiscordClient", User.getProfileUsernameDiscord(str(message.author)))
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

        # ===================== Pass Test =====================
        # TODO THIS WORKS FOR MULTIPLE LINE CODE!!!
        if message.content.startswith('/pass'):
            channel = message.channel
            await channel.send('Say hello!')

            msg = await client.wait_for('message')
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
