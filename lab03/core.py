from model import Item, Order

def add_item(
    order: Order,
    sku: str,
    price: float,
    qty: int,
) -> Order:
    item = Item(sku, price, qty)
    return order.with_item(item)

def add_tag(order: Order, tag: str) -> Order:
    return order.add_tag(tag)

def change_payment_status(order: Order, paid: bool) -> Order:
    return order.change_paid(paid)

def get_subtotal(order: Order) -> float:
    return order.subtotal()
