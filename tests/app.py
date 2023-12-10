import datetime
import logging.config
import os
from random import choice

import dotenv
from finterion_investing_algorithm_framework import create_app
from investing_algorithm_framework import TradingTimeFrame, TradingStrategy, \
    TimeUnit, Algorithm, TradingDataType

config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default'],
            'level': 'WARNING',
            'propagate': False
        },
        'investing_algorithm_framework': {
            'level': 'INFO',  # Set the desired root log level
            'handlers': ['default'],
            'propagate': False
        }
    },
}
logging.config.dictConfig(config)
dotenv.load_dotenv()
api_key = os.environ.get("API_KEY")
app = create_app(api_key=api_key, web=True, base_url="http://localhost:7080/algs")


class Strategy(TradingStrategy):
    trading_data_types = [TradingDataType.OHLCV, TradingDataType.TICKER]
    trading_time_frame = TradingTimeFrame.ONE_MINUTE
    trading_time_frame_start_date = \
        datetime.datetime.utcnow() - datetime.timedelta(days=1)
    interval = 10
    time_unit = TimeUnit.SECOND
    symbols = ["DOT/EUR", "ADA/EUR", "ETH/EUR", "BTC/EUR"]
    market = "BITVAVO"

    def run_strategy(self, market_data, algorithm: Algorithm):
        symbol = choice(self.symbols)
        target_symbol = symbol.split("/")[0]
        algorithm.check_pending_orders()

        if algorithm.has_open_orders(target_symbol=target_symbol):
            print(f"Already has open orders for {target_symbol}")
            return

        if not algorithm.position_exists(symbol=target_symbol, amount_gt=0):
            algorithm.create_limit_order(
                target_symbol=target_symbol,
                percentage_of_portfolio=5,
                side="BUY",
                price=market_data["tickers"][symbol]["ask"],
            )


app.add_strategy(Strategy)


if __name__ == "__main__":
    app.run()
