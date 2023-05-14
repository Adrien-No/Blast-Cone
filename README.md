# Blast Cone
Blast Cone is a Discord bot in python for League of Legends that also use riot games API.

It will help you in-game by giving pre-game information about your opponents and theirs champions. (Usable from the loading screen)

# Informations
- I keep old versions to save ideas, but the only one that is interesting here is the `7.1`.

# Installation
- You'll need theses libraries : riotwatcher, aiohttp, discord and requests

They can be installed with pip with the command : `pip install lib_name`

I was using an old version of the discord lib : you'll need the 1.7.3 (see command below)
```bash
pip install riotwatcher
pip install aiohttp
pip install requests
pip install -U discord==1.7.3 pip install -U discord.py==1.7.3
```

- You will also need your own APIs keys. See [here for riot](https://developer.riotgames.com/) and [here for discord](https://discord.com/developers/).

- Once you are done with that, fill [this file](/v7.1/donnees/tokens.json) with your own keys and also add your discord id (enable developer mode on discord > right clic on your profile to get it) [here](/donnees/v7.1/pseudo.json).

# Examples
![](/pictures/blast_cone_on_discord.png)
![](/pictures/help_message.png)
![](/pictures/example_advices.png)

# Upgrades
I was adding a command to get information about a summoner (that's the name we give to League of Legends players), and also choose which tips you wants by asking to react to a first message from the bot. By doing so, we would have more space in the screen by having tips only against champions that you needed. 
