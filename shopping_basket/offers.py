"""
Allows one to create and manipulate inventory discounts.
"""


class Discount:
    def __init__(self, name):
        self.name = name

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
    def __init__(self, name, to_buy):
        super().__init__(name)
        self.to_buy = to_buy

    def calculate_discount(self, items):
        for item in items:
            if self.name == item.name:
                if item.quantity > self.to_buy:
                    num_free = item.quantity // (self.to_buy + 1)
                    return num_free * item.price


class CheapestOneFree(Discount):
    def __init__(self, name, to_buy):
        super().__init__(name)
        self.to_buy = to_buy
        self.discount = 0

    def _individual_item_discount(self, items):
        """
        Apply discount if an individual items quantity surpasses
        the threshold for the offer
        """
        for item in items:
            if item.quantity >= self.to_buy:
                self.discount += (item.quantity // self.to_buy) * item.price

    def _grouped_discount(self, items):
        """
        Apply discount to grouped items that are collectively above
        the offer threshold but individually beneath it
        """
        relevant_items = [item for item in items if item.quantity < self.to_buy]
        if relevant_items:
            total_quantity = sum(item.quantity for item in relevant_items)
            lowest_price = min([item.price for item in relevant_items])
            if total_quantity >= self.to_buy:
                self.discount += (total_quantity // self.to_buy) * lowest_price

    def calculate_discount(self, items):
        self.discount = 0
        relevant_items = [x for x in items if self.name in x.name]
        if relevant_items:
            self._individual_item_discount(relevant_items)
            self._grouped_discount(relevant_items)
        return self.discount


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
