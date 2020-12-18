import aiohttp, json

async def request(URL):
    async with aiohttp.ClientSession().get(URL) as url:
        
