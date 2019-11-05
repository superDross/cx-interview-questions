"""
Classes allow users to store inventory items
"""

from copy import deepcopy
from typing import List, Union

from catalogue import Catalogue, Item
from offers import Offers
from utils import rounder


class Basket:
    """
    Shopping basket to calculate prices of stored items
    """

    def __init__(self, catalogue: Catalogue, offers: Offers) -> None:
        self._items: List[Item] = []
        self.catalogue: Catalogue = catalogue
        self.offers: Offers = offers
        self.subtotal: Union[int, float] = 0
        self.discount: Union[int, float] = 0
        self.total: Union[int, float] = 0

    def add(self, item_name: str, quantity: int = 1) -> None:
        """
        Place a given quantity of an item into the basket
        """
        item = self.catalogue.get(item_name)
        item.quantity = quantity
        if item:
            self._items.append(item)
            self.calculate_price()

    def remove(self, item_name: str, quantity: int = 1) -> None:
        """
        Take a given quantity of an item out the basket
        """
        for item in self._items:
            if item.name.lower() == item_name:
                if item.quantity > quantity:
                    item.quantity -= quantity
                elif item.quantity == quantity:
                    self._items.remove(item)
        self.calculate_price()

    def apply_discount(self) -> None:
        self.discount = 0
        for offer in self.offers:
            # required otherwise applying discounts alters the quantities
            items = deepcopy(self._items)
            discount = offer.calculate_discount(items)
            if discount:
                self.discount += rounder(discount)

    def calculate_price(self) -> None:
        """
        Calculates subtotal, disount & total price of all items in the basket
        """
        self.subtotal = rounder(sum(item.total_price for item in self._items))
        self.apply_discount()
        self.total = rounder(self.subtotal - self.discount)
