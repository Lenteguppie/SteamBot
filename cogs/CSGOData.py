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
        self.SteamURL = "https://upload.wikimedia.org/wikipedia/commons/8/83/Steam_icon_logo.svg"

    def getAllWeapons(self):
        with open('Weapons.json') as json_file:  
            data = json.load(json_file)
            print (f"\nWeapons: {data}")
            return data
    
    @commands.command(name="CSGO-stat", aliases=["CSGO-stats"])
    @SteamData.refreshSteamData()
    async def CSGO_(self, ctx):
        await ctx.trigger_typing()
        curTimeDate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        discordID = ctx.author.id
        steamData = self.getSteamData(discordID)
        steamID = steamData['steamid']
        steamName = steamData['personaname']
        print(steamID, steamName)

        # intID = int(steamID)
        # print (intID)

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
    
    @commands.command(name="CSGO-lastmatch", aliases=["lastmatch"])
    @SteamData.refreshSteamData()
    async def CSGO_lastmatch(self, ctx):
        await ctx.trigger_typing()
        curTimeDate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        discordID = ctx.author.id
        steamData = self.getSteamData(discordID)
        steamID = steamData['steamid']
        steamName = steamData['personaname']
        print(steamID, steamName)

        #Get the last match's favourite gun data
        favGunName = self.getWeaponByID(self.lastMatch_favWeaponID(steamID))
        favGunKills = self.lastMatch_favWeaponKills(steamID)
        favGunHits = self.lastMatch_favWeaponHits(steamID)
        favGunShots = self.lastMatch_favWeaponShots(steamID)

        #Get amount of wins CT and T side:
        CT_wins = self.lastMatch_ct_wins(steamID)
        T_wins = self.lastMatch_t_wins(steamID)

        #get last match's kills and deaths
        amountOfEKIA = self.lastMatchEKIA(steamID)
        amountOfDeaths = self.lastMatchDeaths(steamID)

        # other last match data
        amountMVP = self.lastMatchMVPs(steamID)
        moneySpent = self.lastMatchMoneySpent(steamID)
        dmg = self.lastMatch_damage(steamID)

        embed = discord.Embed(
            title = 'Last match CS:GO stats',
            description = (f'{steamName}\'s last CS:GO match'),
            color=0x9ea305
        )
        embed.set_author(name="CSGO match stats", icon_url=self.CsGoIconURL)
        embed.add_field(name='Counter Terrorist Wins', value=CT_wins, inline=True)
        embed.add_field(name='Terrorist Win', value=T_wins, inline=True)
        embed.add_field(name='Money spent', value=moneySpent, inline=True)
        embed.add_field(name='Last match MVP\'s', value=amountMVP, inline=True)
        embed.add_field(name='Damage', value=dmg, inline=False)
        embed.add_field(name='Kills', value=amountOfEKIA, inline=True)
        embed.add_field(name='Deaths', value=amountOfDeaths, inline=True)
        embed.add_field(name='Favourite gun:', value=favGunName, inline=True)
        embed.add_field(name='Favourite gun kills', value=favGunKills, inline=True)
        embed.add_field(name='Favourite gun shots', value=favGunShots, inline=True)
        embed.add_field(name='Favourite gun hits', value=favGunHits, inline=True)
        embed.set_thumbnail(url=steamData['avatar'])
        embed.set_footer(text=f"SteamBot | {curTimeDate}")

        await ctx.send(embed = embed)
    
    @commands.command(name="CSGO-weapon")
    @SteamData.refreshSteamData()
    async def CSGO_Weapon(self, ctx, *, weapon : str):
        await ctx.trigger_typing()
        weaponUpper = weapon.upper()
        discordID = ctx.author.id
        steamData = self.getSteamData(discordID)
        if steamData != None:
            steamID = steamData['steamid']
            steamName = steamData['personaname']
            print(steamID, steamName)
            embed = None
            try:
                gun = self.weapons['CSGO']['Weapons'][f'{weaponUpper}']
                officialGunName = gun['OfficialName']
                print (gun)
                curTimeDate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                if (gun['statName'] == 'UA'):
                    embed=discord.Embed(title="Unavailable stats", description=f"We cannot get the stats for the {officialGunName} at the moment, sorry for the inconvenience!", color=0x9ea305)
                    embed.set_author(name="CSGO weapon stats", icon_url=self.CsGoIconURL)
                    embed.set_footer(text=f"SteamBot | {curTimeDate}")
                    print (f'{officialGunName} stats unavailable')
                else:
                    amountOfGunKills = self.getWeaponKills(steamID, gun['statName'])
                    amountOfGunShots = self.getWeaponShots(steamID, gun['statName'])
                    amountOfGunHits = self.getWeaponHits(steamID, gun['statName'])
                    accuracy = (float(amountOfGunHits)/float(amountOfGunShots)) * 100
                    embed=discord.Embed(title=f"{officialGunName} stats for {steamName}", description=f"The amount of kills, shots fired and bullets hit for the {officialGunName}", color=0x9ea305)
                    embed.set_author(name="CSGO weapon stats", icon_url=self.CsGoIconURL)
                    embed.set_footer(text=f"SteamBot | {curTimeDate}")
                    embed.set_image(url=gun['image'])
                    embed.set_thumbnail(url=steamData['avatar'])
                    embed.add_field(name="Amount of kills", value=str(amountOfGunKills), inline = True)
                    embed.add_field(name="Amount of Shots fired", value=str(amountOfGunShots), inline = True)
                    embed.add_field(name="Amount of Shots hit", value=str(amountOfGunHits), inline = True)
                    embed.add_field(name="Accuracy", value=str(accuracy) + " %", inline = True)
            except:
                curTimeDate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                embed=discord.Embed(title="Unknown Gun", description="Please enter a valid gun name to see those stats!", color=0x9ea305)
                embed.set_author(name="CSGO weapon stats", icon_url=self.CsGoIconURL)
                embed.add_field(name="Gunlist", value="https://counterstrike.fandom.com/wiki/Counter-Strike:_Global_Offensive", inline=True)
                embed.set_footer(text=f"SteamBot | {curTimeDate}")
            await ctx.send(embed=embed)
        else:
            curTimeDate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            embed=discord.Embed(title="Unknown Profile", description="It seems that you haven't paired your steam profile yet!", color=0x9ea305)
            embed.set_author(name="Steam", icon_url=self.CsGoIconURL)
            embed.add_field(name="How to pair your profile:", value="To pair you profile use the command /pair [YOUR STEAM URL]", inline=True)
            embed.set_footer(text=f"SteamBot | {curTimeDate}")
            await ctx.send(embed=embed)

    #Get data from Steam
    def acquireTree(self, steamID):
        self.u1=urllib2.urlopen(f'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=376DCAA8CEF57ECB0F7DACBA08C8C535&steamid={steamID}&format=xml')
        tree = ET.parse(self.u1)
        return tree

    #region lastmatch
    def lastMatchEKIA(self, steamID):
        tree = self.acquireTree(steamID)
        elm = tree.find("./stats/stat[name='last_match_kills']")
        return elm.findtext('value')
    
    def lastMatchDeaths(self, steamID):
        tree = self.acquireTree(steamID)
        elm = tree.find("./stats/stat[name='last_match_deaths']")
        return elm.findtext('value')
    
    def lastMatchMVPs(self, steamID):
        tree = self.acquireTree(steamID)
        elm = tree.find("./stats/stat[name='last_match_mvps']")
        return elm.findtext('value')
    
    def lastMatchMoneySpent(self, steamID):
        tree = self.acquireTree(steamID)
        elm = tree.find("./stats/stat[name='last_match_money_spent']")
        return elm.findtext('value')
    
    def lastMatch_t_wins(self, steamID):
        tree = self.acquireTree(steamID)
        elm = tree.find("./stats/stat[name='last_match_t_wins']")
        return elm.findtext('value')
    
    def lastMatch_ct_wins(self, steamID):
        tree = self.acquireTree(steamID)
        elm = tree.find("./stats/stat[name='last_match_ct_wins']")
        return elm.findtext('value')
    
    def lastMatch_wins(self, steamID):
        tree = self.acquireTree(steamID)
        elm = tree.find("./stats/stat[name='last_match_wins']")
        return elm.findtext('value')

    def lastMatch_favWeaponID(self, steamID):
        tree = self.acquireTree(steamID)
        elm = tree.find("./stats/stat[name='last_match_favweapon_id']")
        return elm.findtext('value')
    
    def lastMatch_favWeaponShots(self, steamID):
        tree = self.acquireTree(steamID)
        elm = tree.find("./stats/stat[name='last_match_favweapon_shots']")
        return elm.findtext('value')
    
    def lastMatch_favWeaponHits(self, steamID):
        tree = self.acquireTree(steamID)
        elm = tree.find("./stats/stat[name='last_match_favweapon_hits']")
        return elm.findtext('value')
    
    def lastMatch_favWeaponKills(self, steamID):
        tree = self.acquireTree(steamID)
        elm = tree.find("./stats/stat[name='last_match_favweapon_kills']")
        return elm.findtext('value')
    
    def lastMatch_damage(self, steamID):
        tree = self.acquireTree(steamID)
        elm = tree.find("./stats/stat[name='last_match_damage']")
        return elm.findtext('value')
    #endregion

    #region get Overall stats
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
    #endregion

    #region SteamData
    def getSteamData(self, discordID):
        data = None
        with open('DiscordSteamBridge.json') as json_file:  
            data = json.load(json_file)
            print (data)
        try:
            steamData = data[str(discordID)]
            return steamData
        except:
            return None
    #endregion

    #region Player stats per weapon 
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
    #endregion

    def getWeaponByID(self, WeaponID):
        tempdict = self.weapons['CSGO']['Weapons']
        print("\n -------------------------------------------------------------------------\n")
        print (WeaponID)
        print("\n -------------------------------------------------------------------------\n")
        print (tempdict)
        print("\n -------------------------------------------------------------------------\n")
        # for weapon in tempdict:
        #     print (weapon)
        #     if weapon == WeaponID:
        #         offName = weapon.get("OfficialName")
        #         print(f'offName : {offName}')
        #         return offName
        #     else:
        #         pass

        for weapon, weaponInfo in tempdict.items():
            # print("\nweapon:", weapon)

            # print("\n -------------------------------------------------------------------------\n")
            
            for key in weaponInfo:
                print(key + ':', weaponInfo[key])
                print("\n -------------------------------------------------------------------------\n")
                if ((weaponInfo[key] == f'{WeaponID}') and (key == "ID")):
                    offName = weaponInfo["OfficialName"]
                    print (f'{WeaponID} = {offName}')
                    return offName

            # print(weapon[1],weapon[2])
            # if weapon[2] == WeaponID:
            #     return weapon[1]
            # else:
            #     pass

def setup(bot):
    print("loading the CSGOData extention!")
    bot.add_cog(CSGOData(bot))
