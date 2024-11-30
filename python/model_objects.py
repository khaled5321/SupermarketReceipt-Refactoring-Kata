from enum import Enum


class Product:
    def __init__(self, name, unit):
        self.name = name
        self.unit = unit


class ProductQuantity:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity


class ProductUnit(Enum):
    EACH = 1
    KILO = 2


class SpecialOfferType(Enum):
    THREE_FOR_TWO = 1
    TEN_PERCENT_DISCOUNT = 2
    TWO_FOR_AMOUNT = 3
    FIVE_FOR_AMOUNT = 4

class Offer:
    ITEMS_PER_OFFER = {
        SpecialOfferType.TWO_FOR_AMOUNT: 2,
        SpecialOfferType.THREE_FOR_TWO: 3,
        SpecialOfferType.FIVE_FOR_AMOUNT: 5
    }

    def __init__(self, offer_type, product, argument):
        self.offer_type = offer_type
        self.product = product
        self.argument = argument

    def get_items_per_offer(self):
        return self.ITEMS_PER_OFFER.get(self.offer_type, 1)


class Discount:
    def __init__(self, product, description, discount_amount):
        self.product = product
        self.description = description
        self.discount_amount = discount_amount


class ReceiptItem:
    def __init__(self, product, quantity, price, total_price):
        self.product = product
        self.quantity = quantity
        self.price = price
        self.total_price = total_price
