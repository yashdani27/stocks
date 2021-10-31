import math
from tabulate import tabulate
from get import historical_data_from_yf
import pandas as pd

AVERAGING_FACTOR = 5
list_avg_factor = [3, 5, 7, 9, 11]

UPTREND = 'Uptrend'
DOWNTREND = 'Downtrend'
SIDEWAYS = 'Sideways'


def print_dataframe(p_dataframe):
    print(tabulate(p_dataframe, headers="keys", tablefmt="psql"))


def smooth_out(location, v_list, number):
    # print(type(location), type(v_list), type(v_list[0]), type(number))
    answer = 0
    for i in range(int(-number / 2), int(number / 2) + 1):
        if (location + i) < 0 or (location + i) >= len(v_list):
            answer = v_list[location] * number
            break
        answer += float(v_list[location + i])
    return answer / number


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


hist_df = historical_data_from_yf.get_data_from_start_date('TCS', 'NSE', 'daily', 1, 1, 2020, True, True)
print_dataframe(hist_df)
list_trend_response = prepare_trend(hist_df, 5)

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

# print(position + ' investment decision (calculated over the last ' + str(days) + ' days)')

df_trend_response = pd.DataFrame(list(zip(list_date, list_sessions, list_type, list_switch, list_closing, list_value, list_percent)))
df_trend_response.columns = ['Date', 'Sessions', 'Trend Type', 'Switch at', 'Close', 'Gain / Loss', 'Percent Gain / Loss']
print(tabulate(df_trend_response, headers="keys", tablefmt="psql"))