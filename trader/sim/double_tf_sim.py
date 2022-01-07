import backtrader as bt
from helper.bt_logging import get_logger
from helper.constants import SIM_CONF_FILE
from helper.Configuration import Configuration
from helper.cerebro_helper import get_cerebro_with_filename
from trader.strategies.DoubleTFStrategy import DoubleTFStrategy

if __name__ == "__main__":
    logger = get_logger(__name__)

    conf = Configuration.get_conf(SIM_CONF_FILE)

    cerebro = get_cerebro_with_filename(
        [
            f"~/data/ingestion/binance/ETHUSDT/1h/20220107.csv",
            f"~/data/ingestion/binance/ETHUSDT/4h/20220107.csv"
        ],
        DoubleTFStrategy,
        cash=conf['simulation']["cash"],
        commission=conf['simulation']["commission"],
        stake=conf['simulation']["stake"],
    )

    # cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trades")
    # cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")
    # cerebro.addanalyzer(bt.analyzers.PyFolio, _name="PyFolio")
    # logger.debug(f"Active analyzers are {cerebro.analyzers}")

    logger.debug("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())
    # cerebro.addwriter(bt.WriterFile, csv=False, out="a.csv")
    r = cerebro.run()
    logger.debug("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())


