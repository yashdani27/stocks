from bs4 import BeautifulSoup
import requests
from datetime import datetime
import datetime
import time
from tabulate import tabulate
import pandas as pd
import json
import math

PATH_ROOT_DIR = '/Users/dharmendradani/PycharmProjects/BeautifulSoupTrial/decisions/'
ticker = 'LINCOLN.NS'

EXCHANGES = {
    'NS': 'NSE',
    'BO': 'BSE'
}

print(EXCHANGES['NS'])

intervals = ['1d', '1wk']
interval_text = ['days', 'weeks']
interval_decision = ['Trading', 'Investment']
interval_days = [60, 180]

AVERAGING_FACTOR = 5
list_avg_factor = [3, 5, 7, 9, 11]

UPTREND = 'Uptrend'
DOWNTREND = 'Downtrend'
SIDEWAYS = 'Sideways'

df = pd.DataFrame()


def get_date(number_of_days):
    tomorrows_date = (str(datetime.date.today() + datetime.timedelta(days=number_of_days))).split('-')
    temp_year = int(tomorrows_date[0])
    temp_month = int(tomorrows_date[1])
    temp_day = int(tomorrows_date[2])
    # print(temp_year, temp_month, temp_day)
    return int(time.mktime(datetime.datetime(temp_year, temp_month, temp_day, 23, 59).timetuple()))


# print(get_date(-60))


def get_start_date(p_date, p_month, p_year):
    return int(time.mktime(datetime.datetime(p_year, p_month, p_date, 23, 59).timetuple()))


def prepare_url(p_name, p_interval, p_interval_days):
    period2 = get_date(1)
    if p_interval == '1d':
        period1 = get_date(-p_interval_days)
        return f'https://query1.finance.yahoo.com/v7/finance/download/{p_name}?period1={period1}&period2={period2}&interval={p_interval}&events=history&includeAdjustedClose=true'
    elif p_interval == '1wk':
        period1 = get_date(-p_interval_days)
        return f'https://query1.finance.yahoo.com/v7/finance/download/{p_name}?period1={period1}&period2={period2}&interval={p_interval}&events=history&includeAdjustedClose=true'

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

    print(p_response)

    array_data = p_response.split('\n')
    # print('array_data', array_data)

    for i in range(1, len(array_data)):
        if array_data[i].split(',')[1] != 'null':
            list_date.append(array_data[i].split(',')[0])
            list_open.append(float(array_data[i].split(',')[1]))
            list_high.append(float(array_data[i].split(',')[2]))
            list_low.append(float(array_data[i].split(',')[3]))
            list_close.append(float(array_data[i].split(',')[4]))
            list_adj_close.append(float(array_data[i].split(',')[5]))
            list_volume.append(float(array_data[i].split(',')[6]))

    temp_df = pd.DataFrame(
        list(zip(list_date, list_open, list_high, list_low, list_close, list_adj_close, list_volume)))
    columns = array_data[0].split(',')
    print(columns)
    temp_df.columns = columns

    return temp_df


def smooth_out(location, v_list, number):
    # print(type(location), type(v_list), type(v_list[0]), type(number))
    answer = 0
    for i in range(int(-number / 2), int(number / 2) + 1):
        if (location + i) < 0 or (location + i) >= len(v_list):
            answer = v_list[location] * number
            break
        answer += float(v_list[location + i])
    return answer / number


# print(smooth_out(2, [1, 2, 3, 5, 5], 5))


def prepare_trend(p_df, p_avg_factor):
    list_date = []
    for row in p_df['Date']:
        list_date.append(row)
    list_close = []
    for row in p_df['Close']:
        list_close.append(row)

    list_avg = []
    list_avg_diff = [0]

    for index, row in enumerate(list_close):
        # print(index, row)
        list_avg.append(math.ceil(smooth_out(index, list_close, p_avg_factor)))
        if index != 0:
            list_avg_diff.append(list_avg[index] - list_avg[index - 1])

    # print(list_avg)
    # print(list_avg_diff)

    df_avg = pd.DataFrame(list(zip(list_date, list_close, list_avg, list_avg_diff)))
    df_avg.columns = ['Date', 'Close', 'Avg', 'Avg Diff']
    print(tabulate(df_avg, headers="keys", tablefmt="psql"))

    cumulative = 0

    list_trend_date = []
    list_trend_sessions = []
    list_trend_switch = []
    list_trend_type = []
    list_trend_value = []
    list_trend_percent = []
    list_trend_close = []
    count_sessions = 0

    # value_during_switch = list_avg_5[0]
    value_during_switch = list_avg[1]
    value_closing_price = list_close[1]

    for index, row in enumerate(list_avg_diff):
        if index == 0:
            continue

        if row >= 0:
            if cumulative < 0:
                print('Value during switch: ', value_during_switch)
                # if math.fabs(cumulative) >= percent_of_closing_price(list_close[index - 1], 5):
                if math.fabs(math.floor((cumulative / value_during_switch) * 100)) >= 5:
                    print(list_close[index - 1])
                    print(str(index - 1) + ' :: ' + list_date[index - 1] + ' :: Downtrend ends')
                    list_trend_type.append(DOWNTREND)
                else:
                    print(str(index - 1) + ' :: ' + list_date[index - 1] + ' :: Sideways trend')
                    list_trend_type.append(SIDEWAYS)
                list_trend_date.append(list_date[index - 1])
                list_trend_sessions.append(count_sessions)
                list_trend_switch.append(value_during_switch)
                list_trend_value.append(cumulative)
                list_trend_close.append(value_closing_price)
                # list_trend_value.append(list_avg[index] - value_during_switch)
                list_trend_percent.append((cumulative / value_during_switch) * 100)
                # list_trend_percent.append(((list_avg[index] - value_during_switch) / value_during_switch) * 100)
                print('Stock down by: ' + str((cumulative / value_during_switch) * 100))
                count_sessions = 0
                cumulative = 0
                # print()
                value_during_switch = list_avg[index]
                value_closing_price = list_close[index]
            count_sessions += 1
            cumulative += row
        else:
            if cumulative > 0:
                print('Value during switch', value_during_switch)
                # if cumulative >= percent_of_closing_price(list_close[index], 5):
                if math.ceil((cumulative / value_during_switch) * 100) >= 5:
                    print('Stock up by:' + str(((list_avg[index - 1] - value_during_switch) / value_during_switch) * 100))
                    print(str(index - 1) + ' :: ' + list_date[index - 1] + ' :: Uptrend ends')
                    list_trend_type.append(UPTREND)
                else:
                    print(str(index - 1) + ' :: ' + list_date[index - 1] + ' :: Sideways trend')
                    list_trend_type.append(SIDEWAYS)
                list_trend_date.append(list_date[index - 1])
                list_trend_sessions.append(count_sessions)
                list_trend_switch.append(value_during_switch)
                list_trend_value.append(cumulative)
                list_trend_close.append(value_closing_price)
                # list_trend_value.append(list_avg[index] - value_during_switch)
                list_trend_percent.append((cumulative / value_during_switch) * 100)
                # list_trend_percent.append(((list_avg[index] - value_during_switch) / value_during_switch) * 100)
                print('Stock up by: ' + str((cumulative / value_during_switch) * 100))
                print()
                count_sessions = 0
                cumulative = 0
                value_during_switch = list_avg[index]
                value_closing_price = list_close[index]
            count_sessions += 1
            cumulative += row
        print(cumulative)

        if index == len(list_avg_diff) - 1:
            print('last index')

            if cumulative < 0:
                print('Value during switch: ', value_during_switch)
                # if math.fabs(cumulative) >= percent_of_closing_price(list_close[index - 1], 5):
                if math.fabs(math.floor((cumulative / value_during_switch) * 100)) >= 5:
                    # print(list_close[index - 1])
                    print(str(index - 1) + ' :: ' + list_date[index - 1] + ' :: Downtrend ends')
                    list_trend_type.append(DOWNTREND)
                else:
                    print(str(index - 1) + ' :: ' + list_date[index - 1] + ' :: Sideways trend')
                    list_trend_type.append(SIDEWAYS)
                list_trend_date.append(list_date[index - 1])
                list_trend_sessions.append(count_sessions)
                list_trend_switch.append(value_during_switch)
                list_trend_value.append(cumulative)
                list_trend_close.append(value_closing_price)
                # list_trend_value.append(list_avg[index] - value_during_switch)
                list_trend_percent.append((cumulative / value_during_switch) * 100)
                # list_trend_percent.append(((list_avg[index] - value_during_switch) / value_during_switch) * 100)
                print('Stock down by: ' + str((cumulative / value_during_switch) * 100))
                # print('Stock down by: ' + str(((list_avg[index] - value_during_switch) / value_during_switch) * 100))
                count_sessions = 0
                cumulative = 0
                print()
                value_during_switch = list_avg[index]
                value_closing_price = list_close[index]
            else:
                print('Value during switch', value_during_switch)
                # if cumulative >= percent_of_closing_price(list_close[index], 5):
                if math.ceil((cumulative / value_during_switch) * 100) >= 5:
                    print('Stock up by:' + str(((list_avg[index - 1] - value_during_switch) / value_during_switch) * 100))
                    print(str(index - 1) + ' :: ' + list_date[index - 1] + ' :: Uptrend ends')
                    list_trend_type.append(UPTREND)
                else:
                    print(str(index - 1) + ' :: ' + list_date[index - 1] + ' :: Sideways trend')
                    list_trend_type.append(SIDEWAYS)
                list_trend_date.append(list_date[index - 1])
                list_trend_sessions.append(count_sessions)
                list_trend_switch.append(value_during_switch)
                list_trend_value.append(cumulative)
                list_trend_close.append(value_closing_price)
                # list_trend_value.append(list_avg[index] - value_during_switch)
                list_trend_percent.append((cumulative / value_during_switch) * 100)
                # list_trend_percent.append(((list_avg[index] - value_during_switch) / value_during_switch) * 100)
                print('Stock up by: ' + str((cumulative / value_during_switch) * 100))
                print()
                count_sessions = 0
                cumulative = 0
                value_during_switch = list_avg[index]
                value_closing_price = list_close[index]
        # print(cumulative)

    # print(trend)

    df_trend = pd.DataFrame(
        list(zip(list_trend_date, list_trend_sessions, list_trend_type, list_trend_switch, list_trend_close, list_trend_percent)))
    df_trend.columns = ['Date', 'Sessions', 'Type', 'Switch at', 'Closing Price', 'Percent Gain/Loss']

    print(tabulate(df_trend, headers="keys", tablefmt="psql"))

    list_trend_consolidated = []

    for index, row in enumerate(list_trend_type):
        if index == 0:
            list_trend_consolidated.append({
                'date': list_date[0] + ' - ' + list_trend_date[index],
                'sessions': list_trend_sessions[index],
                'type': list_trend_type[index],
                'switch': str(list_trend_switch[index]) + ' - ' + (str(list_trend_switch[index])),
                'value': list_trend_value[index],
                'percent': list_trend_percent[index],
                'close': str(list_trend_close[index]) + ' - ' + (str(list_trend_close[index]))
            })
            print(list_trend_consolidated)
            continue
        if row == SIDEWAYS and len(list_trend_consolidated) > 0 and list_trend_consolidated[-1]['type'] == SIDEWAYS:
            # list_trend_consolidated[-1]['date'] = list_trend_date[index]
            list_trend_consolidated[-1]['sessions'] += list_trend_sessions[index]
            list_trend_consolidated[-1]['value'] += list_trend_value[index]
            list_trend_consolidated[-1]['percent'] += list_trend_percent[index]
        else:
            if len(list_trend_consolidated) > 0 and list_trend_consolidated[-1]['type'] == SIDEWAYS:
                temp_date = list_trend_consolidated[-1]['date']
                temp_switch = list_trend_consolidated[-1]['switch']
                temp_close = list_trend_consolidated[-1]['close']
                # print(temp_date.split(' - '))
                list_trend_consolidated[-1]['date'] = temp_date.split(' - ')[0] + ' - ' + list_trend_date[index - 1]
                list_trend_consolidated[-1]['switch'] = temp_switch.split(' - ')[0] + ' - ' + str(list_trend_switch[index - 1])
                list_trend_consolidated[-1]['close'] = temp_close.split(' - ')[0] + ' - ' + str(list_trend_close[index - 1])
            list_trend_consolidated.append({
                'date': list_trend_date[index - 1] + ' - ' + list_trend_date[index],
                'sessions': list_trend_sessions[index],
                'type': list_trend_type[index],
                'switch': str(list_trend_switch[index]) + ' - ' + (str(list_trend_switch[index + 1]) if index + 1 < len(list_trend_type) else 'Present Value'),
                'close': str(list_trend_close[index]) + ' - ' + (str(list_trend_close[index + 1]) if index + 1 < len(list_trend_type) else 'Present Value'),
                'value': list_trend_value[index],
                'percent': list_trend_percent[index]
            })

    for list_trend in list_trend_consolidated:
        print(list_trend)

    print('/////////////////////////////////////end/////////////////////////////////////')

    return list_trend_consolidated


def get_decisions_for(ticker, position, days, interval):
    company_name_w_exchange = ticker
    company_name = company_name_w_exchange.split('.')[0]
    stock_index = company_name_w_exchange.split('.')[1]
    print('Trend for ' + company_name + ' at ' + EXCHANGES[stock_index] + ': ')

    url = prepare_url(company_name_w_exchange, interval, days)
    # print('Over the last ' + str(interval_days[index]) + ' days.')
    # print(url)
    response = get_data_from_yahoo_finance(url)
    print(response)

    df_final = prepare_dataframe(response)
    # print(tabulate(df, headers="keys", tablefmt="psql"))

    list_date_3 = []
    list_date_5 = []
    list_date_7 = []
    list_date_9 = []
    list_date_11 = []
    list_trend_3 = []
    list_trend_5 = []
    list_trend_7 = []
    list_trend_9 = []
    list_trend_11 = []

    list_dates_avg = [[], [], [], [], []]
    list_trend_avg = [[], [], [], [], []]

    for pos, avg in enumerate(list_avg_factor):
        print('/////////////////////////////////////Avg Factor = ' + str(avg) + '//////////////////////////////////////')
        list_trend_response = prepare_trend(df_final, avg)

        # print(list_trend_response)

        list_date = []
        list_sessions = []
        list_type = []
        list_switch = []
        list_closing = []
        list_value = []
        list_percent = []
        for list_temp in list_trend_response:
            list_date.append(list_temp['date'])
            list_sessions.append(list_temp['sessions'])
            list_type.append(list_temp['type'])
            list_switch.append(list_temp['switch'])
            list_closing.append(list_temp['close'])
            list_value.append(list_temp['value'])
            list_percent.append(list_temp['percent'])

        print(position + ' investment decision (calculated over the last ' + str(days) + ' days)')

        df_trend_response = pd.DataFrame(list(zip(list_date, list_sessions, list_type, list_switch, list_closing, list_value, list_percent)))
        df_trend_response.columns = ['Date', 'Sessions', 'Trend Type', 'Switch at', 'Close', 'Gain / Loss', 'Percent Gain / Loss']
        print(tabulate(df_trend_response, headers="keys", tablefmt="psql"))

        list_dates_avg[pos].append(list_date)
        list_trend_avg[pos].append(list_type)
        print('Pos: ' + str(pos))

    # plot_data = ''
    # if len(list_trend_response) > 1:
    #     for list_temp in list_trend_response[-2:]:
    #         plot_data += list_temp['date'] + ' :: ' + str(list_temp['sessions']) + ' ' + interval_text[index] + ' :: ' + str('{:.2f}'.format(list_temp['percent'])) + ' :: ' + list_temp['type'] + '\n'
    # else:
    #     for list_temp in list_trend_response:
    #         plot_data += list_temp['date'] + ' :: ' + str(list_temp['sessions']) + ' ' + interval_text[index] + ' :: ' + str('{:.2f}'.format(list_temp['percent'])) + ' :: ' + list_temp['type'] + '\n'
    #
    # print(plot_data)

    print(len(list_dates_avg[0]), len(list_trend_avg[0]))
    print(list_trend_avg[0])
    print(list_trend_avg[1])
    print(list_trend_avg[2])
    print(list_trend_avg[3])

    # df_trend_compare = pd.DataFrame(list(zip(list_dates_avg[0][0], list_trend_avg[0][0])))
    # df_trend_compare.columns = ['Date', 'Trend']
    # print(tabulate(df_trend_compare, headers="keys", tablefmt="psql"))
    #
    df_trend_compare = pd.DataFrame(list(zip(list_dates_avg[0][0], list_trend_avg[0][0], list_dates_avg[1][0], list_trend_avg[1][0], list_dates_avg[2][0], list_trend_avg[2][0], list_dates_avg[3][0], list_trend_avg[3][0], list_dates_avg[4][0], list_trend_avg[4][0])))
    print(tabulate(df_trend_compare, headers="keys", tablefmt="psql"))
    # df_trend_compare.to_csv(r'/Users/dharmendradani/PycharmProjects/' + ticker + '_avg' + '.csv')

    # print(df_trend_compare)


print()


get_decisions_for(ticker, 'short', 500, '1d')
