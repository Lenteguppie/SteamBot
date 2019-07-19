#/usr/bin/python3
# Work with Python 3.6
import asyncio
import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
from os import listdir
from os.path import isfile, join

import sys, traceback
TOKEN = '[OWN BOT TOKEN]'

startup_extentions = ["cogs.Music", "cogs.CSGOData", "cogs.SteamBridge", "cogs.admin"]

bot = commands.Bot("/")

@bot.event
async def on_ready():
    print('Logged in as ')
    print(bot.user.name)
    print('as user: ')
    print(bot.user.id)
    print('------')
    activity = discord.Game(name="/help")
    await bot.change_presence(activity=activity)

class Main_Commands():
    def __init__(self, bot):
        self.bot = bot

@bot.command(pass_context = True)
async def stat(ctx):
    await ctx.channel.send('Your stats arent ready yet {0.author.mention}!'.format(ctx))

@bot.command(name="quit")
async def quit_(ctx):
   
    try:
        await ctx.send('We did it boys, bot is no more!')
        print("Bot shutting down!")
        sys.exit()
    except Exception as e:
        print (e)

@bot.command(pass_context = True)
async def hello(ctx):
    await ctx.channel.send('Hi :wave:')

@bot.command(pass_context = True)
async def ping(ctx):
    await ctx.channel.send('Pong!')

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