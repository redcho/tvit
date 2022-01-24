from trader.strategies.to_train.CombinedStrategy import CombinedStrategy

from helper.bt_logging import get_logger
from helper.cerebro_helper import get_cerebro
from datetime import datetime

logger = get_logger(__name__)

if __name__ == "__main__":

    bt_core = get_cerebro(
        "BNBUSDT",
        "1d",
        datetime(2020, 1, 1),
        datetime(2022, 1, 23),
        CombinedStrategy
    )
    logger.debug("Running the cerebro")
    bt_core.run()
