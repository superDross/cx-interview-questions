from unittest import TestCase, mock

from catalogue import Item
from offers import CheapestOneFree, GetOneFree, Offers, PercentageOff

JSON_ONE = [
    {"name": "Baked Beans", "offer": "getOneFree", "value": 2},
    {"name": "Sardines", "offer": "percentOff", "value": 25},
    {"name": "Shampoo", "offer": "cheapestFree", "value": 3},
]

JSON_TWO = [
    {"name": "Baked Beans", "offer": "getOneFree", "value": 2},
    {"name": "Sardines", "offer": "percentOff", "value": 25},
]


class TestOffers(TestCase):
    @mock.patch("offers.get_json", return_value=JSON_ONE)
    def test_create_offers(self, mocked_func):
        offers = Offers("temp")
        self.assertTrue(isinstance(offers[0], GetOneFree))
        self.assertTrue(isinstance(offers[1], PercentageOff))
        self.assertTrue(isinstance(offers[2], CheapestOneFree))

    @mock.patch("offers.get_json", return_value=JSON_TWO)
    def test_get_offer(self, mocked_func):
        offers = Offers("temp")
        result = offers.get("baked beans")
        self.assertEqual(result, offers[0])


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
        pens = [Item("Pen (Black)", 6.00, 5), Item("Pen (Red)", 1.00)]
        discount = CheapestOneFree("Pen", 4)
        discounted_price = discount.calculate_discount(pens)
        self.assertEqual(discounted_price, 6.00)
