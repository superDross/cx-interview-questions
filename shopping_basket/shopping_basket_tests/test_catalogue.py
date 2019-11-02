from unittest import TestCase

from shopping_basket.catalogue import Catalogue, Item


class TestItem(TestCase):
    def test_value_error_when_name_not_string(self):
        self.assertRaises(ValueError, Item, name=1, price=1)

    def test_value_error_when_price_is_less_zero(self):
        self.assertRaises(ValueError, Item, name='h', price=-1)


class TestCatalogue(TestCase):
    def test_create_catalogue(self):
        catalogue = Catalogue([("Baked Beans", 0.99), ("Biscuits", 1.20)])
        self.assertEqual([x.name for x in catalogue.items], ["Baked Beans", "Biscuits"])
        self.assertEqual([x.price for x in catalogue.items], [0.99, 1.20])
        self.assertEqual([x.quantity for x in catalogue.items], [1, 1])

    def test_get_item(self):
        catalogue = Catalogue([("Baked Beans", 0.99), ("Biscuits", 1.20)])
        result = catalogue.get("baked beans")
        self.assertEqual(result, catalogue.items[0])
