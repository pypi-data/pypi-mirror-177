import math


# 模拟数据中的价格元整
def simulate_round(px):
    if px == 0:
        return px
    px_0_00001 = 0.00001 * px
    if px_0_00001 < 1:
        ndigits = len(str(int(1 / px_0_00001)))
        px_round = round(px, ndigits)
    else:
        px_round = round(px, 1)
    if abs((px_round - px) / px) >= 0.00001:
        raise Exception(
            'px_round={px_round},px={px}'.format(
                px_round=px_round,
                px=px
            )
        )
    else:
        return px_round


# 数量向下按照精度取元整
def decimal_floor(num, precise):
    if float(precise) < 1:  # 0.1 0.01
        m = len(str(precise).split('.')[-1])
        num_round = round(num, m)
    else:
        num_floor = num // float(precise) * float(precise)
        num_round = round(num_floor)
    return num_round


# 价格元整
def round_px(px, tickSz):
    px_round = decimal_floor(num=px, precise=tickSz)
    if abs(px_round - px) / px >= 0.005:
        print(px, 'px')
        print(px_round, 'px_round')
        print(abs(px_round - px) / px)
        raise Exception('error')
    else:
        if int(px_round) == float(px_round):
            px_round = int(px_round)
        return px_round


# 数量元整
def round_sz(sz, minSz):
    sz_round = decimal_floor(num=sz, precise=minSz)
    if int(sz_round) == float(sz_round):
        sz_round = int(sz_round)
    return sz_round


# 计算最多的购买数量
def get_sz(buyLine, buyMoney, lever, ctVal='', minSz=1):
    buyMoney = buyMoney * lever
    if ctVal:
        sz = buyMoney / buyLine / float(ctVal)
        return math.floor(sz)
    else:
        return decimal_floor(buyMoney / buyLine, precise=minSz)


# 将数字按照精度转换为字符串
def to_f(num, precise, valid=True):
    if num == 0:
        return 0
    elif float(precise) < 1:
        m = len(str(precise).split('.')[-1])
    else:
        m = 0
    d_format = '%.{m}f'.format(m=m)
    num_f = d_format % num
    if valid and not float(num_f) == float(num):
        raise Exception('valid error')
    return num_f
