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

#on ajoute le dictionnaire qui permet de relier une donnée de région entrée par l'utilisateur à la véritable syntaxe de la région
amd = {'region': {"br":"br1", "eun":"eun1", "euw":"euw1", "jp" :"jp1", "kr":"kr", "la1":"la1", "la2":"la2", "na":"na1", "oc":"oc1","tr":"tr1","ru":"ru" } }

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
    This function is used each time we want to execute a web request by using an URL (first arg) to extract a json file and create a dictionnary.
    (name) will be the key to acces to this new dict from 'amd'(all_my_dicts).
    '''
    
    async with aiohttp.ClientSession() as client:
        async with client.get(URL) as url:
            amd[name] = await url.json()

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

#I would like to modify the content of an embed when a reaction is added
@bot.event
async def on_raw_reaction_add(payload):
    #check if user isn't a bot. faudrait aussi tester que c'est bien un embed et créé par game_info
    if payload.member.bot == False:
        #on va chercher le channel textuel à partir de son id avec le client(bot)
        channel = bot.get_channel(payload.channel_id)
        #on va récupère le message à partir de son id
        message= await channel.fetch_message(payload.message_id)
        
        embed2 = message.embeds[0].add_field(name='zebi',value='pump it up',inline=True)
        await message.edit(embed=embed2)

        #faut faire les differents cas en fonction de la réaction ajoutée (on peut utiliser une fonction) puis garder les 2premiers add field
        #et supprimer si y'a un 3e car ce sera les info d'un autre invocateur
        
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

#played champ doit être avec la maj au début + faire gaffe à wukong
async def embed_sum(sum_name):
    '''create an embed about a specific summoner'''
    #we check if the summoner is in game or not
    #...
    embed=discord.Embed(title="link to op.gg", url=f"https://euw.op.gg/summoner/userName=sum_name", description="rank in soloQ and xxx mastery points with actually champ")
    embed.set_author(name=sum_name, icon_url="http://ddragon.leagueoflegends.com/cdn/11.3.1/img/profileicon/588.png")
    embed.set_thumbnail(url=f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{played_champ}_0.jpg")

    embed.add_field(name="Countertips", value="mettre des wards", inline=False)
    embed.set_footer(text="react to get more tips")
    return embed
#<=====================================================================>#

@bot.command(aliases=['commands','cmds'])
async def helplease(ctx):
    await ctx.send(help_message)

@bot.command(aliases=['gi'])
async def game_info(ctx, summoner_name.lower(), region='euw'):
    #dict account
    
    await dict_build(f"https://{amd['region'][region]}.api.riotgames.com/lol/summoner/{api_version_riot}/summoners/by-name/{summoner_name}?api_key={api_key_riot}",'{summoner_name}')

    #dict spectator
    await dict_build(f"https://{amd['region'][region]}.api.riotgames.com/lol/spectator/{api_version_riot}/active-games/by-summoner/{amd['{summoner_name}']['id']}?api_key={api_key_riot}",'spectator_{summoner_name}')
    print(f"https://{amd['region'][region]}.api.riotgames.com/lol/spectator/{api_version_riot}/active-games/by-summoner/{amd['profile_{summoner_name}']['id']}?api_key={api_key_riot}")
    #envoi de l'embed de départ
    embed_menu = discord.Embed(title=f"List of summoners in {amd['profile_{summoner_name}']['name']}'s game :")
    #on crée un dic comprenant les participants
    participants = {}
    for i_sum in range(10):
        participants[amd['spectator_{summoner_name}']['participants'][i_sum]['summonerName']]
    embed_menu.add_field(name='**blue team**', value=f":one:{amd['spectator_{summoner_name}']['participants'][0]['summonerName']}\n:two:{amd['spectator_{summoner_name}']['participants'][1]['summonerName']}\n:three:{amd['spectator_{summoner_name}']['participants'][2]['summonerName']}\n:four:{amd['spectator_{summoner_name}']['participants'][3]['summonerName']}\n:five:{amd['spectator_{summoner_name}']['participants'][4]['summonerName']}",inline=True)
    embed_menu.add_field(name='**red team**',value=f":six:{amd['spectator_{summoner_name}']['participants'][5]['summonerName']}\n:seven:{amd['spectator_{summoner_name}']['participants'][6]['summonerName']}\n:eight:{amd['spectator_{summoner_name}']['participants'][7]['summonerName']}\n:nine:{amd['spectator_{summoner_name}']['participants'][8]['summonerName']}\n:keycap_ten:{amd['spectator_{summoner_name}']['participants'][9]['summonerName']}",inline=True)
    embed_menu.set_footer(text="react to get more tips")
    print(ctx.message)
    msg_embed = await ctx.send(embed=embed_menu)
    #ajout des réactions associés au numéro de joueur
    listEmojisNumbers=[emojis[':one:'],emojis[':two:'],emojis[':three:'],emojis[':four:'],emojis[':five:'],emojis[':six:'],emojis[':seven:'],emojis[':eight:'],emojis[':nine:'],'🔟']
    for i in range(len(amd['spectator']['participants'])):
        await msg_embed.add_reaction(listEmojisNumbers[i])
    
    
#<===============================================================================================================================================>#

bot.run(api_key_discord)
