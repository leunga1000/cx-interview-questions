# Documentation

## Running
### Setup
To install pytest and black modules run the following in the shopping_basket parent directory.

```shell script 
pip install -r requirements.txt
```

### Example implementation
example.py contains an example implementation of multiple offers on a sample basket.

```shell script
python example.py
```

### Testing
Testing uses pytest which is included in the Pipfile. Running 

```shell
pytest
```

in the parent shopping_basket or shopping_basket_tests directory will execute the test pack.
Please see the test_shopping_basket to see various ways of using the shopping_basket component.

## Code components
The main components of the code are:

### Catalogue
A list of possible purchase items and their prices.

### Basket
A construct representing the number of each item in the basket. Items can be added as per the spec.

### Offers
A list of offers. An Offer implements compute_discount which is called for each offer to determine the discount applicable
to the basket.

### BasketPricer
BasketPricer takes a Basket, Catalogue and Offers and calculates the subtotal of the basket, the discount applicable and 
also returns the total (subtotal - discount)

## Notes
### Decimal places and floating point rounding errors.
The test for 2 cans of sardines highlights a rounding error to do with the way floating point numbers are represented in
Python. A fix for this would be to use the Decimal module to represent the numbers in this test.