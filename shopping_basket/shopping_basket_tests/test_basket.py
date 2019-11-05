from unittest import TestCase, mock

from basket import Basket
from catalogue import Catalogue
from offers import Offers

CATALOGUE = [
    {"name": "Baked Beans", "price": 0.99},
    {"name": "Sardines", "price": 1.89},
    {"name": "Biscuits", "price": 1.20},
    {"name": "Shampoo (Small)", "price": 2.00},
    {"name": "Shampoo (Medium)", "price": 2.50},
    {"name": "Shampoo (Large)", "price": 3.50},
]

OFFERS = [
    {"name": "Baked Beans", "offer": "getOneFree", "value": 2},
    {"name": "Sardines", "offer": "percentOff", "value": 25},
    {"name": "Super Cool Totes Available Item", "offer": "percentOff", "value": 100},
    {"name": "Shampoo", "offer": "cheapestFree", "value": 3},
]


@mock.patch("catalogue.get_json", return_value=CATALOGUE)
def create_catalogue(mocked_func):
    return Catalogue("temp")


@mock.patch("offers.get_json", return_value=OFFERS)
def create_offers(mocked_func):
    return Offers("temp")


class TestBasket(TestCase):
    def setUp(self):
        catalogue = create_catalogue()
        offers = create_offers()
        self.basket = Basket(catalogue, offers)

    def test_add(self):
        self.basket.add("sardines")
        self.assertEqual(self.basket._items[0].name, "Sardines")

    def test_remove(self):
        self.basket.add("sardines")
        self.basket.add("biscuits")
        self.basket.remove("biscuits")
        self.assertEqual(len(self.basket._items), 1)
        self.assertEqual(self.basket._items[0].name, "Sardines")

    def test_remove_quantity(self):
        self.basket.add("sardines", quantity=2)
        self.basket.add("biscuits", quantity=3)
        self.basket.remove("biscuits", 2)
        self.assertEqual(len(self.basket._items), 2)
        self.assertEqual(self.basket._items[0].name, "Sardines")
        self.assertEqual(self.basket._items[1].name, "Biscuits")
        self.assertEqual(self.basket._items[1].quantity, 1)


    def test_subtotal(self):
        self.basket.add("baked beans")
        self.basket.add("biscuits")
        self.assertEqual(self.basket.subtotal, 2.19)

    def test_buy_two_get_one_free_discounts(self):
        self.basket.add("baked beans", quantity=4)
        self.basket.add("biscuits")

        self.assertEqual(self.basket.subtotal, 5.16)
        self.assertEqual(self.basket.discount, 0.99)
        self.assertEqual(self.basket.total, 4.17)

    def test_percentage_off_discount(self):
        self.basket.add("sardines", quantity=3)
        self.basket.add("biscuits")

        self.assertEqual(self.basket.subtotal, 6.87)
        self.assertEqual(self.basket.discount, 1.42)
        self.assertEqual(self.basket.total, 5.45)

    def test_cheapest_free_discount(self):
        self.basket.add("shampoo (large)", quantity=3)
        self.basket.add("shampoo (medium)")
        self.basket.add("shampoo (small)", quantity=2)

        self.assertEqual(self.basket.subtotal, 17.00)
        self.assertEqual(self.basket.discount, 5.50)
        self.assertEqual(self.basket.total, 11.50)

    def test_mixed_discount(self):
        self.basket.add("baked beans", 2)
        self.basket.add("biscuits")
        self.basket.add("sardines", 2)

        self.assertEqual(self.basket.subtotal, 6.96)
        self.assertEqual(self.basket.discount, 0.95)
        self.assertEqual(self.basket.total, 6.01)

    def test_empty_basket(self):
        self.assertEqual(self.basket.subtotal, 0)
        self.assertEqual(self.basket.discount, 0)
        self.assertEqual(self.basket.total, 0)
