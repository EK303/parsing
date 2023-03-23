import aiohttp
from utils import parse_webpage


async def get_html_data(link):
    async with aiohttp.ClientSession() as connection:
        async with connection.get(link) as response:
            return response


async def get_add_data(url):

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            return await parse_webpage(html)
