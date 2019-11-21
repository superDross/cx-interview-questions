"""
Classes to aid in creating a shopping inventory.
"""

import dataclasses
from typing import List
from utilities import get_json


@dataclasses.dataclass(order=True)
class Item:
    name: str
    price: float
    quantity: int = 1

    def __post_init__(self) -> None:
        if not isinstance(self.name, str):
            raise ValueError("item name must be string")
        if self.price <= 0:
            raise ValueError("price must be greater than zero")

    def __iter__(self):
        yield from dataclasses.astuple(self)

    @property
    def total_price(self):
        return self.price * self.quantity


class Catalogue(list):
    """
    Inventory of Item objects available
    """

    def __init__(self, json_file_path: str) -> None:
        super().__init__()
        self._json2items(json_file_path)

    def _json2items(self, json_file_path: str) -> List[Item]:
        json_ = get_json(json_file_path)
        for item in json_:
            self.append(Item(name=item["name"], price=item["price"]))

    def get(self, item_name: str) -> Item:
        for item in self:
            if item_name.lower() == item.name.lower():
                return item

    def fuzzy_get(self, item_sub: str) -> Item:
        """
        Gets all items with names that match a given substring
        """
        return [item for item in self if item_sub.lower() in item.name.lower()]
