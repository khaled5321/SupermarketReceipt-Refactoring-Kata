import math
from collections import defaultdict

from model_objects import ProductQuantity, SpecialOfferType, Discount


class ShoppingCart:

    def __init__(self):
        self._items = []
        self._product_quantities = defaultdict(float)

    @property
    def items(self):
        return self._items

    def add_item(self, product):
        self.add_item_quantity(product, 1.0)

    @property
    def product_quantities(self):
        return self._product_quantities

    def add_item_quantity(self, product, quantity):
        self._items.append(ProductQuantity(product, quantity))
        self._product_quantities[product] = self._product_quantities[product] + quantity

    def handle_offers(self, receipt, offers, catalog):
        for product in self._product_quantities.keys():
            quantity = self._product_quantities[product]
            if product in offers.keys():
                offer = offers[product]
                unit_price = catalog.unit_price(product)
                quantity_as_int = int(quantity)
                discount = None

                items_per_offer = 1
                if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
                    items_per_offer = 3

                elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
                    items_per_offer = 2
                    if quantity_as_int >= 2:
                        total = offer.argument * (quantity_as_int / items_per_offer) + quantity_as_int % 2 * unit_price
                        discount_amount = unit_price * quantity - total
                        discount = Discount(product, "2 for " + str(offer.argument), -discount_amount)

                if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
                    items_per_offer = 5

                offer_sets = math.floor(quantity_as_int / items_per_offer)
                if offer.offer_type == SpecialOfferType.THREE_FOR_TWO and quantity_as_int > 2:
                    discount_amount = quantity * unit_price - (
                                (offer_sets * 2 * unit_price) + quantity_as_int % 3 * unit_price)
                    discount = Discount(product, "3 for 2", -discount_amount)

                if offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
                    discount = Discount(product, str(offer.argument) + "% off",
                                        -quantity * unit_price * offer.argument / 100.0)

                if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT and quantity_as_int >= 5:
                    discount_total = unit_price * quantity - (
                                offer.argument * offer_sets + quantity_as_int % 5 * unit_price)
                    discount = Discount(product, str(items_per_offer) + " for " + str(offer.argument), -discount_total)

                if discount:
                    receipt.add_discount(discount)
