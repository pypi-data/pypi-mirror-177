# 计算手续费
def get_commission_data(
        posSide,
        buyMoney,
        buyLine,
        sellLine,
        lever,
        buyCommissionRate,
        sellCommissionRate
):
    if posSide == 'long':
        buyCommission = buyMoney * lever * buyCommissionRate
        sellCommission = (sellLine / buyLine) * buyMoney * lever * sellCommissionRate
        commission = round(buyCommission + sellCommission, 4)
        sellMoney = round((sellLine - buyLine) / buyLine * lever * buyMoney + buyMoney - commission, 4)
        profitRate = round((sellMoney - buyMoney) / buyMoney, 4)
        return dict(
            sellMoney=sellMoney,
            commission=commission,
            profitRate=profitRate,
        )
    elif posSide == 'short':
        buyCommission = buyMoney * lever * buyCommissionRate
        sellCommission = (2 * buyLine - sellLine) / buyLine * buyMoney * lever * sellCommissionRate
        commission = round(buyCommission + sellCommission, 4)
        sellMoney = (buyLine - sellLine) / buyLine * buyMoney * lever + buyMoney - commission
        profitRate = round((sellMoney - buyMoney) / buyMoney, 4)
        return dict(
            sellMoney=sellMoney,
            commission=commission,
            profitRate=profitRate,
        )
