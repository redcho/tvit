import backtrader as bt
import json

import numpy as np
import requests

from trader.strategies.DefaultStrategy import DefaultStrategy

from helper.bt_logging import get_logger


class APIStrategy(DefaultStrategy):
    logger = get_logger(__name__)

    params = (
        # Metadata
        ("symbol", ""),
        ("interval", ""),
        ("fromdate", ""),
        ("todate", ""),
        # FAST EMA BAND
        ("ema1", 3),
        ("ema2", 5),
        ("ema3", 8),
        ("ema4", 10),  # ATR Period (standard)
        ("ema5", 12),  # ATR distance for stop price
        ("ema6", 15),
        # SLOW EMA BAND
        ("ema7", 30),
        ("ema8", 35),
        ("ema9", 40),
        ("ema10", 45),
        ("ema11", 50),
        ("ema12", 60),
        ("atrperiod", 14),  # ATR Period (standard)
        ("atrdist", 3.0),  # ATR distance for stop price
    )

    def __init__(self):
        # Main signal
        super().__init__()

        self.strategy_id = "api_bb_ema12"
        self.logger.debug(f"Strategy is being initiated with id {self.strategy_id}")

        self.ema1 = bt.indicators.ExponentialMovingAverage(period=self.p.ema1)
        self.ema2 = bt.indicators.ExponentialMovingAverage(period=self.p.ema2)
        self.ema3 = bt.indicators.ExponentialMovingAverage(period=self.p.ema3)
        self.ema4 = bt.indicators.ExponentialMovingAverage(period=self.p.ema4)
        self.ema5 = bt.indicators.ExponentialMovingAverage(period=self.p.ema5)
        self.ema6 = bt.indicators.ExponentialMovingAverage(period=self.p.ema6)
        self.ema7 = bt.indicators.ExponentialMovingAverage(period=self.p.ema7)
        self.ema8 = bt.indicators.ExponentialMovingAverage(period=self.p.ema8)
        self.ema9 = bt.indicators.ExponentialMovingAverage(period=self.p.ema9)
        self.ema10 = bt.indicators.ExponentialMovingAverage(period=self.p.ema10)
        self.ema11 = bt.indicators.ExponentialMovingAverage(period=self.p.ema11)
        self.ema12 = bt.indicators.ExponentialMovingAverage(period=self.p.ema12)

        self.bb = bt.indicators.BollingerBands()

        self.url = "http://localhost:5000/predict"

    def prenext(self):
        super().next()

    def next(self):
        header = {
            'Content-Type': 'application/json'
        }

        payload = {
                "date": f"{self.data.datetime.date(-1)} {self.data.datetime.time(-1)}",
                "1h_earlier": self.data.close[-2],
                "ema1": self.ema1[-1],
                "ema2": self.ema2[-1],
                "ema3": self.ema3[-1],
                "ema4": self.ema4[-1],
                "ema5": self.ema5[-1],
                "ema6": self.ema6[-1],
                "ema7": self.ema7[-1],
                "ema8": self.ema8[-1],
                "ema9": self.ema9[-1],
                "ema10": self.ema10[-1],
                "ema11": self.ema11[-1],
                "ema12": self.ema12[-1],
                "bbup": self.bb.top[-1],
                "bblow": self.bb.bot[-1],
                "bbmid": self.bb.mid[-1],
            }

        if np.isnan(self.ema12[-1]):
            print("Not ready yet, request contains NaN")
        else:
            response = requests.request("POST", self.url, headers=header, data=json.dumps(payload)).json()

            date_0 = f"{self.data.datetime.date(0)} {self.data.datetime.time(0)}"

            request_str = f"REQUEST ** Candle date: {payload['date']}, Candle close:{self.data.close[-1]} 1h_earlier: {payload['1h_earlier']}"
            expected_str = f"EXPECTED ** Prediction date: {date_0}, price: {self.data.close[0]}"
            result_str = f"RESPONSE ** Prediction date: {response['prediction_date']}, price: {response['prediction']}"

            print(f"{request_str}\n{expected_str}\n{result_str}")

        super().next()

    def stop(self):
        self.log("Simulation ending..")
