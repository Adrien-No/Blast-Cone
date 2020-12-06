import csv, aiohttp, json, asyncio, discord
from discord.ext import commands

api_key_riot = 'RGAPI-decc5fb8-d2d6-4ee8-9d02-15023e78263d'
api_key_discord = 'NzQ5MzgyNDc2OTEyMjYzMjg5.X0rK0Q.sAtArrBOa6W3Hql3DSWTnY5MaPQ'

all_my_dicts = {}
#await dict_build('https://ddragon.leagueoflegends.com/api/versions.json','versions')
#await ctx.send(all_my_dicts['versions'][0])

#on récupère les données du fichier csv
statut_guild_channel = {}
with open('donnees/statut_channel.csv', 'r', newline='') as file:                   
    reader = csv.DictReader(file)
    for row in reader:
        statut_guild_channel[row['guild_id']] = row['channel_id']

#fichier d'aide
with open('donnees/help.txt', 'r') as file:
    help_message = file.read()
    
async def dict_build(URL,name):
    '''
    This function is used each time we want to execute a web request by using an URL (first arg) to extract a json file and create a dictionnaty.
    (name) will be the key to acces to this new dict from 'all_my_dicts'.
    '''
    
    async with aiohttp.ClientSession() as client:
        async with client.get(URL) as url:
            all_my_dicts[name] = await url.json()

#<================================================================== commands ===================================================================>#
            
#<=============================== setup ===============================>#
            
bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

    #dictionnaires 'globaux' :
    await dict_build('https://ddragon.leagueoflegends.com/api/versions.json','versions')
    
    #envoi une alerte de connexion à tout les serveurs
    for key,value in statut_guild_channel.items():
        channel=bot.get_channel(int(value))
        await channel.send('**Connected !    :green_circle:**')
    
@bot.command()
async def stop(ctx):
    global statut_guild_channel
    
    if ctx.message.author.id == 346632637143842817:
        
        #on update le fichier csv avant de quitter
        with open('donnees/statut_channel.csv', 'w') as file:
            fieldnames = ['guild_id','channel_id']
            writer = csv.DictWriter(file,fieldnames=fieldnames)
            writer.writeheader()
            for key,value in statut_guild_channel.items():
                writer.writerow({'guild_id': key, 'channel_id': value})

        #envoi une alerte de déconnexion à tout les serveurs
        for key,value in statut_guild_channel.items():
            channel=bot.get_channel(int(value))
            await channel.send('**Disconnected ! :red_circle:**')
        await bot.logout()

@bot.command()
async def set_statut_channel(ctx):
    '''
    This function is used to set the channel where the informations 'bot connected/bot disconnected' are send in each guilds
    '''
    global statut_guild_channel
    
    statut_guild_channel[ctx.guild.id] = ctx.channel.id
    
    await ctx.send(f'Le channel #{ctx.channel.name} (id : {ctx.channel.id}) à été défini comme channel de statut (bot connecté/déconnecté) \
pour le serveur {ctx.guild.name} (id : {ctx.guild.id}) ')

#<=====================================================================>#

@bot.command()
async def helplease(ctx):
    await ctx.send(help_message)


#<===============================================================================================================================================>#

bot.run(api_key_discord)
