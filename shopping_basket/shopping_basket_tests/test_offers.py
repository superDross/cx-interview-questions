from unittest import TestCase

from catalogue import Item
from offers import CheapestOneFree, GetOneFree, Offers, PercentageOff


class TestOffers(TestCase):
    def test_create_offers(self):
        offers = Offers(
            [("Baked Beans", 0, 2, 0), ("Sardines", 25, 0, 0), ("Shampoo", 0, 0, 3)]
        )
        self.assertTrue(isinstance(offers.discounts[0], GetOneFree))
        self.assertTrue(isinstance(offers.discounts[1], PercentageOff))
        self.assertTrue(isinstance(offers.discounts[2], CheapestOneFree))

    def test_get_offer(self):
        offers = Offers([("Baked Beans", 0, 2, 0), ("Sardines", 25, 0, 0)])
        result = offers.get("baked beans")
        self.assertEqual(result, offers.discounts[0])


class TestDiscounts(TestCase):
    def setUp(self):
        self.items = [
            Item("Baked Beans", 1.80, 4),
            Item("Soup", 0.90, 6),
            Item("Jelly", 0.09, 2),
            Item("TV", 1000, 1),
            Item("Shampoo (Small)", 2.00, 2),
            Item("Shampoo (Medium)", 2.50),
            Item("Shampoo (Large)", 3.50, 3),
        ]

    def test_25_percent_off(self):
        discount = PercentageOff("TV", 25)
        discounted_price = discount.calculate_discount(self.items)
        self.assertEqual(discounted_price, 250)

    def test_33_percent_off(self):
        discount = PercentageOff("TV", 33)
        discounted_price = discount.calculate_discount(self.items)
        self.assertEqual(discounted_price, 330)

    def test_buy_3_get_one_free(self):
        discount = GetOneFree("Baked Beans", 3)
        discounted_price = discount.calculate_discount(self.items)
        self.assertEqual(discounted_price, 1.80)

    def test_buy_1_get_one_free(self):
        discount = GetOneFree("Soup", 1)
        discounted_price = discount.calculate_discount(self.items)
        self.assertEqual(discounted_price, 2.70)

    def test_buy_3_shampoo_get_cheapest_free(self):
        discount = CheapestOneFree("Shampoo", 3)
        discounted_price = discount.calculate_discount(self.items)
        self.assertEqual(discounted_price, 5.50)

    def test_buy_3_mugs_get_cheapest_free(self):
        # 3 large adds 3.50 to discount and the remaining 1 should
        # be calculated as part of the grouped discount along with
        # the other 2 sizes
        mugs = [
            Item("Mug (Small)", 2.00),
            Item("Mug (Medium)", 2.50),
            Item("Mug (Large)", 3.50, 4),
        ]
        discount = CheapestOneFree("Mug", 3)
        discounted_price = discount.calculate_discount(mugs)
        self.assertEqual(discounted_price, 5.50)

    def test_buy_4_pens_get_cheapest_free(self):
        pens = [
            Item("Pen (Black)", 6.00, 5),
            Item("Pen (Red)", 1.00)
        ]
        discount = CheapestOneFree("Pen", 4)
        discounted_price = discount.calculate_discount(pens)
        self.assertEqual(discounted_price, 6.00)


