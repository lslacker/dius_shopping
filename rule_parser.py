import logging
from pyparsing import Literal, oneOf, Regex, OneOrMore, Optional

logger = logging.getLogger(__name__)

number = Regex(r'\d+').setParseAction(lambda t: int(t[0]))
comma = Literal(',')
equal = Literal('=')
space = Literal(' ')
open_bracket = Literal('(').suppress()
close_bracket = Literal(')').suppress()
greaterThan = Literal('>')
plus = Literal('+')
sku = oneOf("ipd mbp atv vga")
operator = greaterThan | equal

# 3 atv
# > (4 ipd)
condition = Optional(open_bracket) + number + sku + Optional(close_bracket)

# = (1 mbp) (1 vga)
ifDefn = Optional(operator, default=equal)('op') + OneOrMore(condition)('params')


def parseToGetPredicate(tokens):
    """
    tokens contains 'op' and 'params'
    'op': could be > or =
    'params': a list of qty and sku
    """

    l = tokens.asDict()
    op = l['op']
    params = l['params']
    
    def func(carts, used):
        conds = []
        indices = []
        clone = []
        for idx in range(0, len(params), 2):
            qty = params[idx]
            sku = params[idx+1]

            matched = [idx for idx, item in enumerate(carts) if item == sku and idx not in used]
            
            if op == '>':
                clone += matched[:]
                conds += [len(matched) > qty]
            else:
                
                clone += matched[:qty]
                conds += [len(matched) >= qty]
        is_matched = all(conds)
        return is_matched, clone if is_matched else used

    return func

ifDefn.setParseAction(parseToGetPredicate)

def get_command(line):
    return ifDefn.parseString(line)[0]
    
