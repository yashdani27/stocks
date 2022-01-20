from datetime import datetime

import pandas as pd
from selenium import webdriver
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from constants import SCREENER_KEYS

DATA_KEYS = [
    SCREENER_KEYS.MARKET_CAP,
    SCREENER_KEYS.PRICE,
    SCREENER_KEYS.HIGH,
    SCREENER_KEYS.PE,
    SCREENER_KEYS.BOOK_VALUE,
    SCREENER_KEYS.DIV_YIELD,
    SCREENER_KEYS.ROCE,
    SCREENER_KEYS.ROE,
    SCREENER_KEYS.FACE_VALUE,
    SCREENER_KEYS.INDUSTRY_PE,
    SCREENER_KEYS.EPS,
    SCREENER_KEYS.PB,
    SCREENER_KEYS.INTRINSIC_VALUE,
    SCREENER_KEYS.GRAHAM_NUMBER,
    SCREENER_KEYS.DEBT,
    SCREENER_KEYS.DEBT_EQUITY,
    SCREENER_KEYS.TRADE_RECEIVABLES,
    SCREENER_KEYS.TRADE_PAYABLES,
    SCREENER_KEYS.ADV_CUSTOMERS,
    SCREENER_KEYS.CASH_EQ,
    SCREENER_KEYS.CONTINGENT_LIABILITIES,
    SCREENER_KEYS.INVENTORY,
    SCREENER_KEYS.FCF,
    SCREENER_KEYS.ROIC,
    SCREENER_KEYS.CURRENT_ASSETS,
    SCREENER_KEYS.CURRENT_LIABILITIES,
    SCREENER_KEYS.EPS_PY_QTR
]

# companies = ['GPIL', 'SARDAEN']


def get_data_from_screener_using_selenium(p_companies):

    driver = webdriver.Chrome(executable_path='../drivers/chromedriver')
    driver.get('https://www.screener.in/login/')

    username = driver.find_element_by_name('username')
    username.send_keys("yashdani90@gmail.com")

    password = driver.find_element_by_name('password')
    password.send_keys("ForgotPassword01")

    password.send_keys(Keys.RETURN)

    try:
        for company in p_companies:
            print(company)
            search_dash = WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located((By.ID, "desktop-search"))
            )
            input_dash = search_dash.find_element_by_class_name("u-full-width")
            # print(input_dash.get_attribute('aria-label'))
            input_dash.clear()
            input_dash.send_keys(company)
            input_dash.send_keys(Keys.RETURN)
            # print(input_dash)

            try:
                results = WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_element_located((By.ID, "top-ratios"))
                )

                elements = results.find_elements_by_css_selector("li.flex.flex-space-between")
                # print(elements)

                dictionary = {}

                for index, element in enumerate(elements):
                    values = element.text.split('\n')
                    # print(values)
                    if len(values) > 1:
                        dictionary[DATA_KEYS[index]] = values[1]
                        # print(values[1])
                    else:
                        dictionary[DATA_KEYS[index]] = 0
                    # print(element.find_elements_by_css_selector("span.name").text)

                # print(dictionary)

                time.sleep(2)

                # print('////////////////////////////////////////////////////////////////////////////////////')

                val_price = dictionary[SCREENER_KEYS.PRICE]
                val_iv = dictionary[SCREENER_KEYS.INTRINSIC_VALUE]
                val_gn = dictionary[SCREENER_KEYS.GRAHAM_NUMBER]
                print('val price', val_price, '|')
                print('val iv', val_iv, '|')
                print('val gn', val_gn, '|')
                if len(val_price) > 1 and len(val_iv) > 1 and len(val_gn) > 1:
                    val_price = float(val_price[2:].replace(',', ''))
                    print('val price', val_price)
                    val_iv = val_iv[2:]
                    print(val_iv)
                    val_iv = float(val_iv.replace(',', ''))
                    print(val_iv)
                    # val_iv = float(val_iv[2:].replace(',', ''))
                    val_gn = float(val_gn[2:].replace(',', ''))
                    print(type(val_price), type(val_gn), type(val_iv))
                    print('val_gn', val_gn)
                    if val_iv > val_price or val_gn > val_price:
                        print('inside if')
                        list_companies.append(company)
                        list_price.append(val_price)
                        list_intrinsic_value.append(val_iv)
                        list_graham_number.append(val_gn)

                print('after if')

                time.sleep(2)

                # return dictionary
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
                print('exception')
                driver.quit()
        df = pd.DataFrame(list(zip(list_companies, list_price, list_intrinsic_value, list_graham_number)))
        df.columns = ['Company', 'Price', 'Intrinsic Value', 'Graham Number']
        df.to_csv(r'/Users/dharmendradani/PycharmProjects/' + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + '.csv')
        print(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
    except:
        driver.quit()


# df_companies = pd.read_csv(r'/Users/dharmendradani/PycharmProjects/ScreenerPeers.csv')
# # print(df_companies['Companies'])
# companies = df_companies['Companies']
# print([c for c in companies])
list_companies = []
list_price = []
list_intrinsic_value = []
list_graham_number = []
companies = ['Alpa Labor']
get_data_from_screener_using_selenium(companies)
