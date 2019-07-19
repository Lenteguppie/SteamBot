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

steamuserinfo = ISteamUser(steam_api_key='376DCAA8CEF57ECB0F7DACBA08C8C535')
profiles = {}

def refreshSteamData():
        def predicate(ctx):
                DiscordID = ctx.author.id
                try:
                        with open('DiscordSteamBridge.json') as json_file:  
                                data = json.load(json_file)
                                print (f'Steam data: {data}')
                                steamid = data[f'{DiscordID}']['steamid']
                                usersummary = steamuserinfo.get_player_summaries(steamid)['response']['players'][0]
                                profiles[str(DiscordID)] = usersummary
                                print ('User updated!')
                                print (profiles)
                                write_json(profiles)
                        return True
                except:
                        return False
        return commands.check(predicate) 

def write_json(data, filename='DiscordSteamBridge.json'):
     with open(filename,'w') as f:
           json.dump(data, f, indent=2, ensure_ascii=False)
