import pathlib
from finterion_investing_algorithm_framework import create_app
from investing_algorithm_framework import TradingStrategy, Algorithm, TimeUnit, \
    RESOURCE_DIRECTORY, CCXTTickerMarketDataSource

# app = create_app(api_key="YkUGI7KLHn2rZHc4mykkecbkXsO0FUYgEP85UEC3xyp4tpkdjwtaHSV50ZxBN54D")
app = create_app(
    api_key="YkUGI7KLHn2rZHc4mykkecbkXsO0FUYgEP85UEC3xyp4tpkdjwtaHSV50ZxBN54D",
    stateless=False,
    config={RESOURCE_DIRECTORY: pathlib.Path(__file__).parent.resolve()}
)

btc_eur_ticker = CCXTTickerMarketDataSource(
    identifier="SOL-ticker",
    market="BITVAVO",
    symbol="BTC/EUR",
)
ada_eur_ticker = CCXTTickerMarketDataSource(
    identifier="SOL-ticker",
    market="BITVAVO",
    symbol="ADA/EUR",
)
eth_eur_ticker = CCXTTickerMarketDataSource(
    identifier="SOL-ticker",
    market="BITVAVO",
    symbol="ETH/EUR",
)
dot_eur_ticker = CCXTTickerMarketDataSource(
    identifier="SOL-ticker",
    market="BITVAVO",
    symbol="DOT/EUR",
)


class TestTradingStrategy(TradingStrategy):
    time_unit = TimeUnit.SECOND
    interval = 1

    def apply_strategy(self, algorithm: Algorithm, market_data):
        print("Applying strategy")
        print(len(algorithm.get_open_trades()))
        print(len(algorithm.get_closed_trades()))
        print(algorithm.get_total_size())
        print(algorithm.get_allocated())
        print(algorithm.get_unallocated())
        print(algorithm.get_position("BTC"))
        print(algorithm.get_position("ADA"))
        print(algorithm.get_position("ETH"))
        print(algorithm.get_position("DOT"))


app.add_strategy(TestTradingStrategy)
app.add_market_data_source(btc_eur_ticker)
app.add_market_data_source(ada_eur_ticker)
app.add_market_data_source(eth_eur_ticker)
app.add_market_data_source(dot_eur_ticker)

if __name__ == "__main__":
    app.run()
