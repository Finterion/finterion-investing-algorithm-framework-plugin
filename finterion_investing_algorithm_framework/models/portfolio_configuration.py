from investing_algorithm_framework import PortfolioConfiguration


class LogicfundsPortfolioConfiguration:

    def __init__(self, api_key, trading_symbol):
        self._api_key = api_key
        self._trading_symbol = trading_symbol

    @property
    def api_key(self):
        return self._api_key

    @property
    def identifier(self):
        return "finterion"

    @property
    def trading_symbol(self):
        return self._trading_symbol

    @property
    def market(self):
        return "finterion"
