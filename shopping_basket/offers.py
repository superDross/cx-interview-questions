"""
Allows one to create and manipulate inventory discounts.
"""

import dataclasses
from typing import List, Tuple, Union

from catalogue import Item


@dataclasses.dataclass
class Discount:
    """
    Individual discount available for a given product name
    """

    name: str

    def calulate_discount(self, items: List[Item]) -> None:
        """
        Returns the amount of money to be discounted from the
        items original price
        """
        raise NotImplementedError


@dataclasses.dataclass
class PercentageOff(Discount):
    name: str
    percentage: Union[int, float]

    def calculate_discount(self, items: List[Item]) -> int:
        for item in items:
            if self.name == item.name:
                discount = (item.price * (self.percentage / 100)) * item.quantity
                return discount


@dataclasses.dataclass
class GetOneFree(Discount):
    name: str
    threshold: int

    def calculate_discount(self, items: List[Item]) -> int:
        for item in items:
            if self.name == item.name:
                if item.quantity > self.threshold:
                    num_free = item.quantity // (self.threshold + 1)
                    return num_free * item.price


@dataclasses.dataclass
class CheapestOneFree(Discount):
    name: str
    threshold: int

    def _individual_item_discount(self, items: List[Item]) -> None:
        """
        Apply discount if an individual items quantity surpasses
        the threshold for the offer
        """
        for item in items:
            if item.quantity >= self.threshold:
                self.discount += (item.quantity // self.threshold) * item.price
                item.quantity = item.quantity % self.threshold

    def _grouped_discount(self, items: List[Item]) -> None:
        """
        Apply discount to grouped items that are collectively above
        the offer threshold but individually beneath it
        """
        relevant_items = [item for item in items if item.quantity < self.threshold]
        if relevant_items:
            total_quantity = sum(item.quantity for item in relevant_items)
            lowest_price = min([item.price for item in relevant_items])
            if total_quantity >= self.threshold:
                self.discount += (total_quantity // self.threshold) * lowest_price

    def calculate_discount(self, items: List[Item]) -> int:
        self.discount = 0
        relevant_items = [item for item in items if self.name in item.name]
        if relevant_items:
            self._individual_item_discount(relevant_items)
            self._grouped_discount(relevant_items)
        return self.discount


class Offers:
    """
    Discounts available for our products
    """

    def __init__(self, discounts: List[Tuple[str, float, float, float]]) -> None:
        self.discounts = self._create(discounts)

    def _create(
        self, discount_list: List[Tuple[str, float, float, float]]
    ) -> List[Discount]:
        store = []
        for discount in discount_list:
            name, perc, onefree, cheapestfree = discount
            if perc:
                store.append(PercentageOff(name, perc))
            elif onefree:
                store.append(GetOneFree(name, onefree))
            elif cheapestfree:
                store.append(CheapestOneFree(name, cheapestfree))
        return store

    def get(self, item_name: str) -> Discount:
        for discount in self.discounts:
            if item_name.lower() == discount.name.lower():
                return discount
