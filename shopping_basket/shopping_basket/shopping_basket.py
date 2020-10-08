""" Module implementing Shopping Basket requirements """

from collections import Counter

from typing import Dict, List


class ItemNotFoundInCatalogueException(Exception):
    pass


class NegativePriceException(Exception):
    pass


class Basket:
    def __init__(self, items):
        self.items = Counter(items)

    def add(self, item_name):
        self.items[item_name] += 1


class Offer:
    def compute_discount(self, basket: Basket, catalogue: Dict[str, float]):
        return 0.0


class BasketPricer:
    def __init__(self, basket: Basket, catalogue: Dict[str, float], offers: List[Offer]):
        self.basket = basket
        self.catalogue = catalogue
        self.offers = offers
        for item in self.basket.items:
            if item not in self.catalogue:
                print(f"{item}")
                raise ItemNotFoundInCatalogueException(item)

    def totals(self):
        subtotal, discount = self.subtotal(), self.discount()
        total = round(subtotal - discount, 2)
        if total < 0.0:
            raise NegativePriceException
        return subtotal, discount, total

    def subtotal(self):
        return round(sum(float(qty) * self.catalogue[item] for item, qty in self.basket.items.items()), 2)

    def discount(self):
        return round(sum(offer.compute_discount(self.basket, self.catalogue) for offer in self.offers), 2)


class BuyXGetYFree(Offer):
    def __init__(self, item_name, x, y):
        self.item_name = item_name
        self.x = x
        self.y = y

    def compute_discount(self, basket: Basket, catalogue: Dict[str, float]):
        qty = basket.items[self.item_name]
        return (qty // (self.x + self.y)) * self.y * catalogue[self.item_name]


class Discount(Offer):
    def __init__(self, item_name, discount):
        self.item_name = item_name
        self.discount = discount

    def compute_discount(self, basket:Basket, catalogue: Dict[str, float]):
        qty = basket.items[self.item_name]
        return qty * self.discount * catalogue[self.item_name]