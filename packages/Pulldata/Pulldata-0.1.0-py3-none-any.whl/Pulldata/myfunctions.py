import requests
import pandas as pd
import time

from datetime import date, datetime, timedelta


def pull_1m_data(symbol, date):
    polygon_api_key = "beBybSi8daPgsTp5yx5cHtHpYcrjp5Jq"
    polygon_rest_baseurl = "https://api.polygon.io/v2/"

    symbol = "C:" + symbol

    multiplier = 1
    timespan = "minute"

    limit = 40000

    sort = "asc"

    start_time = datetime.combine(date, datetime.min.time())
    end_time = start_time + timedelta(days=1)

    start_time = int(start_time.timestamp() * 1000)
    end_time = int(end_time.timestamp() * 1000) - 1

    request_url = f"{polygon_rest_baseurl}aggs/ticker/{symbol}/range/{multiplier}/" +\
        f"{timespan}/{start_time}/{end_time}?adjusted=true&sort={sort}&" + \
        f"limit={limit}&apiKey={polygon_api_key}"

    data = requests.get(request_url).json()

    if "results" in data:
        return data["results"]
    else:
        raise Exception("Something went wrong")
