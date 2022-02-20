import backtrader as bt
from helper.bt_logging import get_logger
from helper.constants import SIM_CONF_FILE
from helper.Configuration import Configuration
from helper.cerebro_helper import get_cerebro_with_filename
from trader.strategies.DoubleTFStrategy import DoubleTFStrategy

import quantstats

def printSQN(analyzer):
    sqn = round(analyzer.sqn, 2)
    print("SQN: {}".format(sqn))


def printTradeAnalysis(analyzer):
    """
    Function to print the Technical Analysis results in a nice format.
    """
    # Get the results we are interested in
    total_open = analyzer.total.open
    total_closed = analyzer.total.closed
    total_won = analyzer.won.total
    total_lost = analyzer.lost.total
    win_streak = analyzer.streak.won.longest
    lose_streak = analyzer.streak.lost.longest
    pnl_net = round(analyzer.pnl.net.total, 2)
    strike_rate = (total_won / total_closed) * 100
    # Designate the rows
    h1 = ["Total Open", "Total Closed", "Total Won", "Total Lost"]
    h2 = ["Strike Rate", "Win Streak", "Losing Streak", "PnL Net"]
    r1 = [total_open, total_closed, total_won, total_lost]
    r2 = [strike_rate, win_streak, lose_streak, pnl_net]
    # Check which set of headers is the longest.
    if len(h1) > len(h2):
        header_length = len(h1)
    else:
        header_length = len(h2)
    # Print the rows
    print_list = [h1, r1, h2, r2]
    row_format = "{:<18}" * (header_length + 1)
    print("Trade Analysis Results:")
    for row in print_list:
        print(row_format.format("", *row))


def printCerebroResult(results, symbol):
    printTradeAnalysis(results[0].analyzers.getbyname("trades").get_analysis())
    printSQN(results[0].analyzers.getbyname("sqn").get_analysis())

    portfolio_stats = results[0].analyzers.getbyname("PyFolio")
    returns, positions, transactions, gross_lev = portfolio_stats.get_pf_items()
    returns.index = returns.index.tz_convert(None)
    quantstats.reports.html(
        returns, output=f"stats-{symbol}.html", title=f"{symbol} Trading Return Report"
    )

if __name__ == "__main__":
    logger = get_logger(__name__)

    conf = Configuration.get_conf(SIM_CONF_FILE)

    # Doesn't exist anymore, adjust to use get_cerebro only
    # Adjust so the timeframes are loaded from config file
    cerebro = get_cerebro_with_filename(
        [
            f"~/data/ingestion/binance/ETHUSDT/1h/20220107.csv",
            f"~/data/ingestion/binance/ETHUSDT/4h/20220107.csv",
        ],
        DoubleTFStrategy,
        cash=conf["simulation"]["cash"],
        commission=conf["simulation"]["commission"],
        stake=conf["simulation"]["stake"],
    )

    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trades")
    cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name="PyFolio")
    # logger.debug(f"Active analyzers are {cerebro.analyzers}")

    logger.debug("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())
    # cerebro.addwriter(bt.WriterFile, csv=False, out="a.csv")
    r = cerebro.run()
    logger.debug("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())

    printCerebroResult(r, "ETHUSDT")
