from unittest import TestCase, mock

from catalogue import Catalogue, Item

JSON_ONE = [{"name": "Baked Beans", "price": 0.99}, {"name": "Biscuits", "price": 1.20}]

JSON_TWO = [
    {"name": "Baked Beans (small)", "price": 0.99},
    {"name": "Baked Beans (large)", "price": 1.99},
    {"name": "Biscuits", "price": 1.20},
]


class TestItem(TestCase):
    def test_value_error_when_name_not_string(self):
        self.assertRaises(ValueError, Item, name=1, price=1)

    def test_value_error_when_price_is_less_zero(self):
        self.assertRaises(ValueError, Item, name="h", price=-1)

    def test_total_price(self):
        item = Item(name="Stuff", price=1.20, quantity=2)
        self.assertEqual(item.total_price, 2.40)
        item.quantity = 3
        self.assertAlmostEqual(item.total_price, 3.60)


class TestCatalogue(TestCase):
    @mock.patch("catalogue.get_json", return_value=JSON_ONE)
    def test_create_catalogue(self, mocked_func):
        catalogue = Catalogue("temp")
        self.assertEqual([x.name for x in catalogue], ["Baked Beans", "Biscuits"])
        self.assertEqual([x.price for x in catalogue], [0.99, 1.20])
        self.assertEqual([x.quantity for x in catalogue], [1, 1])

    @mock.patch("catalogue.get_json", return_value=JSON_ONE)
    def test_get_item(self, mocked_func):
        catalogue = Catalogue("temp")
        result = catalogue.get("baked beans")
        self.assertEqual(result, catalogue[0])

    @mock.patch("catalogue.get_json", return_value=JSON_TWO)
    def test_fuzzy_get(self, mock_func):
        catalogue = Catalogue("temp")
        result = catalogue.fuzzy_get("baked beans")
        self.assertEqual(catalogue[:2], result)
