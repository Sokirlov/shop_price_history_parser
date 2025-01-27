from typing import Optional


class ShopCategory:
    """
        Model for Category in database
    """

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.url

    def __init__(self,
                 name,
                 url,
                 shop_id: int = 1,
                 id: Optional[int] = None,
                 *args, **kwargs):

        self.name = name
        self.url = url
        self.shop_id = shop_id
        self.id = id


class ShopProducts:
    """
        Model for products in database
    """
    def __init__(self,
                 name: str,
                 url: str,
                 category_id: int,
                 packaging: str,
                 img_src: str = '',
                 price: float = 0.0,
                 **kwargs):

        self.in_stock = False if price > 0.0 else True
        self.category_id = category_id
        self.packaging = packaging
        self.img_src = img_src
        self.name = name
        self.price = price
        self.url = url

    def __repr__(self):
        return f'{self.name}: {self.price} грн'
