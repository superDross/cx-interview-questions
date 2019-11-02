"""
Allows one to create and manipulate inventory discounts.
"""


class Discount:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Discount({self.name})"

    def calulate_discount(self, items):
        raise NotImplementedError


class PercentageOff(Discount):
    def __init__(self, name, percentage):
        super().__init__(name)
        self.percentage = percentage

    def calculate_discount(self, items):
        for item in items:
            if self.name == item.name:
                discount = (item.price * (self.percentage / 100)) * item.quantity
                return discount


class GetOneFree(Discount):
    def __init__(self, name, threshold):
        super().__init__(name)
        # number needed to purchase to receive the offer
        self.threshold = threshold

    def calculate_discount(self, items):
        for item in items:
            if self.name == item.name:
                if item.quantity > self.threshold:
                    num_free = item.quantity // (self.threshold + 1)
                    return num_free * item.price


class CheapestOneFree(Discount):
    def __init__(self, name, threshold):
        super().__init__(name)
        # number needed to purchase to receive the offer
        self.threshold = threshold
        self.discount = 0

    def _individual_item_discount(self, items):
        """
        Apply discount if an individual items quantity surpasses
        the threshold for the offer
        """
        for item in items:
            if item.quantity >= self.threshold:
                self.discount += (item.quantity // self.threshold) * item.price

    def _grouped_discount(self, items):
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

    def calculate_discount(self, items):
        self.discount = 0
        relevant_items = [item for item in items if self.name in item.name]
        if relevant_items:
            self._individual_item_discount(relevant_items)
            self._grouped_discount(relevant_items)
        return self.discount


class Offers:
    """
    Discounts available for our products

    Attributes:
        items (list: tuple): tuple contains product name and offers
    """

    def __init__(self, discounts):
        self.discounts = self._create(discounts)

    def _create(self, discount_list):
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

    def get(self, item_name):
        for discount in self.discounts:
            if item_name.lower() == discount.name.lower():
                return discount
