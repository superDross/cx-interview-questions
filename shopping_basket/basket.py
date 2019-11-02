"""
Classes allow users to store inventory items
"""

from utils import rounder


class BaseBasket:
    """
    Shopping basket with no ability to apply discounts

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
        item_names = [x.name for x in self._items]
        item_index = item_names.index(item_name)
        self._items.pop(item_index)
        self.calculate_price()

    def apply_discount(self):
        pass

    def calculate_price(self):
        """
        Calculates subtotal, disount & total price of all items in the basket
        """
        self.subtotal = rounder(sum(x.price * x.quantity for x in self._items))
        self.apply_discount()
        self.total = rounder(self.subtotal - self.discount)


class Basket(BaseBasket):
    """
    Shopping basket that applies discounts
    """

    def __init__(self, catalogue, offers):
        super().__init__(catalogue, offers)

    def _percentage_discount(self, offer):
        item = self.catalogue.get(offer.name)
        if item:
            discount = (item.price * (offer.perc / 100)) * item.quantity
            self.discount += rounder(discount)

    def _one_free_discount(self, offer):
        item = self.catalogue.get(offer.name)
        if item:
            if item.quantity > offer.bgof:
                num_free = item.quantity // (offer.bgof + 1)
                self.discount += rounder(num_free * item.price)

    def apply_discount(self):
        """
        Calculates the discount prices for all items in your basket
        and updates the discount attr accordingly
        """
        self.discount = 0
        offers = [self.offers.get(x.name) for x in self._items]
        for offer in offers:
            if offer and offer.perc:
                self._percentage_discount(offer)
            elif offer and offer.bgof:
                self._one_free_discount(offer)
