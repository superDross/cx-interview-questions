from unittest import TestCase

from shopping_basket.basket import BaseBasket, Basket
from shopping_basket.catalogue import Catalogue
from shopping_basket.offers import Offers


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
            ("Baked Beans", 0, 2),
            ("Sardines", 25, 0),
            ("Super Cool Totes Available Item", 100, 0),
        ]
    )


class TestBasket(TestCase):
    def setUp(self):
        catalogue = create_catalogue()
        offers = create_offers()
        self.basket = Basket(catalogue, offers)

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

    def test_add(self):
        self.basket.add("sardines")
        self.assertEqual(self.basket._items[0].name, "Sardines")

    def test_remove(self):
        self.basket.add("sardines")
        self.basket.add("biscuits")
        self.basket.remove("biscuits")

        self.assertEqual(self.basket._items[0].name, "Sardines")
