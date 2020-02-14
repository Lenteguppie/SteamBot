#/usr/bin/python3
# Work with Python 3.6
import asyncio
import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
from os import listdir
from os.path import isfile, join

import sys, traceback
TOKEN = 'NDYwNDcwNjc0Njk2MTc1NjE2.XSXz9Q.JHq3T3DFyfP7f2_WSsJBwU_z5Yc'
version = "1.0.1"

startup_extentions = ["cogs.CSGOData", "cogs.SteamBridge", "cogs.admin", "cogs.Other", "cogs.PUBG"]

bot = commands.Bot(".")

@bot.event
async def on_ready():
    print('Logged in as ')
    print(bot.user.name)
    print('as user: ')
    print(bot.user.id)
    print('------')
    activity = discord.Game(name=".help")
    await bot.change_presence(activity=activity)

cogs_dir = "cogs"

# Here we load our extensions(cogs) that are located in the cogs directory. Any file in here attempts to load.
if __name__ == '__main__':
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
        except (discord.ClientException, ModuleNotFoundError):
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()

bot.run(TOKEN)