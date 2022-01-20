import time

from pymongo import MongoClient

import json

from constants import TICKER_KEYS
from get.data_from_ticker_bs4 import get_data_from_ticker_using_bs4

connection = MongoClient("mongodb://localhost:27017/")
db = connection["trial_stocks"]
collection = db["ticker_data"]


def new_data_exists(p_dictionary, p_result):
    parameters = [TICKER_KEYS.MARKET_CAP,
                  TICKER_KEYS.ENTERPRISE_VALUE,
                  TICKER_KEYS.NUMBER_OF_SHARES,
                  TICKER_KEYS.PE,
                  TICKER_KEYS.PB,
                  TICKER_KEYS.FV,
                  TICKER_KEYS.DIV_YIELD,
                  TICKER_KEYS.BOOK_VALUE,
                  TICKER_KEYS.CASH_NII,
                  TICKER_KEYS.DEBT_CTI,
                  TICKER_KEYS.PROMOTER_HOLDING,
                  TICKER_KEYS.EPS,
                  TICKER_KEYS.SALES_CAR,
                  TICKER_KEYS.ROE,
                  TICKER_KEYS.ROCE,
                  TICKER_KEYS.PROFIT,
                  TICKER_KEYS.PRICE,
                  TICKER_KEYS.WEEK_52_HIGH,
                  TICKER_KEYS.WEEK_52_LOW,
                  TICKER_KEYS.RATING_FINSTAR,
                  TICKER_KEYS.RATING_OWNERSHIP_VALUE,
                  TICKER_KEYS.RATING_OWNERSHIP_STATUS,
                  TICKER_KEYS.RATING_VALUATION_VALUE,
                  TICKER_KEYS.RATING_VALUATION_STATUS,
                  TICKER_KEYS.RATING_EFFICIENCY_VALUE,
                  TICKER_KEYS.RATING_EFFICIENCY_STATUS,
                  TICKER_KEYS.RATING_FINANCIALS_VALUE,
                  TICKER_KEYS.RATING_FINANCIALS_STATUS,
                  TICKER_KEYS.CARD4,
                  TICKER_KEYS.CARD5,
                  TICKER_KEYS.CARD6,
                  TICKER_KEYS.CARD7]
    update_required = False
    dict_update = {}
    for index, parameter in enumerate(parameters):
        # print(parameter, p_dictionary[parameter], p_result[parameter])
        if p_dictionary[parameter] != p_result[parameter]:
            update_required = True
            dict_update[parameter] = p_dictionary[parameter]
        if index == len(parameters) - 1 and update_required:
            # print(dict_update)
            result_update = collection.update_one({"Ticker": p_dictionary[TICKER_KEYS.TICKER]}, {"$set": dict_update})
            if result_update.acknowledged:
                return True
    return False


def update_bundle(p_bundles):
    bundles = [
        'auto',
        'cement',
        'construction',
        'fmcg',
        'it',
        'pharma',
        'portfolio',
        'steel'
    ]
    print(p_bundles)
    if len(p_bundles) == 0:
        print('hrrr')
        p_bundles = bundles
    # print(p_bundles)
    for bundle in p_bundles:
        f = open('../data/data_companies_' + bundle + '.json')
        data = json.load(f)
        companies = data['companies']
        for company in companies:
            print('//////////////////////////////////////////////////////////////////////////////////////////')
            symbol = company['symbol']
            exchange = company['exchange']
            if exchange == 'BSE':
                # print('here')
                symbol = company['ticker_symbol']
            dictionary = get_data_from_ticker_using_bs4(symbol)
            if dictionary is None:
                print('No data found for: ', symbol)
                continue
            symbol = company['symbol']
            if exchange == 'BSE':
                dictionary[TICKER_KEYS.TICKER] = symbol
            result = collection.find_one({"Ticker": dictionary[TICKER_KEYS.TICKER]})
            if result is None:
                result = collection.insert_one(dictionary)
                if result.acknowledged is False:
                    print('Record insertion failed :: ' + dictionary[TICKER_KEYS.TICKER])
                else:
                    print('Record for', symbol, 'not found. New insertion successful.')
            else:
                print('Record for', dictionary[TICKER_KEYS.TICKER], 'already exists.')
                if new_data_exists(dictionary, result):
                    print('New data for', symbol, 'exists and record updated successfully!')

            # print(dictionary)
            time.sleep(1)
        f.close()


def fetch_ticker_data_from_db(p_ticker):
    return collection.find_one({"Ticker": p_ticker})


