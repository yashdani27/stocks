import time

from bs4 import BeautifulSoup
import requests
import json

from pymongo import MongoClient

connection = MongoClient("mongodb://localhost:27017/")
db = connection["trial_stocks"]
collection = db["portfolio"]


# def create_empty_data_object():
#     dictionary = {
#         'companies': [
#
#         ]
#     }
#     collection.insert(dictionary)
#
#
# create_empty_data_object()


def get_activity_data():
    ticker = input('Enter ticker symbol: ')
    sector = input('Enter sector: ')
    act_type = input('Enter activity type: "buy" or "sell": ')
    price = input('Enter ' + ('buy' if act_type == 'buy' else 'sell') + ' price: ')
    qty = input('Enter quantity ' + ('bought' if act_type == 'buy' else 'sold') + ' : ')
    dot = input('Enter date of transaction: ')
    reason = input('Enter the reason for buying the stock: ')
    dictionary = {
        'ticker': ticker,
        'sector': sector,
        'avg_price': price,
        'total_price': float(price) * float(qty),
        'total_qty': qty,
        'activity': [
            {
                'type': act_type,
                'price': price,
                'qty': qty,
                'date': dot,
                'reason': reason
            }
        ]
    }
    return dictionary


def add_stock_data(dictionary):
    collection.insert_one(dictionary)


add_stock_data(get_activity_data())


def compute_price_qty(record, dictionary):
    total_price = 0
    total_qty = 0
    activities = record['activity']
    activities.append(dictionary)
    for activity in activities:
        if activity['type'] == 'buy':
            total_price += float(activity['price']) * float(activity['qty'])
            total_qty += float(activity['qty'])
        else:
            total_price -= float(activity['price']) * float(activity['qty'])
            total_qty -= float(activity['qty'])
    avg_price = total_price / total_qty
    return avg_price, total_price, total_qty


def update_stock_data(ticker):
    db_object = collection.find_one({'ticker': ticker})
    # print(db_object)
    act_type = input('Enter activity type: "buy" or "sell": ')
    price = input('Enter ' + ('buy' if act_type == 'buy' else 'sell') + ' price: ')
    qty = input('Enter quantity ' + ('bought' if act_type == 'buy' else ' sold') + ': ')
    dot = input('Enter date of transaction: ')
    reason = input('Enter the reason for buying the stock: ')
    dictionary = {
        'type': act_type,
        'price': price,
        'qty': qty,
        'dot': dot,
        'reason': reason
    }
    avg_price, total_price, total_qty = compute_price_qty(db_object, dictionary)
    # db_object['activity'].append(dictionary)
    # activities = db_object['activity']
    # activities.append(dictionary)
    # print(db_object)
    response = collection.update_one(
        {'ticker': ticker},
        {"$push": {'activity': dictionary},
        "$set": {'avg_price': avg_price, 'total_price': total_price, 'total_qty': total_qty}},
        upsert=True)
    print(response.acknowledged)
    print(response.raw_result)


update_stock_data('GPIL')


def get_data_from_portfolio():
    companies = collection.find({})
    # print(companies[0])
    portfolio = []
    for company in companies:
        avg_price = 0
        total_price = 0
        total_qty = 0
        activities = company['activity']
        for activity in activities:
            if activity['type'] == 'buy':
                total_price += float(activity['price']) * float(activity['qty'])
                total_qty += float(activity['qty'])
            else:
                total_price -= float(activity['price']) * float(activity['qty'])
                total_qty -= float(activity['qty'])
        avg_price = total_price / total_qty
        print(avg_price, total_price, total_qty)
        dictionary = {
            'Company': company['ticker'],
            'Sector': company['sector'],
            'Average Price': avg_price,
            'Total Price': total_price,
            'Total Qty': total_qty,
            'Activities': company['activity']
        }
        portfolio.append(dictionary)
    print(portfolio)



get_data_from_portfolio()