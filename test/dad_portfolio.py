# GPPL - 2500 - 137.70
# CASTROLIND - 1000 - 187.68
# IDFCFIRSTB - 15000 - 47.40
# PETRONET LNG - 1000 - 249.90
import time
# import pandas as pd

from get.historical_data_from_yf import get_data_from_start_date

df = get_data_from_start_date('LINCOLN', 'NSE', 'daily', 8, 10, 2021, True, True)
print(df)

gppl = (2500 * 137.7)
castrol = (1000 * 187.68)
idfcf = (15000 * 47.40)
petronet = (1000 * 249.90)

stocks = [
    {
        'ticker': 'GPPL',
        'avg_buy_price': 137.7,
        'qty': 2500
    },
    {
        'ticker': 'GPPL',
        'avg_buy_price': 137.7,
        'qty': 2500
    },
    {
        'ticker': 'GPPL',
        'avg_buy_price': 137.7,
        'qty': 2500
    },
    {
        'ticker': 'GPPL',
        'avg_buy_price': 137.7,
        'qty': 2500
    },

]

print(gppl, castrol, idfcf, petronet)
invested_price = gppl + castrol + idfcf + petronet
print(invested_price)


# tickers = ['GPPL', 'CASTROLIND', 'IDFCFIRSTB', 'PETRONET']
#
# for ticker in tickers:
#
#     time.sleep(1)


class Stock:
    def __init__(self, ticker, avg_buy_price, qty):
        self.ticker = ticker
        self.avg_buy_price = avg_buy_price
        self.qty = qty
