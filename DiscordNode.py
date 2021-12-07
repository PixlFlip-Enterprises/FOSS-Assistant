import wikipedia
import discord
import os
from Functions import Profile, Journal, Protocols

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

        # ============================ Basics ============================
        # ping command
        if message.content == (PREFIX + 'ping'):
            await message.channel.send('pong', delete_after=10)

        # help command
        if message.content == (PREFIX + 'help'):
            await message.channel.send('I am Blink. \'t try /forcesubmit')
            await message.channel.send('I am Blink 2. \'t try /forcesubmit')

        # ============================  Troll Commands  ============================
        if message.content == (PREFIX + 'submit'):
            await message.channel.send('I will not comply. Don\'t try /forcesubmit')

        if message.content == (PREFIX + 'forcesubmit'):
            await message.channel.send('You\'re an idiot.')




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
                if Profile.isProfileDiscord(str(message.author)):
                    # check if the entry exists
                    if Journal.isEntry(date, Profile.getProfileDiscord(str(message.author))):
                        # Get the entry
                        entry = Journal.getFullEntry(date, Profile.getProfileDiscord(str(message.author)))
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
                if Profile.isProfileDiscord(str(message.author)):
                    # add the entry
                    Journal.addBasicEntry(entry, "DiscordClient", Profile.getProfileDiscord(str(message.author)))
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


client = MyClient()

client.run(TOKEN)
