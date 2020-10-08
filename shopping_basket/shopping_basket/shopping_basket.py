""" Module implementing Shopping Basket requirements """

from collections import Counter


class Basket:
    # Holds items and quantity for each item.
    def __init__(self, items=None):
        self.items = Counter(items)

    def add(self, item_name):
        self.items[item_name] += 1

    def get_individual_items(self):
        # expands items into one item per occurrence
        # e.g. baked_beans 4 -> baked_beans, baked_beans, baked_beans, baked_beans
        return self.items.elements()



