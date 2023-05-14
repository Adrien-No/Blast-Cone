# Description
Discord bot in python for League of Legends using riot games API.
It will help you in-game by giving pre-game informations about your opponent and theirs champions. (Usable from the loading screen)

## Informations
- I keep old versions to get ideas but the only one that is interesting here is the `7.1`

## Installation
- You'll need theses libraries : riotwatcher, aiohttp, discord and requests
wich can be installed with pip, with the command `pip install lib_name`
I was using an old version of the discord lib : you'll need the 1.7.3 (see command below)
```bash
pip install riotwatcher
pip install aiohttp
pip install requests
pip install -U discord==1.7.3 pip install -U discord.py==1.7.3
```

- You will also need your own APIs keys. See `https://developer.riotgames.com/` for riot and `https://discord.com/developers/` for discord.

Once you are done with that, fill the file `/v7.1/donnees/tokens.json` with your own keys.

## Examples

## upgrades
I was adding a command to get informations about a summoner (that's the name we give to League of Legends players), and also choose witch tips you wants by asking to react to a first message from the bot. By doing so, we would have more space in the screen by having tips only against champions that you needed. 
