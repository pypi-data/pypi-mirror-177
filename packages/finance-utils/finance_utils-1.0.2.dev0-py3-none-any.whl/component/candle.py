import datetime
import numpy as np
from finance_utils.component.bar import get_bar_interval, predict_bar
from finance_utils.component.date import to_ts
from finance_utils import exception
from typing import Union


# 压缩历史K线
def transform_candle_by_bar(
        candle: np.array,
        target_bar: str,
        org_bar: str = 'auto'
):
    '''
    转换（压缩）历史K线

    :param candle: 历史K线数据
    :param target_bar: 目标K线的bar
    :param org_bar: 原始K线的bar
    :return:转换后的历史K线数据
        array([
            [ts,open,high,low,close,volume],
            [ts,open,high,low,close,volume],
            [ts,open,high,low,close,volume],
        ])


    example：
        将1Minute的K线数据转化成5Minute的K线数据
        transform_candle_by_bar(candle,target_bar='5m',org_bar='1m')

        将1Hour的K线数据转化成1Day的K线数据
        transform_candle_by_bar(candle,target_bar='1d',org_bar='1h')
    '''
    if org_bar == 'auto':
        org_bar = predict_bar(candle)
    # 目标K线ts间隔
    target_bar_interval = get_bar_interval(target_bar)
    # 原始K线ts间隔
    org_tar_interval = get_bar_interval(org_bar)
    # 压缩的数量
    compress_quantity = target_bar_interval / org_tar_interval
    if compress_quantity != int(compress_quantity):
        msg = "Can't transform candle from org_Bar({org_bar}) to target_bar{target_bar}".format(
            org_bar=org_bar,
            target_bar=target_bar,
        )
        raise exception.ParamException(msg)
    compress_quantity = int(compress_quantity)
    # 目标K线数据
    target_datas = []
    for i in range(0, candle.shape[0], compress_quantity):
        if i + compress_quantity < candle.shape[0]:
            this_data = [
                candle[i, 0],  # ts
                candle[i, 1],  # open
                candle[i:i + compress_quantity, 2].max(),  # high
                candle[i:i + compress_quantity, 3].min(),  # low
                candle[i + compress_quantity - 1, 4],  # close
                candle[i:i + compress_quantity, 5].sum()  # volume
            ]
            target_datas.append(this_data)
    # 目标K线Candle
    target_candle = np.array(target_datas)
    return target_candle


# 得到均线
def get_candle_ma(
        candle: np.array,
        n: int
):
    '''
    获取历史均线

    :param candle:历史K线数据
    :param n:间隔
    :return:
        array([
                [ts,mac],
                [ts.mac],
                [ts.mac],
            ])
    '''
    # 均线数据
    mac_datas = []
    for index in range(candle.shape[0]):
        if index < n - 1:
            mac = np.nan
        else:
            mac = candle[index - n + 1:index + 1, 1].mean()
        mac_datas.append([candle[index, 0], mac])
    # 均线Candle
    mac_candle = np.array(mac_datas)
    return mac_candle


# 得到布林带
def get_candle_boll(
        candle: np.array,
        n: int
):
    '''
    获取布林带

    :param candle:历史K线数据
    :param n:间隔
    :return:
        array([
            [ts,mb,up,dn],
            [ts,mb,up,dn],
            [ts,mb,up,dn],
        ])
        (mb:均线 up:上轨 dn:下轨)
    '''
    # 布林带数据
    boll_datas = []
    for index in range(candle.shape[0]):
        if index <= n - 1:
            mb = np.nan
            up = np.nan
            dn = np.nan
        else:
            mb = candle[index - n:index, 4].mean()  # 收盘价均值
            sd = (candle[index - n:index, 4] - mb).std()  # 收盘价标准差
            up = mb + 2 * sd  # 上轨
            dn = mb - 2 * sd  # 下轨
        boll_datas.append(
            [candle[index, 0], mb, up, dn]
        )
    # 布林带Candle
    boll_candle = np.array(boll_datas)
    return boll_candle


# 得到DualThrust中的上轨和下轨
def get_candle_dualThrust(
        candle: np.array,
        n: int,
        ks: float,
        kx: float,
        update_n: int = None
):
    '''
    获取DualThrust Candle

    :param candle:历史K线数据
    :param n:间隔
    :param ks:ks参数
    :param kx:kx参数
    :param update_n:更新的间隔n
    :return:
        array([
            [ts,range_ks,range_kx],
            [ts,range_ks,range_kx],
            [ts,range_ks,range_kx],
        ])
        (range_ks上轨 range_kx下轨)
    '''
    # dualThrust数据
    dualThrust_datas = []
    for i in range(0, candle.shape[0], update_n):
        if i <= n - 1:
            range_kx = np.nan
            range_ks = np.nan
        else:
            last_k_array = candle[i - n:i]  # 前n间隔的数据
            hh = last_k_array[:, 2].max()  # 最高价的最高价
            hc = last_k_array[:, 4].max()  # 最高价的收盘价
            lc = last_k_array[:, 4].min()  # 最低价的收盘价
            ll = last_k_array[:, 3].min()  # 最低价的最低价
            range_ = max(hh - lc, hc - ll)
            o = candle[i, 1]
            range_ks = o + ks * range_  # 上轨
            range_kx = o - kx * range_  # 下轨
        for ts in candle[i:i + update_n, 0]:
            dualThrust_datas.append(
                [ts, range_ks, range_kx]
            )
    # dualThrust Candle
    dualThrust_candle = np.array(dualThrust_datas)
    return dualThrust_candle


# 根据日期，得到K线中的索引
def get_candle_index_by_date(
        candle: np.array,
        date: Union[datetime.datetime, int, float, str,],
        timezone: str = 'Asia/Shanghai',
        default: int = 0
):
    if not date:
        return default
    ts = to_ts(date=date, timezone=timezone, default=default)
    index = np.where(
        candle[:, 0] == ts
    )[0][0]
    return index


if __name__ == '__main__':
    pass
