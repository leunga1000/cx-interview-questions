from shopping_basket.shopping_basket import Basket, BuyXGetYFree, BasketPricer, DiscountPercent

if __name__ == "__main__":
    basket = Basket({"baked_beans": 3,
                     "biscuits": 1,
                     "sardines": 1})
    catalogue = {"baked_beans": 0.99,
                 "biscuits": 1.20,
                 "sardines": 1.89}
    offers = [BuyXGetYFree("baked_beans", x=2, y=1),
              DiscountPercent("sardines", 25)]

    basket_pricer = BasketPricer(basket=basket, catalogue=catalogue, offers=offers)
    subtotal, discount, total = basket_pricer.totals()
    assert subtotal == 6.06
    assert discount == 0.99 + 0.47
    assert total == 4.60
    print(basket.items)
    print(basket_pricer.formatted_totals())

