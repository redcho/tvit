from trader.strategies.APIStrategy import APIStrategy

from helper.bt_logging import get_logger
from helper.cerebro_helper import get_cerebro

logger = get_logger(__name__)

if __name__ == "__main__":
    bt_core = get_cerebro(
        "BNBUSDT", "1h", "None", "None", APIStrategy
    )
    bt_core.run()
