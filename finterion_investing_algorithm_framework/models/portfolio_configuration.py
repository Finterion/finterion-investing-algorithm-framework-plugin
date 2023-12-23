from investing_algorithm_framework import PortfolioConfiguration
from investing_algorithm_framework.domain import ImproperlyConfigured


class FinterionPortfolioConfiguration(PortfolioConfiguration):

    def __init__(self, trading_symbol, market_data_markets):
        try:
            super().__init__(
                market="finterion",
                trading_symbol=trading_symbol,
            )
        except ImproperlyConfigured:
            pass

        if market_data_markets is None:
            raise ImproperlyConfigured(
                "Your algorithm has no markets configured. Please add at "
                "least one market to your algorithm on the finterion platform."
            )

    @property
    def identifier(self):
        return "finterion"
