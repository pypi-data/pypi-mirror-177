from typing import Union
import pendulum
import datetime
import numpy as np
import re
from finance_utils import exception

# %Y-%m-%d %H:%M:%S
datetime_pattern = re.compile('^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
# %Y-%m-%d
date_pattern = re.compile('^\d{4}-\d{2}-\d{2}$')


# 得到毫秒时间戳
def to_ts(date, timezone: str, default: object = 0) -> int:
    if not date:
        ts = default
    elif type(date) in [int, float, np.float64]:
        ts = int(date)
    elif type(date).__name__.lower() == 'datetime':
        ts = int(date.timestamp() * 1000)
    elif type(date).__name__.lower() == 'date':
        ts = int(pendulum.datetime(
            year=date.year,
            month=date.month,
            day=date.day,
            tz=timezone,
        ).timestamp() * 1000)
    # 如果date是%Y-%m-%d %H:%M:%S格式的字符串
    elif isinstance(date, str) and re.match(datetime_pattern, date):
        ts = int(pendulum.from_format(date, 'YYYY-MM-DD HH:mm:ss', tz=timezone).timestamp() * 1000)
    # 如果date是%Y-%m-%d格式的字符串
    elif isinstance(date, str) and re.match(date_pattern, date):
        ts = int(pendulum.from_format(date, 'YYYY-MM-DD', tz=timezone).timestamp() * 1000)
    else:
        print(type(date))
        raise exception.ParamException('Wrong type of date')
    return ts


# 得到时期对象
def to_datetime(date: Union[int, float, str, datetime.date, datetime.datetime], timezone: str):
    if type(date) in [int, float, np.float64, np.int]:  # 时间戳
        ret_date = pendulum.from_timestamp(date / 1000, tz=timezone)
    elif type(date) == str:
        # '2022-01-01'
        if re.match(date_pattern, date):
            ret_date = pendulum.from_format(date, 'YYYY-MM-DD', tz=timezone)
        # '2022-01-01 01:02:03'
        elif re.match(datetime_pattern, date):
            ret_date = pendulum.from_format(date, 'YYYY-MM-DD HH:mm:ss', tz=timezone)
        else:
            raise exception.ParamException('Wrong type of date')
    elif isinstance(date, datetime.date):
        ret_date = pendulum.datetime(
            year=date.year,
            month=date.month,
            day=date.day,
            hour=date.hour if hasattr(date, 'hour') else 0,
            minute=date.minute if hasattr(date, 'minute') else 0,
            second=date.second if hasattr(date, 'second') else 0,
        )
    else:
        raise exception.ParamException('Wrong type of date')
    return ret_date


# 得到日期序列
def get_range_dates(start, end, timezone):
    start_datetime = to_datetime(date=start, timezone=timezone)
    end_datetime = to_datetime(date=end, timezone=timezone)

    start_date = start_datetime.date()
    end_date = end_datetime.date()
    dates: list = [
        (start_date + datetime.timedelta(days=day)).strftime('%Y-%m-%d')
        for day in range((end_date - start_date).days + 1)
    ]
    return dates


# 格式化输出时间
def to_fmt(date, timezone, fmt='%Y-%m-%d %H:%M:%S') -> str:
    ts = to_ts(date, timezone=timezone)
    return pendulum.from_timestamp(ts / 1000, tz=timezone).strftime(fmt)


# 是否在时间段中
def isPeriodAllowed(date, periods, timezone):
    if not periods:
        return False
    if not date:
        time = pendulum.now(tz=timezone).time()
    elif type(date) == str:
        time = pendulum.from_format(date, 'YYYY-MM-DD HH:mm:ss', tz=timezone).time()
    elif type(date) in [int, float, np.float64]:
        time = pendulum.from_timestamp(date / 1000, tz=timezone).time()
    elif type(date).__name__.lower() == 'datetime':
        time = date.time()
    elif type(date).__name__.lower() == 'time':
        time = date
    else:
        raise exception.ParamException('date')
    time = time.strftime('%H:%M:%S')
    # 满足任意一个时间段，则返回True
    for period in periods:
        if time >= period[0] and time <= period[1]:
            return True
    return False


if __name__ == '__main__':
    pass

    # print(datetime_to_ts(datetime.datetime.now()))
    # print(datetime_to_ts(datetime.datetime.now().date()))
    # print(datetime_to_ts('2022-01-01'))
    # print(datetime_to_ts('2022-01-01 00:00:00'))
    # print(pendulum.from_format('2022-01-01', 'YYYY-MM-DD'))
    # print(pendulum.from_format('2022-01-01 01:02:03', 'YYYY-MM-DD HH:mm:ss'))
    # print(to_datetime(date=datetime.datetime.now().date(), timezone='America/New_York'))
    # print(to_datetime(date=pendulum.now(), timezone='America/New_York'))
    # print(to_datetime(date=pendulum.now().date(), timezone='America/New_York'))
    # print(to_datetime(date=datetime.datetime.now(), timezone='America/New_York'))
    # print(to_datetime(date=datetime.datetime.now().date(), timezone='America/New_York'))
    # print(to_datetime(date=time.time() * 1000, timezone='America/New_York'))
    # print(to_datetime(date='2022-01-01', timezone='America/New_York'))
    # print(to_datetime(date='2022-01-01 01:02:03', timezone='America/New_York'))
    # timezone = 'Asia/Shanghai'
    # dates = get_range_dates(
    #     start='2022-01-01 00:01:02',
    #     end=datetime.datetime.now(),
    #     timezone=timezone,
    # )
    # print(dates)
