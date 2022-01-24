import backtrader as bt
import pandas as pd

from trader.strategies.DefaultStrategy import DefaultStrategy

from helper.bt_logging import get_logger


class VolatilityStrategy(DefaultStrategy):
    logger = get_logger(__name__)

    params = (
        # Metadata
        ("symbol", ""),
        ("interval", ""),
        ("fromdate", ""),
        ("todate", ""),
    )

    def __init__(self):
        super().__init__("atr_bb_std")

        self.train_df = pd.DataFrame()
        self.test_df = pd.DataFrame()

        # lines : top, mid, bot
        self.bb = bt.indicators.BollingerBands()

        # lines : atr
        self.atr = bt.indicators.AverageTrueRange()

        # lines : stddev
        self.std = bt.indicators.StandardDeviation()

    def next(self):
        payload = {
            "datetime": f"{self.datas[0].datetime.date()} {self.datas[0].datetime.time()}",
            "close": self.data.close[0],
            # "1h_earlier": self.data.close[-1]
            "std": self.std[0],
            "atr": self.atr[0],
            "bbup": self.bb.top[0],
            "bblow": self.bb.bot[0],
            "bbmid": self.bb.mid[0],
            "volume": self.data.volume[0],
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
