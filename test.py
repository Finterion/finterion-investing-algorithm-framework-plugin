import datetime
import os
import random
import logging.config
from investing_algorithm_framework.infrastructure.models import SQLOrder
# import dotenv
from finterion_investing_algorithm_framework import create_app
from investing_algorithm_framework import TradingTimeFrame, TradingDataType, \
    TradingStrategy, TimeUnit, OrderStatus
from investing_algorithm_framework.app.algorithm import Algorithm


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
        'root': {  # root logger
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
        "finterion": {
            'level': 'INFO',  # Set the desired root log level
            'handlers': ['default'],
            'propagate': False
        },
        'investing_algorithm_framework': {
            'level': 'DEBUG',  # Set the desired root log level
            'handlers': ['default'],
            'propagate': False
        },
    },
}
logging.config.dictConfig(config)

# dotenv.load_dotenv()
# api_key = os.environ.get("API_KEY")
api_key = "89yQtxiScOQkdt9Ppzm3ZoCgqdl8Ty3cMko0e8MAP0EWJEcbsEzV8vxyr0lw8o2x"
app = create_app(api_key=api_key, web=True, base_url="http://localhost:7080/algs")
logger = logging.getLogger(__name__)


class OpenCloseStrategy(TradingStrategy):
    trading_data_types = [TradingDataType.OHLCV, TradingDataType.TICKER]
    trading_time_frame = TradingTimeFrame.ONE_MINUTE
    trading_time_frame_start_date = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    interval = 30
    time_unit = TimeUnit.SECOND
    market = "bitvavo"
    symbols = ["ADA/EUR"]

    def run_strategy(self, market_data, algorithm: Algorithm):
        algorithm.check_pending_orders()
        symbol = random.choice(self.symbols)
        target_symbol, _ = symbol.split("/")
        logger.info("Currently unallocated: %s", algorithm.get_unallocated())
        logger.info("Currently allocated: %s", algorithm.get_allocated())
        logger.info("Currently unfilled: %s", algorithm.get_unfilled())

        logger.info("Positions overview")
        for position in algorithm.get_positions(amount_gt=0):
            logger.info(position)

        logger.info("Open orders overview")
        for order in algorithm.get_orders(status=OrderStatus.OPEN.value):
            logger.info(order)

        if algorithm.position_exists(target_symbol, amount_gt=0) \
                and not algorithm.has_open_orders(target_symbol):
            logger.info(f"closing position {target_symbol}")
            algorithm.close_position(target_symbol)
        elif not algorithm.position_exists(target_symbol, amount_gt=0) \
                and not algorithm.has_open_orders(target_symbol):
            logger.info(f"opening position {target_symbol}")
            algorithm.create_limit_order(
                target_symbol=target_symbol,
                side="buy",
                price=market_data["tickers"][symbol]['bid'],
                percentage_of_portfolio=25
            )


app.add_strategy(OpenCloseStrategy)


if __name__ == "__main__":
    app.run()
