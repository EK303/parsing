import json
import asyncio
import aiohttp

from service import get_urls, combine_lists
from parse_html import get_add_data


# Parse 1: parsing initial data (title, urls, description, tags)
async def get_json_data(session, url):
    async with session.get(url) as response:
        json_data = await response.json()
        return json_data["results"]


# Finally, saving collected data in json
async def final_results():
    urls = get_urls()

    if urls:
        async with aiohttp.ClientSession() as session:

            articles = [get_json_data(session, url) for url in urls]

            # list(coroutine) --> list(list)
            results = await asyncio.gather(*articles)

            # list(list(dict)) --> list(dict)
            json_data = await combine_lists(results)

            # parsing information on articles individually
            try:
                add_data = []

                for page in json_data:
                    page_task = asyncio.create_task(get_add_data(page["url"]))
                    add_data.append(page_task)

                ind_data = await asyncio.gather(*add_data)

            except TypeError:
                print("Error in parsing articles individually")

            for elem, page_info in zip(json_data, ind_data):
                elem["text"] = page_info["text"]
                elem["preview"] = page_info["preview"]
                elem["links"] = page_info["links"]

            with open("articles.json", "w") as file:
                json.dump(json_data, file, indent=2)

    else:
        print("Something went wrong. Check your scripts")
    return False
