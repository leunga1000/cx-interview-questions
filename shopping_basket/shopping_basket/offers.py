""" Implementation of basket offers. Each is a subclass of the abstract class Offer. """

from shopping_basket.shopping_basket import Basket
from typing import Dict, Set
from operator import itemgetter
from abc import ABC, abstractmethod

class OfferTermsException(Exception):
    pass

class Offer(ABC):
    # Base class for offers, compute_discount will be called for each offer.
    # Offer.compute_discount takes basket and catalogue and returns applicable discount
    @abstractmethod
    def compute_discount(self, basket: Basket, catalogue: Dict[str, float]) -> float:
        return 0.0


class BuyXGetYFree(Offer):
    def __init__(self, item_name, x, y):
        self.item_name = item_name
        self.x = x
        self.y = y

    def compute_discount(self, basket: Basket, catalogue: Dict[str, float]) -> float:
        qty = basket.items[self.item_name]
        return (qty // (self.x + self.y)) * self.y * catalogue[self.item_name]


class DiscountPercent(Offer):
    def __init__(self, item_name, discount_percent):
        self.item_name = item_name
        self.discount = discount_percent / 100.0

    def compute_discount(self, basket: Basket, catalogue: Dict[str, float]) -> float:
        qty = basket.items[self.item_name]
        return qty * self.discount * catalogue[self.item_name]


class BuyNGetCheapestAFree(Offer):
    def __init__(self, items_in_offer: Set[str], n: int, a: int = 1):
        self.items_in_offer = items_in_offer
        self.n = n
        self.a = a
        if n < a:
            raise OfferTermsException

    def compute_discount(self, basket: Basket, catalogue: Dict[str, float]) -> float:
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
