"""
Classes to aid in creating a shopping inventory.
"""

from typing import List, Tuple


class Item:
    """
    Individual shopping item available in the inventory
    """

    def __init__(self, name: str, price: float, quantity: int = 1) -> None:
        self.name = name
        self.price = price
        self.quantity = quantity

        self._check_valid()

    def __str__(self) -> None:
        return self.name

    def __repr__(self) -> None:
        return f"Item({self.name}, {self.price}, {self.quantity})"

    def _check_valid(self) -> None:
        if not isinstance(self.name, str):
            raise ValueError("item name must be string")
        if self.price <= 0:
            raise ValueError("price must be greater than zero")


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
