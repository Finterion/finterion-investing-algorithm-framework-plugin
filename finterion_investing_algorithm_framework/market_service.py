from datetime import datetime
import ccxt
from dateutil import parser
from decimal import Decimal

from investing_algorithm_framework.infrastructure.services import MarketService
from investing_algorithm_framework import Order
from investing_algorithm_framework.domain import OperationalException, \
    parse_decimal_to_string
from finterion import Finterion


class FinterionMarketService(MarketService):

    def __init__(self, api_key, base_url=None, initialize=True):
        self._api_key = api_key
        self._market = "finterion"

        if initialize:
            if base_url is not None:
                self._finterion = Finterion(api_key, base_url=base_url)
            else:
                self._finterion = Finterion(api_key)

    @property
    def market(self):
        return self._market

    @market.setter
    def market(self, value):

        if not isinstance(value, str):
            raise OperationalException("Market must be a string")

        if value == "finterion":
            return

        self._market = value.lower()

        if not hasattr(ccxt, self._market):
            raise OperationalException(
                f"No market service found for market id {self._market}"
            )

        self.exchange_class = getattr(ccxt, self._market)
        self.exchange = self.exchange_class()

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
            side=finterion_order.get("order_side"),
            status=finterion_order.get("status"),
            amount=finterion_order.get("amount"),
            target_symbol=finterion_order.get("target_symbol"),
            trading_symbol=finterion_order.get("trading_symbol"),
            price=finterion_order.get("price"),
            trade_closed_price=finterion_order.get("trade_closed_price"),
            filled_amount=finterion_order.get("filled"),
            remaining_amount=finterion_order.get("remaining"),
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


