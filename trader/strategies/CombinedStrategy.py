import backtrader as bt
import pprint as pp
from trader.indicators.SuperTrend import SuperTrend

class CombinedStrategy(bt.Strategy):
    params = (
        # Standard MACD Parameters
        ("macd1", 12),
        ("macd2", 26),
        ("macdsig", 9),
        ("atrperiod", 14),  # ATR Period (standard)
        ("atrdist", 3.0),  # ATR distance for stop price
        # ('smaperiod', 15),  # SMA Period (pretty standard)
        # ('dirperiod', 3),  # Lookback period to consider SMA trend direction
        ("atrperiod", 14),  # ATR Period (standard)
        ("atrdist", 3.0),  # ATR distance for stop price
        ("kama", 10),
        ("supertrend", 7),
        ("psar", 2),
    )

    def log(self, txt, doprint=False, params=None):
        """Logging function fot this strategy"""
        if doprint:
            if params is not None:
                pp.pprint(params)
            dt = self.datas[0].datetime.date(0)
            tm = self.datas[0].datetime.time()
            print("%s: %s, %s" % (dt.isoformat(), tm, txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    "BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f"
                    % (order.executed.price, order.executed.value, order.executed.comm)
                )

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log(
                    "SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f"
                    % (order.executed.price, order.executed.value, order.executed.comm)
                )

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log(
            "OPERATION PROFIT, GROSS %.5f, NET %.5f, STOP_LOSS %.5f"
            % (trade.pnl, trade.pnlcomm, self.pstop)
        )

    def __init__(self):
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.pstop = None

        self.dataclose = self.datas[0].close

        # MACD
        self.macd = bt.indicators.MACDHisto(
            self.data,
            period_me1=self.p.macd1,
            period_me2=self.p.macd2,
            period_signal=self.p.macdsig,
        )
        # MACD X SIGNAL CROSSOVER
        self.macd_crossover = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

        # eATR
        self.atr = bt.indicators.ATR(
            self.data,
            period=self.p.atrperiod,
            movav=bt.indicators.ExponentialMovingAverage,
        )

        # SuperTrend
        self.supertrend = SuperTrend(self.data, period=self.p.supertrend)

        # self.kama = bt.indicators.AdaptiveMovingAverage(self.data, period=self.p.kama)
        self.psar = bt.indicators.ParabolicSAR(self.data, period=self.p.psar)

    def next(self):
        if False:  # self.data.datetime < bt.date2num(datetime.datetime(2021, 3, 6)):
            return

        if self.order:
            return

        if not self.position:
            # We might BUY
            if self.supertrend < self.dataclose and self.macd_crossover > 0:
                self.order = self.buy()
                pdist = self.atr[0] * self.p.atrdist
                self.pstop = self.dataclose - pdist
        else:
            if self.macd_crossover[0] < 0:
                self.order = self.sell()
            # STOP LOSS
            elif self.data.close < self.pstop:
                self.order = self.sell()
            else:
                pdist = self.atr * self.p.atrdist
                # Update only if greater than
                self.pstop = max(self.pstop, self.dataclose - pdist)

    def stop(self):
        self.log(
            "Ending Value %.2f" % self.broker.getvalue(),
            doprint=True,
            params=(
                # Standard MACD Parameters
                ("macd1", self.params.macd1),
                ("macd2", self.params.macd2),
                ("macdsig", self.params.macdsig),
                ("atrperiod", self.params.atrperiod),  # ATR Period (standard)
                ("atrdist", self.params.atrdist),  # ATR distance for stop price
                # ('smaperiod', 15),  # SMA Period (pretty standard)
                # ('dirperiod', 3),  # Lookback period to consider SMA trend direction
                ("atrperiod", self.params.atrperiod),  # ATR Period (standard)
                ("atrdist", self.params.atrdist),  # ATR distance for stop price
                ("kama", self.params.kama),
                ("supertrend", self.params.supertrend),
                ("psar", self.p.psar),
            ),
        )
