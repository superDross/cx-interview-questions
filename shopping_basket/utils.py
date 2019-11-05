import decimal
from typing import Union


def rounder(number: Union[int, float]) -> float:
    """
    Round up at 0.5

    python3 round() func rounds down at midpoint
    """
    context = decimal.getcontext()
    context.rounding = decimal.ROUND_HALF_UP
    rounded_decimal = round(decimal.Decimal(str(number)), 2)
    return float(rounded_decimal)
