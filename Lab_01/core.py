from collections.abc import Callable
from typing import TypedDict


class Item(TypedDict):
    price: float
    qty: int


class Order(TypedDict, total=False):
    id: int
    items: list[Item]
    paid: bool
    total: float


class ProcessResult(TypedDict):
    count: int
    revenue: float
    orders: list[Order]


def order_subtotal(order: Order) -> float:
    return sum(item["price"] * item["qty"] for item in order["items"])


def with_total(order: Order, total: float) -> Order:
    return {**order, "total": total}


def is_paid(order: Order) -> bool:
    return order["paid"]


def meets_minimum(subtotal: float, minimum: float) -> bool:
    return subtotal >= minimum


def calculate_total(
    subtotal: float,
    apply_discount: Callable[[float], float],
    apply_tax: Callable[[float], float],
) -> float:
    return apply_tax(apply_discount(subtotal))


def make_processor(
    *,
    accept: Callable[[float], bool],
    apply_discount: Callable[[float], float],
    apply_tax: Callable[[float], float],
) -> Callable[[list[Order]], ProcessResult]:

    def process(orders: list[Order]) -> ProcessResult:
        qualified = []
        revenue = 0.0

        for order in orders:
            if not is_paid(order):
                continue

            subtotal = order_subtotal(order)

            if not accept(subtotal):
                continue

            total = calculate_total(subtotal, apply_discount, apply_tax)
            qualified.append(with_total(order, total))
            revenue += total

        return {
            "count": len(qualified),
            "revenue": revenue,
            "orders": qualified,
        }

    return process


def process_orders_pure(
    orders: list[Order],
    *,
    min_total: float,
    discount: float,
    tax_rate: float,
) -> ProcessResult:
    processor = make_processor(
        accept=lambda subtotal: meets_minimum(subtotal, min_total),
        apply_discount=lambda subtotal: subtotal * (1 - discount),
        apply_tax=lambda subtotal: subtotal * (1 + tax_rate),
    )
    return processor(orders)
