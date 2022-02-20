import backtrader as bt
from trader.strategies.DefaultStrategy import DefaultStrategy
from trader.indicators.TrendWithGuppy import TrendWithGuppy
from trader.indicators.GuppyMMA import GuppyMMA
from backtrader.order import Order

class SuperTrendBand(bt.Indicator):
    """
    Helper inidcator for Supertrend indicator
    """

    params = (("period", 7), ("multiplier", 3))
    lines = ("basic_ub", "basic_lb", "final_ub", "final_lb")

    def __init__(self):
        self.atr = bt.indicators.AverageTrueRange(period=self.p.period)
        self.l.basic_ub = ((self.data.high + self.data.low) / 2) + (
            self.atr * self.p.multiplier
        )
        self.l.basic_lb = ((self.data.high + self.data.low) / 2) - (
            self.atr * self.p.multiplier
        )

    def next(self):
        if len(self) - 1 == self.p.period:
            self.l.final_ub[0] = self.l.basic_ub[0]
            self.l.final_lb[0] = self.l.basic_lb[0]
        else:
            # =IF(OR(basic_ub<final_ub*,close*>final_ub*),basic_ub,final_ub*)
            if (
                self.l.basic_ub[0] < self.l.final_ub[-1]
                or self.data.close[-1] > self.l.final_ub[-1]
            ):
                self.l.final_ub[0] = self.l.basic_ub[0]
            else:
                self.l.final_ub[0] = self.l.final_ub[-1]

            # =IF(OR(baisc_lb > final_lb *, close * < final_lb *), basic_lb *, final_lb *)
            if (
                self.l.basic_lb[0] > self.l.final_lb[-1]
                or self.data.close[-1] < self.l.final_lb[-1]
            ):
                self.l.final_lb[0] = self.l.basic_lb[0]
            else:
                self.l.final_lb[0] = self.l.final_lb[-1]


class SuperTrend(bt.Indicator):
    """
    Super Trend indicator
    """

    params = (("period", 7), ("multiplier", 3))
    lines = ("super_trend",)
    plotinfo = dict(subplot=False)

    def __init__(self):
        self.stb = SuperTrendBand(period=self.p.period, multiplier=self.p.multiplier)

    def next(self):
        if len(self) - 1 == self.p.period:
            self.l.super_trend[0] = self.stb.final_ub[0]
            return

        if self.l.super_trend[-1] == self.stb.final_ub[-1]:
            if self.data.close[0] <= self.stb.final_ub[0]:
                self.l.super_trend[0] = self.stb.final_ub[0]
            else:
                self.l.super_trend[0] = self.stb.final_lb[0]

        if self.l.super_trend[-1] == self.stb.final_lb[-1]:
            if self.data.close[0] >= self.stb.final_lb[0]:
                self.l.super_trend[0] = self.stb.final_lb[0]
            else:
                self.l.super_trend[0] = self.stb.final_ub[0]

class DoubleTFStrategy(DefaultStrategy):
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
        # Bollinger Bands
        ("bb_period", 20),
        ("dev_factor", 2.0),
    )

    def __init__(self):
        super().__init__("double_tf_strategy")

        self.trend_mapping = ["Strong Downtrend", "Weak Downtrend", "Weak Uptrend", "Strong Uptrend"]

        self.trend = TrendWithGuppy(bt_data=self.data1)

        # Lines : mid, top, bot
        self.st_bb = bt.indicators.BollingerBands(
            self.data0, period=self.p.bb_period, devfactor=self.p.dev_factor
        )
        self.bt_bb = bt.indicators.BollingerBands(
            self.data1, period=self.p.bb_period, devfactor=self.p.dev_factor
        )

    def next(self):
        self.log(f"Candle #{len(self)}, Close {self.data0.close[0]}, Direction: {self.trend_mapping[int(self.trend[0])]}")

        perc = 1.0
        perc_amt = (self.data0.close[0] * perc / 100.0)

        if self.trend.st_guppy_crossover[0] == 1.0 and self.trend[0] == 2:
            pstop = self.data0.close[0] - perc_amt
            take_profit = self.data0.close[0] + perc_amt

            self.log(f"Uptrend detected in the small timeframe {self.data0.close[0]}")
            self.order = self.buy(exectype=Order.Market, transmit=False)
            self.sell(price=pstop, exectype=Order.Stop, size=self.order.size, transmit=False, parent=self.order)
            self.sell(price=take_profit, exectype=Order.Limit, size=self.order.size, transmit=True, parent=self.order)
        if self.trend.st_guppy_crossover[0] == -1.0 and self.trend[0] == 0:
            pstop = self.data0.close[0] + perc_amt
            take_profit = self.data0.close[0] - perc_amt

            self.log(f"Downtrend detected in the small timeframe {self.data0.close[0]}")
            self.order = self.sell(exectype=Order.Market, transmit=False)
            self.buy(price=pstop, exectype=Order.Stop, size=self.order.size, transmit=False, parent=self.order)
            self.buy(price=take_profit, exectype=Order.Limit, size=self.order.size, transmit=True, parent=self.order)

    def notify_order(self, order):
        order_type = ""
        if order.exectype == Order.Market:
            order_type = "Market"
        elif order.exectype == Order.Limit:
            order_type = "Limit"
        elif order.exectype == Order.Stop:
            order_type = "Stop"

        if order.status == order.Completed:
            if order.isbuy():
                self.log(f'BUY {order_type} @price: {order.executed.price}')
            elif order.issell():
                self.log(f'SELL {order_type} @price: {order.executed.price}')
        elif order.status == order.Canceled:
            self.log('CANCEL {}@price: {:.2f} {}'.format(
                order_type, order.executed.price, 'buy' if order.isbuy() else 'sell'))
        else:
            pass
