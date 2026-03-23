import datetime

import requests
import yfinance as yf


def get_actual_currency_rate() -> list[dict]:
    """Получение курсов USD и EUR на текущий день по отношению к рублю"""

    result = []
    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    response = requests.get(url).json()
    resp_list = response["Valute"]

    for currency in resp_list:
        if currency in ["USD", "EUR"]:
            curr_rate = {"currency": currency, "rate": resp_list[currency]["Value"]}
            result.append(curr_rate)

    return result


def get_action_prices(date_time):
    """Получение цен на акциии s&p500"""
    result = []

    date_end = date_time.split(" ")[0]

    year = int(date_end.split("-")[0])
    month = int(date_end.split("-")[1])
    day = int(date_end.split("-")[2])

    date_beg = datetime.datetime(year, month, day) + datetime.timedelta(days=-1)

    user_stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]

    for stock in user_stocks:
        df = yf.download(stock, start=date_beg, end=date_end, progress=False)

        frame_as_dict = df.to_dict(orient="records")[0]

        res_dict = {
            "stock": stock,
            "price": round(frame_as_dict[("Close", stock)], 2),
        }

        result.append(res_dict)

    return result
