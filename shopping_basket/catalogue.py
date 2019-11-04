"""
Classes to aid in creating a shopping inventory.
"""


class Item:
    """
    Individual shopping item available in the inventory

    Attributes:
        name (str): product name
        price (float): product cost
        quantity (int): number of products
    """

    def __init__(self, name, price, quantity=1):
        self.name = name
        self.price = price
        self.quantity = quantity

        self._check_valid()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Item({self.name}, {self.price}, {self.quantity})"

    def _check_valid(self):
        if not isinstance(self.name, str):
            raise ValueError(f"item name must be string")
        if self.price <= 0:
            raise ValueError(f"price must be greater than zero")


class Catalogue:
    """
    Inventory of Item objects available

    Attributes:
        items (list: tuple): product names and prices
    """

    def __init__(self, items):
        self.items = self._create(items)

    def _create(self, item_list):
        return [Item(name=item[0], price=item[1]) for item in item_list]

    def get(self, item_name):
        for item in self.items:
            if item_name.lower() == item.name.lower():
                return item

    def fuzzy_get(self, item_sub):
        """
        Gets all items with names that match a given substring
        """
        return [item for item in self.items if item_sub.lower() in item.name.lower()]
