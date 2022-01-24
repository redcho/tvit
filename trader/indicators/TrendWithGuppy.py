import backtrader as bt
from trader.indicators.GuppyMMA import GuppyMMA

class TrendWithGuppy(bt.Indicator):
    """
    Guppy MMA Indicator
    """
    params = (
        ("bt_data", None),
    )
    lines = ("trend","st_guppy_crossover", "bt_guppy_crossover")
    plotinfo = dict(subplot=False)

    def __init__(self):
        self.st_guppy = GuppyMMA(self.data)
        self.bt_guppy = GuppyMMA(self.p.bt_data)

        self.l.st_guppy_crossover = bt.indicators.CrossOver(self.st_guppy.fastAvg, self.st_guppy.slowAvg)
        self.l.bt_guppy_crossover = bt.indicators.CrossOver(self.bt_guppy.fastAvg, self.bt_guppy.slowAvg)

    def next(self):
        if self.bt_guppy.fastAvg > self.bt_guppy.slowAvg:
            self.l.trend[0] = 2 # Weak Uptrend
            if self.st_guppy.fastAvg > self.st_guppy.slowAvg:
                self.l.trend[0] = 3 # Strong Uptrend
        else:
            self.l.trend[0] = 0 # Strong Downtrend
            if self.st_guppy.fastAvg > self.st_guppy.slowAvg :
                self.l.trend[0] = 1 # Weak Downtrend
