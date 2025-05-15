from logging import getLogger
from investing_algorithm_framework import AppHook
from finterion import Finterion

logger = getLogger("investing_algorithm_framework")


class FinterionPingAction(AppHook):
    """
    A class that implements the AppHook interface to perform a ping action
    on the Finterion API.
    """
    def on_run(self, context):
        """
        Method to be called when the algorithm is run.
        It pings the Finterion API and prints the response.

        Args:
            context: The context of the framework
        """
        logger.info("Pinging Finterion")
        market_credential = context.get_market_credential("finterion")
        finterion_client = self.initialize(market_credential)
        finterion_client.ping()

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
