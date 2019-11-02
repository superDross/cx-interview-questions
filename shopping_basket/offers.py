"""
Allows one to create and manipulate inventory discounts.
"""
from utils import rounder


class Discount:
    def __init__(self, name):
        self.name = name


class PercentageOff(Discount):
    def __init__(self, name, percentage):
        super().__init__(name)
        self.percentage = percentage

    def calculate_discount(self, item):
        if self.name == item.name:
            discount = (item.price * (self.percentage / 100)) * item.quantity
            return rounder(discount)


class GetOneFree(Discount):
    def __init__(self, name, to_buy):
        super().__init__(name)
        self.to_buy = to_buy

    def calculate_discount(self, item):
        if self.name == item.name:
            if item.quantity > self.to_buy:
                num_free = item.quantity // (self.to_buy + 1)
                return rounder(num_free * item.price)


class Offers:
    """
    Discounts available for our products

    Attributes:
        items (list: tuple): product name, percentage off &/or bgof number
    """

    def __init__(self, discounts):
        self.discounts = self._create(discounts)

    def _create(self, discount_list):
        store = []
        for discount in discount_list:
            name, perc, onefree = discount
            if perc:
                store.append(PercentageOff(name, perc))
            elif onefree:
                store.append(GetOneFree(name, onefree))
        return store

    def get(self, item_name):
        for discount in self.discounts:
            if item_name.lower() == discount.name.lower():
                return discount
