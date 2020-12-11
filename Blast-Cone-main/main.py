import csv, aiohttp, json, asyncio, discord
from discord.ext import commands

api_key_riot = 'RGAPI-52541b27-ec68-4ff8-afaf-340fb85352bb'
api_key_discord = 'NzQ5MzgyNDc2OTEyMjYzMjg5.X0rK0Q.P7LoKQrS-GH1p1erfwpLA7gikpo'
api_version_riot = 'v4'
discord_id_adrifirst = 346632637143842817
#on ajoute le dictionnaire qui permet de relié une donnée de région entrée par l'utilisateur à la véritable syntaxe de la région
all_my_dicts = {'region': {"br":"br1", "eun":"eun1", "euw":"euw1", "jp" :"jp1", "kr":"kr", "la1":"la1", "la2":"la2", "na":"na1", "oc":"oc1","tr":"tr1","ru":"ru" } }

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
        await channel.send('**:green_circle:   Connected !     :green_circle:**')
    
@bot.command()
async def stop(ctx):
    global statut_guild_channel
    
    if ctx.message.author.id == discord_id_adrifirst:
        
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
            await channel.send('*le tout-puissant AdriFirst a ordonné la déconnection du bot...*\n**:red_circle: Disconnected ! :red_circle:**')
            await ctx.message.delete()
        await bot.logout()
    else:
        await ctx.send(f'{ctx.message.author.mention} eh fréro t\'as pas de droit de faire ça !')

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

@bot.command()
async def game_info(ctx, summoner_name, region='euw'):
    #dict account
    await dict_build(f"https://{all_my_dicts['region'][region]}.api.riotgames.com/lol/summoner/{api_version_riot}/summoners/by-name/{summoner_name}?api_key={api_key_riot}",'profile_{summoner_name}')
    #dict spectator
    await dict_build(f"https://{all_my_dicts['region'][region]}.api.riotgames.com/lol/spectator/{api_version_riot}/active-games/by-summoner/{all_my_dicts['profile_{summoner_name}']['id']}?api_key={api_key_riot}",'spectator')
    print(f"https://{all_my_dicts['region'][region]}.api.riotgames.com/lol/spectator/{api_version_riot}/active-games/by-summoner/{all_my_dicts['profile_{summoner_name}']['id']}?api_key={api_key_riot}")
    embed_menu = discord.Embed(title=f"List of summoners in {all_my_dicts['profile_{summoner_name}']['name']}'s game :")
    
    embed_menu.add_field(name='**red team**', value=f":one:{all_my_dicts['spectator']}\n:two:{s2}\n:three:{s3}\n:four:{s4}\n:five:{s5}'.format(s1=summoner0.Name(0),s2=summoner0.Name(1),s3=summoner0.Name(2),s4=summoner0.Name(3),s5=summoner0.Name(4)),inline=True")
    embed_menu.add_field(name='**blue team**',value=':six:{s6}\n:seven:{s7}\n:eight:{s8}\n:nine:{s9}\n:keycap_ten:{s10}'.format(s6=summoner0.Name(5),s7=summoner0.Name(6),s8=summoner0.Name(7),s9=summoner0.Name(8),s10=summoner0.Name(9)),inline=True)
    embed_menu.set_footer(text="react to get more tips")
    
    await ctx.send(embed=embed_menu)
#<===============================================================================================================================================>#

bot.run(api_key_discord)
