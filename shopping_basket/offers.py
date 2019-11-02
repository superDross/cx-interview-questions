"""
Allows one to create and manipulate inventory discounts.
"""


class Discount:
    """
    Particular deal for a shopping item in our inventory

    Attributes:
        name (str): product name
        perc (int): percentage off a given product
        bgof (int): number of products to buy to get one free
    """

    def __init__(self, name, perc=0, bgof=0):
        self.name = name
        self.perc = perc
        self.bgof = bgof

        self._check_offers_valid()

    def _check_offers_valid(self):
        evaluate = [self.perc, self.bgof]
        if not isinstance(self.name, str):
            raise ValueError(f"item name must be string")
        elif any(x < 0 for x in evaluate):
            raise ValueError(f"Cannot assign negative integers")
        elif all(x == 0 for x in evaluate):
            raise AttributeError(f"No discount applied to product")
        elif all(x > 0 for x in evaluate):
            raise AttributeError("Cannot have 2 types of offers")


class Offers:
    """
    Discounts available for our products

    Attributes:
        items (list: tuple): product name, percentage off &/or bgof number
    """

    def __init__(self, discounts):
        self.discounts = self._create(discounts)

    def _create(self, discount_list):
        return [Discount(name=x[0], perc=x[1], bgof=x[2]) for x in discount_list]

    def get(self, item_name):
        for discount in self.discounts:
            if item_name.lower() == discount.name.lower():
                return discount
