from riotwatcher import *
import aiohttp
import json
import asyncio
import discord
import os
import requests
from discord.ext import commands

region_code = {"br": "br1", "eun": "eun1", "euw": "euw1", "jp": "jp1", "kr": "kr",
               "la1": "la1", "la2": "la2", "na": "na1", "oc": "oc1", "tr": "tr1", "ru": "ru"}
get_champ_id = {}

# on ajoute les clés d'api
with open(os.getcwd()+'/donnees/tokens.json','r') as tokens:
    informations = json.load(tokens)
    api_key_riot = informations['api_key_riot']
    api_key_discord = informations['api_key_discord']

# ajout de l'id discord de l'owner
with open(os.getcwd()+'/donnees/pseudo.json', 'r') as pseudo:
    informations = json.load(pseudo)
    pseudo_founder = informations['id_founder']

# help message
with open(os.getcwd()+'/donnees/help.txt', 'r') as file:
    help_message = file.read()
# instanciation de la classe lol_watcher permettant d'effectuer des recherches web (API riot)
lol_watcher = LolWatcher(api_key_riot)

# get latest version from data_dragon
versions = lol_watcher.data_dragon.versions_for_region('euw1')
latest_version = versions['n']['champion']
champions = lol_watcher.data_dragon.champions(latest_version)
#on complète get_champ_id
for champ in champions['data'].values():
    get_champ_id[champ['key']] = (champ['id'])

team_color = {'100':0x0097FF, '200': 0xff0000}
#<------------------------------- importation des fichiers locaux --------------------------------->#
# ensuite on va piquer dans ce dic pour prendre ce qu'il nous faut pour chaque embed (sinon on dépasserais la limite des 10files)
all_local_files = {}
#<----------rank---------->
path = 'donnees/tiers/'
div = ['i', 'ii', 'iii', 'iv']
tiers = ['iron', 'bronze', 'silver', 'gold', 'platinum', 'diamond']
tiers_without_divs = ['unranked', 'master', 'grandmaster', 'challenger']
for t in tiers:
    for d in div:
        all_local_files[t+d] = discord.File(f'{path}{t}_{d}.png', filename =t+d+'.png')
for t in tiers_without_divs:
        all_local_files[t+'i' ] = discord.File(f'{path}{t}_i.png', filename =t+'i.png')
#<------------------------>

#<-----mastery level------>
path = 'donnees/icons/'
for level in range(8):
    all_local_files[str(level)] = discord.File(f'{path}{level}.png', filename =str(level)+'.png')
#<------------------------>
#print(all_local_files)
#<------------------------------------------------------------------------------------------------>#

#<-------- infos précises chargées petit à petit (on pourra plus tard stocker sur le pc) --------->#
strict_info_champ = {} #clés sont sous forme d'id de champion
players = {} #clés sous forme de summonerName attention faudra update
#<------------------------------------------------------------------------------------------------>#

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

##@bot.event
##async def on_command_error(ctx, error):
##    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
##        await ctx.send('a required argument is missing.')
##    print('error')

@bot.command()
async def stop(ctx):
    '''only me can use this :devil:'''
    if ctx.message.author.id == pseudo_founder:
        await bot.logout()

@bot.command(aliases=['cmds', 'h', 'helps', 'helplease', 'amlost'])
async def commands(ctx):
    '''send a detailled help message'''
    await ctx.send(help_message)

@bot.command(aliases=['gameinfo', 'gi', 'tip', 'advices'])
async def tips(ctx, host_name, region='euw', language='fr_FR'):
    '''Send an embed with tips to play with or against each champs in host_name's game'''
    # host is the player witch we are looking for his match

    region = region.lower()
    regionc = region_code[region] #region code, smth like : "euw1"
    #summoner = lol_watcher.summoner.by_name(regionc, host_name)
    #spectators = lol_watcher.spectator.by_summoner(regionc,summoner['id'])
    try:
        summoner = lol_watcher.summoner.by_name(regionc, host_name)
        spectators = lol_watcher.spectator.by_summoner(regionc,summoner['id'])
    except requests.exceptions.HTTPError:
        await ctx.send(f'{host_name} is not currently in-game')
        return

    host_id = summoner['id']

    #on récupère l'équipe du joueur recherché (pour adapter les conseils)
    for summ in spectators['participants']:
        if host_id == summ['summonerId']:
            host_team = str(summ['teamId'])

    for summ in spectators['participants']:
        #attention, certains noms d'invocateur, à cause de certains chars,
        #semblent poser soucis

        summ_id = summ['summonerId']
        summ_name = summ['summonerName']
        summ_name_no_space = summ_name.replace(' ', '')
        #summ_name_no_space = ''
        summ_champ_id = str(summ['championId'])
        summ_champ_name = get_champ_id[summ_champ_id]
        summ_team = str(summ['teamId'])

        league = lol_watcher.league.by_summoner(regionc, summ_id)
        champ_mastery = lol_watcher.champion_mastery.by_summoner_by_champion(regionc, summ_id, summ_champ_id)

        #----------------------------------on met au point les conseils-------------------------------------#
        #pour aggrandir strict_info_champ, pas avoir à faire tout au début et pas faire 2x la meme chose
        #strict info champ est là où l'on récupère les conseils (tips)
        if summ_champ_id  not in strict_info_champ.keys():
            async with aiohttp.ClientSession() as client:
                async with client.get(f'http://ddragon.leagueoflegends.com/cdn/{latest_version}/data/{language}/champion/{summ_champ_name}.json') as url:
                    #print(url)
                    strict_info_champ[summ_champ_id] = await url.json()

        tips = ''
        #conseil d'ami
        if summ_team == host_team:
            for tip in strict_info_champ[summ_champ_id] ['data'] [summ_champ_name] ['allytips']:
                tips+=':arrow_right:'+tip+'\n'

        #conseil d'enemy
        elif summ_team != host_team:
            for tip in strict_info_champ[summ_champ_id] ['data'] [summ_champ_name] ['enemytips']:
                tips+=':arrow_right:'+tip+'\n'

        #si jamais y'a pas de donnée
        if tips == '':
            tips = ':x: no datas :sob:'
        #---------------------------------------------------------------------------------------------------#

        #----------------------local files importation (pictures of rank and mastery level)-----------------#
        # on récupère les fichiers dont on a besoin pour cet embed depuis all_local_files
        local_files = []
        #tier = league[0]['tier'].lower()
        #rank = league[0]['rank'].lower()

        #print(all_local_files)
        #print(all_local_files[tier+rank])

        #local_files.append(all_local_files[tier+rank])

        #---------------------------------------------------------------------------------------------------#

        e=discord.Embed(title=summ_name, url=f"https://{region}.op.gg/summoner/userName={summ_name_no_space}", color=team_color[summ_team])
        e.set_author(name=summ_champ_name, url=f"https://u.gg/lol/champions/{summ_champ_name}/build", icon_url=f"http://ddragon.leagueoflegends.com/cdn/{latest_version}/img/champion/{summ_champ_name}.png")

        e.add_field(name='tips', value=tips, inline = False)
        e.add_field(name='lolcounter', value='https://lolcounter.com/champions/{summ_champ_name}')
        e.set_thumbnail(url='attachment://challengeri.png')
        e.set_footer(text ='react to get an Embed with more details about this summoner')
        await ctx.send(embed=e)
bot.run(api_key_discord)
