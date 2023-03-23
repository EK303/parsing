import json
import asyncio
import aiohttp
from utils import create_urls, combine_lists


async def get_json_data(session, url):

    # async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        json_data = await response.json()
        return json_data["results"]


async def final_results():
    urls = create_urls()

    if urls:
        async with aiohttp.ClientSession() as session:
            articles = [get_json_data(session, url) for url in urls]

            # list(coroutine) --> list(list)
            results = await asyncio.gather(*articles)

            # list(list(dict)) --> list(dict)
            json_data = await combine_lists(results)

            with open("articles.json", "w") as file:
                json.dump(json_data, file)

    else:
        print("Something went wrong. Check your scripts")
    return False
