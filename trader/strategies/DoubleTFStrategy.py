import backtrader as bt
from trader.strategies.DefaultStrategy import DefaultStrategy
from backtrader.order import Order


class DoubleTFStrategy(DefaultStrategy):
    params = (
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
        # Bollinger Bands
        ("bb_period", 20),
        ("dev_factor", 2.0),
    )

    def __init__(self):
        super().__init__()

        # self.ema1 = bt.indicators.ExponentialMovingAverage(period=self.p.ema1)
        # self.ema2 = bt.indicators.ExponentialMovingAverage(period=self.p.ema2)
        # self.ema3 = bt.indicators.ExponentialMovingAverage(period=self.p.ema3)
        # self.ema4 = bt.indicators.ExponentialMovingAverage(period=self.p.ema4)
        # self.ema5 = bt.indicators.ExponentialMovingAverage(period=self.p.ema5)
        # self.ema6 = bt.indicators.ExponentialMovingAverage(period=self.p.ema6)
        # self.ema7 = bt.indicators.ExponentialMovingAverage(period=self.p.ema7)
        # self.ema8 = bt.indicators.ExponentialMovingAverage(period=self.p.ema8)
        # self.ema9 = bt.indicators.ExponentialMovingAverage(period=self.p.ema9)
        # self.ema10 = bt.indicators.ExponentialMovingAverage(period=self.p.ema10)
        # self.ema11 = bt.indicators.ExponentialMovingAverage(period=self.p.ema11)
        # self.ema12 = bt.indicators.ExponentialMovingAverage(period=self.p.ema12)

        # Lines : mid, top, bot
        self.st_bb = bt.indicators.BollingerBands(
            self.data0, period=self.p.bb_period, devfactor=self.p.dev_factor
        )
        self.bt_bb = bt.indicators.BollingerBands(
            self.data1, period=self.p.bb_period, devfactor=self.p.dev_factor
        )

    def next(self):
        if self.order:
            print("Passing")
            return

        if not self.position:
            # Logic to buy

            if (
                self.data0.close[0] < self.bt_bb.bot[0]
                and self.data0.close < self.st_bb.bot[0]
            ):
                self.log(
                    f"Close {self.data0.close[0]}, bt_bb.bot {self.bt_bb.bot[0]}, st_bb.bot {self.st_bb.bot[0]}"
                )
                self.order = self.buy(
                    data=None,
                    size=None,
                    price=None,
                    plimit=None,
                    exectype=Order.Market,
                    valid=None,
                )
        else:
            # Logic to sell
            if self.data0.close[0] > self.st_bb.mid[0]:

                self.order = self.sell(
                    data=None,
                    size=None,
                    price=None,
                    plimit=None,
                    exectype=Order.Market,
                    valid=None,
                )
