from unittest import TestCase
from investing_algorithm_framework import Order
from finterion_investing_algorithm_framework.market_service import FinterionMarketService


class TestOrderModels(TestCase):

    def test_order_model(self):
        response_data = {
            'items': [
                {
                    'id': 9,
                    'target_symbol': 'DOT',
                    'trading_symbol': 'EUR',
                    'price': 4.5767,
                    'amount': 54.62451111062556,
                    'order_type': 'LIMIT',
                    'order_side': 'buy',
                    'status': 'created',
                    'created_at': '2023-08-13T15:27:13.431188Z',
                    'updated_at': '2023-08-13T15:27:13.431205Z',
                    'trade_closed_at': '0001-01-01T00:00:00',
                    'trade_closed_price': 0,
                    'filled': 0,
                    'remaining': 0,
                    'cost': 0
                },
                {
                    'id': 10,
                    'target_symbol': 'ETH',
                    'trading_symbol': 'EUR',
                    'price': 1686.6,
                    'amount': 0.1482272026562315,
                    'order_type': 'LIMIT',
                    'order_side': 'buy',
                    'status': 'created',
                    'created_at': '2023-08-13T15:27:26.715753Z',
                    'updated_at': '2023-08-13T15:27:26.715753Z',
                    'trade_closed_at': '0001-01-01T00:00:00',
                    'trade_closed_price': 0,
                    'filled': 0,
                    'remaining': 0,
                    'cost': 0
                },
                {
                    'id': 8,
                    'target_symbol': 'BTC',
                    'trading_symbol': 'EUR',
                    'price': 27198.9,
                    'amount': 0.0001,
                    'order_type': 'LIMIT',
                    'order_side': 'BUY',
                    'status': 'CLOSED',
                    'created_at': '2023-08-11T14:40:56.626362Z',
                    'updated_at': '2023-08-11T14:41:08.433805Z',
                    'trade_closed_at': '0001-01-01T00:00:00',
                    'trade_closed_price': 0,
                    'filled': 0,
                    'remaining': 0,
                    'cost': 0
                }
            ],
            'total': 3
        }

        for order in response_data['items']:
            order = FinterionMarketService(None, initialize=False)\
                ._convert_order(order)
