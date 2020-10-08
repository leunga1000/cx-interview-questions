from shopping_basket.shopping_basket import Basket
from shopping_basket.offers import Offer
from typing import Dict, List

class ItemNotFoundInCatalogueException(Exception):
    pass

class NegativePriceException(Exception):
    pass

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
