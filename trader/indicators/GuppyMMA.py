import backtrader as bt

class GuppyMMA(bt.Indicator):
    """
    Guppy MMA Indicator
    """
    params = (
        ("ema1", 3),
        ("ema2", 5),
        ("ema3", 8),
        ("ema4", 10),
        ("ema5", 12),
        ("ema6", 15),
        # SLOW EMA BAND
        ("ema7", 30),
        ("ema8", 35),
        ("ema9", 40),
        ("ema10", 45),
        ("ema11", 50),
        ("ema12", 60),
    )

    lines = ("ema1", "ema2", "ema3", "ema4", "ema5", "ema6", "ema7", "ema8", "ema9", "ema10", "ema11", "ema12", "slowAvg", "fastAvg")
    plotinfo = dict(subplot=False)

    def __init__(self):
        self.l.ema1 = bt.indicators.ExponentialMovingAverage(period=self.p.ema1)
        self.l.ema2 = bt.indicators.ExponentialMovingAverage(period=self.p.ema2)
        self.l.ema3 = bt.indicators.ExponentialMovingAverage(period=self.p.ema3)
        self.l.ema4 = bt.indicators.ExponentialMovingAverage(period=self.p.ema4)
        self.l.ema5 = bt.indicators.ExponentialMovingAverage(period=self.p.ema5)
        self.l.ema6 = bt.indicators.ExponentialMovingAverage(period=self.p.ema6)
        self.l.ema7 = bt.indicators.ExponentialMovingAverage(period=self.p.ema7)
        self.l.ema8 = bt.indicators.ExponentialMovingAverage(period=self.p.ema8)
        self.l.ema9 = bt.indicators.ExponentialMovingAverage(period=self.p.ema9)
        self.l.ema10 = bt.indicators.ExponentialMovingAverage(period=self.p.ema10)
        self.l.ema11 = bt.indicators.ExponentialMovingAverage(period=self.p.ema11)
        self.l.ema12 = bt.indicators.ExponentialMovingAverage(period=self.p.ema12)

        self.l.fastAvg = (self.l.ema1 + self.l.ema2 + self.l.ema3 + self.l.ema4 + self.l.ema5 + self.l.ema6) / 6
        self.l.slowAvg = (self.l.ema7 + self.l.ema8 + self.l.ema9 + self.l.ema10 + self.l.ema11 + self.l.ema12) / 6