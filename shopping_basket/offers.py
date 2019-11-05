"""
Allows one to json2discounts and manipulate inventory discounts.
"""

import dataclasses
from typing import List, Union

from catalogue import Item
from utils import get_json


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
                discount = item.total_price * (self.percentage / 100)
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
    discount: float = 0.00

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


class Offers(list):
    """
    Discounts available for our products
    """

    def __init__(self, json_file_path: str) -> None:
        super().__init__()
        self.available_offers = {
            "getOneFree": GetOneFree,
            "cheapestFree": CheapestOneFree,
            "percentOff": PercentageOff,
        }

        self._json2discounts(json_file_path)

    def _json2discounts(self, json_file_path: str) -> List[Discount]:
        json_ = get_json(json_file_path)
        for discount in json_:
            discount_class = self.available_offers.get(discount["offer"])
            self.append(discount_class(discount["name"], discount["value"]))

    def get(self, item_name: str) -> Discount:
        for discount in self:
            if item_name.lower() == discount.name.lower():
                return discount
