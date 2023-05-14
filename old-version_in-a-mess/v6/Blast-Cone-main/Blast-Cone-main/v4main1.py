import requests, json, discord, random, logging
from discord.ext import commands
from emoji import EMOJI_ALIAS_UNICODE as emojis

#<================================================================== Variables ==================================================================>#
#logs
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

apiKeyRiot = 'RGAPI-decc5fb8-d2d6-4ee8-9d02-15023e78263d'
apiKeyDiscord = 'NzQ5MzgyNDc2OTEyMjYzMjg5.X0rK0Q.V84y2crEaDClBI3Cm3FMPTHyxHw'
dictRegion = { "br":"br1", "eun":"eun1", "euw":"euw1", "jp" :"jp1", "kr":"kr", "la1":"la1", "la2":"la2", "na":"na1", "oc":"oc1","tr":"tr1","ru":"ru" }
dictLanguages = {'cz':'cs_CZ', 'gr':'el_GR','pl':'pl_PL','ro':'ro_RO','hu':'hu_HU','de':'de_DE','es':'es_ES','it':'it_IT','fr':'fr_FR','ja':'ja_JP','ko':'ko_KR','ru':'ru_RU','tu':'tr_TR','th':'th_TH','vi':'vn_VN','id':'id_ID','ch':'zh_CN'}
#crée le dictionnaire des versions de patch
patchURL = 'https://ddragon.leagueoflegends.com/api/versions.json' ; patchAPI = requests.get(patchURL) ; dictPatch = patchAPI.json()

helpMessage = "\n:arrow_right:  **general commands**\n\n > ~help | **displays this menu.**\n\n\n :arrow_right:  **Information about champions**\n\n > ~atips (champion) (first two letters of your language) | **Display Ally Tips about (champion).**\n > ~etips (champion) (first two letters of your language) | **Display Enemy Tips against(champion).**\n\n\n :arrow_right:  **Profile**\n\n > **~pp (username) (server)** | Show the summoner's Profile Picture.\n > **~level (username) (server)** | Display summoner's Level.\n > **~main (username) (server) (number in the ranking of the champions you played the most)**| Display the 'number'th champion who you played the most. example : *~main otpyasuo na 2* will give the second champions played the most by 'otpyasuo'\n > **~mpoint (summoner) (server)** (champion's name with uppercase initials)| Display Mastery Point (summoner) has with (champion) "

#info générales de champions
championDataURL = 'http://ddragon.leagueoflegends.com/cdn/{patch}/data/fr_FR/champion.json'.format(patch=dictPatch[0]) ; championDataAPI = requests.get(championDataURL) ; dictChampionData = championDataAPI.json()

#On crée deux dictionnaires 'dictIdNom' et 'dictNomId' qui permettent en renseignant une donnée (Idchampion ou Nomchampion) d'accèder à l'autre
listNom = dictChampionData['data'].keys() ; dictIdNom = {} ; dictNomId = {}
for nomChampion in listNom:
    dictIdNom[dictChampionData['data'][nomChampion]['key']] = nomChampion ; dictNomId[nomChampion] = dictChampionData['data'][nomChampion]['key']

#images
#file = open('img/lol_logo.jpg')
#with open("/img/lol_logo.jpg", mode='rb') as fileLogo:
#  await channel.send("lol_logo", file=fileLogo)
#<===============================================================================================================================================>#


#<================================================================== classes ===================================================================>#
class summoner():
    def __init__(self,summonerName,region):
        self.summonerName = summonerName
        self.region = region
        #https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/adrifirst?api_key=RGAPI-decc5fb8-d2d6-4ee8-9d02-15023e78263d
        summonerURL = 'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key={apikey}'.format(region=dictRegion[region],summonerName=self.summonerName,apikey=apiKeyRiot)
        summonerAPI = requests.get(summonerURL)
        self.dictSummoner = summonerAPI.json()
        #https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/e7wAdalGkKCgSRID_ustA_xarlkEj6Fr389bWFB72PNgsFg?api_key=RGAPI-decc5fb8-d2d6-4ee8-9d02-15023e78263d
        championMasteryURL = 'https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summonerId}?api_key={apikey}'.format(region = dictRegion[self.region], summonerId = self.dictSummoner['id'], apikey = apiKeyRiot)
        championMasteryAPI = requests.get(championMasteryURL)
        self.dictChampionMastery = championMasteryAPI.json()

        #permet de traduire un id en numéro de Classement de Maitrise de Champion
        self.dictIdNumeroclassement = {}
        for numeroclassement in range(len(self.dictChampionMastery)):
            self.dictIdNumeroclassement[self.dictChampionMastery[numeroclassement]['championId']] = numeroclassement
    #gameInfo _____________________________________________________________________________________________________________________________________
        
        spectatorURL = 'https://{region}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summonerId}?api_key={apikey}'.format(region=dictRegion[self.region],summonerId=self.dictSummoner['id'],apikey=apiKeyRiot) ; spectatorAPI = requests.get(spectatorURL) ; self.dictSpectator = spectatorAPI.json()
        #print(self.dictSpectator)
        self.listNameParticipants = []
        for oneSumm in self.dictSpectator['participants']:
            self.listNameParticipants.append(oneSumm['summonerName'])
        print('liste des participants ',self.listNameParticipants)

    def Name(self,num):
        return self.listNameParticipants[num]
    
    #______________________________________________________________________________________________________________________________________________

    def idEnNumeroclassement(self,Id):
        return self.dictIdNumeroclassement[int(Id)]
    
    def summonerId(self):
        return self.dictSummoner['id']
    def accountId(self):
        return self.dictSummoner['accountId']
    def puuid(self):
        return self.dictSummoner['puuid']
    def name(self):
        return self.dictSummoner['name']
    def summonerLevel(self):
        return self.dictSummoner['summonerLevel']
    def profileIconId(self):
        return self.dictSummoner['profileIconId']
    
class championMastery(summoner):
    def __init__(self,summonerName,region,championNumber):
        summoner.__init__(self,summonerName,region)
        self.championNumber = championNumber

    def championId(self):
        return self.dictChampionMastery[self.championNumber]['championId']
    def championLevel(self):
        return self.dictChampionMastery[self.championNumber]['championLevel']
    def championPoints(self):
        return self.dictChampionMastery[self.championNumber]['championPoints']
    def lastPlayTime(self):
        return self.dictChampionMastery[self.championNumber]['lastPlayTime']
    def chestGranted(self):
        return self.dictChampionMastery[self.championNumber]['chestGranted']
    def tokenEarned(self):
        return self.dictChampionMastery[self.championNumber]['tokenEarned']

class championInfo():
    def __init__(self,champion,language):
        self.champion = champion
        self.language = dictLanguages[language.lower()]
        
        #donnée pour un champion précisémment
        championInfoURL = 'http://ddragon.leagueoflegends.com/cdn/{patch}/data/{language}/champion/{champion}.json'.format(patch=dictPatch[0], language=self.language, champion=self.champion) ; championInfoAPI = requests.get(championInfoURL) ; self.dictChampionInfo = championInfoAPI.json()
        
    def allyTips(self):
        tips = ''
        for i in range(len(self.dictChampionInfo['data'][self.champion]['allytips'])):
            tips += '\n'+self.dictChampionInfo['data'][self.champion]['allytips'][i]
        return tips
    
    def enemyTips(self):
        tips = ''
        for i in range(len(self.dictChampionInfo['data'][self.champion]['enemytips'])):
            tips += '\n'+self.dictChampionInfo['data'][self.champion]['enemytips'][i]
        return tips
        
#<===============================================================================================================================================>#

#<================================================================== commands ===================================================================>#
#crée une instance de 'Bot' : https://discordpy.readthedocs.io/en/latest/ext/commands/api.html
bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def image(ctx):
    await ctx.send("image", file=discord.File(logoFile))


@bot.command()
async def hello(ctx, arg1, arg2):
    await ctx.send('You passed {} and {}'.format(arg1, arg2))

@bot.command()
async def game(ctx, summonerName, region):

    #crée une instance d'un invocateur
    summoner0=summoner(summonerName,region)

    #paramétrage de l'embed (menu principal)
    embedMenu=discord.Embed(title="List of summoners in {summoner}'s game:".format(summoner=summonerName),color=0xff0000)

    embedMenu.add_field(name='**red team**', value=':one:{s1}\n:two:{s2}\n:three:{s3}\n:four:{s4}\n:five:{s5}'.format(s1=summoner0.Name(0),s2=summoner0.Name(1),s3=summoner0.Name(2),s4=summoner0.Name(3),s5=summoner0.Name(4)),inline=True)
    embedMenu.add_field(name='**blue team**',value=':six:{s6}\n:seven:{s7}\n:eight:{s8}\n:nine:{s9}\n:keycap_ten:{s10}'.format(s6=summoner0.Name(5),s7=summoner0.Name(6),s8=summoner0.Name(7),s9=summoner0.Name(8),s10=summoner0.Name(9)),inline=True)
    embedMenu.set_footer(text="react to get more tips")

    message = await ctx.send(embed=embedMenu)
    listEmojisNumbers=[emojis[':one:'],emojis[':two:'],emojis[':three:'],emojis[':four:'],emojis[':five:'],emojis[':six:'],emojis[':seven:'],emojis[':eight:'],emojis[':nine:'],'🔟']
    for i in range(len(summoner0.listNameParticipants)):
        await message.add_reaction(listEmojisNumbers[i])
    
   #embed.set_image(url='https://ddragon.leagueoflegends.com/cdn/10.23.1/img/profileicon/4811.png')
#<===============================================================================================================================================>#

bot.run(apiKeyDiscord)
