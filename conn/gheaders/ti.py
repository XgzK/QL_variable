import time


def date_minutes():
    """
    当前日期时间精确到·分钟
    :return: 当前日期时间精确到·分钟
    """
    return time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
