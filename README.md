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
from finterion_investing_algorithm_framework import create_app

app = create_app(api_key="<YOUR_TRADING_BOT_FINTERION_API_KEY>")

# Add your investing algorithm framework market data sources
# ..... 

# Add your investing algorithm framework trading strategies
# ....

if __name__ == "__main__":
    app.run()
```

## Documentation
You can find the official documentation at our [documentation website](https://docs.finterion.com/)