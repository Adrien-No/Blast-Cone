import csv, aiohttp, json, asyncio, discord
from discord.ext import commands
from emoji import EMOJI_ALIAS_UNICODE as emojis
#fichier avec les clés, non envoyé quand on push to git
with open('donnees/tokens.json', 'r') as tokens:
    informations = json.load(tokens)
    api_key_riot = informations['api_key_riot']
    api_key_discord = informations['api_key_discord']
api_version_riot = 'v4'
discord_id_adrifirst = 346632637143842817

async def get_real_name(sum_name):
    '''Users will output sum_name but not everytime with the exactly spelling. That's why we shearch for the \
        exactly spelling here'''
    URL = f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{sum_name}?api_key={api_key_riot}'
    async with aiohttp.ClientSession() as client:
        async with client.get(URL) as url:
            temp_dic = await url.json()
    return temp_dic['name']

amd={}
async def dict_build(URL,name):
    '''
    This function is used each time we want to execute a web request by using an URL (first arg) to extract a json file and create a dictionnary.
    (name) will be the key to acces to this new dict from 'amd'(all_my_dicts).
    '''
    
    async with aiohttp.ClientSession() as client:
        async with client.get(URL) as url:
            amd[name] = await url.json()

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_message(message):
    if message.author.id == discord_id_adrifirst:
        sum_name='Adrifirst'
        played_champ='Shaco'
        region = 'euw1'
        ingame=False

        sum_name = await get_real_name(sum_name)

        #dict summoner acc
        await dict_build(f'https://{region}.api.riotgames.com/lol/summoner/{api_version_riot}/summoners/by-name/{sum_name}?api_key={api_key_discord}','acc_{sum_name}')

        #dict des champions de sum_name
        await dict_build(f'https://{region}.api.riotgames.com/lol/champion-mastery/{api_version_riot}/champion-masteries/by-summoner/{amd["acc_"+"sum_name"][id]}?api_key={api_key_riot}', 'champ_{sum_name}')

        #dict de la league du sum_name
        await dict_build(f'
        embed=discord.Embed(title="link to op.gg", url=f"https://euw.op.gg/summoner/userName={sum_name}", description="rank in soloQ and xxx mastery points with actually champ", color=0xff0000)
        embed.set_author(name=sum_name, icon_url="http://ddragon.leagueoflegends.com/cdn/11.3.1/img/profileicon/588.png")
        embed.set_thumbnail(url=f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{played_champ}_0.jpg")

        embed.add_field(name="Countertips", value="mettre des wards", inline=False)
        embed.set_footer(text="react to get more tips")
        await message.channel.send(embed=embed)

        await dict_build('https://ddragon.leagueoflegends.com/api/versions.json','version')

bot.run(api_key_discord)
