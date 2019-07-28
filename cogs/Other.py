import urllib.request as urllib2
import xml.etree.ElementTree as ET
import discord
from discord.ext import commands
from time import gmtime, strftime
from .utils import checks

import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
import json

class Other_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True, hidden = True)
    async def stat(ctx):
        await ctx.channel.send('Your stats arent ready yet {0.author.mention}!'.format(ctx))

    @commands.command(pass_context=True)
    async def deletethis(self, ctx):
        await ctx.send('Command received')
        await ctx.message.delete()
        await ctx.send('Message deleted')

    @commands.command(name="quit")
    @checks.isOwner()
    async def quit_(self, ctx):
    
        try:
            await ctx.send('We did it boys, bot is no more!')
            print("Bot shutting down!")
            sys.exit()
        except Exception as e:
            print (e)

    @commands.command(pass_context = True)
    async def hello(self, ctx):
        await ctx.channel.send('Hi :wave:')

    @commands.command(pass_context = True)
    async def ping(self, ctx):
        await ctx.channel.send('Pong!')

def setup(bot):
    print("loading the CSGOData extention!")
    bot.add_cog(Other_Commands(bot))