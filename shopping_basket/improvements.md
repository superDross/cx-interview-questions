# Solution Improvements

## Optimisations

- Optimise by using `cProfile` to identify slow parts of the code.
- Use `memory-profiler` to identify high memory functions

- `Catalogue` should store a dict instead and an item can be added like below.
  * you can then simply use the dicts get method instead of the inefficient iterative one implemented

```
item = {'item-name': {'price': 10.00, 'quantity': 2}}
```

## Preparation

- Do more research on inventory management

## Readability/Integrity

- Use item barcode or stock keeping unit for an item as an identifier between Item and Discount

## Implemented

- Basket.remove() does not take quantity into consideration

- Catalogue & Offers should inherit from list

- Use type hinting

- `CheapestOneFree` discount would likely only work with the test case given
  * e.g. if the `Shampoo (Large)` was 4 instead of 3, then that 1 extra remaining large would not be included in the offer calculated in `_grouped_discount()`.

- Item & Discount should be dataclasses as they simply store state and not much logic.
  * Would also take care of a lot boiler plate

- Use JSON as input into `Catalogues` & `Offers`, instead of list of tuples.

- `Offers` uses a long conditional that would only get longer as the number of offers increased
  * solution: each input discount looked like the JSON below, we could use a dict to return the specific offer.

```json
# discount JSON
{'name': 'Apple', 'offer': 'one_free', 'number': 2}

```

```python
# refactored Offers

class Offers:
    def __init__(self, discounts):
        self.discounts = self._create(discounts)
        self.available_offers = {
            'one_free': GetOneFree,
            'cheapest_free': CheapestOneFree,
            'percentage_off': PercentageOff,
        }

    def _create(self, discount_list):
        store = []
        for discount in discount_list:
            name = discount.get('name')
            offer = discount.get('offer')
            number = discount.get('number')

            discount = self.available_offers(discount['offer'])
            store.append(discount(discount['name'], discount['number'])
        return store
```
