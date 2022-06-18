import json
import time
from datetime import datetime, date
import datetime

import requests
from tabulate import tabulate

from constants import SCREENER_KEYS
from get import data_from_screener_bs4
from get.data_from_screener_bs4 import get_data_from_screener_using_bs4
from get.historical_data_from_yf import get_data_from_start_date, get_data_for_date
# from get.store_fetch_ticker_data_db import fetch_ticker_data_from_db

MONTHS = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']


def get_start_end_period(p_date, p_month, p_year):
    period1 = int(time.mktime(datetime.datetime(p_year, p_month, p_date, 8, 0).timetuple()))
    period2 = int(time.mktime(datetime.datetime(p_year, p_month, p_date, 23, 59).timetuple()))
    return period1, period2


def get_data_from_yf(p_ticker, p_str_date):
    arr_date = p_str_date.split('-')
    period1, period2 = get_start_end_period(int(arr_date[2]), int(arr_date[1]), int(arr_date[0]))
    url = f'https://query1.finance.yahoo.com/v7/finance/download/{p_ticker}?period1={period1}&period2={period2}&interval=1d&events=history&includeAdjustedClose=true'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }
    return requests.get(url, headers=headers).text


def print_dataframe(p_dataframe):
    print(tabulate(p_dataframe, headers="keys", tablefmt="psql"))


def get_buy_opportunities(bundle):
    f = open('../data/data_companies_' + bundle + '.json')
    data = json.load(f)
    companies = data['companies']
    dict_companies = []
    for company in companies:
        symbol = company['symbol']
        print(symbol)
        exchange = company['exchange']
        q_result_date = company['q_result_date']
        arr_date = q_result_date[-1].split('-')
        final_df = get_data_for_date(symbol, exchange, int(arr_date[2]), int(arr_date[1]), int(arr_date[0]))
        # print_dataframe(final_df)
        # print(response)
        price_close_result_date = final_df['Close']
        dictionary_screener = get_data_from_screener_using_bs4(symbol)
        price_close_current_date = dictionary_screener[SCREENER_KEYS.PRICE]
        print(price_close_result_date, price_close_current_date)
        # print(dictionary_screener)
        # print(dictionary_screener[SCREENER_KEYS.QR_SALES])
        qr_sales = ((float(dictionary_screener['Rel ' + SCREENER_KEYS.QR_SALES][-1]) - 1) * 100)
        qr_exp = "{:.2f}".format((float(dictionary_screener['Rel ' + SCREENER_KEYS.QR_EXPENSES][-1]) - 1) * 100)
        qr_profit = ((float(dictionary_screener['Rel ' + SCREENER_KEYS.QR_NET_PROFIT][-1]) - 1) * 100)
        print(qr_sales, qr_exp, qr_profit)

        # calculate number of days between the result and present date
        current_date = str(datetime.datetime.now())
        arr_current_date = current_date.split(' ')[0].split('-')
        arr_result_date = q_result_date[-1].split('-')
        # print(arr_current_date, arr_result_date)
        days_between_result_present = (
                    date(int(arr_current_date[0]), int(arr_current_date[1]), int(arr_current_date[2])) -
                    date(int(arr_result_date[0]), int(arr_result_date[1]), int(arr_result_date[2]))).days
        print('days_between_result_present -', days_between_result_present)

        if qr_sales > 0 and qr_profit > 0:
            price_close_result_date = float(price_close_result_date)
            price_close_current_date = float(price_close_current_date.replace(',', ''))
            if price_close_current_date/price_close_result_date < 1:
                final_df = get_data_from_start_date(symbol, exchange, 'daily', int(arr_date[2]), int(arr_date[1]),
                                                    int(arr_date[0]), False, False)
                ticker_data = fetch_ticker_data_from_db(company['symbol'])
                # print(ticker_data)
                # print(final_df)
                dict_temp = {
                    "company": company,
                    "date": final_df['Date'].tolist(),
                    "close": final_df['Close'].tolist(),
                    "days_since_result": days_between_result_present,
                    "sessions_since_result": final_df.shape[0],
                    "price_below_result": "{:.2f}".format((price_close_current_date - price_close_result_date) / price_close_result_date * 100),
                    "qr_sales": "{:.2f}".format(qr_sales),
                    "qr_profit": "{:.2f}".format(qr_profit),
                    "last_result_date": arr_date[2] + ' ' + MONTHS[int(arr_date[1])],
                    "ticker_data": ticker_data
                }
                dict_companies.append(dict_temp)
                print('!!Potential buying opportunity!!')
                # print('Stock trading at: ',
                #       (price_close_current_date - price_close_result_date) / price_close_result_date * 100,
                #       '% below result date price')
            else:
                print('Stock trading at: ', (price_close_current_date - price_close_result_date) / price_close_result_date * 100, '% above result date price')

        print('///////////////////////////////////////////////////////////////')
        time.sleep(1)
        # sales_increase = ((qr_sales[-1] / qr_sales[-2]) - 1) * 100
        # exp_increase = ((qr_exp[-1] / qr_exp[-2]) - 1) * 100
        # profit_increase = ((qr_profit[-1] / qr_profit[-2]) - 1) * 100
    print(dict_companies)
    return dict_companies


# get_buy_opportunities()


