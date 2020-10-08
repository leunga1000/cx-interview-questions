# Tests for shopping basket

from shopping_basket.shopping_basket import Basket, BasketPricer, BuyXGetYFree


def test_add_basket():
    basket = Basket({"baked_beans": 2, "biscuits": 1})
    basket.add("sardines")
    assert "sardines" in basket.items
    assert basket.items["sardines"] == 1


def test_empty_basket():
    basket_pricer = BasketPricer(basket=Basket({}), catalogue={}, offers=[])
    subtotal, discount, total = basket_pricer.totals()
    assert subtotal == 0.0
    assert discount == 0.0
    assert total == 0.0


def test_single_item():
    basket = Basket({'baked_beans': 1})
    catalogue = {'baked_beans': 0.99}
    basket_pricer = BasketPricer(basket=basket, catalogue=catalogue, offers=[])
    subtotal, discount, total = basket_pricer.totals()
    assert subtotal == 0.99
    assert discount == 0.0
    assert total == 0.99


def test_multiple_of_one_item():
    basket = Basket({'baked_beans': 2})
    catalogue = {'baked_beans': 0.99}
    basket_pricer = BasketPricer(basket=basket, catalogue=catalogue, offers=[])
    subtotal, discount, total = basket_pricer.totals()
    assert subtotal == 1.98
    assert discount == 0.0
    assert total == 1.98


def test_multiple_items():
    basket = Basket({'baked_beans': 2, 'biscuits': 1})
    catalogue = {'baked_beans': 0.99, 'biscuits': 1.20}
    basket_pricer = BasketPricer(basket=basket, catalogue=catalogue, offers=[])
    subtotal, discount, total = basket_pricer.totals()
    print(subtotal, discount, total)
    assert subtotal == 3.18
    assert discount == 0.0
    assert total == 3.18


def test_buy_2_get_1_free_insufficient_numbers():
    basket = Basket({'baked_beans': 2, 'biscuits': 1})
    catalogue = {'baked_beans': 0.99, 'biscuits': 1.20}
    offers = [BuyXGetYFree('baked_beans', x=2, y=1)]
    basket_pricer = BasketPricer(basket=basket, catalogue=catalogue, offers=offers)
    subtotal, discount, total = basket_pricer.totals()
    assert subtotal == 3.18
    assert discount == 0.0
    assert total == 3.18


def test_buy_2_get_1_free():
    basket = Basket({'baked_beans': 3, 'biscuits': 1})
    catalogue = {'baked_beans': 0.99, 'biscuits': 1.20}
    offers = [BuyXGetYFree('baked_beans', x=2, y=1)]
    basket_pricer = BasketPricer(basket=basket, catalogue=catalogue, offers=offers)
    subtotal, discount, total = basket_pricer.totals()
    assert subtotal == 4.17
    assert discount == 0.99
    assert total == 3.18


def test_buy_4_get_2_free():
    basket = Basket({'baked_beans': 6, 'biscuits': 1})
    catalogue = {'baked_beans': 0.99, 'biscuits': 1.20}
    offers = [BuyXGetYFree('baked_beans', x=2, y=1)]
    basket_pricer = BasketPricer(basket=basket, catalogue=catalogue, offers=offers)
    subtotal, discount, total = basket_pricer.totals()
    assert subtotal == 7.14
    assert discount == 1.98
    assert total == 5.16
