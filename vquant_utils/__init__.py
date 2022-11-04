from decimal import Decimal


def retry(count):
    """
    重试装饰器
    """

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