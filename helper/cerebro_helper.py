import backtrader as bt
from helper.bt_logging import get_logger
import pytz
from helper.BackTraderIO import BackTraderIO

logger = get_logger(__name__)
tz = pytz.timezone("UTC")

# TODO Deprecate this method and use the generic one for multiple timeframe loading
def get_cerebro_with_filename(
    filenames, strategy, cash=None, commission=None, stake=None
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
        cerebro.addstrategy(strategy)
        logger.debug(f"Strategy added to cerebro")
    except Exception as e:
        logger.error(f"Encountered an error trying to add strategy")
        raise

    try:
        for filename in filenames:
            # TODO This constructor won't work due to deleted overloaded __init__ in BackTraderIO
            bt_data = BackTraderIO([filename]).get_all_data()
            logger.debug(f"Data loaded from {filename}")

            data = bt.feeds.PandasData(dataname=bt_data, tz=tz)

            # TODO Add name parameter in case different symbols are present
            cerebro.adddata(data)

        cerebro.addtz(tz)
        logger.debug(f"Data feed added to the simulation feed")
    except Exception as e:
        logger.error(f"Encountered an error trying to add data")

    return cerebro


def get_cerebro(
    symbol,
    interval,
    fromdate,
    todate,
    strategy,
    cash=None,
    commission=None,
    stake=None,
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
            strategy, symbol=symbol, interval=interval, fromdate=fromdate, todate=todate
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

        data = bt.feeds.PandasData(dataname=bt_data, tz=tz)
        cerebro.adddata(data)
        cerebro.addtz(tz)
        logger.debug(f"Data feed added to the simulation feed")
    except Exception as e:
        logger.error(f"Encountered an error trying to add data: {e}")
        raise

    return cerebro
