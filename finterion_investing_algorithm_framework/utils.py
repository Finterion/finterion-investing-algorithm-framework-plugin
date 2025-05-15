from dateutil import parser
from investing_algorithm_framework import Order, Position


def convert_finterion_order_to_order(finterion_order):
    """
    Convert a Finterion order to an Order object from the
    investing_algorithm_framework.

    Args:
        finterion_order (dict): The Finterion order data.

    Returns:
        Order: An Order object populated with the data
        from the Finterion order.
    """
    order = Order(
        external_id=finterion_order.get("id"),
        order_type=finterion_order.get("order_type"),
        order_side=finterion_order.get("order_side"),
        status=finterion_order.get("status"),
        amount=float(finterion_order.get("amount")),
        target_symbol=finterion_order.get("target_symbol"),
        trading_symbol=finterion_order.get("trading_symbol"),
        price=float(finterion_order.get("price")),
        filled=float(finterion_order.get("filled")),
        remaining=float(finterion_order.get("remaining")),
        cost=float(finterion_order.get("cost")),
    )

    if finterion_order.get("created_at") is not None:
        order.created_at = parser.parse(finterion_order.get("created_at"))

    if finterion_order.get("updated_at") is not None:
        order.updated_at = parser.parse(finterion_order.get("updated_at"))

    return order


def convert_finterion_position_to_position(finterion_position) -> Position:
    """
    Convert a Finterion position to a Position object from the
    investing_algorithm_framework.

    Args:
        finterion_position (dict): The Finterion position data.

    Returns:
        Position: An Position object populated with the data
        from the Finterion position.
    """
    return Position(
        symbol=finterion_position.get("symbol"),
        amount=float(finterion_position.get("amount")),
        cost=float(finterion_position.get("cost")),
    )
