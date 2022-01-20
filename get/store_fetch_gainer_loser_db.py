import time

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

from constants import TICKER_KEYS
from get.data_from_ticker_bs4 import get_data_from_ticker_using_bs4, get_html_from_ticker, parse_html_from_ticker

connection = MongoClient("mongodb://localhost:27017/")
db = connection["trial_stocks"]
col_top_gainers = db["col_top_gainers"]
col_top_losers = db["col_top_losers"]

urls = ['https://ticker.finology.in/market/top-gainers', 'https://ticker.finology.in/market/top-losers']
company_url_skeleton = 'https://ticker.finology.in'


def get_gainer_loser_companies():
    companies = [[], []]
    for location, url in enumerate(urls):
        print('/////////////////////////////////////////////', url, '/////////////////////////////////////////////')
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'lxml')

        rows = soup.find(id="mainContent_pnlhighlow").find('tbody').find_all('tr')
        for index, row in enumerate(rows):
            # if index > 20:
            #     continue
            anchor = row.find_all('td')[1].find('a')['href']
            price = float(row.find_all('td')[2].text)
            # print(price)
            # if price > 100:
                # print(anchor)

            dictionary = get_data_from_ticker_using_bs4(anchor)

            if dictionary is None:
                print('dictionary none for', anchor)
            else:
                print('dictionary available for', anchor)
                if dictionary[TICKER_KEYS.RATING_OWNERSHIP_VALUE] > 2 and dictionary[
                    TICKER_KEYS.RATING_VALUATION_VALUE] > 2 and dictionary[TICKER_KEYS.RATING_EFFICIENCY_VALUE] > 2 and \
                        dictionary[TICKER_KEYS.RATING_FINANCIALS_VALUE] > 2:

                    companies[location].append(dictionary)
                    print(dictionary[TICKER_KEYS.NAME],
                          dictionary[TICKER_KEYS.PRICE],
                          dictionary[TICKER_KEYS.RATING_OWNERSHIP_VALUE],
                          dictionary[TICKER_KEYS.RATING_OWNERSHIP_STATUS],
                          dictionary[TICKER_KEYS.RATING_VALUATION_VALUE],
                          dictionary[TICKER_KEYS.RATING_VALUATION_STATUS],
                          dictionary[TICKER_KEYS.RATING_EFFICIENCY_VALUE],
                          dictionary[TICKER_KEYS.RATING_EFFICIENCY_STATUS],
                          dictionary[TICKER_KEYS.RATING_FINANCIALS_VALUE],
                          dictionary[TICKER_KEYS.RATING_FINANCIALS_STATUS])
                    print('////////////////////////////')

            time.sleep(1)
    return companies


def update_gainer_loser_data():
    companies = get_gainer_loser_companies()
    col_top_gainers.drop()
    col_top_losers.drop()
    col_top_gainers.insert_many(companies[0])
    col_top_losers.insert_many(companies[1])


def fetch_gainer_loser_data():
    top_gainers = col_top_gainers.find({})
    top_losers = col_top_losers.find({})
    return top_gainers, top_losers