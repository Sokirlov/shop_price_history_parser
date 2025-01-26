import aiohttp
import asyncio
from bs4 import BeautifulSoup
from settings.controller import PageControler

class Scraper:
    """
    Get pages from page.url and add soup to object then add to to_parse_html
    """

    # to_get_page: list[Page] = []
    # to_parse_html: list[Page] = []
    # print('[fetch_all_urls] {}'.format(self.cookies) )
    #         cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}

    async def fetch_url(self, session, page: PageControler):

        try:
            async with session.get(page.url, ssl=False) as response:
                html =  await response.text()  # Отримуємо текстовий вміст сторінки
                print(f'[get_page] {response.status} => {page.url} => {len(html)} symbols')
                page.soup = BeautifulSoup(html, "html.parser")
                result = page.analyze_page()
                return result

        except Exception as e:
            print(f"Error fetching {page}: {e}")
            await asyncio.sleep(3)
            await self.fetch_url(session, page)

    async def fetch_all_urls(self):


        async with aiohttp.ClientSession(cookies=self.cookies) as session:
            async with self.lock:
                tasks = [self.fetch_url(session, page) for page in self.to_get_page[:3]]  # Створюємо список завдань
                self.to_get_page.clear()

            results = await asyncio.gather(*tasks)
            for result in results:
                # print(f'[get_page] => {len(result)}')
                if result:
                    self.to_get_page.extend(result)

        if self.to_get_page:
            print('I have {} pages to fetch'.format(len(self.to_get_page)))
            return self.to_get_page
        print('all_urls done fetching\n')

    def __init__(self, urls: list[PageControler], cookies: dict[str, str] = None):
        self.lock = asyncio.Lock()
        self.to_get_page = urls
        self.cookies = cookies
