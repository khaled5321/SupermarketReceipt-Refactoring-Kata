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
        for product, quantity in self._product_quantities.items():
            if product not in offers:
                continue

            offer = offers[product]
            unit_price = catalog.unit_price(product)
            quantity_as_int = int(quantity)
            discount = None

            items_per_offer = offer.get_items_per_offer()
            offer_sets = math.floor(quantity_as_int / items_per_offer)
            total_amount = unit_price * quantity

            if offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT and quantity_as_int >= 2:
                amount_after_discount = (offer.argument * offer_sets) + ((quantity_as_int % 2) * unit_price)
                discount_amount = total_amount - amount_after_discount
                discount = Discount(product, f"2 for {offer.argument}", -discount_amount)

            if offer.offer_type == SpecialOfferType.THREE_FOR_TWO and quantity_as_int > 2:
                amount_after_discount = (offer_sets * 2 * unit_price) + ((quantity_as_int % 3) * unit_price)
                discount_amount = total_amount - amount_after_discount
                discount = Discount(product, "3 for 2", -discount_amount)

            if offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
                discount_amount = total_amount * offer.argument / 100.0
                discount = Discount(product, f"{offer.argument}% off", -discount_amount)

            if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT and quantity_as_int >= 5:
                amount_after_discount = (offer.argument * offer_sets) + ((quantity_as_int % 5) * unit_price)
                discount_amount = total_amount - amount_after_discount
                discount = Discount(product, f"{items_per_offer} for {offer.argument}", -discount_amount)

            if discount:
                receipt.add_discount(discount)
