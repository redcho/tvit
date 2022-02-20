import backtrader as bt
from helper.bt_logging import get_logger
import pytz
from helper.BackTraderIO import BackTraderIO

logger = get_logger(__name__)
tz = pytz.timezone("UTC")


def get_cerebro(
    symbol,
    interval,
    fromdate,
    todate,
    strategy,
    cash=None,
    commission=None,
    stake=None,
    higher_intervals=[],
    trade_from=None
):
    cerebro = bt.Cerebro()
    logger.debug("Cerebro created..")

    if cash is not None:
        cerebro.broker.setcash(cash)
        logger.debug(f"Initial cash amount is set to {cash}")

    if commission is not None:
        cerebro.broker.setcommission(commission=commission)
        logger.debug(f"Broker commission is set to {commission}")

    if stake is not None:
        cerebro.addsizer(bt.sizers.SizerFix, stake=stake)
        logger.debug(f"Position size is fixed to {stake}")

    try:
        cerebro.addstrategy(
            strategy, symbol=symbol, interval=interval, fromdate=fromdate, todate=todate, trade_from=trade_from
        )
        logger.debug(f"Strategy added to cerebro")
    except Exception as e:
        logger.error(f"Encountered an error trying to add strategy")
        raise

    try:
        # Load with filename
        # bt_data = BackTraderIO("./20220119.csv").get_all_data()

        bt_data = BackTraderIO(symbol, interval, fromdate, todate).filter()

        logger.debug(
            f"Data loaded from {fromdate} to {todate} for {symbol} per {interval}"
        )

        # TODO Add data id since multiple dataframes can be added
        data = bt.feeds.PandasData(dataname=bt_data, tz=tz)
        cerebro.adddata(data)

        # TODO TEST THIS
        for higher_interval in higher_intervals:
            bt_data = BackTraderIO(symbol, higher_interval, fromdate, todate).filter()
            logger.debug(
                f"Higher interval data loaded from {fromdate} to {todate} for {symbol} per {interval}"
            )
            data = bt.feeds.PandasData(dataname=bt_data, tz=tz)
            cerebro.adddata(data)

        cerebro.addtz(tz)

        logger.debug(f"Data feed added to the simulation feed")
    except Exception as e:
        logger.error(f"Encountered an error trying to add data: {e}")
        raise

    return cerebro
