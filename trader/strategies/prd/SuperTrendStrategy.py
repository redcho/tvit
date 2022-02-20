from trader.strategies.DefaultStrategy import DefaultStrategy
from trader.indicators.SuperTrend import SuperTrend
from backtrader.order import Order

class SuperTrendStrategy(DefaultStrategy):
    params = (
        # Metadata
        ("symbol", ""),
        ("interval", ""),
        ("fromdate", ""),
        ("todate", ""),
        ("trade_from",""),
        # -----
        ("supertrend_period", 15),
        ("supertrend_multiplier", 2)
    )

    def __init__(self):
        super().__init__("supertrend_prd")

        self.stop_perc = 1.0

        self.supertrend = SuperTrend(self.data0, period=self.p.supertrend_period, multiplier=self.p.supertrend_multiplier)

    def next(self):
        if not self.data0.datetime.date() > self.p.trade_from:
            return

        perc_amt = (self.data0.close[0] * self.stop_perc / 100.0)

        if self.supertrend[0] < self.data0.close[0]:
            pstop = self.supertrend[0] - perc_amt
            take_profit = self.supertrend[0] + perc_amt

            # Change to limit with properly cancelling the old orders
            self.order = self.buy(price=self.supertrend[0], exectype=Order.Limit, transmit=False)
            self.sell(price=pstop, exectype=Order.Stop, size=self.order.size, transmit=False, parent=self.order)
            self.sell(price=take_profit, exectype=Order.Limit, size=self.order.size, transmit=True, parent=self.order)
        else:
            pstop = self.supertrend[0] + perc_amt
            take_profit = self.supertrend[0] - perc_amt

            self.order = self.sell(price=self.supertrend[0], exectype=Order.Limit, transmit=False)
            self.buy(price=pstop, exectype=Order.Stop, size=self.order.size, transmit=False, parent=self.order)
            self.buy(price=take_profit, exectype=Order.Limit, size=self.order.size, transmit=True, parent=self.order)

    # def notify_order(self, order):
    #     order_type = ""
    #     if order.exectype == Order.Market:
    #         order_type = "Market"
    #     elif order.exectype == Order.Limit:
    #         order_type = "Limit"
    #     elif order.exectype == Order.Stop:
    #         order_type = "Stop"
    #
    #     if order.status == order.Completed:
    #         if order.isbuy():
    #             self.log(f'BUY {order_type} @price: {order.executed.price}')
    #         elif order.issell():
    #             self.log(f'SELL {order_type} @price: {order.executed.price}')
    #     elif order.status == order.Canceled:
    #         self.log('CANCEL {}@price: {:.2f} {}'.format(
    #             order_type, order.executed.price, 'buy' if order.isbuy() else 'sell'))
    #     else:
    #         pass