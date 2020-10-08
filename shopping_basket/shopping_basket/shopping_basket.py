""" Module implementing Shopping Basket requirements """

from collections import Counter
from typing import Dict, List, Set
from operator import itemgetter


class ItemNotFoundInCatalogueException(Exception):
    pass


class NegativePriceException(Exception):
    pass


class OfferTermsException(Exception):
    pass


class Basket:
    # Holds items and quantity for each.
    def __init__(self, items=None):
        if items is None:
            self.items = Counter()
        else:
            self.items = Counter(items)

    def add(self, item_name):
        self.items[item_name] += 1

    def get_individual_items(self):
        # expands items into one item per occurrence
        # e.g. baked_beans 4 -> baked_beans, baked_beans, baked_beans, baked_beans
        return self.items.elements()


class Offer:
    # Base class for offers, compute_discount will be called for each offer.
    def compute_discount(self, basket: Basket, catalogue: Dict[str, float]):
        return 0.0


class BasketPricer:
    def __init__(
        self, basket: Basket, catalogue: Dict[str, float], offers: List[Offer]
    ):
        self.basket = basket
        self.catalogue = catalogue
        self.offers = offers
        for item in self.basket.items:
            if item not in self.catalogue:
                raise ItemNotFoundInCatalogueException(item)

    def subtotal(self):
        return round(
            sum(
                float(qty) * self.catalogue[item]
                for item, qty in self.basket.items.items()
            ),
            2,
        )

    def discount(self):
        return round(
            sum(
                offer.compute_discount(self.basket, self.catalogue)
                for offer in self.offers
            ),
            2,
        )

    def totals(self):
        subtotal, discount = self.subtotal(), self.discount()
        total = round(subtotal - discount, 2)
        if total < 0.0:
            raise NegativePriceException
        return subtotal, discount, total

    def formatted_totals(self):
        subtotal, discount, total = self.totals()
        return f"Subtotal: £{subtotal:.2f}\nDiscount: £{discount:.2f}\nTotal: £{total:.2f}\n"


class BuyXGetYFree(Offer):
    def __init__(self, item_name, x, y):
        self.item_name = item_name
        self.x = x
        self.y = y

    def compute_discount(self, basket: Basket, catalogue: Dict[str, float]):
        qty = basket.items[self.item_name]
        return (qty // (self.x + self.y)) * self.y * catalogue[self.item_name]


class DiscountPercent(Offer):
    def __init__(self, item_name, discount_percent):
        self.item_name = item_name
        self.discount = discount_percent / 100.0

    def compute_discount(self, basket: Basket, catalogue: Dict[str, float]):
        qty = basket.items[self.item_name]
        return qty * self.discount * catalogue[self.item_name]


class BuyNGetCheapestAFree(Offer):
    def __init__(self, items_in_offer: Set[str], n: int, a: int = 1):
        self.items_in_offer = items_in_offer
        self.n = n
        self.a = a
        if n < a:
            raise OfferTermsException

    def compute_discount(self, basket: Basket, catalogue: Dict[str, float]):
        # Get list of Tuples with (item_name, price) for each individual item in basket
        items_prices = [
            (item, catalogue[item])
            for item in basket.get_individual_items()
            if item in self.items_in_offer
        ]
        sorted_items_prices = sorted(items_prices, key=itemgetter(1), reverse=True)
        # Now go through and calculate discount per N batch, remove that batch and pass remaining list
        # into method recursively.
        return self.get_batch_discount_and_remove(sorted_items_prices)

    def get_batch_discount_and_remove(self, batch):
        if len(batch) < self.n:
            return 0.0
        this_batch = batch[: self.n]
        this_discount = sum(px for item, px in this_batch[-self.a :])
        next_batch = batch[self.n :]
        return this_discount + self.get_batch_discount_and_remove(next_batch)
