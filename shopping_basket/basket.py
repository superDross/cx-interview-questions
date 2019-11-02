"""
Classes allow users to store inventory items
"""

from utils import rounder


class Basket:
    """
    Shopping basket to calculate prices of stored items

    Attributes:
        catalogue (Catalogue): shopping inventory
        offers (Offers): discounts available across products
    """

    def __init__(self, catalogue, offers):
        self._items = []
        self.catalogue = catalogue
        self.offers = offers
        self.subtotal = 0
        self.discount = 0
        self.total = 0

    def add(self, item_name, quantity=1):
        """
        Place a given quantity of an item into the basket
        """
        item = self.catalogue.get(item_name)
        item.quantity = quantity
        if item:
            self._items.append(item)
            self.calculate_price()

    def remove(self, item_name, quantity=1):
        """
        Take a given quantity of an item out the basket
        """
        item_names = [item.name.lower() for item in self._items]
        item_index = item_names.index(item_name)
        self._items.pop(item_index)
        self.calculate_price()

    def apply_discount(self):
        self.discount = 0
        for offer in self.offers.discounts:
            discount = offer.calculate_discount(self._items)
            if discount:
                self.discount += rounder(discount)

    def calculate_price(self):
        """
        Calculates subtotal, disount & total price of all items in the basket
        """
        self.subtotal = rounder(sum(item.price * item.quantity for item in self._items))
        self.apply_discount()
        self.total = rounder(self.subtotal - self.discount)
