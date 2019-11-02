# Shopping Basket

A library to calculate subtotal, discount & total price of a selection of shopping items.

Compatible with Python 3.6 or higher.

## Usage

The catalogue and offers are defined which can then be used to create a basket class:

```python
from basket import Basket
from catalogue import Catalogue
from offers import Offers

catalogue = Catalogue(
    [
        ("Baked Beans (small)", 0.99),
        ("Baked Beans (large)", 1.99),
        ("Biscuits", 1.20),
        ("Sardines", 1.89),
    ]
)

offers = Offers(
    [
        ("Baked Beans", 0, 2),
        ("Sardines", 25, 0),
    ]
)

basket = Basket(catalogue, offers)

basket.add("baked beans (small)", quantity=5)
basket.add("sardines")

print(
    f"Subtotal: {basket.subtotal}, Discount: {basket.discount}, Total: {basket.total}"
)

```

## Testing

```
python3.6 -m unittest discover shopping_basket_tests
```
