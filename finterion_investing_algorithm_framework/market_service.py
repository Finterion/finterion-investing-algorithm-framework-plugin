from datetime import datetime
from decimal import Decimal

from dateutil import parser
from finterion import Finterion
from investing_algorithm_framework import Order
from investing_algorithm_framework.domain import parse_decimal_to_string
from investing_algorithm_framework.infrastructure import CCXTMarketService


class FinterionMarketService(CCXTMarketService):

    def cancel_order(self, order):
        pass

    def get_open_orders(self, target_symbol: str = None,
                        trading_symbol: str = None):
        pass

    def get_closed_orders(self, target_symbol: str = None,
                          trading_symbol: str = None):
        pass

    def __init__(self, api_key, base_url=None, initialize=True):
        self._api_key = api_key
        self._market = "finterion"

        if initialize:
            if base_url is not None:
                self._finterion = Finterion(api_key, base_url=base_url)
            else:
                self._finterion = Finterion(api_key)

    def initialize(self, portfolio_configuration):
        pass

    def get_order(self, order):
        order = self._finterion.get_order(order.external_id)
        return self._convert_order(order)

    def get_orders(self, symbol, since: datetime = None):
        orders = self._finterion.get_orders(target_symbol=symbol)
        return [self._convert_order(order) for order in orders]

    def get_balance(self):
        positions = self._finterion.get_positions()
        entries = {}

        for position in positions:
            entries[position["symbol"]] = {
                "free": Decimal(position["amount"]),
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
            amount=str(amount),
            target_symbol=target_symbol,
        )
        return self._convert_order(order)

    def create_limit_sell_order(
        self,
        target_symbol: str,
        trading_symbol: str,
        amount,
        price
    ):
        order = self._finterion.create_limit_order(
            order_side="sell",
            amount=parse_decimal_to_string(amount),
            target_symbol=target_symbol,
            price=price
        )
        return self._convert_order(order)

    def create_limit_buy_order(
        self,
        target_symbol: str,
        trading_symbol: str,
        amount: float,
        price: float
    ):
        order = self._finterion.create_limit_order(
            order_side="buy",
            amount=str(amount),
            target_symbol=target_symbol,
            price=str(price)
        )
        return self._convert_order(order)

    def _convert_order(self, finterion_order):
        order = Order(
            external_id=finterion_order.get("id"),
            order_type=finterion_order.get("order_type"),
            order_side=finterion_order.get("order_side"),
            status=finterion_order.get("status"),
            amount=finterion_order.get("amount"),
            target_symbol=finterion_order.get("target_symbol"),
            trading_symbol=finterion_order.get("trading_symbol"),
            price=finterion_order.get("price"),
            trade_closed_price=finterion_order.get("trade_closed_price"),
            filled=finterion_order.get("filled"),
            remaining=finterion_order.get("remaining"),
            cost=finterion_order.get("cost"),
        )

        if finterion_order.get("trade_closed_at") is not None:
            order.trade_closed_at = parser.parse(
                finterion_order.get("trade_closed_at")
            )

        if finterion_order.get("created_at") is not None:
            order.created_at = parser.parse(finterion_order.get("created_at"))

        if finterion_order.get("updated_at") is not None:
            order.updated_at = parser.parse(finterion_order.get("updated_at"))

        return order


