import asyncio
from os import environ

import aiohttp
import ujson
from bs4 import BeautifulSoup, element

URL = 'https://departures.to/'
WEBHOOK_URL = environ.get("TESTFLIGHT")
data_old = []
urls_dict = {}


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def fetch_current():
    current_apps = []
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, URL)
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.find_all(class_='columns')

        for result in results:
            if isinstance(result, element.Tag):
                if result.find('p', class_="has-text-success") is not None:

                    time = result.find(
                        'p', class_="has-text-light").text.strip()
                    try:
                        if ("second" in time) or ("minute" in time and int(time.split()[0]) < 5) or ("now" in time):
                            name = result.find(
                                'p', class_="has-text-warning").text.strip()

                            urls_dict[name] = f'http://departures.to{result.find_parent("a")["href"]}'
                            current_apps.append(name)
                    except ValueError:
                        pass

    return current_apps


async def main():
    data_old = await fetch_current()
    print(data_old)

    while True:
        data_now = await fetch_current()
        diff = list(set(data_now) - set(data_old))
        for app in diff:
            async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
                await session.post(WEBHOOK_URL, json={'username': 'Departures.To', 'avatar_url': 'https://miro.medium.com/max/384/1*zW1AZEwt3xklS7HZcmm2sg.png', 'content': f'{app} just had a TestFlight spot open up! {urls_dict[app]}'})
            print("NEW", app + urls_dict[app])
        data_old = data_now
        await asyncio.sleep(10)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
