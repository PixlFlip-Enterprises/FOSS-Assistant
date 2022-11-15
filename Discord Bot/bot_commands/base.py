import os
import discord
import json, random
from discord.ext import commands
from discord.commands import Option
import wikipedia

# load config
config = json.load(open('config.json',))


# Just your standard run-of-the-mill hello meet and greet functionality.
class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome to the server {member.mention}.')

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}~')
        else:
            await ctx.send(f'Hello {member.name}... This feels familiar.')
        self._last_member = member

    # returns the help.txt file contents. Maybe renovate the UI on this someday?
    @commands.slash_command(name="help", description="basic help command", guild_ids=config['guild_ids'])
    async def warn(self, ctx):
        print("Help command issued")
        # open discord help file
        file = open('help.txt')
        returnList = ""
        for line in file:
            returnList += line
        await ctx.respond(returnList)

    # returns a summary of wikipedia article from searched term
    @commands.slash_command(name="wikipedia", description="Provides a summary of a wikipedia term")
    async def wikipedia(self, ctx, search_term: Option(str, "Search Wikipedia", required=True, default="Megalomaniac")):
        await ctx.trigger_typing()
        try:
            summary = wikipedia.summary(search_term, sentences=5)
            # build and return the embed
            embed = discord.Embed(color=discord.Colour.blue())
            embed.add_field(name="Summary:", value=f'{summary}')
            embed.set_footer(text=config["embed"]["footer_text"])  # todo add pfp of user running command
            await ctx.respond(embed=embed)  # Send the embed with some text
        except:
            await ctx.respond('Error In Retrieving Article From Wikipedia')

    @commands.slash_command(name="ping", description="Test your ping")
    async def ping(self, ctx):
        print("Discord ID of person asking:")
        member = ctx.author
        print(member)
        print(member.id)
        await ctx.respond("Pong!" + member.mention)

    @commands.slash_command(name="anyone", description="Randomly ping someone in the server")
    async def anyone(self, ctx):
        channel = self.bot.get_channel(ctx.channel.id)
        server_members = list(channel.members)
        await ctx.respond("Anyone ping! I choose you " + random.choice(server_members).mention)