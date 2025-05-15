from logging import getLogger

from investing_algorithm_framework import OrderExecutor, OrderType, \
    OrderSide, Order, OperationalException
from finterion import Finterion

from .utils import convert_finterion_order_to_order

logger = getLogger("investing_algorithm_framework")


class FinterionOrderExecutor(OrderExecutor):
    """
    FinterionOrderExecutor is a class that implements the OrderExecutor
    interface for executing and canceling orders using the Finterion API.
    """

    def execute_order(self, portfolio, order, market_credential) -> Order:
        """
        Executes an order for a given portfolio on Finterion.

        Args:
            order: The order to be executed
            portfolio: The portfolio in which the order will be executed
            market_credential: The market credential to use for the order

        Returns:
            Order: Instance of the executed order. The order instance
            should copy the id of the order that has been provided as a
        """
        finterion_client = self.initialize(market_credential)
        target_symbol = order.get_target_symbol()
        amount = order.get_amount()
        price = order.get_price()
        order_type = order.get_order_type()
        order_side = order.get_order_side()

        try:
            if OrderType.LIMIT.equals(order_type):
                if OrderSide.BUY.equals(order_side):
                    external_order = finterion_client.create_limit_order(
                        order_side="buy",
                        amount=str(amount),
                        target_symbol=target_symbol,
                        price=price
                    )
                    external_order = (
                        convert_finterion_order_to_order(external_order)
                    )
                else:
                    external_order = finterion_client.create_limit_order(
                        order_side="sell",
                        amount=str(amount),
                        target_symbol=target_symbol,
                        price=price
                    )
                    external_order = (
                        convert_finterion_order_to_order(external_order)
                    )
            else:
                raise OperationalException(
                    f"Order type {order_type} not supported "
                    f"by CCXT OrderExecutor"
                )

            external_order.id = order.id
            return external_order
        except Exception as e:
            logger.exception(e)
            raise OperationalException("Could not create finterion order")

    def cancel_order(self, portfolio, order, market_credential) -> Order:
        """
        Cancels an order for a given portfolio on a CCXT exchange.

        Args:
            order: The order to be canceled
            portfolio: The portfolio in which the order was executed
            market_credential: The market credential to use for the order

        Returns:
            Order: Instance of the canceled order.
        """
        raise OperationalException("Cancel order not supported")

    @staticmethod
    def initialize(market_credential) -> Finterion:
        """
        Function to initialize the finterion api client.

        Args:
            market_credential (MarketCredential): The market credential to use
                with the finterion api client

        Returns:
            Finterion: Instance of the Finterion API client
        """
        api_key = market_credential.api_key
        return Finterion(api_key)

    def supports_market(self, market):
        """
        Function to check if the market is supported by the portfolio
        provider.

        Args:
            market: Market object

        Returns:
            bool: True if the market is supported, False otherwise
        """
        return market.lower() == "finterion"
