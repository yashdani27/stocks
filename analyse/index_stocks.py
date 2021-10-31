import json
import time
import pandas as pd
from tabulate import tabulate
from get.historical_data_from_yf import get_data_from_start_date, get_yearly_gains, compute_cagr


def print_dataframe(p_dataframe):
    print(tabulate(p_dataframe, headers="keys", tablefmt="psql"))


file_nifty = open('../data/data_companies_nifty.json')
file_sensex = open('../data/data_companies_sensex.json')

companies_nifty = json.load(file_nifty)['companies']
companies_sensex = json.load(file_sensex)['companies']
companies = [companies_nifty, companies_sensex]
exchange = ['NSE', 'BSE']
filename = ['NIFTY_10Y', 'SENSEX_10Y']

df_main = None

for index, stock_index in enumerate(companies):
    df_main = None
    for location, company in enumerate(stock_index):
        # if location > 5:
        #     continue
        print('Data for', company)
        df = get_data_from_start_date(company, exchange[index], 'monthly', 1, 1, 2010, True, True)
        df_yearly_gains = get_yearly_gains(df)
        df_cagr = compute_cagr(df_yearly_gains)
        # print_dataframe(df_cagr)
        if df_main is None:
            df_main = pd.DataFrame(list(zip(df_cagr['Date'])))
            df_main.columns = ['Date']
            df_main.set_index('Date')
        df_main[company + '_YoY'] = df_cagr['PercentChange']
        df_main[company + '_CAGR(before Covid)'] = df_cagr['CAGR (before COVID)']
        df_main[company + '_CAGR(after Covid)'] = df_cagr['CAGR (after COVID)']
        # print(df_yearly_gains['Date'][1])
        # print_dataframe(get_yearly_gains(df))
        time.sleep(1)
    df_main.to_csv(r'/Users/dharmendradani/PycharmProjects/' + filename[index] + '.csv')

# print_dataframe(df_main)


# print_dataframe(final_df)
# # print_dataframe(get_monthly_gains(final_df))
#
# print_dataframe(get_yearly_gains(final_df))