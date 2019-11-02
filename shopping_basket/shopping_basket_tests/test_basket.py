from unittest import TestCase

from basket import Basket
from catalogue import Catalogue
from offers import Offers


def create_catalogue():
    return Catalogue(
        [
            ("Baked Beans", 0.99),
            ("Biscuits", 1.20),
            ("Sardines", 1.89),
            ("Shampoo (Small)", 2.00),
            ("Shampoo (Medium)", 2.50),
            ("Shampoo (Large)", 3.50),
        ]
    )


def create_offers():
    return Offers(
        [
            ("Baked Beans", 0, 2, 0),
            ("Sardines", 25, 0, 0),
            ("Super Cool Totes Available Item", 100, 0, 0),
            ("Shampoo", 0, 0, 3),
        ]
    )


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
        self.assertEqual(self.basket._items[0].name, "Sardines")

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
