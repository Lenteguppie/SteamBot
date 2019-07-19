import discord
from discord.ext import commands

import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
import json

import urllib.request as urllib
import xml.etree.ElementTree as ET

from steamwebapi.api import ISteamUser, IPlayerService, ISteamUserStats


class Steam(commands.Cog):  
    __slots__ = ('bot', 'players')
    def __init__(self, bot):
        self.bot = bot
        self.profile = {}
        self.steamuserinfo = ISteamUser(steam_api_key='376DCAA8CEF57ECB0F7DACBA08C8C535')

    @commands.command(name="pair")
    async def pair_(self, ctx, *, steamUrl: str = None):
        """Pair your Discord ID to your steam account so you can see your stats from your games and other cool stuff 
        ------------
        Pair: str [Required]
            To pair all you need is a Steam profile Url
        ------------
        """
        self.profiles = self.getSteamData()
        if steamUrl != None:
            print (f"known profiles: {self.profiles}")
            steamid = steamUrl[36:54]
            print (steamid)
            usersummary = self.steamuserinfo.get_player_summaries(steamid)['response']['players'][0]
            print(f"SteamID substring: \n{usersummary}")
            print(usersummary['personaname'])
            self.profiles[str(ctx.author.id)] = usersummary
            print (self.profiles)
            self.write_json(self.profiles)
            await ctx.send(('{0} successfully paired his steam account {1}!\n {2}').format(ctx.author, usersummary['personaname'], usersummary['profileurl']))
        else:
            await ctx.send(f'{ctx.author.mention}, usage: -pair [Your Steam URL]')
    
    def write_json(self, data, filename='DiscordSteamBridge.json'):
        with open(filename,'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def getSteamData(self):
        with open('DiscordSteamBridge.json') as json_file:  
            data = json.load(json_file)
            print (f"data: {data}")
            return data

def setup(bot):
    print("loading the SteamData extention!")
    bot.add_cog(Steam(bot))