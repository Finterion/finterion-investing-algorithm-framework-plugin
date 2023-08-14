from investing_algorithm_framework import PortfolioConfiguration


class FinterionPortfolioConfiguration(PortfolioConfiguration):

    def __init__(self, api_key, trading_symbol):
        super().__init__(
            market="finterion",
            trading_symbol=trading_symbol,
            api_key=api_key,
            secret_key=None,
        )

    @property
    def identifier(self):
        return "finterion"
