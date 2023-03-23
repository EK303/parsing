import json
import asyncio
import aiohttp
from utils import create_urls


async def get_json_data(session, url):
    # async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        json_data = await response.json()
        return json_data["results"]


async def final_results():

    urls = create_urls()

    if urls:

        json_data = []

        async with aiohttp.ClientSession() as session:
            articles = [get_json_data(session, url) for url in urls]
            results = await asyncio.gather(*articles)
            for result in results:
                json_data.append(result[0])
        with open("articles.json", "w") as file:
            json.dump(results[0], file)



