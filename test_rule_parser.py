import pytest
import rule_parser
from pyparsing import ParseException

def test_parse_string_to_get_predicate():
    func = rule_parser.get_command('> 3 atv')
    assert callable(func)
    cmd = rule_parser.get_command('> (1 mbp) (1 vga)')
    assert callable(func)

def test_parse_string_throw_error():
    with pytest.raises(ParseException):
        func = rule_parser.get_command('I am not matched your syntax')
    