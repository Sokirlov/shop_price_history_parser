import requests

from urllib import parse
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

from settings.model import ShopCategory, ShopProducts
from settings.config import settings


class BaseParser(ABC):
    base_url: str
    BACKEND_URLS = {
        'categories': settings.API_URL_CATEGORIES,
        'products': settings.API_URL_PRODUCTS,
    }

    __categories: dict[str, ShopCategory] = {}
    __products: list[ShopProducts] = []

    @property
    def products(self):
        return self.__products

    @products.setter
    def products(self, value):
        self.__products.append(ShopProducts(**value))

    @products.deleter
    def products(self):
        self.__products = []

    @property
    def categories(self) -> dict[str, ShopCategory]:
        return self.__categories

    @categories.setter
    def categories(self, value: dict) -> None:
        if not value or 'name' not in value or 'url' not in value:
            raise AttributeError('Category name and url are required.')
        url = value['url']
        self.__categories[url] = ShopCategory(**value)

    @categories.deleter
    def categories(self) -> None:
        self.__categories = {}

    @abstractmethod
    def get_category(self, soup: BeautifulSoup) -> None:
        """
        This method parse html data with BeautifulSoup and add each category
        to self.categories.
        Example:
            self.categories = {'name':name, 'url':url, 'shop_id': 1}

        :param soup:
        :return:
        """
        pass

    @abstractmethod
    def get_paginated_page(self, soup: BeautifulSoup) -> list[str]:
        """
        This method parse html data with BeautifulSoup and mast return full url to additional pages in this category.
        :param soup:
        :return:
        """
        pass

    @abstractmethod
    def get_products(self, soup: BeautifulSoup, category_id: int) -> list[ShopProducts]:
        """
        This method parse html data with BeautifulSoup and add each product to self.products.
         Example:
            self.products = {
                    'name':name,
                    'url':url,
                    'category_id': 1,
                    'packaging': '200г,
                    'img_src': 'https://my_omen.com/img.jpg',
                    'price': 0.0,
            }

        :param soup: it`s html data from page in BeautifulSoup object
        :param category_id: you can get from self.categories
        :return:
        """
        pass

    @staticmethod
    def send_data(url, data):
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def get_full_url(self, url: str) -> str:
        return parse.urljoin(self.base_url, url)

    def send_categories(self, n=5) -> None:
        data = [i.__dict__ for i in self.categories.values()]
        response = self.send_data(self.BACKEND_URLS['categories'], data)

        for category in response:
            self.categories = category

    def send_products(self) -> None:
        data = [i.__dict__ for i in self.products]
        self.send_data(self.BACKEND_URLS['products'], data)
