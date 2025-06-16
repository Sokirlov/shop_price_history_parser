from bs4 import BeautifulSoup

from .base_parser import BaseParser


class PageControler:
    soup: BeautifulSoup

    def analyze_page(self):
        tasks = []
        if not self.soup:
            raise AttributeError('soup is required. Get soup first.')

        self.parser.get_products(self.soup, self.category_id)
        self.parser.send_products()

        if self.category_page:
            additional_pages = self.parser.get_paginated_page(self.soup)
            tasks = [PageControler(i, self.category_id, self.parser) for i in additional_pages]

        return tasks


    def __hash__(self):
        return hash(self.url)

    def __eq__(self, other):
        return self.url == other.url

    def __repr__(self):
        return f'{self.url}'

    def __init__(self, url: str, category_id: int, parser_class:BaseParser, category_page: bool=False):
        self.parser = parser_class
        self.url = url
        self.category_id = category_id
        self.category_page = category_page
