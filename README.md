# Finterion Investing Algorithm Framework Plugin
This is the official plugin for the [investing algorithm framework](https://investing-algorithm-framework.com) open source project.

## Installation
You can install the plugin with pip.
```shell
pip install finterion-investing-algorithm-framework
```

## Usage 
In order to use the plugin you must register the following components in your investing algorithm framework application:
- **FinterionOrderExecutor**: This component is responsible for executing orders on the finterion platform.
- **FinterionPortfolioProvider**: This component is responsible for connecting the portfolio and syncing positions.
- **FinterionPingHook**: This component is responsible for pinging the finterion platform.

> **Note:** You must provide the API key of your algorithm in order to use 
> the plugin. You can find your API keys in the developer dashboard of
> your algorithm on the finterion platform.

## Example
```python
import logging.config
from dotenv import load_dotenv

from investing_algorithm_framework import create_app, DEFAULT_LOGGING_CONFIG

from finterion_investing_algorithm_framework import \
    FinterionPortfolioProvider, FinterionOrderExecutor, FinterionPingAction


load_dotenv()
logging.config.dictConfig(DEFAULT_LOGGING_CONFIG)

app = create_app()
app.on_strategy_run(FinterionPingAction)
app.add_order_executor(FinterionOrderExecutor)
app.add_portfolio_provider(FinterionPortfolioProvider)
app.add_market(
    market="Finterion",
    api_key="<FINTERION_API_KEY>", # Or set the environment variable FINTERION_API_KEY
    trading_symbol="EUR",
)
```

## Documentation
You can find the official documentation at our [documentation website](https://docs.finterion.com/)