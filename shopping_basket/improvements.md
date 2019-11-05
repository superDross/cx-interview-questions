# Solution Improvements

## Optimisations

- Optimise by using `cProfile` to identify slow parts of the code.
- Use `memory-profiler` to identify high memory functions

## Preparation

- Do more research on inventory management

## Readability/Integrity

- Use type hinting

- Catalogue & Offers should inherit from list

- Use item barcode or stock keeping unit for an item as an identifier between Item and Discount

## Other

- Use JSON as input into `Catalogues` & `Offers`, instead of list of tuples.

- `Offers` uses a long conditional that would only get longer as the number of offers increased
  - solution: each input discount looked like the JSON below, we could use a dict to return the specific offer.

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

## Implemented

- `CheapestOneFree` discount would likely only work with the test case given
  - e.g. if the `Shampoo (Large)` was 4 instead of 3, then that 1 extra remaining large would not be included in the offer calculated in `_grouped_discount()`.
  - solution (WON'T WORK): in `_individual_item_discount()` return the quantity used to add to the discount. Back in `calculate_discount()` deduct the returned quantity from the specific item (`item.quantity`) in `items` list before parsing `items` to `_grouped_discount()`
