import pandas as pd
import finance_utils
from finance_utils import exception
import os
from typing import Union, Literal
import datetime
import numpy as np
from multiprocessing import Manager, Pool
import re


# 配合pool模块，采用多进程的方式读取candle
def _pool_load_candle(q_param, q_result):
    ''' 如果在读取的时候或在数据验证的时候，出现了错误，会在进程内报告异常 '''
    while True:
        try:
            param = q_param.get(block=False, timeout=0)
        except:
            return None
        instType = param['instType']
        instId = param['instId']
        start_date = param['start_date']
        end_date = param['end_date']
        timezone = param['timezone']
        bar = param['bar']
        base_dir = param['base_dir']
        valid_diff = param.get('valid_diff', True)
        valid_start = param.get('valid_start', True)
        valid_end = param.get('valid_end', True)

        candle = load_candle_by_date(
            instId=instId,
            start_date=start_date,
            end_date=end_date,
            timezone=timezone,
            bar=bar,
            instType=instType,
            base_dir=base_dir,
            valid_diff=valid_diff,
            valid_end=valid_end,
            valid_start=valid_start,
        )

        q_result.put(
            {
                'instId': instId,
                'candle': candle,
            }
        )


# 将instType、timezone与bar转换成文件夹的名字
def _param_to_dirname(
        instType: str,
        timezone: str,
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m'
):
    timezone = re.sub('/', '', timezone)
    return '-'.join([instType, timezone, bar])


# 得到某一个天candle的路径
def get_candle_day_path(
        instType: str,
        instId: str,
        date: datetime.date,
        base_dir='',
        timezone='Asia/Shanghai',
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
):
    date_str = finance_utils.date.to_fmt(date=date, timezone=timezone, fmt='%Y-%m-%d')
    filepath = os.path.join(
        base_dir,
        _param_to_dirname(instType=instType, timezone=timezone, bar=bar),
        date_str[0:7],
        date_str,
        '%s.csv' % instId
    )
    return filepath


# 获取数字货币的地址
def get_candle_file_path(
        instType: str,
        instId: str,
        base_dir='',
        timezone='Asia/Shanghai',
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
):
    '''
    instId产品名字是以.csv进行结尾
    '''
    filepath = os.path.join(
        base_dir,
        _param_to_dirname(instType=instType, timezone=timezone, bar=bar),
        '%s.csv' % instId
    )
    return filepath


# 检查instId是否在start_date到end_date都有本地数据
def check_candle_files(
        instType: str,
        instId: str,
        start_date: datetime.date,
        end_date: datetime.date,
        base_dir='',
        timezone='Asia/Shanghai',
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',

):
    '''
    如果csv文件数据齐全，返回True，否则返回False
    '''
    dates = finance_utils.date.get_range_dates(start=start_date, end=end_date, timezone=timezone)

    for date in sorted(dates, reverse=True):
        path = get_candle_day_path(instType=instType, instId=instId, date=date, timezone=timezone, base_dir=base_dir,
                                   bar=bar)
        if not os.path.isfile(path):
            return False
    return True


# 读取candle
def load_candle_by_date(
        instType: str,
        instId: str,
        start_date: Union[datetime.date, str],
        end_date: Union[datetime.date, str],
        base_dir='',
        timezone='Asia/Shanghai',
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        valid_diff=True,
        valid_start=True,
        valid_end=True,
):
    '''
    按照日期范围，读取Candle
    todo 注意candle的ts的类型是浮点数
    '''
    # 检查是否有数据
    if not check_candle_files(instType=instType, instId=instId, start_date=start_date, end_date=end_date,
                              timezone=timezone, bar=bar, base_dir=base_dir):
        raise exception.CandleFileError('数据不足')
    # 获取数据的序列
    date_range = finance_utils.date.get_range_dates(
        start=start_date,
        end=end_date,
        timezone=timezone,
    )
    # 获取数据的路径列表
    paths = [
        get_candle_day_path(
            instType=instType,
            instId=instId,
            date=date,
            timezone=timezone,
            bar=bar,
            base_dir=base_dir,

        )
        for date in date_range
    ]

    dfs = []
    for path in paths:
        df = pd.read_csv(path)
        dfs.append(df)
    df = pd.concat(dfs)
    df = df.reset_index(drop=True)
    ts_column_name = df.columns[0]
    df[ts_column_name] = df[ts_column_name].astype(int)
    df = df.drop_duplicates(subset=ts_column_name)
    df = df.sort_values(by=ts_column_name)
    candle = df.to_numpy()
    bar_interval = finance_utils.bar.get_bar_interval(bar=bar)
    if valid_diff and not (np.diff(candle[:, 0]) == bar_interval).all():
        msg = '{instId}的candle的时间间隔错误'.format(instId=instId)
        return exception.CandleDiffError(msg)

    if valid_start and candle[0, 0] != finance_utils.date.to_ts(date=start_date, timezone=timezone):
        msg = '{instId}的candle的时间起始错误'.format(instId=instId)
        return exception.CandleStartError(msg)

    if valid_end and candle[-1, 0] != finance_utils.date.to_ts(date=end_date,
                                                               timezone=timezone) + 1000 * 60 * 60 * 24 - bar_interval:
        msg = '{instId}的candle的时间终止错误'.format(instId=instId)
        return exception.CandleEndError(msg)
    return candle


# 按照日期读取candle_map
def load_candle_map_by_date(
        instType: str,
        start_date: Union[datetime.date, str],
        end_date: Union[datetime.date, str],
        instIds: list = [],
        base_dir='',
        timezone='Asia/Shanghai',
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        contains='-USDT',
        p_num=4,
        valid_diff=True,
        valid_start=True,
        valid_end=True,
):
    # 如果没有产品的名字，获取产品类型数据中，有start_date到end_date中有完整数据的instId
    if not instIds:
        dates = finance_utils.date.get_range_dates(start=start_date, end=end_date, timezone=timezone)
        instIds = set()
        for date in dates:
            date_dirpath = os.path.dirname(
                get_candle_day_path(base_dir=base_dir, instType=instType, timezone=timezone, date=date, bar=bar,
                                    instId='')
            )
            this_instIds = []
            for filename in os.listdir(date_dirpath):
                instId = filename.rsplit('.', maxsplit=1)[0]
                if contains and not contains in instId:
                    continue
                else:
                    this_instIds.append(instId)
            if not instIds:
                instIds = set(this_instIds)
            else:
                instIds = instIds & set(this_instIds)
    candle_map = {}
    if p_num > 1:
        q_param = Manager().Queue()
        q_result = Manager().Queue()
        for instId in instIds:
            q_param.put(
                dict(
                    instType=instType,
                    instId=instId,
                    start_date=start_date,
                    end_date=end_date,
                    timezone=timezone,
                    bar=bar,
                    base_dir=base_dir,
                    valid_diff=valid_diff,
                    valid_start=valid_start,
                    valid_end=valid_end,
                )
            )
        pool = Pool(p_num)
        for i in range(p_num):
            pool.apply_async(
                func=_pool_load_candle,
                kwds={
                    'q_param': q_param,
                    'q_result': q_result
                }
            )
        pool.close()
        pool.join()
        for i in range(q_result.qsize()):
            result = q_result.get(block=False, timeout=0)
            instId = result['instId']
            candle = result['candle']
            candle_map[instId] = candle

    else:
        for instId in instIds:
            candle_map[instId] = load_candle_by_date(
                instType=instType,
                instId=instId,
                start_date=start_date,
                end_date=end_date,
                timezone=timezone,
                bar=bar,
                base_dir=base_dir,
                valid_diff=valid_diff,
                valid_start=valid_start,
                valid_end=valid_end,
            )
    bar_interval = finance_utils.bar.get_bar_interval(bar)
    for instId, candle in candle_map.items():
        if valid_diff and not (np.diff(candle[:, 0]) == bar_interval).all():
            msg = '{instId}的candle的时间间隔错误'.format(instId=instId)
            raise exception.CandleDiffError(msg)
        if valid_start and not candle[0, 0] == finance_utils.date.to_ts(date=start_date, timezone=timezone):
            msg = '{instId}的candle的时间起始错误'.format(instId=instId)
            raise exception.CandleStartError(msg)
        if valid_end and candle[-1, 0] != finance_utils.date.to_ts(date=end_date,
                                                                   timezone=timezone) + 1000 * 60 * 60 * 24 - bar_interval:
            msg = '{instId}的candle的时间终止错误'.format(instId=instId)
            raise exception.CandleEndError(msg)
    return candle_map


# 按照日期保存Candle
def save_candle_by_date(
        candle: np.array,
        instType: str,
        instId: str,
        start_date: Union[datetime.date, str],
        end_date: Union[datetime.date, str],
        base_dir='',
        timezone='Asia/Shanghai',
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        sort=True,
        valid_diff=True,
        valid_start=True,
        valid_end=True,
):
    '''
    边按照日期写入，边进行valid，如果valid报告错误，之前的数据可以成功写入，后面的数据则不会继续写入
    '''
    dates = finance_utils.date.get_range_dates(start=start_date, end=end_date, timezone=timezone)
    bar_interval = finance_utils.bar.get_bar_interval(bar)
    df = pd.DataFrame(candle)
    ts_column_name = df.columns[0]
    df[ts_column_name] = df[ts_column_name].astype(int)
    df = df.drop_duplicates(subset=ts_column_name)
    if sort:
        df = df.sort_values(by=ts_column_name)  # 排序
    for date in dates:
        start_ts = finance_utils.date.to_ts(date=date, timezone=timezone)
        end_ts = start_ts + 1000 * 60 * 60 * 24 - bar_interval
        this_df = df[(df[0] >= start_ts) & (df[0] <= end_ts)]

        if valid_diff and not (np.diff(this_df[0]) == bar_interval).all():
            msg = '{instId}的candle的时间间隔错误'.format(instId=instId)
            raise exception.CandleDiffError(msg)
        if valid_start and this_df[0].min() != start_ts:
            msg = '{instId}的candle的时间起始错误，时间的起点是：{datetime}'.format(
                instId=instId,
                datetime=finance_utils.date.to_fmt(date=int(this_df[0].min()), timezone=timezone,
                                                   fmt='%Y-%m-%d %H:%M:%S'),
            )
            raise exception.CandleStartError(msg)
        if valid_end and this_df[0].max() != end_ts:
            msg = '{instId}的candle的时间终止错误，时间终点是：{datetime}'.format(
                instId=instId,
                datetime=finance_utils.date.to_fmt(date=int(this_df[0].max()), timezone=timezone,
                                                   fmt='%Y-%m-%d %H:%M:%S')
            )

            raise exception.CandleEndError(msg)
        path = get_candle_day_path(
            instType=instType,
            instId=instId,
            date=date,
            bar=bar,
            timezone=timezone,
            base_dir=base_dir
        )
        dirpath = os.path.dirname(path)
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
        this_df.to_csv(path, index=False)
    return True


# 按照日期保存candle_map
def save_candle_map_by_date(
        candle_map: dict,
        instType: str,
        instIds: list,
        start_date: Union[datetime.date, str],
        end_date: Union[datetime.date, str],
        base_dir='',
        timezone='Asia/Shanghai',
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        sort=True,
        valid_diff=True,
        valid_start=True,
        valid_end=True,
):
    '''
    如果写入的时候出现了错误，报错之前写入成功，报错后面的则不能正常写入
    '''
    if not instIds:
        instIds = [instId for instId in candle_map.keys()]
    for instId in instIds:
        candle = candle_map[instId]
        save_candle_by_date(
            instType=instType,
            instId=instId,
            candle=candle,
            start_date=start_date,
            end_date=end_date,
            bar=bar,
            timezone=timezone,
            base_dir=base_dir,
            sort=sort,
            valid_diff=valid_diff,
            valid_start=valid_start,
            valid_end=valid_end,
        )


# 通过文件地址读取Candle
def load_candle_by_file(
        instType: str,
        instId: str,
        path: str = None,
        base_dir='',
        timezone='Asia/Shanghai',
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        valid_diff=True,
):
    '''
    如果有path路径，按照path路径读取文件
    如果没有path路径，按照base_dir、instId、instType、bar和timezone计算产品路径
    '''
    if path == None:
        path = get_candle_file_path(
            instType=instType,
            instId=instId,
            bar=bar,
            timezone=timezone,
            base_dir=base_dir,
        )
    df = pd.read_csv(path)
    ts_column_name = df.columns[0]
    # 转化类型
    df[ts_column_name] = df[ts_column_name].astype(int)
    # 排序
    df = df.sort_values(by=ts_column_name)
    # 去重
    df = df.drop_duplicates(subset=ts_column_name)
    candle = df.to_numpy()
    bar_interval = finance_utils.bar.get_bar_interval(bar)
    if valid_diff and not (np.diff(candle[:, 0]) == bar_interval).all():
        msg = '{instId}的candle的时间间隔错误'.format(instId=instId)
        raise exception.CandleDiffError(msg)
    return candle


# 通过文件夹地址读取Candle_map
def load_candle_map_by_file(
        instType: str,
        instIds: list = [],
        path=None,
        base_dir='',
        timezone='Asia/Shanghai',
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        valid_diff=True,

):
    # 如果没有文件夹的地址
    if path == None:
        path = os.path.dirname(get_candle_file_path(
            instType=instType,
            base_dir=base_dir,
            timezone=timezone,
            bar=bar,
            instId='xx',
        ))
    # 如果没有产品的名字，读取文金价中全部的产品
    if not instIds:
        filenames = os.listdir(path)
        instIds = []
        for filename in filenames:
            instId = filename.rsplit('.', maxsplit=1)[0]
            instIds.append(instId)
    # 读取数据
    candle_map = {}
    for instId in instIds:
        candle = load_candle_by_file(
            instId=instId,
            instType=instType,
            base_dir=base_dir,
            timezone=timezone,
            bar=bar,
            valid_diff=valid_diff
        )
        candle_map[instId] = candle
    return candle_map


# 按照文件地址保存Candle
def save_candle_by_file(
        candle: np.array,
        instType: str,
        instId: str,
        path=None,
        base_dir='',
        timezone='Asia/Shanghai',
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        valid_diff=True,
):
    # 验证valid_diff
    bar_interval = finance_utils.bar.get_bar_interval(bar)
    if valid_diff and not (np.diff(candle[:, 0]) == bar_interval).all():
        msg = '{instId}的candle的时间间隔错误'.format(instId=instId)
        raise exception.CandleDiffError(msg)
    # 得到路径
    if path == None:
        path = get_candle_file_path(
            instType=instType,
            instId=instId,
            bar=bar,
            timezone=timezone,
            base_dir=base_dir,
        )
    df = pd.DataFrame(candle)
    ts_column_name = df.columns[0]
    # 转化类型
    df[ts_column_name] = df[ts_column_name].astype(int)
    # 排序
    df = df.sort_values(by=ts_column_name)
    # 去重
    df = df.drop_duplicates(subset=ts_column_name)
    dirpath = os.path.dirname(path)
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
    df.to_csv(path, index=False)


# 按照文件地址保存Candle_map
def save_candle_map_by_file(
        candle_map: dict,
        instType: str,
        base_dir='',
        timezone='Asia/Shanghai',
        bar: Literal['1m', '3m', '5m', '15m', '1H', '2H', '4H'] = '1m',
        valid_diff=True,
):
    for instId, candle in candle_map.items():
        save_candle_by_file(
            candle=candle,
            instType=instType,
            instId=instId,
            path=None,
            base_dir=base_dir,
            timezone=timezone,
            bar=bar,
            valid_diff=valid_diff
        )


if __name__ == '__main__':
    timezone = 'Asia/Shanghai'
    base_dir = '/Users/kzlknight/Documents/okx_candle'
    start_date = '2022-01-01'
    end_date = '2022-01-05'
    bar = '1m'
    candle_BTC_USDT = load_candle_by_date(
        instType='SPOT',
        instId='BTC-USDT',
        start_date=start_date,
        end_date=end_date,
        timezone='Asia/Shanghai',
        bar='1m',
        base_dir=base_dir,
        valid_diff=True,
        valid_start=True,
        valid_end=True,
    )
    print(candle_BTC_USDT)
    save_candle_by_date(
        instId='BTC-USDT',
        candle=candle_BTC_USDT,
        start_date=start_date,
        end_date=end_date,
        bar=bar,
        timezone=timezone,
        instType='SPOT',
        sort=True,
        valid_diff=True,
        valid_start=True,
        valid_end=True,
        base_dir='./3'

    )

    candle_map_SPOT1 = load_candle_map_by_date(
        start_date=start_date,
        end_date=end_date,
        timezone=timezone,
        bar='1m',
        base_dir=base_dir,
        instIds=[],
        instType='SPOT',
        p_num=0,
        contains='-USDT',
        valid_diff=True,
        valid_start=True,
        valid_end=True,
    )
    print(candle_map_SPOT1)

    save_candle_by_date(
        instId='BTC-USDT',
        candle=candle_BTC_USDT,
        start_date=start_date,
        end_date=end_date,
        bar='1m',
        timezone=timezone,
        base_dir='./1',
        instType='SPOT',
        sort=True,
        valid_diff=True,
        valid_start=True,
        valid_end=True,
    )
    candle_BTC_USDT_SWAP = load_candle_by_date(
        instType='SWAP',
        instId='BTC-USDT-SWAP',
        start_date=start_date,
        end_date=end_date,
        timezone='Asia/Shanghai',
        bar='1m',
        base_dir=base_dir,
        valid_diff=True,
        valid_start=True,
        valid_end=True,
    )

    print(candle_BTC_USDT_SWAP)

    save_candle_by_date(
        instId='BTC-USDT-SWAP',
        candle=candle_BTC_USDT_SWAP,
        start_date=start_date,
        end_date=end_date,
        bar='1m',
        timezone=timezone,
        base_dir='./1',
        instType='SWAP',
        sort=True,
        valid_diff=True,
        valid_start=True,
        valid_end=True,
    )
    candle_map_SPOT1 = load_candle_map_by_date(
        start_date=start_date,
        end_date=end_date,
        timezone=timezone,
        bar='1m',
        base_dir=base_dir,
        instIds=[],
        instType='SPOT',
        p_num=4,
        contains='-USDT',
        valid_diff=True,
        valid_start=True,
        valid_end=True,
    )

    print(candle_map_SPOT1)
    save_candle_map_by_date(
        instType='SPOT',
        instIds=[],
        candle_map=candle_map_SPOT1,
        start_date=start_date,
        end_date=end_date,
        bar='1m',
        timezone=timezone,
        base_dir='./1',
        sort=True,
        valid_diff=True,
        valid_start=True,
        valid_end=True,
    )
    candle_map_SWAP1 = load_candle_map_by_date(
        start_date=start_date,
        end_date=end_date,
        timezone=timezone,
        bar='1m',
        base_dir=base_dir,
        instIds=['BTC-USDT-SWAP', 'ETH-USDT-SWAP'],
        instType='SWAP',
        p_num=4,
        contains='-USDT',
        valid_diff=True,
        valid_start=True,
        valid_end=True,
    )

    print(candle_map_SWAP1)
    save_candle_map_by_date(
        instType='SWAP',
        instIds=[],
        candle_map=candle_map_SWAP1,
        start_date=start_date,
        end_date=end_date,
        bar='1m',
        timezone=timezone,
        base_dir='./1',
        sort=True,
        valid_diff=True,
        valid_start=True,
        valid_end=True,
    )
    candle_BTC_USDT = load_candle_by_date(
        instType='SPOT',
        instId='BTC-USDT',
        start_date=start_date,
        end_date=end_date,
        timezone='Asia/Shanghai',
        bar='1m',
        base_dir=base_dir,
        valid_diff=True,
        valid_start=True,
        valid_end=True,
    )
    print(candle_BTC_USDT)

    save_candle_by_file(
        candle=candle_BTC_USDT,
        instId='BTC-USDT',
        instType='SPOT',
        base_dir='./2',
        timezone=timezone,
        bar='1m',
        valid_diff=True,
    )
    #
    candle_BTC_USDT_SWAP = load_candle_by_date(
        instType='SWAP',
        instId='BTC-USDT-SWAP',
        start_date=start_date,
        end_date=end_date,
        timezone='Asia/Shanghai',
        bar='1m',
        base_dir=base_dir,
        valid_diff=True,
        valid_start=True,
        valid_end=True,
    )

    print(candle_BTC_USDT_SWAP)

    save_candle_by_file(
        candle=candle_BTC_USDT_SWAP,
        instId='BTC-USDT-SWAP',
        instType='SWAP',
        base_dir='./2',
        timezone=timezone,
        bar='1m',
        valid_diff=True,
    )
    #
    candle_map_SWAP = load_candle_map_by_date(
        start_date=start_date,
        end_date=end_date,
        timezone=timezone,
        bar='1m',
        base_dir=base_dir,
        instIds=[],
        instType='SWAP',
        p_num=4,
        contains='-USDT',
        valid_diff=True,
        valid_start=True,
        valid_end=True,
    )

    save_candle_map_by_file(
        candle_map=candle_map_SWAP,
        instType='SWAP',
        base_dir='./2',
        timezone=timezone,
        bar='1m',
        valid_diff=True,
    )
    candle = load_candle_by_file(
        instId='BTC-USDT-SWAP',
        instType='SWAP',
        path=None,
        base_dir='./2',
        timezone=timezone,
        bar='1m',
        valid_diff=True
    )
    print(candle)
    #
    candle_map = load_candle_map_by_file(
        instType='SWAP',
        instIds=['BTC-USDT-SWAP'],
        base_dir='./2',
        timezone=timezone,
        bar='1m',
        valid_diff=True
    )
    print(candle_map)
