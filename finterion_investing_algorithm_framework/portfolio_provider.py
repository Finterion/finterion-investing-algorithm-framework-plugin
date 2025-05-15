from logging import getLogger
from typing import Union

from investing_algorithm_framework.domain import PortfolioProvider, \
    OperationalException, Order, Position
from finterion import Finterion

from .utils import convert_finterion_order_to_order, \
    convert_finterion_position_to_position

logger = getLogger("investing_algorithm_framework")


class FinterionPortfolioProvider(PortfolioProvider):
    """
    Implementation of Portfolio Provider for Finterion.
    """

    def get_order(
        self, portfolio, order, market_credential
    ) -> Union[Order, None]:
        """
        Method to check if there are any pending orders for the portfolio.
        This method will retrieve the open orders from the exchange and
        check if there are any pending orders for the portfolio.

        !IMPORTANT: This function should return None if the order is
        not found or if the order is not available on the
        exchange or broker. Please do not throw an exception if the
        order is not found.

        Args:
            portfolio: Portfolio object
            order: Order object from the database
            market_credential: Market credential object

        Returns:
            None
        """
        finterion_client = self.initialize(market_credential)

        try:
            external_order = finterion_client.get_order(
                order.get_external_id()
            )
            external_order = (
                convert_finterion_order_to_order(external_order)
            )
            external_order.id = order.id
            return external_order
        except Exception as e:
            logger.exception(e)
            raise OperationalException(
                "Could not retrieve order from Finterion"
            )

    def get_position(
        self, portfolio, symbol, market_credential
    ) -> Union[Position, None]:
        """
        Function to get the position for a given symbol in the portfolio.
        The returned position should be an object that reflects the current
        state of the position on the exchange or broker.

        !IMPORTANT: This function should return None if the position is
        not found or if the position is not available on the
        exchange or broker. Please do not throw an exception if the
        position is not found.

        Args:
            portfolio (Portfolio): Portfolio object
            symbol (str): Symbol object
            market_credential (MarketCredential): MarketCredential object

        Returns:
            Position: Position for the given symbol in the portfolio
        """

        finterion_client = self.initialize(market_credential)
        symbol = symbol

        try:
            external_positions = finterion_client.get_positions(
                symbol=symbol
            )
            external_position = (
                convert_finterion_position_to_position(external_positions[0])
            )
            external_position.portfolio_id = portfolio.id
            return external_position
        except Exception as e:
            logger.exception(e)
            raise OperationalException(
                "Could not retrieve position from Finterion"
            )

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
