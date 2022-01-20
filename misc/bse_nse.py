import pandas as pd
from tabulate import tabulate

bse_url = '/Users/dharmendradani/Desktop/EQUITY_BSE.csv'
nse_url = '/Users/dharmendradani/Desktop/EQUITY_NSE.csv'

df_bse = pd.read_csv(bse_url)
df_nse = pd.read_csv(nse_url)

print(df_bse.head())
print(df_nse.head())

print(sorted(df_nse['SYMBOL']))
# print(df_bse['Security Id'])

print(sorted(df_bse['Security Id']))

list_bse_stocks = sorted(df_bse['Security Id'])
list_nse_stocks = sorted(df_nse['SYMBOL'])

stock_found = False
counter = 0
only_bse_counter = 0
for nse_stock in list_nse_stocks:
    stock_found = False
    for bse_stock in list_bse_stocks:
        if 0 >= int(bse_stock[0]) >= 9:
            print(bse_stock[0])
            continue
        if bse_stock[0] < nse_stock[0]:
            only_bse_counter += 1
            print('ignored', only_bse_counter, bse_stock)
            break
        if nse_stock == bse_stock:
            stock_found = True
            break
    if not stock_found:
        counter += 1
        print(counter, nse_stock)
    # print(nse_stock)

print(list_bse_stocks[0][1])

# print(tabulate(df_bse, headers="keys", tablefmt="psql"))
# print(tabulate(df_nse, headers="keys", tablefmt="psql"))

