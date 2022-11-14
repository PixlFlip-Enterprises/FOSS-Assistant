import discord
import json
from discord.ext import commands, pages
from discord.commands import Option
import requests
from datetime import datetime

# load config
config = json.load(open('config.json',))


class Notes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # perform api call to grab all notes of user
    @commands.slash_command(name="notebook-view", description="View all your notes.")
    async def notebook_view(self, ctx):
        # quick reply since this may take a second
        await ctx.respond('Retrieving your notebook!')
        # get member who made query
        member = ctx.author
        # get all notes
        api_call = requests.get(config['database']['host'] + "notes/" + str(member.id) + "/")
        api_call = api_call.json()

        the_pages = []
        if api_call['status'] == 'Completed.':
            # Get and display the notes of our user
            embed = discord.Embed(title= str(member) + "'s Notebook", color=discord.Colour.blue())
            for n in api_call['notes']:
                embed = discord.Embed(title=str(member) + "'s Notebook", description=str(n[3]), color=discord.Colour.blue())
                embed.add_field(name="Note:", value=f'{str(n[4])}', inline=False)
                embed.add_field(name="ID", value=f'{str(n[0])}', inline=True)
                embed.add_field(name="Date", value=f'{str(n[2])[:10]}', inline=True)
                embed.set_footer(text=config["embed"]["footer_text"])  # todo add pfp of user running command
                the_pages.append(embed)
            paginator = pages.Paginator(pages=the_pages)
            await paginator.respond(ctx.interaction, ephemeral=False)
        else:
            await ctx.respond('Internal server error.')


    # new note
    @commands.slash_command(name="note-new", description="Write a new note into your notebook")
    async def note_new(self, ctx, title: Option(str, "Note title", required=False, default="Unnamed Note"), body: Option(str, "Note Body", required=True, default="I exist..."), starred: Option(bool, "Favorite Entry?", required=False, default=False)):
        x = datetime.now().__str__().replace(" ", "")
        # get member who made query
        member = ctx.author
        # add the entry using api
        api_call = requests.put(config['database']['host'] + "notes/" + str(member.id) + "/", json={'date': "'" + x + "'", 'title': title.replace("\n", ""), 'body': body.replace("\n", ""), 'creation_device': 'DiscordClient', 'starred': str(starred), 'time_zone': 'EST'})
        api_call = api_call.json()
        if api_call['status'] == 'Completed':
            # tell the user the entry was recorded
            await ctx.respond('Note Created.', delete_after=12)
        else:
            await ctx.respond('Internal server error. Error Message: ' + api_call['error_msg'])


def setup(bot):
    bot.add_cog(Notes(bot))