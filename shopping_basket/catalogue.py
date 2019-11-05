"""
Classes to aid in creating a shopping inventory.
"""

import dataclasses

from typing import List, Tuple


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


class Catalogue:
    """
    Inventory of Item objects available
    """

    def __init__(self, items: List[Tuple[str, float]]) -> None:
        self.items = self._create(items)

    def _create(self, item_list: List[Tuple[str, float]]) -> List[Item]:
        return [Item(name=item[0], price=item[1]) for item in item_list]

    def get(self, item_name: str) -> Item:
        for item in self.items:
            if item_name.lower() == item.name.lower():
                return item

    def fuzzy_get(self, item_sub: str) -> Item:
        """
        Gets all items with names that match a given substring
        """
        return [item for item in self.items if item_sub.lower() in item.name.lower()]
