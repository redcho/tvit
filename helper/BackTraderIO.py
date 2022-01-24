import pandas as pd
import pytz
import backtrader as bt


class BackTraderIO:
    def __init__(
        self, symbol, interval, fromdate, todate, tz=pytz.timezone("UTC")
    ):
        self.symbol = symbol
        self.interval = interval
        self.tz = tz

        self.fromdate = fromdate
        self.todate = todate

        self.filenames = [f"data/ingestion/binance/{self.symbol}/{self.interval}/{i}.csv"
                          for i in range(fromdate.year, todate.year + 1)]

        self.bt_df = self._binance_to_bt_df(self._read_df())

    def _read_df(self):
        return pd.concat(map(pd.read_csv, self.filenames))

    def _binance_to_bt_df(self, df):
        df["datetime"] = (
            pd.to_datetime(df["OpenTime"], unit="ms")
            .dt.tz_localize("UTC")
        )

        COLUMNS = [
            "datetime",
            "Open",
            "Close",
            "High",
            "Low",
            "Volume",
            "NumberOfTrades",
        ]

        bt_source = df[COLUMNS].copy()
        bt_source.set_index("datetime", inplace=True)

        return bt_source

    def filter(self):
        start_filt = pd.to_datetime(self.fromdate).tz_localize(self.tz)
        end_filt = pd.to_datetime(self.todate).tz_localize(self.tz)
        return self.bt_df[(self.bt_df.index >= start_filt) & (self.bt_df.index < end_filt)]

    def get_all_data(self):
        return self.bt_df

