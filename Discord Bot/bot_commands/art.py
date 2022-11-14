import time, json, os
from datetime import datetime
import requests
from base64 import b64decode
import discord
from discord.ext import commands
from discord.commands import Option

# load config
config = json.load(open('config.json',))

# load api jsons
async_art_gen = {
    "prompt": "string",
    "params": {
        "sampler_name": "k_lms",
        "toggles": [1,4],
        "cfg_scale": 5,
        "denoising_strength": 0.75,
        "seed": "string",
        "height": 512,
        "width": 512,
        "seed_variation": 1,
        "use_gfpgan": True,
        "karras": False,
        "use_real_esrgan": True,
        "use_ldsr": True,
        "use_upscaling": True,
        "steps": 50,
        "n": 1
    },
    "nsfw": True,
    "trusted_workers": True,
    "censor_nsfw": False,
}

async def get_model_list_from_db(ctx: discord.AutocompleteContext):
    # get available models
    api_call = requests.get("https://stablehorde.net/api/v2/status/models")
    api_call = api_call.json()
    # Code where you fetch data from db
    return sorted([i for i in api_call if i['name'].startswith(ctx.value.lower())])



# todo eventually perhaps an async def would be better?
def draw(stable_horde_api_key, prompt, seed):
    # build the json
    async_art_gen['prompt'] = prompt
    async_art_gen['params']['seed'] = str(seed)
    # api call
    api_call = requests.post("https://stablehorde.net/api/v2/generate/async", json=async_art_gen, headers={"apikey": stable_horde_api_key})
    api_call = api_call.json()
    # name file based on current time and save to folder
    x = datetime.now().__str__().replace(" ", "")
    file_loc = "generated_media/" + x + '.png'
    shouldEnd = False
    while shouldEnd == False:
        api_call2 = requests.get("https://stablehorde.net/api/v2/generate/check/" + api_call['id'])
        api_call2 = api_call2.json()
        if (api_call2['finished'] == 1):
            api_call3 = requests.get("https://stablehorde.net/api/v2/generate/status/" + api_call['id'])
            api_call3 = api_call3.json()
            with open(file_loc, 'wb') as fh:
                fh.write(b64decode(api_call3['generations'][0]['img']))
            shouldEnd = True
            break
        time.sleep(10)  # Delay for 10 seconds


# All code below this point is functional, not UI/UX.

# goes and requests artwork that is already being processed. Once complete returns nothing and puts image at file_name
def get_drawing(gen_id, file_name):
    shouldEnd = False
    while shouldEnd == False:
        api_call2 = requests.get("https://stablehorde.net/api/v2/generate/check/" + gen_id)
        api_call2 = api_call2.json()
        if (api_call2['finished'] == 1):
            api_call3 = requests.get("https://stablehorde.net/api/v2/generate/status/" + gen_id)
            api_call3 = api_call3.json()
            with open(file_name, 'wb') as fh:
                fh.write(b64decode(api_call3['generations'][0]['img']))
            shouldEnd = True
            break
        time.sleep(api_call2['wait_time'])

class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="", row=0, style=discord.ButtonStyle.primary, emoji="⭐")
    async def button_callback(self, button, interaction):
        # todo code here to add photo to star leaderboard and possibly a dataset
        await interaction.response.send_message("You clicked the star button!") # Send a message when the button is clicked


    @discord.ui.button(label="Upscale", row=0, style=discord.ButtonStyle.primary, emoji="⏩")
    async def upscale_button_callback(self, button, interaction):
        # todo rerun the prompt given before with upscaling... this is gonna suck.
        await interaction.response.send_message("You clicked the upscale button!")  # Send a message when the button is clicked


    @discord.ui.button(label="Report", row=0, style=discord.ButtonStyle.primary, emoji="🚩")  # Create a button with the label "😎 Click me!" with color Blurple
    async def report_button_callback(self, button, interaction):
        # todo should send image to be checked immediately
        await interaction.response.send_message("You clicked the report button! Well that isn't good!")  # Send a message when the button is clicked

class Draw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # more vars could be added here

    @commands.slash_command(name="draw", description="Create an image based on your prompt", guild_ids=config['guild_ids'])
    async def draw(self, ctx, prompt: Option(str, "Enter your image prompt", required=True, default='rickroll'),
                   seed: Option(int, "Enter your seed", required=False, default=-1),
                   batch: Option(int, "Enter batch size", required=False, default=1),
                   model: Option(str, "Enter a Model", required=False, default="stable-diffusion"),
                   height: Option(int, "Height of image", required=False, default=512),
                   width: Option(int, "Width of image", required=False, default=512)):
        # get user
        member = ctx.author
        # build the json
        async_art_gen['prompt'] = prompt
        async_art_gen['params']['seed'] = str(seed)
        async_art_gen['height'] = height
        async_art_gen['width'] = width
        # name file based on current time and save to folder
        x = datetime.now().__str__().replace(" ", "")
        file_loc = x + '.png'
        api_call = requests.post("https://stablehorde.net/api/v2/generate/async", json=async_art_gen, headers={"apikey": config["stable_horde_api_key"]})
        api_call = api_call.json()
        api_call2 = requests.get("https://stablehorde.net/api/v2/generate/check/" + api_call['id'])
        api_call2 = api_call2.json()
        await ctx.respond("Generating your prompt! Est. time to completion: " + str(api_call2['wait_time']) + " seconds")
        await ctx.trigger_typing()
        try:
            # get the art
            get_drawing(api_call['id'], file_loc)
            # create discord object for image
            file = discord.File(file_loc, filename='imageToSave.png')
            # build and return the embed
            embed = discord.Embed(color=discord.Colour.blue())
            embed.add_field(name="Prompt:", value=f'{prompt}')
            embed.add_field(name="Seed:", value=f'{str(seed)}')
            embed.set_footer(text=config["embed"]["footer_text"])  # todo add pfp of user running command
            embed.set_author(name=config['name'], icon_url="https://example.com/link-to-my-image.png")
            embed.set_image(url="attachment://imageToSave.png")
            await ctx.respond(member.mention, file=file, embed=embed, view=MyView(timeout=300))  # Send the embed with some text
            # delete temp file
            os.remove(file_loc)
        except Exception as e:
            print(e)
            await ctx.respond("Couldn't generate that image " + member.mention)  # Send the embed with some text


def setup(bot):
    bot.add_cog(Draw(bot))