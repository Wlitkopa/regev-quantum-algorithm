def convert_to_order_list(all_orders) -> str:
    """Human-readable summary of the Shor order-finding results."""
    return "".join(
        f"\norder with {shots} shots: {order}" for order, shots in all_orders
    )
