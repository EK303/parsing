import asyncio

from parsing import create_urls, final_results


loop = asyncio.get_event_loop()
loop.run_until_complete(final_results())




