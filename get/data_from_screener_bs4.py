from bs4 import BeautifulSoup
import requests
from datetime import datetime
import datetime
import time
from tabulate import tabulate
import pandas as pd
import json
import math

from constants import SCREENER_KEYS
# from get import data_from_screener_selenium


def prepare_url(p_ticker):
    return 'https://www.screener.in/company/' + p_ticker + '/consolidated/'


def get_html_from_screener(p_url):
    response = requests.get(p_url).text
    # print(response)
    return response


def parse_data_from_screener(p_ticker, p_response):
    dictionary = {}
    soup = BeautifulSoup(p_response, 'lxml')
    singular_data = soup.find(class_="company-ratios").find_all('li')
    dictionary['CHECK'] = singular_data[0].find(class_="nowrap value").find(class_="number").text.strip()
    if dictionary['CHECK'] == '':
        response = requests.get('https://www.screener.in/company/' + p_ticker).text
        soup = BeautifulSoup(response, 'lxml')
        dictionary = {}
        # print('match')
    singular_data = soup.find(class_="company-ratios").find_all('li')
    single_value_data_keys = [
        SCREENER_KEYS.MARKET_CAP,
        SCREENER_KEYS.PRICE,
        SCREENER_KEYS.HIGH,
        SCREENER_KEYS.PE,
        SCREENER_KEYS.BOOK_VALUE,
        SCREENER_KEYS.DIV_YIELD,
        SCREENER_KEYS.ROCE,
        SCREENER_KEYS.ROE,
        SCREENER_KEYS.FACE_VALUE,
    ]

    # print(singular_data)
    for index, i in enumerate(singular_data):
        # print(i.find(class_="name").text.strip(), end=" = ")
        # print(i.find(class_="nowrap value").find(class_="number").text.strip())
        dictionary[single_value_data_keys[index]] = i.find(class_="nowrap value").find(class_="number").text.strip()
        if index == 2:
            # print(i.find(class_="nowrap value").find_all(class_="number")[1].text.strip())
            dictionary[SCREENER_KEYS.LOW] = i.find(class_="nowrap value").find_all(class_="number")[1].text.strip()

    # print(dictionary)
    # print(dictionary[SCREENER_KEYS.HIGH])
    # print(dictionary[SCREENER_KEYS.LOW])
    # print(dictionary[SCREENER_KEYS.PRICE])
    # ttm_high = float((dictionary[SCREENER_KEYS.HIGH]).replace(',', ''))
    # ttm_low = float((dictionary[SCREENER_KEYS.LOW]).replace(',', ''))
    # price = float((dictionary[SCREENER_KEYS.PRICE]).replace(',', ''))
    #
    # dictionary[SCREENER_KEYS.PERCENT_FROM_52_HIGH] = "{:.2f}".format((ttm_high - price) / ttm_high * 100)
    # dictionary[SCREENER_KEYS.PERCENT_FROM_52_LOW] = "{:.2f}".format((price - ttm_low) / price * 100)

    # responsive-holder fill-card-width
    list_tables = []
    var_tables = soup.find_all(True, {'class': ['responsive-holder', 'fill-card-width']})
    for index, var_table in enumerate(var_tables):
        if var_table['class'][0] == 'responsive-holder' and var_table['class'][1] != 'hidden':
            list_tables.append(var_table)
    # print(var_tables[0]['class'])
    # print(list_tables[0]['class'])
    # print(list_tables[1]['class'])
    # print(list_tables[2]['class'])
    # print(list_tables[3]['class'])
    # print(list_tables[4]['class'])
    # print(list_tables[5]['class'])
    # modifier = 0
    for outer_index, var_table in enumerate(list_tables):
        # if var_table['class'][0] == 'responsive-holder' and var_table['class'][1] == 'fill-card-width':
        # print('outer_index', outer_index)
        heading = var_table.find('thead').find('tr').find_all('th')[1:]
        # print(heading)
        body = var_table.find('tbody').find_all('tr')
        dictionary[SCREENER_KEYS.ARRAY_HEADINGS[outer_index]] = [val.text for val in heading]
        # print([val.text for val in heading])
        # print(len(body))
        for index, row in enumerate(body):
            each_body_row = row.find_all('td')[1:]
            # print(each_body_row)
            # print(outer_index, each_body_row)
            # print('index', len(SCREENER_KEYS.ARRAY_ALL[outer_index]))
            if index < len(SCREENER_KEYS.ARRAY_ALL[outer_index]):
                dictionary[SCREENER_KEYS.ARRAY_ALL[outer_index][index]] = [val.text if val.text else '' for val in each_body_row]
            else:
                # print('promoters', dictionary[SCREENER_KEYS.SP_PROMOTERS])
                # print(dictionary[SCREENER_KEYS.SP_DII])
                # print(dictionary[SCREENER_KEYS.SP_FII])
                # print(dictionary[SCREENER_KEYS.SP_PUBLIC])
                dictionary[SCREENER_KEYS.SP_GOVT] = dictionary[SCREENER_KEYS.SP_PUBLIC]
                dictionary[SCREENER_KEYS.SP_PUBLIC] = [val.text if val.text else '' for val in each_body_row]
            # print([val.text for val in each_body_row])
        # print(body)
        # else:
        #     modifier = -1

        # for element in body:
        #     print(element.text)

    # print(SCREENER_KEYS.ARRAY_HEADINGS)
    # print(SCREENER_KEYS.ARRAY_ALL)
    #
    # print(dictionary[SCREENER_KEYS.AR_SALES])

    return dictionary


def get_data_from_screener_using_bs4(p_ticker):
    url = prepare_url(p_ticker)
    response = get_html_from_screener(url)
    dictionary = parse_data_from_screener(p_ticker, response)
    # print(dictionary)

    keys = [
        SCREENER_KEYS.QR_SALES,
        SCREENER_KEYS.QR_EXPENSES,
        SCREENER_KEYS.QR_OPERATING_PROFIT,
        SCREENER_KEYS.QR_PBT,
        SCREENER_KEYS.QR_NET_PROFIT,
        SCREENER_KEYS.QR_EPS,
        SCREENER_KEYS.AR_SALES,
        SCREENER_KEYS.AR_EXPENSES,
        SCREENER_KEYS.AR_OPERATING_PROFIT,
        SCREENER_KEYS.AR_PBT,
        SCREENER_KEYS.AR_NET_PROFIT,
        SCREENER_KEYS.AR_EPS,
        SCREENER_KEYS.CF_OA
    ]

    sh_keys = [
        SCREENER_KEYS.SP_PROMOTERS,
        SCREENER_KEYS.SP_DII,
        SCREENER_KEYS.SP_FII,
        SCREENER_KEYS.SP_GOVT,
        SCREENER_KEYS.SP_PUBLIC
    ]

    if SCREENER_KEYS.SP_GOVT not in dictionary:
        del sh_keys[3]

    # print(sh_keys)

    for index, sh_key in enumerate(sh_keys):
        # if dictionary[sh_key] is None:
        #     print('yes')
        #     dictionary['Diff ' + sh_key] = ["{:.2f}".format(float(temp_list[index + 1]) - float(val)) for index, val in
        #                                 enumerate(temp_list[:-1])]
        # else:
        #     print('no')
        temp_list = dictionary[sh_key]
        dictionary['Diff ' + sh_key] = ["{:.2f}".format(float(temp_list[index + 1]) - float(val)) for index, val in enumerate(temp_list[:-1])]

    for key in keys:
        temp_list = dictionary[key]
        try:
            # print(temp_list)
            # for val in temp_list[:-1]:
            #     val = float(val.replace(',', ''))
            # dictionary['Rel ' + key] = ["{:.2f}".format(((float(temp_list[index + 1].replace(',', '')) - float(val.replace(',', ''))) / float(val.replace(',', ''))) if float(val.replace(',', '')) > 0 else float(val.replace(',', '')) * -1) for index, val in enumerate(temp_list[:-1])]
            # print(key)
            dictionary['Rel ' + key] = ["{:.2f}".format((float(temp_list[index + 1].replace(',', '')) if temp_list[index + 1] != '' else float(val.replace(',', ''))) / float(val.replace(',', ''))) for index, val in enumerate(temp_list[:-1]) if val != '']
        except ValueError:
            # print(temp_list)
            # print(key)
            # print('value error')
            break
        except ZeroDivisionError:
            print(key)
    # for key in keys:
    #     print(key, dictionary[key])
    #     print('Rel ' + key, dictionary['Rel ' + key])

        # {{(((val | float) - 1) * 100) | int}}

    # list_sales = dictionary[SCREENER_KEYS.QR_SALES]
    # print(list_sales[:-1])
    # dictionary['DIFF_' + SCREENER_KEYS.QR_SALES] = [float(list_sales[index + 1]) / float(list_sale) for index, list_sale in enumerate(list_sales[:-1])]
    # print(dictionary['DIFF_' + SCREENER_KEYS.QR_SALES])
    # print(dictionary)
    return dictionary