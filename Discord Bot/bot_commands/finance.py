import os
import discord
import json
from discord.ext import commands, pages
from discord.commands import Option
import requests
from datetime import datetime

# load config
config = json.load(open('config.json',))


class Finance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # perform api call to store journal entry
    @commands.slash_command(name="finance-new", description="Create a new transaction.")
    async def finance_new(self, ctx, title: Option(str, "Transaction title", required=True, default="Tx."), memo: Option(str, "Memo", required=False, default=" "), deposit: Option(bool, "True if adding money, false if not.", required=True, default=False), amount: Option(float, "Charge", required=True, default=0.00)):
        x = datetime.now().__str__().replace(" ", "")
        # get member who made query
        member = ctx.author
        # add the entry using api
        api_call = requests.put(config['database']['host'] + "finance/" + str(member.id) + "/", json={'date': "'" + x + "'", 'title': title.replace("\n", "").replace('"', ""), 'memo': memo.replace("\n", "").replace('"', ""), 'deposit': deposit, 'amount': amount})
        api_call = api_call.json()
        if api_call['status'] == 'Completed':
            # tell the user the entry was recorded
            await ctx.respond('Transaction Recorded.', delete_after=12)
        else:
            await ctx.respond('Internal server error. Error Message: ' + api_call['error_msg'])


    # perform api call to retrieve financial transactions
    @commands.slash_command(name="finance-view", description="View Financial Transactions")
    async def finance_view(self, ctx):
        # get member who made query
        member = ctx.author
        # get a load of this guy, requesting his entire journal
        # quick call back to give us time to compile
        await ctx.respond("Retrieving your transactions.")
        await ctx.trigger_typing()
        # pages of transactions setup
        the_pages = []
        # api call
        api_call = requests.get(config['database']['host'] + "finance/" + str(member.id) + "/", json={'device_id': "DiscordClient"})
        api_call = api_call.json()
        # put together entire journal
        for dl in api_call['by_date']:
            embed = discord.Embed(title=str(member) + "'s Transactions", description=str(api_call[dl][0]), color=discord.Colour.blue())
            embed.add_field(name="Memo", value=f'{str(api_call[dl][1])}', inline=False)
            embed.add_field(name="Date", value=f'{str(dl)[:10]}', inline=True)
            embed.add_field(name="Value", value=f'{str(api_call[dl][2])}', inline=True)
            embed.add_field(name="Account Balance", value=f'{str(api_call[dl][3])}', inline=True)
            embed.set_footer(text=config["embed"]["footer_text"])  # todo add pfp of user running command
            the_pages.append(embed)
        paginator = pages.Paginator(pages=the_pages)
        await paginator.respond(ctx.interaction, ephemeral=False)


def setup(bot):
    bot.add_cog(Finance(bot))