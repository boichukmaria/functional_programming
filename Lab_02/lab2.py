from collections.abc import Callable, Iterable
from functools import reduce
from itertools import islice
from typing import NotRequired, TypedDict, cast


class Record(TypedDict):
    id: int
    name: str
    age: int
    city: str
    purchases: list[float]
    total: NotRequired[float]


class Accumulator(TypedDict):
    count: int
    sum_total: float


Transform = Callable[[Iterable[Record]], Iterable[Record]]


def compose(*functions: Transform) -> Transform:
    def composed(records: Iterable[Record]) -> Iterable[Record]:
        result = records

        for function in reversed(functions):
            result = function(result)

        return result

    return composed


def pipe(
    value: object,
    *functions: Callable[[object], object],
) -> object:
    result = value

    for function in functions:
        result = function(result)

    return result


def juxt(
    value: object,
    *functions: Callable[[object], object],
) -> tuple[object, ...]:
    return tuple(function(value) for function in functions)


def only_adults(min_age: int = 18) -> Transform:
    return lambda records: filter(
        lambda record: record["age"] >= min_age,
        records,
    )


def with_total() -> Transform:
    return lambda records: map(
        lambda record: cast(
            Record,
            {
                **record,
                "total": float(sum(record["purchases"])),
            },
        ),
        records,
    )


def boost_city(city: str, factor: float) -> Transform:
    def transform(records: Iterable[Record]) -> Iterable[Record]:
        return map(
            lambda record: cast(
                Record,
                {
                    **record,
                    "total": (
                        float(record.get("total", 0.0)) * factor
                        if record["city"] == city
                        else float(record.get("total", 0.0))
                    ),
                },
            ),
            records,
        )

    return transform


def normalize_names() -> Transform:
    return lambda records: map(
        lambda record: cast(
            Record,
            {
                **record,
                "name": record["name"].strip().title(),
            },
        ),
        records,
    )


def sort_by_total_desc() -> Transform:
    return lambda records: sorted(
        records,
        key=lambda record: (
            -float(record.get("total", 0.0)),
            record["id"],
        ),
    )


def take(n: int) -> Transform:
    return lambda records: list(islice(records, n))


def _add_record(
    accumulator: Accumulator,
    record: Record,
) -> Accumulator:
    return {
        "count": accumulator["count"] + 1,
        "sum_total": accumulator["sum_total"] + float(record.get("total", 0.0)),
    }


def reduce_stats(records: Iterable[Record]) -> dict[str, float]:
    initial: Accumulator = {
        "count": 0,
        "sum_total": 0.0,
    }

    accumulator = reduce(_add_record, records, initial)

    count = accumulator["count"]
    sum_total = accumulator["sum_total"]
    avg_total = sum_total / count if count else 0.0

    return {
        "count": float(count),
        "sum_total": sum_total,
        "avg_total": avg_total,
    }


def build_pipeline(
    top_n: int = 2,
    city: str = "Delhi",
    factor: float = 1.1,
) -> Transform:
    return compose(
        take(top_n),
        sort_by_total_desc(),
        boost_city(city, factor),
        with_total(),
        only_adults(18),
        normalize_names(),
    )
