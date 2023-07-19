# Finterion Investing Algorithm Framework Plugin
This is the official plugin for the [investing algorithm framework](https://investing-algorithm-framework.com) open source project.

## Installation
You can install the plugin with pip.
```shell
pip install finterion-investing-algorithm-framework
```

## Usage 
In order to use the plugin you must use the 'create_app' function provided 
by the plugin. This function will return an instance of the investing 
algorithm framework configured with the finterion platform.

> **Note:** You must provide the API key of your algorithm in order to use 
> the plugin. You can find your API keys in the developer dashboard of
> your algorithm on the finterion platform.

```python
import os
import pathlib
from datetime import datetime, timedelta

from finterion_investing_algorithm_framework import create_app
from investing_algorithm_framework import RESOURCE_DIRECTORY, TimeUnit, \
    TradingTimeFrame, TradingDataType, OrderSide

dir_path = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir))
app = create_app(
    api_key="<your_api_key>", 
    config={RESOURCE_DIRECTORY: pathlib.Path(__file__).parent.resolve()}
)


@app.strategy(
    time_unit=TimeUnit.SECOND, # Algorithm will be executed every 5 seconds
    interval=5,
    market="binance", # Will retrieve trading data from binance
    symbols=["BTC/USDT", "ETH/USDT", ["DOT/USDT"]], # Symbols must be in the format of TARGET/TRADE symbol (e.g. BTC/USDT)
    trading_data_types=[TradingDataType.OHLCV, TradingDataType.TICKER, TradingDataType.ORDER_BOOK],
    trading_time_frame_start_date=datetime.utcnow() - timedelta(days=1), # Will retrieve data from the last 24 hours
    trading_time_frame=TradingTimeFrame.ONE_MINUTE # Will retrieve data on 1m interval (OHLCV)
)
def perform_strategy(algorithm, market_data):
    print(algorithm.get_allocated())
    print(algorithm.get_unallocated())
    print(market_data)
    algorithm.create_limit_order(
        target_symbol="BTC", 
        side=OrderSide.BUY,
        price=market_data["TICKER"]["BTC/USDT"]["BID"], 
        amount_target_symbol=0.00001
    )

    
if __name__ == "__main__":
    app.run()
```

## Documentation
You can find the official documentation at our [documentation website](https://docs.finterion.com/)