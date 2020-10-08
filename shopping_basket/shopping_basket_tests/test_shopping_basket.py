# Tests for shopping basket

from shopping_basket.shopping_basket import Basket, BasketPricer


def test_add_basket():
    basket = Basket({"baked_beans": 2, "biscuits": 1})
    basket.add("sardines")
    assert "sardines" in basket.items
    assert basket.items["sardines"] == 1


def test_empty_basket():
    basket_pricer = BasketPricer(basket={}, catalogue={}, offers=[])
    subtotal, discount, total = basket_pricer.totals()
    assert subtotal == 0.0
    assert discount == 0.0
    assert total == 0.0