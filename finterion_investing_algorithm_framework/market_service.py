from datetime import datetime

from investing_algorithm_framework.infrastructure.services import MarketService
from investing_algorithm_framework import Order
from finterion import Finterion


class FinterionMarketService(MarketService):

    def __init__(self, api_key, base_url=None):
        self._api_key = api_key

        if base_url is not None:
            self._finterion = Finterion(api_key, base_url=base_url)
        else:
            self._finterion = Finterion(api_key)

    def initialize(self, portfolio_configuration):
        pass

    def get_order(self, order):
        order = self._finterion.get_order(order.external_id)
        return self._conver_order(order)

    def get_orders(self, symbol, since: datetime = None):
        orders = self._finterion.get_orders(symbol=symbol)
        return [self._conver_order(order) for order in orders]

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
        order = self._finterion.create_market_order(
            order_side="sell",
            amount=amount,
            target_symbol=target_symbol,
        )
        return self._conver_order(order)

    def create_limit_sell_order(
        self,
        target_symbol: str,
        trading_symbol: str,
        amount: float,
        price: float
    ):
        order = self._finterion.create_limit_order(
            order_side="sell",
            amount=amount,
            target_symbol=target_symbol,
            price=price
        )
        return self._conver_order(order)

    def create_limit_buy_order(
        self,
        target_symbol: str,
        trading_symbol: str,
        amount: float,
        price: float
    ):
        order = self._finterion.create_limit_order(
            order_side="buy",
            amount=amount,
            target_symbol=target_symbol,
            price=price
        )
        return self._conver_order(order)

    def _conver_order(self, finterion_order):
        return Order(
            external_id=finterion_order.get("id"),
            type=finterion_order.get("order_type"),
            side=finterion_order.get("order_side"),
            status=finterion_order.get("status"),
            amount=finterion_order.get("amount"),
            target_symbol=finterion_order.get("target_symbol"),
            trading_symbol=finterion_order.get("trading_symbol"),
            price=finterion_order.get("price"),
            created_at=finterion_order.get("created_at"),
            updated_at=finterion_order.get("updated_at"),
            trade_closed_at=finterion_order.get("trade_closed_at"),
            trade_closed_price=finterion_order.get("trade_closed_price"),
            filled_amount=finterion_order.get("filled_amount"),
            remaining_amount=finterion_order.get("remaining_amount"),
            cost=finterion_order.get("cost"),
            fee=finterion_order.get("fee"),
        )
