import backtrader as bt
import pandas as pd

from trader.strategies.DefaultStrategy import DefaultStrategy

from helper.bt_logging import get_logger


class MomentumStrategy(DefaultStrategy):
    logger = get_logger(__name__)

    params = (
        # Metadata
        ("symbol", ""),
        ("interval", ""),
        ("fromdate", ""),
        ("todate", ""),
    )

    def __init__(self):
        super().__init__("cci_rsi_stoch")

        self.train_df = pd.DataFrame()
        self.test_df = pd.DataFrame()

        # lines : cci
        self.cci = bt.indicators.CommodityChannelIndex()

        # lines : percK, percD
        self.stoch = bt.indicators.Stochastic()

        # lines : rsi
        self.rsi = bt.indicators.RSI_EMA()

    def next(self):
        payload = {
            "datetime": f"{self.datas[0].datetime.date()} {self.datas[0].datetime.time()}",
            "close": self.data.close[0],
            # "1h_earlier": self.data.close[-1]
            "cci": self.cci[0],
            "rsi": self.rsi[0],
            "stochk": self.stoch.percK[0],
            "stochd": self.stoch.percD[0],
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
