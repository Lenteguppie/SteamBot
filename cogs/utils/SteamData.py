import discord
from discord.ext import commands

import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
import json
from time import gmtime, strftime

import urllib.request as urllib
import xml.etree.ElementTree as ET

from steamwebapi.api import ISteamUser, IPlayerService, ISteamUserStats

steamuserinfo = ISteamUser(steam_api_key='376DCAA8CEF57ECB0F7DACBA08C8C535')
profiles = {}

CsGoIconURL = "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/apps/730/69f7ebe2735c366c65c0b33dae00e12dc40edbe4.jpg"
SteamURL = "https://upload.wikimedia.org/wikipedia/commons/f/f5/SteamLogo.png"

def refreshSteamData():
        async def predicate(ctx):
                DiscordID = ctx.author.id
                try:
                        with open('DiscordSteamBridge.json') as json_file:  
                                data = json.load(json_file)
                                profiles = data
                                print (f'Steam data: {data}')
                                try:
                                        steamid = data[f'{DiscordID}']['steamid']
                                except Exception as e:
                                        curTimeDate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                                        embed=discord.Embed(title="Unknown Profile", description="It seems that you haven't paired your steam profile yet!", color=0x9ea305)
                                        embed.set_author(name="Steam", icon_url=SteamURL)
                                        embed.add_field(name="How to pair your profile:", value="To pair you profile use the command /pair [YOUR STEAM URL]", inline=True)
                                        embed.set_footer(text=f"SteamBot | {curTimeDate}")
                                        await ctx.send(embed=embed)
                                        return False
                                
                                usersummary = steamuserinfo.get_player_summaries(steamid)['response']['players'][0]
                                profiles[str(DiscordID)] = usersummary
                                print ('User updated!')
                                # await ctx.send("Steam Users updated...")
                                print (profiles)
                                write_json(profiles)
                                return True
                except:
                        
                        return False
        return commands.check(predicate) 

def write_json(data, filename='DiscordSteamBridge.json'):
     with open(filename,'w') as f:
           json.dump(data, f, indent=2, ensure_ascii=False)
