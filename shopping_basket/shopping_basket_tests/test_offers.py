from unittest import TestCase

from shopping_basket.offers import Discount, Offers


class TestDiscount(TestCase):
    def test_value_error_when_name_not_string(self):
        self.assertRaises(ValueError, Discount, name=1, perc=10)

    def test_value_error_when_assigning_negative_percentage(self):
        self.assertRaises(ValueError, Discount, name="h", perc=-1)

    def test_value_error_when_assigning_negative_buy_get_free(self):
        self.assertRaises(ValueError, Discount, name="h", bgof=-1)

    def test_value_error_multiple_discounts(self):
        self.assertRaises(AttributeError, Discount, name="hh", perc=1, bgof=1)

    def test_attr_error_no_discounts(self):
        self.assertRaises(AttributeError, Discount, name="hh")


class TestOffers(TestCase):
    def test_create_offers(self):
        offers = Offers([("Baked Beans", 0, 2), ("Sardines", 25, 0)])
        self.assertEqual([x.name for x in offers.discounts], ["Baked Beans", "Sardines"])
        self.assertEqual([x.perc for x in offers.discounts], [0, 25])
        self.assertEqual([x.bgof for x in offers.discounts], [2, 0])

    def test_get_offer(self):
        offers = Offers([("Baked Beans", 0, 2), ("Sardines", 25, 0)])
        result = offers.get("baked beans")
        self.assertEqual(result, offers.discounts[0])
