# Work with Python 3.6
import discord

# PRIVATE KEY VARIABLES
TOKEN = 'Nzc5MTAzMDYzNzc5ODM1OTM0.X7bqRQ.79aIq0ECOLaXYcYqORy_G8i2oAk'


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')


client = MyClient()

client.run(TOKEN)