import csv, aiohttp, json, asyncio, discord
from discord.ext import commands
from emoji import EMOJI_ALIAS_UNICODE as emojis
#pour compter le nombre d'une réaction
from discord.utils import get

list_emojis_numbers=[emojis[':one:'],emojis[':two:'],emojis[':three:'],emojis[':four:'],emojis[':five:'],emojis[':six:'],emojis[':seven:'],emojis[':eight:'],emojis[':nine:'],'🔟']

with open('donnees/tokens.json', 'r') as tokens:
    informations = json.load(tokens)
    api_key_riot = informations['api_key_riot']
    api_key_discord = informations['api_key_discord']
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

@bot.event
async def on_raw_reaction_add(payload):
    print(payload)
    print('emoji:',payload.emoji.name)
    if payload.emoji.name in list_emojis_numbers:
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = get(message.reactions, emoji=payload.emoji.name)
        #lorsqu'un utilisateur autre que le bot ajoute une réaction
        if reaction.count<1 and str("'"+payload.emoji.name+"'") in list_emojis_numbers:
            print('yessssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
            if payload.emoji.name is list_emojis_numbers[0]:
                print('0')
            elif payload.emoji.name is list_emojis_numbers[1]:
                print('1')
            elif payload.emoji.name is list_emojis_numbers[2]:
                print('2')
            elif payload.emoji.name is list_emojis_numbers[3]:
                print('3')
            elif payload.emoji.name is list_emojis_numbers[4]:
                print('4')
            elif payload.emoji.name is list_emojis_numbers[5]:
                print('5')
            elif payload.emoji.name is list_emojis_numbers[6]:
                print('6')
            elif payload.emoji.name is list_emojis_numbers[7]:
                print('7')
            elif payload.emoji.name is list_emojis_numbers[8]:
                print('8')
            elif payload.emoji.name is list_emojis_numbers[9]:
                print('0')
        else:
            print('marche po:', payload.emoji.name,list_emojis_numbers)
        
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

    
    embed_menu.add_field(name='**red team**', value=f":one:{all_my_dicts['spectator']['participants'][0]['summonerName']}\n\
                                                      :two:{all_my_dicts['spectator']['participants'][1]['summonerName']}\n\
                                                      :three:{all_my_dicts['spectator']['participants'][2]['summonerName']}\n\
                                                      :four:{all_my_dicts['spectator']['participants'][3]['summonerName']}\n\
                                                      :five:{all_my_dicts['spectator']['participants'][4]['summonerName']}")
    embed_menu.add_field(name='**blue team**',value=f":six:{all_my_dicts['spectator']['participants'][5]['summonerName']}\n\
                                                      :seven:{all_my_dicts['spectator']['participants'][6]['summonerName']}\n\
                                                      :eight:{all_my_dicts['spectator']['participants'][7]['summonerName']}\n\
                                                      :nine:{all_my_dicts['spectator']['participants'][8]['summonerName']}\n\
                                                      :keycap_ten:{all_my_dicts['spectator']['participants'][9]['summonerName']}")
    embed_menu.set_footer(text="react to get more tips")
    print('type de l\'embed :',type(embed_menu))
    message = await ctx.send(embed=embed_menu)
    for i in range(len(all_my_dicts['spectator']['participants'])):
        await message.add_reaction(list_emojis_numbers[i])
#<===============================================================================================================================================>#

bot.run(api_key_discord)
