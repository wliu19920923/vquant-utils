import math
from datetime import datetime

TimeFormatStr = '%Y-%m-%d %H:%M:%S'


def datetime_str_to_microsecond(datetime_str, format=TimeFormatStr):
    return int(datetime.strptime(datetime_str, format).timestamp() * 1000)


def microsecond_to_datetime_str(microseconds):
    return datetime.fromtimestamp(math.floor(microseconds / 1000)).strftime(TimeFormatStr)
