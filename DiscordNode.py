# Work with Python 3.6
import discord

# PRIVATE KEY VARIABLES
TOKEN = ''
PREFIX = '/'


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == (PREFIX + 'ping'):
            await message.channel.send('pong')

        if message.content == (PREFIX + 'journal'):
            await message.channel.send('the data you are trying to access is unavailable.')

        if message.content.startswith('/greet'):
            channel = message.channel
            await channel.send('Say hello!')

            def check(m):
                return m.content == 'hello' and m.channel == channel

            msg = await client.wait_for('message', check)
            await channel.send('Hello {.author}!'.format(msg))


client = MyClient()

client.run(TOKEN)