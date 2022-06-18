from flask import Flask, render_template
from flask_cors import CORS

from constants import TICKER_KEYS, SCREENER_KEYS
from get.data_from_ticker_bs4 import get_data_from_ticker_using_bs4
from get.data_from_screener_bs4 import get_data_from_screener_using_bs4
app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return render_template("index.html")
    # dictionary_ticker = get_data_from_ticker_using_bs4('JUSTDIAL')
    # dictionary_screener = get_data_from_screener_using_bs4('JUSTDIAL')
    # return str(dictionary_ticker[TICKER_KEYS.ROE]) + ' ' + str(dictionary_screener[SCREENER_KEYS.ROE])

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)