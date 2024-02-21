from finterion import Finterion
from finterion_investing_algorithm_framework.exceptions import \
    FinterionInvestingAlgorithmFrameworkException


def check_portfolio_active(finterion_client: Finterion):
    portfolio = finterion_client\
        .get_portfolio(query_params={"ShowMetrics": "False"})

    if portfolio['active'] is False:
        raise FinterionInvestingAlgorithmFrameworkException(
            "Cannot run on in-active portfolio, "
            "please activate your portfolio"
        )
