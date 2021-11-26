import wikipedia
import discord

# PRIVATE KEY VARIABLES
from discord.ext.commands import bot

from Functions import Profile, Journal

TOKEN = 'example token'
PREFIX = '/'


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        # ============================ Ping ============================
        if message.content == (PREFIX + 'ping'):
            await message.channel.send('pong')

        # ============================  Troll Commands  ============================
        if message.content == (PREFIX + 'submit'):
            await message.channel.send('I will not comply. Don\'t try /forcesubmit')

        if message.content == (PREFIX + 'forcesubmit'):
            await message.channel.send('Foolish mortal. ')




        # ============================ Journal ============================
        # shelved for now. Needs to scan contact database for a matching discord to contact, then load their journal
        # and return or post whatever sub command is issued.
        if message.content.startswith(PREFIX + 'journal'):
            # set channel to same as one command issued in
            channel = message.channel
            # we know the command now parse sub command always at char value 9

            # 1 entered meaning they want to view entry
            if (message.content[9]) == '1':
                # parse next part for a date
                # return entry of matching user and date
                date = message.content[10:]
                # check if a profile exists
                if Profile.isProfileDiscord(str(message.author)):
                    # check if the entry exists
                    if Journal.isEntry(date, Profile.getProfileDiscord(str(message.author))):
                        entry = Journal.viewEntry(date, Profile.getProfileDiscord(str(message.author)))
                        await channel.send('Entry for the Date ' + date + ': \n' + entry[1])
                    else:
                        # return error to user
                        await channel.send('Invalid Date. Try again using the format YYYY-MM-DD (include the - ')
                else:
                    # Failed to find profile
                    await channel.send('Profile for Discord Tag ' + (str(message.author)) + ' not found. You must be authorized to use this command.')

            # 2 entered meaning new entry
            elif (message.content[9]) == '2':
                # format all remaining information in the message and store in variable
                entry = message.content[10:]
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
            #await channel.send('Please Select An Option:\n 1 | View Entry\n 2 | Add Entry\n 3 | Delete Entry\n 4 | Export Journal')





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
                summary = wikipedia.summary(message.content[-6:], 7)
                await message.channel.send('Wikipedia Top Result: ' + summary)
            except:
                await message.channel.send('No Data Found From Wikipedia')

    async def play(ctx):
        guild = ctx.guild
        voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
        audio_source = discord.FFmpegPCMAudio('vuvuzela.mp3')
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)

client = MyClient()

client.run(TOKEN)
