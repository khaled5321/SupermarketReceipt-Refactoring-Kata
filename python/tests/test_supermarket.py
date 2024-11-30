import unittest

from model_objects import Product, SpecialOfferType, ProductUnit
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


class TestSuperMarket(unittest.TestCase):
    def setUp(self):
        # test products
        self.toothbrush = Product("toothbrush", ProductUnit.EACH)
        self.apples = Product("apples", ProductUnit.KILO)

        self.catalog = FakeCatalog()
        self.catalog.add_product(self.toothbrush, 0.99)
        self.catalog.add_product(self.apples, 1.99)

    def test_ten_percent_discount(self):
        teller = Teller(self.catalog)
        teller.add_special_offer(
            SpecialOfferType.TEN_PERCENT_DISCOUNT, self.toothbrush, 10.0
        )

        cart = ShoppingCart()
        cart.add_item_quantity(self.apples, 2.5)

        receipt = teller.checks_out_articles_from(cart)

        self.assertAlmostEqual(4.975, receipt.total_price())
        self.assertEqual(receipt.discounts, [])
        self.assertEqual(1, len(receipt.items))

        receipt_item = receipt.items[0]
        self.assertEqual(receipt_item.product, self.apples)
        self.assertEqual(receipt_item.price, 1.99)
        self.assertEqual(receipt_item.total_price, 2.5 * 1.99)
        self.assertEqual(receipt_item.quantity, 2.5)
