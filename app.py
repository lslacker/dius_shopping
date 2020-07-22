import sys
from typing import List
import logging
from pyparsing import Literal, oneOf, Regex, OneOrMore, Optional
import rule_parser

logger = logging.getLogger(__name__)


class PricingRule:

    base_on_qty = False

    def when(self, cond):
        self.pred = rule_parser.get_command(cond)
        return self

    def then(self, amount):
        self.amount = amount

    def then(self, amount):
        self.amount = amount
        return self

    def each(self):
        self.base_on_qty = True
        return self

    def test(self, carts, used_indices):
        '''test a condition is matched
        returns a tuple of (whether_is_matched, matched_skus)
        '''
        is_matched, clone = self.pred(carts, used_indices)
        self.qty = len(clone)
        return is_matched, clone

    def total(self):
        return self.amount * self.qty if self.base_on_qty else self.amount


price = {
    'atv': 109.5,
    'ipd': 549.99,
    'mbp': 1399.99,
    'vga': 30
}

class Checkout:
    '''
    Dius shopping cart to calculate
    price with certain promotions
    '''
    def __init__(self, pricing_rules):
        self.pricing_rules = pricing_rules
        self.items = []

    def scan(self, item):
        self.items += [item]
    
    def total(self):
        indices = []
        total = 0.0
        for rule in self.pricing_rules:
            while True:
                is_matched, used = rule.test(self.items, indices)
                if is_matched:
                    subtotal = rule.total()
                    total += subtotal
                    indices += used
                else:
                    break
        # find the unmatched products and get their total price
        bal = sum([price[x] for idx, x in enumerate(self.items) if idx not in indices])

        return total + bal
