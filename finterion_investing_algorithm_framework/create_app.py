import logging

from finterion import Finterion
from investing_algorithm_framework import create_app as framework_create_app, \
    Task, TimeUnit, App

from finterion_investing_algorithm_framework.market_service import \
    FinterionMarketService
from finterion_investing_algorithm_framework.models.portfolio_configuration \
    import LogicfundsPortfolioConfiguration

logger = logging.getLogger(__name__)


def create_app(
    api_key,
    config={},
    stateless=False,
    web=False,
    initialize=True
) -> App:
    client = Finterion(api_key=api_key)
    client.ping()
    model = client.get_algorithm_model()
    logger.info(
        f"Running algorithm {model['name']} in "
        f"environment {model['environment']}"
    )
    portfolio_configuration = LogicfundsPortfolioConfiguration(
        api_key=api_key, trading_symbol=model['profile']['trading_symbol']
    )

    app = framework_create_app(
        config=config, web=web, stateless=stateless, initialize=initialize
    )
    app.container.market_service.override(
        FinterionMarketService(api_key=api_key)
    )
    app.add_portfolio_configuration(portfolio_configuration)

    if not stateless:
        class PingTask(Task):
            interval = 1
            time_unit = TimeUnit.HOUR

            def run(self, algorithm):
                client.ping()

        app.add_task(PingTask)

    return app
