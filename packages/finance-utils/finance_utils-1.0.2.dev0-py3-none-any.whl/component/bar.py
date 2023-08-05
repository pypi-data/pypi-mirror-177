import numpy as np
from finance_utils import exception


# 得到时间间隔，单位毫秒
def get_bar_interval(bar: str, MINUTE_BAR_INTERVAL=60000) -> float:
    '''

    Get ts interval by bar

    :param bar:
    Time interval of historical k line
        bar = '1m'  1 minute
        bar = '5m'  5 minute
        bar = '1h'  1 hour
        bar = '1d'  1 day
        ... ...

    :param MINUTE_BAR_INTERVAL:
    Number interval per minute, in milliseconds
        MINUTE_BAR_INTERVAL = 60000    Ts is in milliseconds
        MINUTE_BAR_INTERVAL = 60       Ts is in seconds

    :return: interval
    '''
    bar_int = int(bar[0:-1].strip())
    suffix = bar[-1].lower()
    if suffix == 'm':
        interval = MINUTE_BAR_INTERVAL * bar_int
    elif suffix == 'h':
        interval = MINUTE_BAR_INTERVAL * 60 * bar_int
    elif suffix == 'd':
        interval = MINUTE_BAR_INTERVAL * 60 * 24 * bar_int
    elif suffix == 'w':
        interval = MINUTE_BAR_INTERVAL * 60 * 24 * 7 * bar_int
    else:
        raise exception.ParamException(
            "The format of bar should be like ['1m ',' 2m ',' 1h ',' 2h ',' 1d ',' 2d '...]"
        )
    return interval


# 估计K线中的时间粒度间隔
def predict_bar_interval(candle: np.array) -> float:
    '''

    Predict ts interval by candle

    :param candle: History Candle
        array[
            [ts,open,high,low,close,volume],
            [ts,open,high,low,close,volume],
            [ts,open,high,low,close,volume],
        ]

    :return:interval
    '''
    return np.min(np.diff(candle[:, 0]))


# 估计K线中的时间粒度
def predict_bar(candle: np.array, MINUTE_BAR_INTERVAL=60000) -> str:
    '''
    :param candle: np.array
    :return: bar
    '''
    bar_interval = np.min(np.diff(candle[:, 0]))
    bar_int = bar_interval / MINUTE_BAR_INTERVAL
    if bar_int <= 59:
        suffix = 'm'
        bar_int = bar_int
    elif bar_int <= 60 * 23:
        suffix = 'h'
        bar_int = bar_int / 60
    else:
        bar_int = bar_int / 60 * 24
        suffix = 'd'

    if not bar_int == int(bar_int):
        raise exception.ParamException('Unable to predict bar')
    return '{bar_int}{suffix}'.format(bar_int=int(bar_int), suffix=suffix)


if __name__ == '__main__':
    pass
