from bs4 import BeautifulSoup
import requests
from datetime import datetime
import datetime
import time
from tabulate import tabulate
import pandas as pd
import json
import math

from constants import YF_DF_COL


# print(get_date(-60))
def get_date(number_of_days):
    tomorrows_date = (str(datetime.date.today() + datetime.timedelta(days=number_of_days))).split('-')
    temp_year = int(tomorrows_date[0])
    temp_month = int(tomorrows_date[1])
    temp_day = int(tomorrows_date[2])
    # print(temp_year, temp_month, temp_day)
    return int(time.mktime(datetime.datetime(temp_year, temp_month, temp_day, 23, 59).timetuple()))


def get_start_end_period(p_date, p_month, p_year):
    period1 = int(time.mktime(datetime.datetime(p_year, p_month, p_date, 8, 0).timetuple()))
    period2 = int(time.mktime(datetime.datetime(p_year, p_month, p_date, 23, 59).timetuple()))
    return period1, period2


def get_start_date(p_date, p_month, p_year):
    return int(time.mktime(datetime.datetime(p_year, p_month, p_date, 8, 30).timetuple()))


def prepare_url(p_ticker, period1, period2, p_interval):
    interval = ''
    if p_interval == 'daily':
        interval = '1d'
    elif p_interval == 'weekly':
        interval = '1wk'
    elif p_interval == 'monthly':
        interval = '1mo'
    return f'https://query1.finance.yahoo.com/v7/finance/download/{p_ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

# https://query1.finance.yahoo.com/v7/finance/download/LINCOLN.NS?period1=1595085832&period2=1626621832&interval=1d&events=history&includeAdjustedClose=true


def get_data_from_yahoo_finance(p_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }
    return requests.get(p_url, headers=headers).text


def prepare_dataframe(p_response):
    list_date = []
    list_open = []
    list_high = []
    list_low = []
    list_close = []
    list_adj_close = []
    list_volume = []

    # print(p_response)

    array_data = p_response.split('\n')
    # print('array_data', array_data)

    for i in range(1, len(array_data)):
        if array_data[i].split(',')[1] != 'null':
            list_date.append(array_data[i].split(',')[0])
            list_open.append(math.ceil(float(array_data[i].split(',')[1])))
            list_high.append(float(array_data[i].split(',')[2]))
            list_low.append(float(array_data[i].split(',')[3]))
            list_close.append(math.ceil(float(array_data[i].split(',')[4])))
            list_adj_close.append(float(array_data[i].split(',')[5]))
            list_volume.append(float(array_data[i].split(',')[6]))

    temp_df = pd.DataFrame(list(zip(list_date, list_open, list_high, list_low, list_close, list_adj_close, list_volume)))
    columns = array_data[0].split(',')
    # print(columns)
    temp_df.columns = columns

    return temp_df


def prepare_ticker(p_ticker, p_exchange):
    if p_exchange == 'NSE':
        return p_ticker + '.NS'
    elif p_exchange == 'BSE':
        return p_ticker + '.BO'
    else:
        return p_ticker


def add_net_change_column_to_df(df):
    list_close = df['Close']
    list_net_change = [0]
    for index, list_close_val in enumerate(list_close):
        if index == 0:
            continue
        list_net_change.append(list_close_val - list_close[index - 1])
    df[YF_DF_COL.NETCHANGE] = list_net_change
    return df


def add_percent_change_column_to_df(df):
    list_close = df[YF_DF_COL.CLOSE]
    list_percent_change = [0]
    for index, list_close_val in enumerate(list_close):
        if index == 0:
            continue
        list_percent_change.append((list_close_val - list_close[index - 1]) / list_close[index - 1] * 100)
    df[YF_DF_COL.PERCENTCHANGE] = list_percent_change
    return df


# get_data_from_start_date('LINCOLN', 'NSE', 'daily', 1, 1, 2010, True, True)
def get_data_from_start_date(p_ticker, p_exchange, p_interval, p_date, p_month, p_year, p_net_change, p_percent_change):
    ticker = prepare_ticker(p_ticker, p_exchange)
    if ticker == 1:
        return ticker
    period1 = get_start_date(p_date, p_month, p_year)
    period2 = get_date(1)
    url = prepare_url(ticker, period1, period2, p_interval)
    data = get_data_from_yahoo_finance(url)
    dataframe = prepare_dataframe(data)
    if p_net_change:
        dataframe = add_net_change_column_to_df(dataframe)
    if p_percent_change:
        dataframe = add_percent_change_column_to_df(dataframe)

    return dataframe


# get_data_for_trailing_days('LINCOLN', 'NSE', 'daily', '30', True, True)
def get_data_for_trailing_days(p_ticker, p_exchange, p_interval, p_interval_days, p_net_change, p_percent_change):
    ticker = prepare_ticker(p_ticker, p_exchange)
    if ticker == 1:
        return ticker
    period1 = get_date(-p_interval_days)
    period2 = get_date(1)
    url = prepare_url(ticker, period1, period2, p_interval)
    data = get_data_from_yahoo_finance(url)
    dataframe = prepare_dataframe(data)
    if p_net_change:
        dataframe = add_net_change_column_to_df(dataframe)
    if p_percent_change:
        dataframe = add_percent_change_column_to_df(dataframe)

    return dataframe


# get_data_from_start_date('LINCOLN', 'NSE'', 1, 1, 2010)
def get_data_for_date(p_ticker, p_exchange, p_date, p_month, p_year):
    ticker = prepare_ticker(p_ticker, p_exchange)
    period1, period2 = get_start_end_period(p_date, p_month, p_year)
    url = prepare_url(ticker, period1, period2, 'daily')
    data = get_data_from_yahoo_finance(url)
    dataframe = prepare_dataframe(data)
    return dataframe


def get_monthly_gains(p_dataframe):
    return p_dataframe[[YF_DF_COL.DATE, YF_DF_COL.PERCENTCHANGE]]


# def get_yearly_gains(p_dataframe):
def get_yearly_gains(p_ticker, p_exchange, p_interval, p_date, p_month, p_year, p_net_change, p_percent_change):
    p_dataframe = get_data_from_start_date(p_ticker, p_exchange, p_interval, p_date, p_month, p_year, p_net_change, p_percent_change)
    df_yearly = pd.DataFrame([])
    total_rows = p_dataframe.shape[0]
    print_dataframe(p_dataframe)
    print(p_dataframe.shape[0]/12)
    total_iterations = math.ceil(p_dataframe.shape[0]/12)
    print('total iterations', total_iterations)
    # list_date = [p_dataframe[YF_DF_COL.DATE][0].split('-')[0]]
    list_date = []
    # list_percent = [0]
    list_percent = []
    list_open = []
    list_close = []
    last_close = 1
    last_open = 1
    if total_iterations > 1:
        for iteration in range(total_iterations):
            print(iteration)
            if iteration == 0:
                continue
            df_index = iteration * 12
            list_date.append(p_dataframe[YF_DF_COL.DATE][df_index - 12].split('-')[0])
            # list_date.append(p_dataframe[YF_DF_COL.DATE][df_index - 12] + ' - ' + p_dataframe[YF_DF_COL.DATE][df_index])
            temp = (p_dataframe[YF_DF_COL.CLOSE][df_index - 1] - p_dataframe[YF_DF_COL.OPEN][df_index - 12]) / p_dataframe[YF_DF_COL.OPEN][df_index - 12] * 100
            list_percent.append(math.ceil(temp))
            list_open.append(p_dataframe[YF_DF_COL.OPEN][df_index - 12])
            list_close.append(p_dataframe[YF_DF_COL.CLOSE][df_index - 1])
            if iteration == total_iterations - 1:
                last_close = p_dataframe[YF_DF_COL.CLOSE][df_index - 1]
                last_open = p_dataframe[YF_DF_COL.OPEN][df_index]

            # df_yearly[YF_DF_COL.DATE] = p_dataframe[YF_DF_COL.DATE][df_index]
            # df_yearly[YF_DF_COL.PERCENTCHANGE] = (p_dataframe[YF_DF_COL.CLOSE][df_index] - p_dataframe[YF_DF_COL.CLOSE][df_index - 12]) / p_dataframe[YF_DF_COL.CLOSE][df_index - 12] * 100
        list_date.append(p_dataframe[YF_DF_COL.DATE][total_rows - 1].split('-')[0])
        list_percent.append(math.ceil((p_dataframe[YF_DF_COL.CLOSE][total_rows - 1] - last_open) / last_close * 100))
        list_open.append(last_open)
        list_close.append(p_dataframe[YF_DF_COL.CLOSE][total_rows - 1])
        df_yearly = pd.DataFrame(list(zip(list_date, list_percent, list_open, list_close)))
    else:
        val_open = p_dataframe[YF_DF_COL.OPEN][0]
        val_close = p_dataframe[YF_DF_COL.CLOSE][p_dataframe.shape[0] - 1]
        val_percent = (val_close - val_open) / val_open * 100
        print(val_open, val_close, val_percent)
        df_yearly = pd.DataFrame(list(zip([2021], [val_percent], [val_open], [val_close])))
    df_yearly.columns = [YF_DF_COL.DATE, YF_DF_COL.PERCENTCHANGE, YF_DF_COL.OPEN, YF_DF_COL.CLOSE]
    print('dataframe')
    # print_dataframe(df_yearly)
    return df_yearly


def print_dataframe(p_dataframe):
    print(tabulate(p_dataframe, headers="keys", tablefmt="psql"))


def reverse_list(p_list):
    list_length = len(p_list)
    # print(list_length)
    limit = math.floor(list_length / 2)
    # print(limit)
    for i in range(limit):
        temp = p_list[i]
        p_list[i] = p_list[list_length - i - 1]
        p_list[list_length - i - 1] = temp
    # print(p_list)


def compute_cagr(df_yearly_gains):
    # df_yearly_gains.set_index('Date')
    # print_dataframe(df)
    val_close_before_covid = df_yearly_gains[YF_DF_COL.CLOSE][-3:-2]
    # print('val_close_before_covid', val_close_before_covid)
    val_close = df_yearly_gains[YF_DF_COL.CLOSE][-1:]
    list_open = df_yearly_gains[YF_DF_COL.OPEN]
    # print(list_open)
    list_cagr = []
    list_cagr_before_covid = []

    list_open = reversed(list_open)
    covid_index = 0
    # print('list_open', [li for li in list_open])
    for index, price in enumerate(list_open):
        list_cagr.append(math.ceil(float(((val_close / price) ** (1 / (index + 1)) - 1) * 100)))
        if index >= 2:
            list_cagr_before_covid.append(math.ceil(float(((val_close_before_covid / price) ** (1 / (covid_index + 1)) - 1) * 100)))
            covid_index += 1
    # print(val_close)
    # print([val for val in list_cagr])
    reverse_list(list_cagr)
    # print(list_cagr_before_covid)
    reverse_list(list_cagr_before_covid)
    # print(list_cagr_before_covid)
    if df_yearly_gains.shape[0] > 1:
        list_cagr_before_covid.append(0)
        list_cagr_before_covid.append(0)
    else:
        list_cagr_before_covid.append(0)
    # list_cagr = reversed(list_cagr)
    # print([val for val in list_cagr])
    # print(list_cagr)
    df_yearly_gains['CAGR (after COVID)'] = list_cagr
    print(list_cagr, list_cagr_before_covid)
    df_yearly_gains['CAGR (before COVID)'] = list_cagr_before_covid
    # df_yearly_gains.insert(4, "CAGR", list_cagr, True)
    return df_yearly_gains


# final_df = get_data_for_date('POWERMECH', 'NSE', 6, 8, 2021)
# print_dataframe(final_df)

# print(get_data_for_trailing_days('LINCOLN', 'NSE', 'daily', 30, False, False))

# final_df = get_data_from_start_date('NESTLEIND', 'NSE', 'monthly', 1, 1, 2010, False, False)
# print_dataframe(final_df)

# df_year = get_yearly_gains('POWERMECH', 'NSE', 'monthly', 1, 1, 2010, True, True)
# print_dataframe(df_year)
# df_cagr = compute_cagr(df_year)
# print_dataframe(df_cagr)


#
# final_df = get_data_for_trailing_days('NESTLEIND', 'NSE', 'monthly', 30, False, False)
# print_dataframe(final_df)
# df_year = get_yearly_gains('%5ENSEI', '', 'monthly', 1, 1, 2010, True, True)
# print_dataframe(df_year)
# df_cagr = compute_cagr(df_year)
# print_dataframe(df_cagr)

# # print_dataframe(get_monthly_gains(final_df))
#
# filt = final_df[YF_DF_COL.PERCENTCHANGE] == min(final_df[YF_DF_COL.PERCENTCHANGE])
# print_dataframe(final_df[filt])

# print(print_dataframe(get_data_from_start_date('LINCOLN', 'NSE', 'monthly', 1, 1, 2010, True, True)))
# get_data_from_start_date('LINCOLN', 'NSE', 'monthly', 1, 1, 2021, True, False)