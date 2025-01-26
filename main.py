import time
import asyncio
import schedule

from drivers.aiohttp_driver import Scraper
from shops.silpo import Silpo


def run_silpo():
    silpo = Silpo()
    cookies = silpo.fetch_index_page()

    urls = silpo.build_pages(Silpo)
    print(f'I have {len(urls)} pages')
    urls = asyncio.run(Scraper(urls, cookies=cookies).fetch_all_urls())
    print('start scraping {} pages'.format(len(urls)))
    asyncio.run(Scraper(urls=urls, cookies=cookies).fetch_all_urls())


# Запускаємо парсер сільпо кожного дня о 12:30
schedule.every().day.at("12:30").do(run_silpo)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(60)

