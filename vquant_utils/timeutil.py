import math
from datetime import datetime

TimeFormatStr = '%Y-%m-%d %H:%M:%S'


def microsecond_to_datetime_str(microseconds):
    return datetime.fromtimestamp(math.floor(microseconds / 1000)).strftime(TimeFormatStr)
