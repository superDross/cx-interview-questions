from unittest import TestCase

from shopping_basket.utils import rounder


class TestRounder(TestCase):
    def test_round_half_up(self):
        self.assertEqual(4.45, rounder(4.4501))
