import decimal


def rounder(number):
    """
    Round up at 0.5

    python3 round() func rounds down at midpoint
    """
    context = decimal.getcontext()
    context.rounding = decimal.ROUND_HALF_UP
    d = round(decimal.Decimal(str(number)), 2)
    return float(d)
