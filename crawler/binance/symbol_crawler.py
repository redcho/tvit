"""
Fetches the last 24hr changes statistics from Binance
Required parameters are via Environment variable
    API_KEY,
    SECRET_KEY
"""

from binance.client import Client

from helper.date_helper import get_to_day

import pandas as pd
import os

PROVIDER = "binance"

# TODO Deprecate param based & do conf based
PARAM__SYMBOL_ARR = [
    # "ETHUSDT",
    # "BNBUSDT",
    # "LTCUSDT",
    # "RSRUSDT",
    # "CAKEUSDT",
    # "LINKUSDT",
    # "ADAUSDT",
    # "MANAUSDT",
    # "UNIUSDT",
    # "FILUSDT",
    # "COTIUSDT",
    # "IOTAUSDT",
    # "THETAUSDT",
    # "SOLUSDT",
    # "MATICUSDT",
    # "1INCHUSDT",
    # "AAVEUSDT",
    "EGLDUSDT",
    # Speculatives
    "XRPUSDT",
    "DOGEUSDT",
    "SHIBUSDT",
    # People are in loss
    "BTTUSDT",
    "ONTUSDT",
    "CHZUSDT",
    "HOTUSDT"
]

PARAM__SYMBOL = "ETHUSDT"
PARAM__INTERVAL = "1h"
PARAM__FROM = "1 Jan, 2020"
PARAM__TO = "now"


def log(msg, symbol=None):
    print(f"{msg} - SYMBOL: {PARAM__SYMBOL if symbol is None else symbol}, INTERVAL: {PARAM__INTERVAL}, FROM: {PARAM__FROM}, TO: {PARAM__TO}")


if __name__ == "__main__":
    KLINE_COLUMNS = ["OpenTime", "Open", "High", "Low", "Close", "Volume", "CloseTime", "QuoteAssetVolume",
                     "NumberOfTrades", "TakerBuyAssetVolume", "TakerBuyQuoteAssetVolume", "Ignore"]

    client = Client(os.environ["API_KEY"], os.environ["SECRET_KEY"])

    for symbol in PARAM__SYMBOL_ARR:
        data_dir = f"data/{PROVIDER}/{symbol}/{PARAM__INTERVAL}"

        os.makedirs(data_dir, exist_ok=True)
        # TODO Deterministic daily shards
        csv_id = f"{data_dir}/{get_to_day()}.csv"

        log("Fetch started", symbol)
        klines = client.get_historical_klines(symbol, PARAM__INTERVAL, PARAM__FROM, PARAM__TO)
        log("Fetch finished")

        log("Export started", symbol)
        pd.DataFrame(klines, columns=KLINE_COLUMNS).to_csv(csv_id, index=False)
        log(f"Export finished to {csv_id}", symbol)