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

class CSGOData(commands.Cog):
    __slots__ = ('bot', 'players')
    def __init__(self, bot):
        self.bot = bot
        self.weapons = self.getAllWeapons()
        self.CsGoIconURL = "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/apps/730/69f7ebe2735c366c65c0b33dae00e12dc40edbe4.jpg"

    def getAllWeapons(self):
        with open('Weapons.json') as json_file:  
            data = json.load(json_file)
            print (f"\nWeapons: {data}")
            return data

    
    @commands.command(name="CSGO", alias=["CSGO-Stat"])
    @SteamData.refreshSteamData()
    async def CSGO_(self, ctx):
        await ctx.trigger_typing()
        curTimeDate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        discordID = ctx.author.id
        steamData = self.getSteamData(discordID)
        steamID = steamData['steamid']
        steamName = steamData['personaname']
        print(steamID, steamName)

        amountOfWins = self.getTotalWins(steamID)
        amountOfKills = self.getTotalKills(steamID)
        amountOfDeaths = self.getTotalDeaths(steamID)
        embed = discord.Embed(
            title = 'Overall CS:GO stats',
            description = (f'The CS:GO stats for player: {steamName}'),
            color=0x9ea305
        )
        embed.set_author(name="CSGO weapon stats", icon_url=self.CsGoIconURL)
        embed.add_field(name='Total Wins', value=amountOfWins, inline=False)
        embed.add_field(name='Total Kills', value=amountOfKills, inline=True)
        embed.add_field(name='Total Deaths', value=amountOfDeaths, inline=True)
        embed.set_thumbnail(url=steamData['avatar'])
        embed.set_footer(text=f"SteamBot | {curTimeDate}")

        await ctx.send(embed = embed)
    
    @commands.command(name="CSGO-weapon")
    @SteamData.refreshSteamData()
    async def CSGO_Weapon(self, ctx, *, weapon : str):
        await ctx.trigger_typing()
        discordID = ctx.author.id
        steamData = self.getSteamData(discordID)
        steamID = steamData['steamid']
        steamName = steamData['personaname']
        print(steamID, steamName)
        embed = None
        try:
            gun = self.weapons['CSGO']['Weapons'][f'{weapon}']
            print (gun)
            curTimeDate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            if (gun['statName'] == 'UA'):
                embed=discord.Embed(title="Unavailable stats", description=f"We cannot get the stats for the {weapon} at the moment, sorry for the inconvenience!", color=0x9ea305)
                embed.set_author(name="CSGO weapon stats", icon_url=self.CsGoIconURL)
                embed.set_footer(text=f"SteamBot | {curTimeDate}")
                print (f'{weapon} stats unavailable')
            else:
                amountOfGunKills = self.getWeaponKills(steamID, gun['statName'])
                amountOfGunShots = self.getWeaponShots(steamID, gun['statName'])
                amountOfGunHits = self.getWeaponHits(steamID, gun['statName'])
                accuracy = (float(amountOfGunHits)/float(amountOfGunShots)) * 100
                embed=discord.Embed(title=f"{weapon} stats for {steamName}", description=f"The amount of kills, shots fired and bullets hit for the {weapon}", color=0x9ea305)
                embed.set_author(name="CSGO weapon stats", icon_url=self.CsGoIconURL)
                embed.set_footer(text=f"SteamBot | {curTimeDate}")
                embed.set_image(url=gun['image'])
                embed.set_thumbnail(url=steamData['avatar'])
                embed.add_field(name="Amount of kills", value=str(amountOfGunKills), inline = True)
                embed.add_field(name="Amount of Shots fired", value=str(amountOfGunShots), inline = True)
                embed.add_field(name="Amount of Shots hit", value=str(amountOfGunHits), inline = True)
                embed.add_field(name="Accuracy", value=str(accuracy) + "%", inline = True)
        except:
            curTimeDate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            embed=discord.Embed(title="Unknown Gun", description="Please enter a valid gun name to see those stats!", color=0x9ea305)
            embed.set_author(name="CSGO weapon stats", icon_url=self.CsGoIconURL)
            embed.add_field(name="Gunlist", value="https://counterstrike.fandom.com/wiki/Counter-Strike:_Global_Offensive", inline=True)
            embed.set_footer(text=f"SteamBot | {curTimeDate}")
        await ctx.send(embed=embed)

    #Get data from Steam
    def acquireTree(self, steamID):
        self.u1=urllib2.urlopen(f'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=376DCAA8CEF57ECB0F7DACBA08C8C535&steamid={steamID}&format=xml')
        tree = ET.parse(self.u1)
        return tree

    def lastMatchKIA(self, steamID):
        tree = self.acquireTree(steamID)
        elm = tree.find("./stats/stat[name='last_match_kills']")
        return elm.findtext('value')

    def getTotalMoneyEarned(self, steamID):
        tree = self.acquireTree(steamID)
        elm = tree.find("./stats/stat[name='total_money_earned']")
        return elm.findtext('value')

    def getTotalWins(self, steamID):
        tree = self.acquireTree(steamID)
        elm = tree.find("./stats/stat[name='total_wins']")
        return elm.findtext('value')
    
    def getTotalKills(self, steamID):
        tree = self.acquireTree(steamID)
        elm = tree.find("./stats/stat[name='total_kills']")
        return elm.findtext('value')
    
    def getTotalDeaths(self, steamID):
        tree = self.acquireTree(steamID)
        elm = tree.find("./stats/stat[name='total_deaths']")
        return elm.findtext('value')

    def getSteamData(self, discordID):
        data = None
        with open('DiscordSteamBridge.json') as json_file:  
            data = json.load(json_file)
            print (data)
        steamData = data[str(discordID)]
        return steamData
    
    def getWeaponKills(self, steamID, gun):
        tree = self.acquireTree(steamID)
        elm = tree.find(f"./stats/stat[name='total_kills_{gun}']")
        print (gun, elm.findtext('value'))
        return elm.findtext('value')

    def getWeaponShots(self, steamID, gun):
        tree = self.acquireTree(steamID)
        elm = tree.find(f"./stats/stat[name='total_shots_{gun}']")
        print (gun, elm.findtext('value'))
        return elm.findtext('value')
    
    def getWeaponHits(self, steamID, gun):
        tree = self.acquireTree(steamID)
        elm = tree.find(f"./stats/stat[name='total_hits_{gun}']")
        print (gun, elm.findtext('value'))
        return elm.findtext('value')



def setup(bot):
    print("loading the CSGOData extention!")
    bot.add_cog(CSGOData(bot))