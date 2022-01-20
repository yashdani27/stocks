import json
import time
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, url_for, request
from tabulate import tabulate

from algorithms.algorithm_trend_yf import get_trend
from constants import TICKER_KEYS, SCREENER_KEYS
from buy_opportunity import get_buy_opportunities
from get import historical_data_from_yf
from get.data_from_ticker_bs4 import get_data_from_ticker_using_bs4
from get.data_from_screener_bs4 import get_data_from_screener_using_bs4
from get.historical_data_from_yf import get_data_from_start_date
# from get.store_fetch_gainer_loser_db import fetch_gainer_loser_data
# from get.store_fetch_ticker_data_db import fetch_ticker_data_from_db

# from gainer_loser import get_gainer_loser_companies

from login import LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '4345f06299b08d2300afb29a3f55129d'

Screener_Keys = [
    'Market Cap',
    'P/E',
    'Book Value',
    'Price (LTP)',
    '52 Week High',
    '52 Week Low',
    'Div. Yield',
    'ROCE',
    'ROE'
]


def print_dataframe(p_dataframe):
    print(tabulate(p_dataframe, headers="keys", tablefmt="psql"))


@app.route("/<ticker>")
def company(ticker):
    start_time = time.time()
    ticker = ticker
    time_ticker = time.time()
    # dictionary_ticker = fetch_ticker_data_from_db(ticker)
    dictionary_ticker = None
    if dictionary_ticker is None:
        dictionary_ticker = get_data_from_ticker_using_bs4(ticker)
    print("--- %s ticker seconds ---" % (time.time() - time_ticker))
    time_screener = time.time()
    dictionary_screener = get_data_from_screener_using_bs4(ticker)
    print("--- %s screener seconds ---" % (time.time() - time_screener))

    key_ratios = [
        {
            'key': 'MCap',
            'value': dictionary_ticker[TICKER_KEYS.MARKET_CAP],
            'class': 'text-green' if dictionary_ticker[TICKER_KEYS.MARKET_CAP] > dictionary_ticker[
                TICKER_KEYS.ENTERPRISE_VALUE] else 'text-red'
        },
        {
            'key': 'EV',
            'value': dictionary_ticker[TICKER_KEYS.ENTERPRISE_VALUE],
            'class': 'text-green' if dictionary_ticker[TICKER_KEYS.MARKET_CAP] > dictionary_ticker[
                TICKER_KEYS.ENTERPRISE_VALUE] else 'text-red'

        },
        {
            'key': 'P/E',
            'value': dictionary_ticker[TICKER_KEYS.PE],
            'class': 'text-green' if dictionary_ticker[TICKER_KEYS.PE] < 20 else 'text-red'
        },
        {
            'key': 'P/B',
            'value': dictionary_ticker[TICKER_KEYS.PB],
            'class': 'text-green' if dictionary_ticker[TICKER_KEYS.PB] < 2 else 'text-red'
        },
        {
            'key': 'ROE',
            'value': dictionary_ticker[TICKER_KEYS.ROE],
            'class': 'text-green' if dictionary_ticker[TICKER_KEYS.ROE] > 20 else 'text-red'
        },
        {
            'key': 'ROCE',
            'value': dictionary_ticker[TICKER_KEYS.ROCE],
            'class': 'text-green' if dictionary_ticker[TICKER_KEYS.ROCE] > 20 else 'text-red'
        },
        {
            'key': 'Profit',
            'value': dictionary_ticker[TICKER_KEYS.PROFIT],
            'class': 'text-green' if dictionary_ticker[TICKER_KEYS.PROFIT] > 10 else 'text-red'
        },
        {
            'key': 'Sales',
            'value': dictionary_ticker[TICKER_KEYS.SALES_CAR],
            'class': 'text-green' if dictionary_ticker[TICKER_KEYS.SALES_CAR] > 10 else 'text-red'
        },
        {
            'key': 'D/E',
            'value': dictionary_ticker[TICKER_KEYS.CARD4],
            'class': 'text-green' if dictionary_ticker[TICKER_KEYS.CARD4] < '1' else 'text-red'
        },
        {
            'key': 'CFO/PAT',
            'value': dictionary_ticker[TICKER_KEYS.CARD7],
            'class': 'text-green' if dictionary_ticker[TICKER_KEYS.CARD7] > '1' else 'text-red'
        },
        {
            'key': 'P/CF',
            'value': dictionary_ticker[TICKER_KEYS.CARD5],
            'class': 'text-green' if dictionary_ticker[TICKER_KEYS.CARD5] < '20' else 'text-red'
        },
        {
            'key': 'ICR',
            'value': dictionary_ticker[TICKER_KEYS.CARD6],
            'class': 'text-green' if dictionary_ticker[TICKER_KEYS.CARD6] > '002' else 'text-red'
        }
    ]

    keys_qr = [
        SCREENER_KEYS.QR_SALES,
        SCREENER_KEYS.QR_EXPENSES,
        SCREENER_KEYS.QR_OPERATING_PROFIT,
        SCREENER_KEYS.QR_PBT,
        SCREENER_KEYS.QR_NET_PROFIT,
        SCREENER_KEYS.QR_EPS
    ]

    keys_ar = [
        SCREENER_KEYS.AR_SALES,
        SCREENER_KEYS.AR_EXPENSES,
        SCREENER_KEYS.AR_OPERATING_PROFIT,
        SCREENER_KEYS.AR_PBT,
        SCREENER_KEYS.AR_NET_PROFIT,
        SCREENER_KEYS.AR_EPS
    ]

    keys_cf = [
        SCREENER_KEYS.CF_OA
    ]

    keys_sh = [
        SCREENER_KEYS.SP_PROMOTERS,
        SCREENER_KEYS.SP_DII,
        SCREENER_KEYS.SP_FII,
        SCREENER_KEYS.SP_PUBLIC
    ]

    if SCREENER_KEYS.SP_GOVT in dictionary_screener:
        keys_sh[3] = SCREENER_KEYS.SP_GOVT
        keys_sh.append(SCREENER_KEYS.SP_PUBLIC)

    dictionary_tables = [
        {
            'Heading Center': 'Quarterly Results',
            'Heading Left': 'Quarters',
            'Heading': dictionary_screener['QR Quarters'],
            'keys': keys_qr,
            'prefix': 'Rel ',
            'comp_value': '1'
        },
        {
            'Heading Center': 'Annual P&L Results',
            'Heading Left': 'Years',
            'Heading': dictionary_screener['Years'],
            'keys': keys_ar,
            'prefix': 'Rel ',
            'comp_value': '1'
        },
        {
            'Heading Center': 'Cash Flow',
            'Heading Left': 'Years',
            'Heading': dictionary_screener['Years'],
            'keys': keys_cf,
            'prefix': 'Rel ',
            'comp_value': '1'
        },
        {
            'Heading Center': 'Shareholding Pattern',
            'Heading Left': 'Quarters',
            'Heading': dictionary_screener['SH Quarters'],
            'keys': keys_sh,
            'prefix': 'Diff ',
            'comp_value': '0.00'
        }
    ]

    time_company_gains = time.time()
    df_yearly_gains_company = historical_data_from_yf.get_yearly_gains(ticker, 'NSE', 'monthly', 1, 1, 2010, True, True)
    df_cagr_company = historical_data_from_yf.compute_cagr(df_yearly_gains_company)
    print("--- %s company gains seconds ---" % (time.time() - time_company_gains))
    # print_dataframe(df_cagr_company)
    print('df_cagr_company', df_cagr_company['Date'][0])
    time_index_gains = time.time()
    df_yearly_gains_index = historical_data_from_yf.get_yearly_gains('%5ENSEI', '', 'monthly', 1, 1,
                                                                     int(df_cagr_company['Date'][0]), True, True)
    df_cagr_index = historical_data_from_yf.compute_cagr(df_yearly_gains_index)
    print("--- %s index gain seconds ---" % (time.time() - time_index_gains))
    print(dictionary_ticker[TICKER_KEYS.BOOK_VALUE] if dictionary_ticker is not None else 'No Data',
          dictionary_screener[SCREENER_KEYS.BOOK_VALUE])

    time_trend = time.time()
    df_trend, dict_data_points, hist_df = get_trend(ticker, 'NSE', 'weekly',
                                                    int(str(datetime.now()).split(' ')[0].split('-')[2]),
                                                    int(str(datetime.now()).split(' ')[0].split('-')[1]),
                                                    int(str(datetime.now()).split(' ')[0].split('-')[0]) - 1)
    print("--- %s trend seconds ---" % (time.time() - time_trend))

    graph_x = hist_df['Date'].tolist()
    graph_y = hist_df['Close'].tolist()
    print(graph_x, graph_y)
    graph_y_sorted = sorted(graph_y)

    # print_dataframe(hist_df)

    # df_trend, dict_data_points = get_trend(ticker, 'NSE', 'weekly',
    #                                        1,
    #                                        5,
    #                                        2020)

    print(dict_data_points)

    qr_heading = dictionary_screener[SCREENER_KEYS.QR_HEADING]
    qr_sales = dictionary_screener[SCREENER_KEYS.QR_SALES]
    qr_expenses = dictionary_screener[SCREENER_KEYS.QR_EXPENSES]
    qr_profit = dictionary_screener[SCREENER_KEYS.QR_NET_PROFIT]

    val_qr_sales = [float(qr_sales[-5].replace(',', '')), float(qr_sales[-1].replace(',', '')), float(qr_sales[-2].replace(',', ''))]
    rel_qr_sales = ["{:.2f}".format(val_qr_sales[1] / val_qr_sales[0]), dictionary_screener['Rel ' + SCREENER_KEYS.QR_SALES][-1]]
    # print('here', val_qr_sales)
    # print('here', rel_qr_sales)

    val_qr_expenses = [float(qr_expenses[-5].replace(',', '')), float(qr_expenses[-1].replace(',', '')),
                    float(qr_expenses[-2].replace(',', ''))]
    rel_qr_expenses = ["{:.2f}".format(val_qr_expenses[1] / val_qr_expenses[0]),
                    dictionary_screener['Rel ' + SCREENER_KEYS.QR_EXPENSES][-1]]
    # print('here', val_qr_sales)
    # print('here', rel_qr_sales)

    val_qr_profit = [float(qr_profit[-5].replace(',', '')), float(qr_profit[-1].replace(',', '')),
                    float(qr_profit[-2].replace(',', ''))]
    rel_qr_profit = ["{:.2f}".format(val_qr_profit[1] / val_qr_profit[0]),
                    dictionary_screener['Rel ' + SCREENER_KEYS.QR_NET_PROFIT][-1]]
    # print('here', val_qr_sales)
    # print('here', rel_qr_sales)

    quarterly_data = {
        'keys': ['quarter_heading', 'quarter_sales', 'quarter_expenses', 'quarter_profit'],
        'quarter_heading': [qr_heading[-5], qr_heading[-1], qr_heading[-2]],
        'rel_quarter_heading': ['', ''],
        'quarter_sales': [qr_sales[-5], qr_sales[-1], qr_sales[-2]],
        'rel_quarter_sales': rel_qr_sales,
        'quarter_expenses': [qr_expenses[-5], qr_expenses[-1], qr_expenses[-2]],
        'rel_quarter_expenses': rel_qr_expenses,
        'quarter_profit': [qr_profit[-5], qr_profit[-1], qr_profit[-2]],
        'rel_quarter_profit': rel_qr_profit,

    }

    print("--- %s total seconds ---" % (time.time() - start_time))

    return render_template("layout_data.html",
                           dictionary_ticker=dictionary_ticker,
                           Screener_Keys=Screener_Keys,
                           dictionary_screener=dictionary_screener,
                           key_ratios=key_ratios,
                           quarterly_data=quarterly_data,
                           keys_qr=keys_qr,
                           keys_ar=keys_ar,
                           keys_cf=keys_cf,
                           keys_sh=keys_sh,
                           df_cagr_company=df_cagr_company,
                           df_cagr_index=df_cagr_index,
                           dictionary_tables=dictionary_tables,
                           dict_data_points=dict_data_points,
                           graph_x=graph_x,
                           graph_y=graph_y,
                           graph_y_sorted=graph_y_sorted)

    # return str(dictionary_ticker[TICKER_KEYS.ROE]) + ' ' + str(dictionary_screener[SCREENER_KEYS.ROE])


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    options = [
        {
            "option": "Bundles",
            "desc": "View different stock bundles based on sectors, indices and portfolio.",
            "endpoint": "bundle"
        },
        {
            "option": "Gainers / Losers",
            "desc": "View the top gainers and losers of the previous trading session.",
            "endpoint": "gainer-loser"
        },
        {
            "option": "Buy Opportunities",
            "desc": "Check out potential buy opportunities based on quarterly results and current price trend.",
            "endpoint": "buy-op"
        },
        {
            "option": "Compare CAGR",
            "desc": "Compare CAGR for same sector companies.",
            "endpoint": "comp-cagr"
        }
    ]
    form = LoginForm()
    if form.is_submitted():
        print('////////////////////////////////////////submitted////////////////////////////////////////')
        print(form.company.data)
        return redirect(url_for('company', ticker=form.company.data))
    else:
        return render_template("home.html", form=form, options=options)


@app.route("/bundle")
def show_bundles():
    list_bundles = [
        "auto",
        "cement",
        "construction",
        "fmcg",
        "it",
        "pharma",
        "portfolio",
        "steel",
        "sensex",
        "nifty"
    ]
    components = []
    for bundle in list_bundles:
        f = open('../data/data_companies_' + bundle + '.json')
        components.append(json.load(f)['companies'])
    print(components)
    return render_template("list_of_bundles.html", bundles=list_bundles, components=components)


@app.route("/gainer-loser")
def gainer_loser():
    print('gainer-loser')
    companies = []
    # gainers, losers = fetch_gainer_loser_data()
    # types = [gainers, losers]
    # headings = ['Top Gainers', 'Top Losers']
    # # companies = get_gainer_loser_companies()
    # return render_template("gainer-loser.html", headings=headings, types=types)


@app.route("/comp-cagr", methods=['GET', 'POST'])
def comp_cagr():
    selected_index = None
    companies = []
    df_cagr = pd.DataFrame()
    list_bundles = [
        "auto",
        "cement",
        "construction",
        "fmcg",
        "it",
        "pharma",
        "portfolio",
        "steel"
    ]
    df_yearly_gains_index = historical_data_from_yf.get_yearly_gains('%5ENSEI', '', 'monthly', 1, 1,
                                                                     2010, True, True)
    df_cagr_index = historical_data_from_yf.compute_cagr(df_yearly_gains_index)
    if request.method == 'POST':
        print(request.form['action'])
        sector = request.form['action']
        if sector == 'auto':
            selected_index = 1
        elif sector == 'cement':
            selected_index = 2
        elif sector == 'construction':
            selected_index = 3
        elif sector == 'fmcg':
            selected_index = 4
        elif sector == 'it':
            selected_index = 5
        elif sector == 'pharma':
            selected_index = 6
        elif sector == 'portfolio':
            selected_index = 7
        elif sector == 'steel':
            selected_index = 8
        bundle = request.form['action']
        f = open('../data/data_companies_' + bundle + '.json')
        bundle = bundle[0:-1]
        print(bundle)
        data = json.load(f)
        # print(data['companies'])
        companies = data['companies']
        company_cagr = []
        df_cagr = pd.DataFrame()
        df_cagr['Year'] = df_cagr_index['Date']
        df_cagr['Index'] = df_cagr_index['CAGR (after COVID)']
        total_rows = int(df_cagr_index['Date'][df_cagr_index.shape[0] - 1]) - 2010 + 1
        for comp in companies:
            print(comp['symbol'])
            df_yearly_gains_company = historical_data_from_yf.get_yearly_gains(comp['symbol'], 'NSE', 'monthly', 1, 1, 2010,
                                                                               True, True)
            df_cagr_company = historical_data_from_yf.compute_cagr(df_yearly_gains_company)
            # print_dataframe(df_cagr_company)
            company_cagr.append(df_cagr_company['CAGR (after COVID)'].tolist())
            padding = [0] * (total_rows - df_cagr_company.shape[0])
            df_cagr[comp['symbol']] = (padding + df_cagr_company['CAGR (after COVID)'].to_list())
            df_cagr[comp['symbol'] + 'b'] = (padding + df_cagr_company['CAGR (before COVID)'].to_list())
            df_cagr[comp['symbol'] + 'p'] = (padding + df_cagr_company['PercentChange'].to_list())

            # print(comp['symbol'])
            print('////////////////////////////////////')
        print_dataframe(df_cagr)
        # print(company_cagr)
    return render_template("comp_cagr.html", list_bundles=list_bundles, companies=companies, df_cagr=df_cagr, selected_index=selected_index)


@app.route("/buy-op/<bundle>")
def buy_op(bundle):
    print('buy op')
    dict_companies = get_buy_opportunities(bundle)
    print(dict_companies)
    list_list_dates = []
    list_dates = []
    for dict_company in dict_companies:
        for date in dict_company['date']:
            list_dates.append(str(date))
        list_list_dates.append(list_dates)

    print(list_list_dates)

    # company data structure
    # name, last quarterly result date, yf daily data from result-date to present-date, get trend df, db ticker data
    return render_template("buy_opportunity.html", dict_companies=dict_companies, count=len(dict_companies), bundle=bundle)


@app.route("/list/<bundle>")
def bundles(bundle):
    try:
        f = open('../data/data_companies_' + bundle + '.json')
        list_dict_data_points = []
        data_companies = json.load(f)
        for index, company in enumerate(data_companies['companies']):
            df_trend, dict_data_points, hist_df = get_trend(company['symbol'], 'NSE', 'weekly',
                                                            int(str(datetime.now()).split(' ')[0].split('-')[2]),
                                                            int(str(datetime.now()).split(' ')[0].split('-')[1]),
                                                            int(str(datetime.now()).split(' ')[0].split('-')[0]) - 1)
            print(index, company)
            list_dict_data_points.append(dict_data_points)
        f.close()
        print(list_dict_data_points)
        return render_template("list_of_companies.html", data_companies=data_companies,
                               list_dict_data_points=list_dict_data_points)
    except FileNotFoundError:
        error = 'Invalid endpoint'
        return render_template("list_of_companies.html", error=error, data_companies=[], list_dict_data_points=[])


@app.route("/chart/<bundle>")
def charts(bundle):
    try:
        f = open('../data/data_companies_' + bundle + '.json')
        list_dict_data_points = []
        data_companies = json.load(f)
        for index, company in enumerate(data_companies['companies']):
            arr_date = str(datetime.now()).split(' ')[0].split('-')
            year = int(arr_date[0])
            month = int(arr_date[1])
            print('month', month)
            day = int(arr_date[2])
            # year = 2020
            # month = 3
            # day = 12
            df = get_data_from_start_date(company['symbol'], 'NSE', 'weekly', day,
                                          (month - 3) if (month - 3) > 0 else (12 + (month - 3)),
                                          year if month - 3 > 0 else year - 1, True, True)

            padding = [0] * (df.shape[0] - len(df['Date'].tolist()))
            print(padding)
            list_date = (padding + df['Date'].tolist())
            print(list_date)
            list_close = (padding + df['Close'].tolist())
            print(list_close)

            rows = df.shape[0]
            print(rows)
            meta_data_points = [1, 2, 3, 4, 8, 12]
            open_data_points = []
            val_data_points = []

            price_close = df['Close'][rows - 1]
            print(price_close)
            for datapoint in meta_data_points:
                if rows - datapoint - 1 > 0:
                    price_open = df['Open'][rows - datapoint - 1]
                else:
                    price_open = df['Open'][0]
                open_data_points.append(price_open)
                val_data_points.append("{:.2f}".format((price_close - price_open) / price_open * 100))
                # print(datapoint, price_open, (price_close - price_open) / price_close * 100, (price_close - price_open) / price_open * 100)

            dict_periodic_data = {
                'meta_data_points': meta_data_points,
                'open_data_points': open_data_points,
                'val_data_points': val_data_points
            }

            list_dict_data_points.append(
                {'Company': company['symbol'], 'Date': list_date, 'Close': list_close, 'meta_data_points': meta_data_points,
                 'open_data_points': open_data_points, 'val_data_points': val_data_points})

        print(list_dict_data_points)
        f.close()
        return render_template("charts.html", list_dict_data_points=list_dict_data_points, count=len(list_dict_data_points), bundle_name=bundle)
    except FileNotFoundError:
        error = 'Invalid endpoint'
        return render_template("list_of_companies.html", error=error, data_companies=[], list_dict_data_points=[])


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
