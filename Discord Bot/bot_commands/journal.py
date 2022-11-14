import os
import discord
import json
from discord.ext import commands, pages
from discord.commands import Option
import requests
from datetime import datetime

# load config
config = json.load(open('config.json',))


class Journal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # perform api call to store journal entry
    @commands.slash_command(name="journal-new", description="Write a new entry into your journal")
    async def journal_new_entry(self, ctx, entry: Option(str, "Enter Entry", required=True, default="I am."), starred: Option(bool, "Favorite Entry?", required=False, default=False)):
        x = datetime.now().__str__().replace(" ", "")
        # get member who made query
        member = ctx.author
        # add the entry using api
        api_call = requests.put(config['database']['host'] + "journal/" + str(member.id) + "/", json={'date': "'" + x + "'", 'entry': entry.replace("\n", "").replace('"', ""), 'creation_device': 'DiscordClient', 'starred': "'" + str(starred) + "'", 'time_zone': 'EST'})
        api_call = api_call.json()
        if api_call['status'] == 'Completed':
            # tell the user the entry was recorded
            await ctx.respond('Entry Recorded.', delete_after=12)
        else:
            await ctx.respond('Internal server error. Error Message: ' + api_call['error_msg'])

    # perform api call to retrieve journal entry
    @commands.slash_command(name="journal-view", description="View an entry from your journal")
    async def journal_view(self, ctx, month: Option(int, "Enter Date Of Entry", required=False, default=1), day: Option(int, "Enter Date Of Entry", required=False, default=1), year: Option(int, "Enter Date Of Entry", required=False, default=1)):
        # get member who made query
        member = ctx.author
        # check if we are doing the whole thing or just a single entry
        if (str(month) == '1') or (str(year) == '1') or (str(day) == '1'):
            # get a load of this guy, requesting his entire journal
            # quick call back to give us time to compile
            await ctx.respond("Retrieving your journal.")
            await ctx.trigger_typing()
            # pages of journal setup
            the_pages = []
            # api call
            api_call = requests.get(config['database']['host'] + "journal/" + str(member.id) + "/", json={'device_id': "DiscordClient"})
            api_call = api_call.json()
            # put together entire journal
            for dl in api_call['by_date']:
                embed = discord.Embed(title=str(member) + "'s Journal", description=str(api_call[dl][0]), color=discord.Colour.blue())
                embed.add_field(name="Starred", value=f'{str(api_call[dl][1])}', inline=True)
                embed.add_field(name="Date", value=f'{str(dl)[:10]}', inline=True)
                embed.set_footer(text=config["embed"]["footer_text"])  # todo add pfp of user running command
                the_pages.append(embed)
            paginator = pages.Paginator(pages=the_pages)
            await paginator.respond(ctx.interaction, ephemeral=False)
        else:
            # user requesting singular entry
            # format data
            if len(str(month)) < 2:
                month = "0" + str(month)
            if len(str(day)) < 2:
                day = "0" + str(day)
            if len(str(year)) < 4:
                year = "20" + str(year)
            # validate the date
            if not (len(str(month)) <= 2) & (len(str(day)) <= 2) & (len(str(year)) <= 4):
                await ctx.respond("Invalid Date. Make sure to use DD MM YYYY.")
                return
            # create date from data
            date = str(year) + "-" + str(month) + "-" + str(day)
            # request from api server
            api_call = requests.get(config['database']['host'] + "journal/" + str(member.id) + "/", json={"date": date, 'device_id': "DiscordClient"})
            api_call = api_call.json()
            # check if the entry exists
            if api_call['status'] == 'Completed.':
                # Return the entry and related information and delete after 120 seconds for security
                # build and return the embed
                embed = discord.Embed(title="Journal Entry For " + date, description=api_call['entry'], color=discord.Colour.blue())
                embed.add_field(name="Favorited", value=f'{str(api_call["starred"])}', inline=True)
                embed.add_field(name="Origin Timezone", value=f'{str(api_call["timezone"])}', inline=True)
                embed.set_footer(text=config["embed"]["footer_text"])  # todo add pfp of user running command
                await ctx.respond(embed=embed, delete_after=120)  # Send the embed
            else:
                # return error to user
                await ctx.respond('Entry Does Not Exist. Try again using a different date.')


def setup(bot):
    bot.add_cog(Journal(bot))