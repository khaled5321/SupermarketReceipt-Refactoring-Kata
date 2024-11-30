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

    def test_ten_percent_discount_multiple_items(self):
        teller = Teller(self.catalog)
        teller.add_special_offer(
            SpecialOfferType.TEN_PERCENT_DISCOUNT, self.toothbrush, 10.0
        )

        cart = ShoppingCart()
        cart.add_item(self.apples)
        cart.add_item(self.toothbrush)

        receipt = teller.checks_out_articles_from(cart)

        self.assertAlmostEqual(
            (1.99 + (0.99 * 0.9)), receipt.total_price()
        )
        self.assertEqual(len(receipt.discounts), 1)
        self.assertEqual(2, len(receipt.items))

        receipt_item = receipt.items[0]
        self.assertEqual(receipt_item.product, self.apples)
        self.assertEqual(receipt_item.total_price, 1.99)
        self.assertEqual(receipt_item.quantity, 1)

        receipt_item = receipt.items[1]
        self.assertEqual(receipt_item.product, self.toothbrush)
        self.assertEqual(receipt_item.total_price, 0.99)
        self.assertEqual(receipt_item.quantity, 1)

    def test_no_special_offer(self):
        teller = Teller(self.catalog)

        cart = ShoppingCart()
        cart.add_item(self.apples)
        cart.add_item(self.toothbrush)

        receipt = teller.checks_out_articles_from(cart)

        self.assertAlmostEqual(2.98, receipt.total_price())
        self.assertEqual(receipt.discounts, [])
        self.assertEqual(2, len(receipt.items))

        receipt_item = receipt.items[0]
        self.assertEqual(receipt_item.product, self.apples)
        self.assertEqual(receipt_item.total_price, 1.99)
        self.assertEqual(receipt_item.quantity, 1)

        receipt_item = receipt.items[1]
        self.assertEqual(receipt_item.product, self.toothbrush)
        self.assertEqual(receipt_item.total_price, 0.99)
        self.assertEqual(receipt_item.quantity, 1)

    def test_multiple_discounts(self):
        teller = Teller(self.catalog)
        teller.add_special_offer(
            SpecialOfferType.TEN_PERCENT_DISCOUNT, self.toothbrush, 10.0
        )
        teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, self.apples, 3)

        cart = ShoppingCart()
        cart.add_item_quantity(self.apples, 3)
        cart.add_item(self.toothbrush)

        receipt = teller.checks_out_articles_from(cart)

        toothbrush_price_after_discount = 0.99 * 0.9
        apples_price_after_discount = 1.99 * 2

        self.assertAlmostEqual(
            apples_price_after_discount + toothbrush_price_after_discount,
            receipt.total_price(),
        )
        self.assertEqual(len(receipt.discounts), 2)
        self.assertEqual(2, len(receipt.items))

        receipt_item = receipt.items[0]
        self.assertEqual(receipt_item.product, self.apples)
        self.assertEqual(receipt_item.price, 1.99)
        self.assertEqual(receipt_item.total_price, 1.99 * 3)
        self.assertEqual(receipt_item.quantity, 3)

        receipt_item = receipt.items[1]
        self.assertEqual(receipt_item.product, self.toothbrush)
        self.assertEqual(receipt_item.price, 0.99)
        self.assertEqual(receipt_item.total_price, 0.99)
        self.assertEqual(receipt_item.quantity, 1)

    def test_five_for_amount_discount(self):
        teller = Teller(self.catalog)
        teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, self.apples, 25)

        cart = ShoppingCart()
        cart.add_item_quantity(self.apples, 5)

        receipt = teller.checks_out_articles_from(cart)

        self.assertAlmostEqual(25, receipt.total_price())
        self.assertEqual(len(receipt.discounts), 1)

        # test adding more items
        cart.add_item_quantity(self.apples, 5)

        receipt = teller.checks_out_articles_from(cart)

        self.assertAlmostEqual(50, receipt.total_price())
        self.assertEqual(len(receipt.discounts), 1)

    def test_two_for_amount_discount(self):
        teller = Teller(self.catalog)
        teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, self.apples, 5)

        cart = ShoppingCart()
        cart.add_item_quantity(self.apples, 4)

        receipt = teller.checks_out_articles_from(cart)

        self.assertAlmostEqual(10, receipt.total_price())
        self.assertEqual(len(receipt.discounts), 1)
