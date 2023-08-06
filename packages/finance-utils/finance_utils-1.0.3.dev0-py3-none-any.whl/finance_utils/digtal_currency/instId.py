import re


# 预测okx中的产品的种类
def okx_predict_instType(instId: str):
    if instId.endswith('-SWAP'):
        return 'SWAP'
    elif re.match('^.+-\d+$', instId):
        return 'FUTURES'
    else:
        return 'SPOT'
