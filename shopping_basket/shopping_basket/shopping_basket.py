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
        pass


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
        total = subtotal - discount
        if total < 0.0:
            raise NegativePriceException
        return subtotal, discount, total

    def subtotal(self):
        return sum(qty * self.catalogue[item] for item, qty in self.basket.items.items())

    def discount(self):
        return sum(offer.compute_discount(self.basket, self.catalogue) for offer in self.offers)
            