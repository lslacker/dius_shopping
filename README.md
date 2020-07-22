# Dius Shopping

## ASSUMPTION
- products data loaded

## FILES
- app.py is main file, which contains Checkout, and PricingRule classes
- app.py is not runnable, use pytest
- test_app.py and test_rule_parsers are 2 test files

## APPROACH
- A parser, to parse each line into a function, which will accept a shopping cart and matched product list, and return a match object
e.g '3 atv' is parsed into function(shopping_cart, use_indices)
- ParsingRule object is initiated as below
e.g PricingRule().when(condition).then()
- Checkout is the main class, which take a list of rules, then scan each item, and get total

## GET TOTAL
- for each rule, until no more match (condition is matched for unmatched products), get the total
- the rest of prouducts, will be calculated as per normal

# Build a run using virtual environment (Python 3.6+)
  - Clone the repository, change to project directory
  - Create new environment: 
```
  $> python -m venv env
  $> source env/bin/activate
  $> pip install -r requirements.txt
  $> pytest
```
