from investing_algorithm_framework import PortfolioConfiguration
from investing_algorithm_framework.domain import ImproperlyConfigured


class FinterionPortfolioConfiguration(PortfolioConfiguration):

    def __init__(self, api_key, trading_symbol):
        try:
            super().__init__(
                market="finterion",
                trading_symbol=trading_symbol,
                api_key=api_key,
                secret_key=None,
            )
        except ImproperlyConfigured:
            pass

    @property
    def identifier(self):
        return "finterion"
