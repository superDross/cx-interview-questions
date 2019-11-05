from unittest import TestCase

from utils import get_json, rounder


class TestUtils(TestCase):
    def test_round_half_up(self):
        self.assertEqual(4.45, rounder(4.4501))

    def test_get_json(self):
        expected = [
            {"name": "Baked Beans", "price": 0.99},
            {"name": "Biscuits", "price": 1.2},
            {"name": "Sardines", "price": 1.89},
            {"name": "Shampoo (Small)", "price": 2.0},
            {"name": "Shampoo (Medium)", "price": 2.5},
            {"name": "Shampoo (Large)", "price": 3.5},
        ]
        json_ = get_json("products.json")
        self.assertEqual(json_, expected)
