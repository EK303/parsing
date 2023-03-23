import asyncio

from parsing import final_results


loop = asyncio.get_event_loop()
loop.run_until_complete(final_results())




