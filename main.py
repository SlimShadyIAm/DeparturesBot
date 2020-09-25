import aiohttp
import asyncio
from bs4 import BeautifulSoup

URL = 'https://departures.to'


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'http://python.org')
        print(html)

        soup = BeautifulSoup(html, 'html.parser')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
