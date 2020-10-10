""" Module implementing Shopping Basket requirements """

from collections import Counter


class Basket:
    """ Holds items and quantity for each item.
    Can be instantiated empty and then items added
    b = Basket()
    b.add('baked_beans')
    b.add('baked_beans')
    b.add('biscuits')
     or with a dictionary of items and quantities passed in:
    e.g. Basket( {'baked_beans': 3, 'biscuits': 1} )
    """
    def __init__(self, items=None):
        self.items = Counter(items)

    def add(self, item_name):
        self.items[item_name] += 1

    def get_individual_items(self):
        # expands items into one item per occurrence
        # e.g. baked_beans 4 -> baked_beans, baked_beans, baked_beans, baked_beans
        return self.items.elements()



