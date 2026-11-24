from core import Order, ProcessResult, process_orders_pure


def render_report(result: ProcessResult) -> None:
    print("Кількість замовлень:", result["count"])

    for order in result["orders"]:
        print("Замовлення:", order["id"], "| Сума:", round(order["total"], 2))

    print("Загальна виручка:", round(result["revenue"], 2))


def run(orders: list[Order]) -> None:
    result = process_orders_pure(
        orders,
        min_total=100,
        discount=0.1,
        tax_rate=0.2,
    )
    render_report(result)


if __name__ == "__main__":
    sample_orders: list[Order] = [
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
            "items": [
                {"price": 30.0, "qty": 1},
            ],
            "paid": True,
        },
        {
            "id": 3,
            "items": [
                {"price": 200.0, "qty": 1},
            ],
            "paid": False,
        },
    ]

    run(sample_orders)
