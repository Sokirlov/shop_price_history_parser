import time
import asyncio
import schedule

from drivers.aiohttp_driver import Scraper
from shops.silpo import Silpo


def run_silpo():
    cookies_dict = None
    silpo = Silpo()
    cookies = silpo.fetch_index_page()
    if cookies:
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    urls = silpo.build_pages(Silpo)
    print(f'I have {len(urls)} pages')
    urls = asyncio.run(Scraper(urls, cookies=cookies_dict).fetch_all_urls())
    print('start scraping {} pages'.format(len(urls)))
    asyncio.run(Scraper(urls=urls, cookies=cookies_dict).fetch_all_urls())


# Запускаємо парсер сільпо кожного дня о 9:30
schedule.every().day.at("09:30").do(run_silpo)

if __name__ == '__main__':
    # run_silpo()
    while True:
        schedule.run_pending()
        time.sleep(60)


# if __name__ == '__main__':
#     silpo = Silpo()
#     silpo.fetch_index_page()
#     pages = silpo.build_pages(Silpo)
#     print(f'I have {len(pages)} pages')
#     run_scraper(pages)
