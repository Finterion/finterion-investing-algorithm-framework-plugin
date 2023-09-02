import logging

from finterion import Finterion
from investing_algorithm_framework import create_app as framework_create_app, \
    Task, TimeUnit, App

from finterion_investing_algorithm_framework.market_service import \
    FinterionMarketService
from finterion_investing_algorithm_framework.models.portfolio_configuration \
    import FinterionPortfolioConfiguration

logger = logging.getLogger("finterion_investing_algorithm_framework_plugin")


def create_app(
    api_key,
    config={},
    stateless=False,
    web=False,
    base_url=None,
) -> App:
    client = Finterion(api_key=api_key, base_url=base_url)
    client.ping()
    model = client.get_algorithm_model()
    portfolio_configuration = FinterionPortfolioConfiguration(
        api_key=api_key,
        trading_symbol=model['profile']['trading_symbol'],
        market_data_markets=model['profile']['markets'],
    )
    app = framework_create_app(config=config, web=web, stateless=stateless)
    app.container.market_service.override(
        FinterionMarketService(api_key=api_key, base_url=base_url)
    )
    app.add_portfolio_configuration(portfolio_configuration)

    class PingTask(Task):
        interval = 30
        time_unit = TimeUnit.MINUTE

        def run(self, algorithm):
            logger.debug("Pinging Finterion platform")
            client.ping()

    app.add_task(PingTask)
    return app
