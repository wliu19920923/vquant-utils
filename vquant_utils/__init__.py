from decimal import Decimal


class Order:
    Buy, Sell = ('buy', 'sell')
    Sides = (Buy, Sell)

    Limit, Market = ('limit', 'market')
    Types = (Limit, Market)

    GTC, IOC, FOK = ('GTC', 'IOC', 'FOK')
    Lines = (GTC, IOC, FOK)

    Created, Submitted, PartialFilled, Filled, Cancelling, PartialCanceled, Canceled, Rejected, Expired = (
        'created', 'submitted', 'partial_filled', 'filled', 'cancelling', 'partial_canceled',
        'canceled', 'rejected', 'expired'
    )
    Status = (Created, Submitted, PartialFilled, Filled, Cancelling, PartialCanceled, Canceled, Rejected, Expired)


class Position:
    BOTH, LONG, SHORT = ('BOTH', 'LONG', 'SHORT')
    Directions = (BOTH, LONG, SHORT)

    ISOLATED, CROSSED = ('ISOLATED', 'CROSSED')
    MarginMolds = (ISOLATED, CROSSED)


class CandleLine:
    M1, M5, M15, M30, H, D, W, M = ('1min', '5min', '15min', '30min', 'H', 'D', 'W', 'M')
    Intervals = (M1, M5, M15, M30, H, D, W, M)


def retry(count):
    def wrapper(func):
        def decorate(*args, **kwargs):
            for i in range(count):
                try:
                    return func(*args, **kwargs)
                except Exception as exp:
                    raise exp

        return decorate

    return wrapper


def decimal_precision(decimal):
    return abs(Decimal(str(decimal)).as_tuple().exponent)
