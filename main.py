import time
import asyncio
import schedule
import logging

from drivers.aiohttp_driver import Scraper
from shops.silpo import Silpo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def run_silpo():
    logging.info('Starting Silpo parsing')
    cookies_dict = None
    try:
        silpo = Silpo()
        cookies = silpo.fetch_index_page()
        if cookies:
            cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        urls = silpo.build_pages(Silpo)
        logging.info(f'I have {len(urls)} pages')
        loop = asyncio.new_event_loop()
        logging.info('Create async loop')
        scraper = Scraper(urls, cookies_dict)
        logging.info(f'Scrape initial {len(urls)} urls')
        urls = loop.run_until_complete(scraper.fetch_all_urls())
        logging.info('start scraping {} pages'.format(len(urls)))
        scraper = Scraper(urls, cookies_dict)
        logging.info(f'Scrape initial {len(urls)} urls')
        loop.run_until_complete(scraper.fetch_all_urls())
    except Exception as e:
        logging.error(e)
        raise e

# Запускаємо парсер сільпо кожного дня о 9:30  server time - 3 hour
schedule.every().day.at("07:00").do(run_silpo)

if __name__ == '__main__':
    # run_silpo()
    while True:
        schedule.run_pending()
        time.sleep(60)
