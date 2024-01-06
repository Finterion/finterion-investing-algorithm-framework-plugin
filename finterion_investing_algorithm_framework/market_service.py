from datetime import datetime

from dateutil import parser
from finterion import Finterion
from investing_algorithm_framework import Order
from investing_algorithm_framework.infrastructure import CCXTMarketService


class FinterionMarketService(CCXTMarketService):

    def cancel_order(self, order, market):
        pass

    def get_open_orders(
        self, market, target_symbol: str = None, trading_symbol: str = None
    ):
        pass

    def get_closed_orders(
        self, market, target_symbol: str = None, trading_symbol: str = None
    ):
        pass

    def __init__(
        self,
        api_key,
        market_credential_service,
        base_url=None,
        initialize=True
    ):
        super().__init__(market_credential_service)
        self._api_key = api_key
        self._market = "finterion"

        if initialize:
            if base_url is not None:
                self._finterion = Finterion(api_key, base_url=base_url)
            else:
                self._finterion = Finterion(api_key)

    def initialize(self, portfolio_configuration):
        pass

    def get_order(self, order, market):
        order = self._finterion.get_order(order.get_external_id())
        return self._convert_order(order)

    def get_orders(self, symbol, market, since: datetime = None):
        orders = self._finterion.get_orders(target_symbol=symbol)
        return [self._convert_order(order) for order in orders]

    def get_balance(self, market):
        positions = self._finterion.get_positions()
        entries = {"free": {}}

        for position in positions:
            entries[position["symbol"]] = {
                "free": position["amount"],
            }
            entries["free"][position["symbol"]] = float(position["amount"])

        return entries

    def create_market_sell_order(
        self,
        target_symbol: str,
        trading_symbol: str,
        amount: float,
        market
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
        price,
        market
    ):
        order = self._finterion.create_limit_order(
            order_side="sell",
            amount=str(amount),
            target_symbol=target_symbol,
            price=price
        )
        return self._convert_order(order)

    def create_limit_buy_order(
        self,
        target_symbol: str,
        trading_symbol: str,
        amount: float,
        price: float,
        market
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
