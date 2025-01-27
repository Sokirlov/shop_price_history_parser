import re
from urllib import parse
from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from settings.model import ShopProducts
from settings.controller import PageControler
from settings.base_parser import BaseParser
from drivers.undetect_chrom import Scraper


class Silpo(BaseParser):
    """
    Parsing for Silpo products.


    """
    __name__ = 'Silpo'
    base_url = 'https://silpo.ua'
    def fetch_index_page(self):
        """
        Будуємо список з посилань на категорії з основної сторінки
        через селеніум відкриваємо сторінку, клікаємо на кнопку меню чекаємо 1 сек
        забираємо html
        """
        driver_ = Scraper()
        html = driver_.get_page(url='https://silpo.ua', click_=[By.ID, "category-menu-button"])
        soup = BeautifulSoup(html, 'html.parser')
        cookies = driver_.driver.get_cookies()
        driver_.close_driver()
        self.get_category(soup)
        return cookies


    def get_category(self, soup: BeautifulSoup):
        category_block = soup.find('ul', class_='menu-categories')
        all_categories = category_block.find_all(class_='menu-categories__link')
        for category in all_categories:
            name = category.text.strip()
            url = self.get_full_url(category.get('href'))
            self.categories = dict(name=name, url=url)
        self.send_categories()

    def build_pages(self, *args, **kwargs):
        pages = [PageControler(url=i.url, category_id=i.id, parser_class=self, category_page=True) for i in self.categories.values()]
        return pages

    # def get_products(self, soup: BeautifulSoup):
    #     print('get_products')
    #
    # def get_paginated_page(self, soup: BeautifulSoup) -> list[str]:
    #     print('get_paginated_page')

    # --------------------
    @staticmethod
    def get_price(card: BeautifulSoup) -> float:
        # try:
        price_ = card.find('div', class_='product-card-price')
        price_ = price_.findNext('div').get_text().strip()

        # except Exception as e:
        #     print(f'[get_price] {e}')
        #     return 0.0

        price_ = re.search(r'\d+.\d\d', price_).group(0)
        try:
            price = float(price_)
        except ValueError:
            print(f'[get_price] => ValueError {price_} no float')
            return 0.0
        return price

    def get_products(self, soup, category_id) -> list[ShopProducts]:
        all_cards = soup.find_all('shop-silpo-common-product-card')
        del self.products
        for card in all_cards:
            url = None
            link = card.find('a')
            if link:
                url = self.get_full_url(link.get('href'))
            try:
                card_inner = card.find('div', class_='product-card__top-inner')
                img_src = card_inner.find('img').get('src')
            except NoSuchElementException:
                img_src = None
            body_card = card.find('div', class_='product-card__body')
            packege = body_card.find_all('div')[-1]
            if packege:
                try:
                    rating = packege.find(class_='catalog-card-rating--container ng-star-inserted')
                    if rating:
                        rating.decompose()
                except (NoSuchElementException, AttributeError):
                    ...
                packege = packege.get_text().strip()
            try:
                name = card.find('div', class_='product-card__title').get_text().strip()
            except NoSuchElementException:
                continue

            if card.find('div', class_=['card-add-to-basket-soldout', 'cart-soldout']):
                in_stock = True
                price = 0.0
            else:
                in_stock = False
                try:
                    price = self.get_price(card)
                except Exception as e:
                    print(f'[get_price] => {e} | => {name}\t| => {url}')
                    price = 0.0

            prod = dict(name=name,
                                 url=url,
                                 category_id=category_id,
                                 packaging=packege,
                                 img_src=img_src,
                                 price=price,
                                 in_stock=in_stock,
                                 )
            self.products = prod
        return self.products


    def get_updated_pagination_link(self, url, query_, last_page: int) -> str:
        for page in range(2, last_page + 1):
            query_.update(page=page)
            updated_query = parse.urlencode(query_)
            updated_url = url._replace(query=updated_query)
            new_link = updated_url.geturl()
            yield new_link

    def build_pagination_pages(self, link: str) -> list[str]:
        pages = []
        try:
            url = parse.urlparse(link)
            query_ = parse.parse_qs(url.query)
            last_page = query_.get('page')
        except Exception as e:
            # logger.error(f'ERROR -> parse.urlparse({link}) -> {e}')
            return pages

        if isinstance(last_page, list):
            last_page = last_page[0]

        try:
            last_page = int(last_page)
        except ValueError:
            # logger.warning(f'[ERROR PAGINATION PAGE] VALUE IS {last_page}')
            return pages

        for link in self.get_updated_pagination_link(url, query_, last_page):
            new_link = self.get_full_url(link)
            pages.append(new_link)
        return pages

    def get_paginated_page(self, soup: BeautifulSoup) -> list[str]:
        try:
            pagination_block = soup.find('div', class_='pagination__items')
            pagination = pagination_block.find_all('a', class_='pagination-item')
        except (NoSuchElementException, AttributeError):
            return []

        last_pagination = pagination[-1].get('href')
        pages = self.build_pagination_pages(last_pagination)
        print(f'[get_paginations] - > last_pagination: {last_pagination} | {len(pages)} pages | {pages}')
        return pages


    def __init__(self, ):
        super().__init__()

