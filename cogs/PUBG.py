import requests
import urllib.request as urllib2
import xml.etree.ElementTree as ET
import discord
from discord.ext import commands
from time import gmtime, strftime
from .utils import SteamData

import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
import json

url = "https://api.pubg.com/shards/steam/players?filter[playerNames]=Lenteguppie"
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyNGY4ZTQ5MC05YzFhLTAxMzctYmUwYS01N2Q5ZjU2NGY2ZmUiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTY1Mjc1OTgyLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImxlbnRlZ3VwcGllLW91In0._aDwu17JUhqJcR9p7q2KoYJrv42LGBQPo6DxrN_yZ0E"



class PUBGData(commands.Cog):
    __slots__ = ('bot', 'players')
    def __init__(self, bot):
      header = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/vnd.api+json"
      }

      r = requests.get(url, headers=header)

      iets = r.json()

      print (iets)

def setup(bot):
    print("loading the PUBGData extention!")
    bot.add_cog(PUBGData(bot))

