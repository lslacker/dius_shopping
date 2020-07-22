import pytest
import io
from app import Checkout, PricingRule, price
import csv


@pytest.fixture
def checkout():

    rule1 = PricingRule().when('3 atv').then(2 * price['atv'])
    rule2 = PricingRule().when('> 4 ipd').then(499.99).each()
    rule3 = PricingRule().when('(1 mbp) (1 vga)').then(price['mbp'])

    rules = [rule1, rule2, rule3]

    co = Checkout(rules)

    return co

@pytest.fixture
def checkout_norules():
    co = Checkout([])
    return co

@pytest.mark.parametrize("line,expected", 
[('atv, atv, atv, vga', 249.00),
 ('atv, ipd, ipd, atv, ipd, ipd, ipd', 2718.95), 
 ('mbp, vga, ipd', 1949.98),
 ])
def test_checkout_with_rules(checkout, line, expected):
    items = [x.strip() for x in line.split(',')]
    for i in items:
        checkout.scan(i)
    assert checkout.total() == expected


@pytest.mark.parametrize("line,expected", 
[('atv, atv, atv, vga', 358.5),
 ('mbp, vga, ipd', 1979.98),
 ])
def test_checkout_without_rules(checkout_norules, line, expected):
    items = [x.strip() for x in line.split(',')]
    for i in items:
        checkout_norules.scan(i)
    assert checkout_norules.total() == expected