from investing_algorithm_framework import PortfolioConfiguration
from investing_algorithm_framework.domain import ImproperlyConfigured


class FinterionPortfolioConfiguration(PortfolioConfiguration):

    def __init__(self, api_key, trading_symbol, market_data_markets):
        try:
            super().__init__(
                market="finterion",
                trading_symbol=trading_symbol,
                api_key=api_key,
                secret_key=None,
            )
        except ImproperlyConfigured:
            pass

        if market_data_markets is None:
            raise ImproperlyConfigured(
                "Your algorithm has no markets configured. Please add at "
                "least one market to your algorithm on the finterion platform."
            )

        self._market = market_data_markets[0]

    @property
    def identifier(self):
        return "finterion"


