from copy import deepcopy

from core import make_processor, process_orders_pure


def sample_orders():
    return [
        {
            "id": 1,
            "items": [
                {"price": 80.0, "qty": 2},
                {"price": 50.0, "qty": 1},
            ],
            "paid": True,
        },
        {
            "id": 2,
            "items": [{"price": 30.0, "qty": 1}],
            "paid": True,
        },
        {
            "id": 3,
            "items": [{"price": 200.0, "qty": 1}],
            "paid": False,
        },
    ]


def test_referential_transparency():
    orders = sample_orders()
    args = {
        "min_total": 100,
        "discount": 0.1,
        "tax_rate": 0.2,
    }

    first = process_orders_pure(orders, **args)
    second = process_orders_pure(orders, **args)

    assert first == second


def test_no_mutation():
    orders = sample_orders()
    original = deepcopy(orders)

    process_orders_pure(
        orders,
        min_total=100,
        discount=0.1,
        tax_rate=0.2,
    )

    assert orders == original


def test_callable_policies():
    processor = make_processor(
        accept=lambda subtotal: subtotal >= 50,
        apply_discount=lambda subtotal: subtotal * 0.9,
        apply_tax=lambda subtotal: subtotal * 1.2,
    )

    result = processor(sample_orders())

    assert result["count"] == 1
    assert round(result["revenue"], 2) == 226.8


def test_with_total_does_not_change_order():
    orders = sample_orders()
    original = deepcopy(orders)

    process_orders_pure(
        orders,
        min_total=0,
        discount=0,
        tax_rate=0,
    )

    assert orders == original
