from datetime import datetime

from investing_algorithm_framework.infrastructure.services import MarketService
from finterion import Finterion


class FinterionMarketService(MarketService):

    def __init__(self, api_key):
        self._api_key = api_key
        self._finterion = Finterion(api_key)

    def initialize(self, portfolio_configuration):
        pass

    def get_order(self, order):
        return self._finterion.get_order(order.external_id)

    def get_orders(self, symbol, since: datetime = None):
        return self._finterion.get_orders(symbol=symbol)

    def get_balance(self):
        positions = self._finterion.get_positions()
        entries = {}

        for position in positions:
            entries[position["symbol"]] = {
                "free": position["amount"],
            }

        return entries

    def create_market_sell_order(
        self,
        target_symbol: str,
        trading_symbol: str,
        amount: float,
    ):
        return self._finterion.create_market_order(
            order_side="sell",
            amount=amount,
            target_symbol=target_symbol,
        )

    def create_limit_sell_order(
        self,
        target_symbol: str,
        trading_symbol: str,
        amount: float,
        price: float
    ):
        return self._finterion.create_limit_order(
            order_side="sell",
            amount=amount,
            target_symbol=target_symbol,
            price=price
        )

    def create_limit_buy_order(
        self,
        target_symbol: str,
        trading_symbol: str,
        amount: float,
        price: float
    ):
        return self._finterion.create_limit_order(
            order_side="buy",
            amount=amount,
            target_symbol=target_symbol,
            price=price
        )
