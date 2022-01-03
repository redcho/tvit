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

if __name__ == "__main__":
    client = Client(os.environ["API_KEY"], os.environ["SECRET_KEY"])

    tickers = client.get_ticker()

    data_dir = f"data/{PROVIDER}/24hr_chg"

    print(os.makedirs(data_dir, exist_ok=True))
    csv_id = f"{data_dir}/{get_to_day()}.csv"

    pd.DataFrame(tickers).to_csv(csv_id, index=False)
    print(f"Last 24 hr changes have been fetched and saved to {csv_id}")
