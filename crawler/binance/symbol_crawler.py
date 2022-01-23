"""
Fetches the last 24hr changes statistics from Binance
Required parameters are via Environment variable
    API_KEY,
    SECRET_KEY
"""

from binance.client import Client

from helper.gdrive_helper import *
import pandas as pd
import os

PROVIDER = "binance"

PARAM__SYMBOL_ARR = [
    # "ETHUSDT",
    "BNBUSDT",
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
    # "EGLDUSDT",
    # # Speculatives
    # "XRPUSDT",
    # "DOGEUSDT",
    # "SHIBUSDT",
    # # People are in loss
    # "BTTUSDT",
    # "ONTUSDT",
    # "CHZUSDT",
    # "HOTUSDT",
]

PARAM__INTERVAL = "1h"
PARAM__FROM = "1 Jan, 2022"
PARAM__TO = "now"

PARAM__UPLOAD_GDRIVE = True

def log(msg, symbol=None):
    print(
        f"{msg} - SYMBOL: {symbol}, INTERVAL: {PARAM__INTERVAL}, FROM: {PARAM__FROM}, TO: {PARAM__TO}"
    )


if __name__ == "__main__":
    KLINE_COLUMNS = [
        "OpenTime",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "CloseTime",
        "QuoteAssetVolume",
        "NumberOfTrades",
        "TakerBuyAssetVolume",
        "TakerBuyQuoteAssetVolume",
        "Ignore",
    ]

    client = Client(os.environ["API_KEY"], os.environ["SECRET_KEY"])

    for symbol in PARAM__SYMBOL_ARR:
        data_dir = f"data/ingestion/{PROVIDER}/{symbol}/{PARAM__INTERVAL}"
        os.makedirs(data_dir, exist_ok=True)

        log("Fetch started", symbol)
        klines = client.get_historical_klines(
            symbol, PARAM__INTERVAL, PARAM__FROM, PARAM__TO
        )
        log("Fetch finished", symbol)

        log("Export started", symbol)
        export_df = pd.DataFrame(klines, columns=KLINE_COLUMNS)

        ts = pd.to_datetime(export_df['OpenTime'], unit="ms").dt.strftime('%Y')
        for i, x in export_df.groupby(ts):
            csv_id = f"{data_dir}/{i}.csv"
            x.to_csv(csv_id, index=False)

            log(f"Export finished to {csv_id}", symbol)

            if PARAM__UPLOAD_GDRIVE:
                log(f"Uploading to gdrive://{csv_id}", symbol)
                # TODO Check for duplicates and prevent duplicates.
                # Either delete/recreate OR update the existing file
                upload_file(csv_id, csv_id)
