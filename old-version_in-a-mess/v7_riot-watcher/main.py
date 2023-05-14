from riotwatcher import *
import aiohttp
import json
import asyncio
import discord
from discord.ext import commands

# on ajoute les clés d'api
with open('C:\Users\Adriroot\Documents\INFORMATIQUE\Python\bot_discord\v7_riot-watcher\donnees','r') as tokens:
    informations = json.load(tokens)
    api_key_riot = informations['api_key_riot']
    api_key_discord = informations['api_key_discord']

# itération de la classe lol_watcher permettant d'effectuer des recherches web
lol_watcher = LolWatcher(api_key_riot)
# used for
# get latest version from data_dragon
versions = lol_watcher.data_dragon.versions_for_region('euw1')
latest_version = versions['n']['champion']
print(latest_version)
current_champ_list = lol_watcher.data_dragon.champions(latest_version)


def embed_sum(sum_name, server='euw1', ingame=False):
    '''create an embed about a specific summoner'''
    summoner = lol_watcher.summoner.by_name(server, sum_name)

    league = lol_watcher.league.by_summoner(server, summoner['id'])

    champion_mastery = lol_watcher.champion_mastery.by_summoner(
        server, summoner['id'])

    #embed=discord.Embed(title="link to op.gg", url=f"https://euw.op.gg/summoner/userName={sum_name}", description="rank in soloQ and xxx mastery points with actually champ")
    #embed.set_author(name=sum_name, icon_url="http://ddragon.leagueoflegends.com/cdn/11.3.1/img/profileicon/588.png")
    # embed.set_image(current_champ_list['Aatrox']['image']['full'])


embed_sum('AdriFirst')
