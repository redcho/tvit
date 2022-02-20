import backtrader as bt
import pandas as pd

from trader.strategies.DefaultStrategy import DefaultStrategy

from helper.bt_logging import get_logger


class CombinedStrategy(DefaultStrategy):
    params = (
        # Metadata
        ("symbol", ""),
        ("interval", ""),
        ("fromdate", ""),
        ("todate", ""),
        ("trade_from", ""),
        # -----
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
    )

    def __init__(self):
        super().__init__("combined_all")

        self.train_df = pd.DataFrame()
        self.test_df = pd.DataFrame()

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

        # lines : cci
        self.cci = bt.indicators.CommodityChannelIndex()

        # lines : percK, percD
        self.stoch = bt.indicators.Stochastic()

        # lines : rsi
        self.rsi = bt.indicators.RSI_EMA()

        self.bb = bt.indicators.BollingerBands()

        # lines : psar
        self.psar = bt.indicators.ParabolicSAR()

        # lines : macd, histo, signal
        self.macd = bt.indicators.MACDHisto()

        # lines : atr
        self.atr = bt.indicators.AverageTrueRange()

        # lines : stddev
        self.std = bt.indicators.StandardDeviation()


    def next(self):
        payload = {
            "datetime": f"{self.datas[0].datetime.date()} {self.datas[0].datetime.time()}",
            "close": self.data.close[0],
            "ema1": self.ema1[0],
            "ema2": self.ema2[0],
            "ema3": self.ema3[0],
            "ema4": self.ema4[0],
            "ema5": self.ema5[0],
            "ema6": self.ema6[0],
            "ema7": self.ema7[0],
            "ema8": self.ema8[0],
            "ema9": self.ema9[0],
            "ema10": self.ema10[0],
            "ema11": self.ema11[0],
            "ema12": self.ema12[0],
            "bbup": self.bb.top[0],
            "bblow": self.bb.bot[0],
            "bbmid": self.bb.mid[0],
            "volume": self.data.volume[0],
            # "1h_earlier": self.data.close[-1]
            "std": self.std[0],
            "atr": self.atr[0],
            "cci": self.cci[0],
            "rsi": self.rsi[0],
            "stochk": self.stoch.percK[0],
            "stochd": self.stoch.percD[0],
            "psar": self.psar[0],
            "macd_macd": self.macd.macd[0],
            "macd_signal": self.macd.signal[0],
            "macd_histo": self.macd.histo[0]
        }

        TEST_YEAR = 2022
        if not self.datas[0].datetime.date().year == TEST_YEAR:
            self.train_df = self.train_df.append(
                payload,
                ignore_index=True,
            )
        else:
            self.test_df = self.test_df.append(
                payload,
                ignore_index=True,
            )

        super().next()

    def stop(self):
        self.log("Export started for training dataset")
        self.train_df.to_csv(
            f"train_{self.p.symbol}_{self.p.interval}_{self.p.fromdate}_{self.p.todate}_{self.strategy_id}.csv",
            index=False,
        )

        self.log("Export started for test dataset")
        self.test_df.to_csv(
            f"test_{self.p.symbol}_{self.p.interval}_{self.p.fromdate}_{self.p.todate}_{self.strategy_id}.csv",
            index=False,
        )

        self.log("Simulation ending..")
