# Shopping Basket

A library to calculate subtotal, discount & total price of a selection of shopping items.

Compatible with Python 3.6 or higher.

## Usage

The catalogue and offers are defined which can then be used to create a Basket object:

```python
from basket import Basket
from catalogue import Catalogue
from offers import Offers

catalogue = Catalogue('./products.json')
offers = Offers('./offers.json')

basket = Basket(catalogue, offers)

basket.add("baked beans", quantity=5)
basket.add("sardines")

print(
    f"Subtotal: {basket.subtotal}, Discount: {basket.discount}, Total: {basket.total}"
)

```

## Testing

```
python3.6 -m unittest discover shopping_basket_tests
```
