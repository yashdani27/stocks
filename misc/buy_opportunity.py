import json
import time
from datetime import datetime, date
import datetime

import requests

from constants import SCREENER_KEYS
from get import data_from_screener_bs4
from get.data_from_screener_bs4 import get_data_from_screener_using_bs4

f = open('../data/data_companies_temp.json')
data = json.load(f)
companies = data['companies']


def get_start_date(p_date, p_month, p_year):
    return int(time.mktime(datetime.datetime(p_year, p_month, p_date, 8, 30).timetuple()))


def get_end_date(p_date, p_month, p_year):
    return int(time.mktime(datetime.datetime(p_year, p_month, p_date, 23, 59).timetuple()))


def get_data_from_yf(p_ticker, p_str_date):
    arr_date = p_str_date.split('-')
    period1 = get_start_date(int(arr_date[2]), int(arr_date[1]), int(arr_date[0]))
    period2 = get_end_date(int(arr_date[2]), int(arr_date[1]), int(arr_date[0]))
    url = f'https://query1.finance.yahoo.com/v7/finance/download/{p_ticker}?period1={period1}&period2={period2}&interval=1d&events=history&includeAdjustedClose=true'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }
    return requests.get(url, headers=headers).text


for company in companies:
    symbol = company['symbol']
    print(symbol)
    exchange = company['exchange']
    ticker = symbol
    if exchange == 'NSE':
        ticker += '.NS'
    else:
        ticker += '.BO'
    q_result_date = company['q_result_date']
    response = get_data_from_yf(ticker, q_result_date[-1])
    # print(response)
    array_data = response.split('\n')
    price_close_result_date = array_data[1].split(',')[4]
    print(price_close_result_date)
    time.sleep(1)
    dictionary_screener = get_data_from_screener_using_bs4(symbol)
    price_close_current_date = dictionary_screener[SCREENER_KEYS.PRICE]
    # print(price_close_result_date, price_close_current_date)
    # print(dictionary_screener)
    # print(dictionary_screener[SCREENER_KEYS.QR_SALES])
    qr_sales = ((float(dictionary_screener['Rel ' + SCREENER_KEYS.QR_SALES][-1]) - 1) * 100)
    qr_exp = "{:.2f}".format((float(dictionary_screener['Rel ' + SCREENER_KEYS.QR_EXPENSES][-1]) - 1) * 100)
    qr_profit = ((float(dictionary_screener['Rel ' + SCREENER_KEYS.QR_NET_PROFIT][-1]) - 1) * 100)
    print(qr_sales, qr_exp, qr_profit)

    current_date = str(datetime.datetime.now())
    arr_current_date = current_date.split(' ')[0].split('-')
    arr_result_date = q_result_date[-1].split('-')
    # print(arr_current_date, arr_result_date)
    days_between_result_present = (date(int(arr_current_date[0]), int(arr_current_date[1]), int(arr_current_date[2])) - date(int(arr_result_date[0]), int(arr_result_date[1]), int(arr_result_date[2]))).days
    print('days_between_result_present', days_between_result_present)

    if qr_sales > 5 and qr_profit > 5:
        price_close_result_date = float(price_close_result_date.replace(',', ''))
        price_close_current_date = float(price_close_current_date.replace(',', ''))
        if price_close_current_date/price_close_result_date < 1.05:
            print('!!Potential buying opportunity!!')
            print('Stock trading at: ',
                  (price_close_current_date - price_close_result_date) / price_close_result_date * 100,
                  '% below result date price')
        else:
            print('Stock trading at: ', (price_close_current_date - price_close_result_date) / price_close_result_date * 100, '% above result date price')

    print('///////////////////////////////////////////////////////////////')
    time.sleep(1)
    # sales_increase = ((qr_sales[-1] / qr_sales[-2]) - 1) * 100
    # exp_increase = ((qr_exp[-1] / qr_exp[-2]) - 1) * 100
    # profit_increase = ((qr_profit[-1] / qr_profit[-2]) - 1) * 100
