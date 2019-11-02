from unittest import TestCase

from shopping_basket.offers import Offers, GetOneFree, PercentageOff


class TestOffers(TestCase):
    def test_create_offers(self):
        offers = Offers([("Baked Beans", 0, 2), ("Sardines", 25, 0)])
        self.assertTrue(isinstance(offers.discounts[0], GetOneFree))
        self.assertTrue(isinstance(offers.discounts[1], PercentageOff))

    def test_get_offer(self):
        offers = Offers([("Baked Beans", 0, 2), ("Sardines", 25, 0)])
        result = offers.get("baked beans")
        self.assertEqual(result, offers.discounts[0])
