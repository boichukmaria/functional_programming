from collections.abc import Callable
from functools import reduce
from typing import TypedDict


class Record(TypedDict, total=False):
    id: int
    name: str
    age: int
    city: str
    purchases: list[float]
    total: float


def compose(*functions):
    def result(data):
        for function in reversed(functions):
            data = function(data)
        return data

    return result


def normalize_names(records: list[Record]) -> list[Record]:
    return [{**r, "name": r["name"].strip().title()} for r in records]


def only_adults(records: list[Record]) -> list[Record]:
    return [r for r in records if r["age"] >= 18]


def with_total(records: list[Record]) -> list[Record]:
    return [{**r, "total": sum(r["purchases"])} for r in records]


def boost_city(records: list[Record], city: str, factor: float) -> list[Record]:
    return [
        {**r, "total": r["total"] * factor if r["city"] == city else r["total"]}
        for r in records
    ]


def sort_records(records: list[Record]) -> list[Record]:
    return sorted(records, key=lambda r: (-r["total"], r["id"]))


def take(records: list[Record], n: int) -> list[Record]:
    return records[:n]


def build_pipeline(
    top_n: int = 2, city: str = "Delhi", factor: float = 1.1
) -> Callable[[list[Record]], list[Record]]:

    def boost(records):
        return boost_city(records, city, factor)

    return compose(
        lambda records: take(records, top_n),
        sort_records,
        boost,
        with_total,
        only_adults,
        normalize_names,
    )


def reduce_stats(records: list[Record]) -> dict[str, float]:
    result = reduce(
        lambda acc, r: {
            "count": acc["count"] + 1,
            "sum_total": acc["sum_total"] + r["total"],
        },
        records,
        {"count": 0.0, "sum_total": 0.0},
    )

    average = result["sum_total"] / result["count"] if result["count"] else 0.0

    return {
        "count": result["count"],
        "sum_total": result["sum_total"],
        "avg_total": average,
    }
