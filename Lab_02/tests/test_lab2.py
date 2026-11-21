from copy import deepcopy
from Lab_02.lab2 import (
    build_pipeline,
    compose,
    normalize_names,
    only_adults,
    reduce_stats,
    with_total,
)


def get_records():
    return [
        {
            "id": 1,
            "name": "anna ivanova",
            "age": 25,
            "city": "Delhi",
            "purchases": [100.0, 50.0],
        },
        {
            "id": 2,
            "name": "petro kovalenko",
            "age": 30,
            "city": "Lviv",
            "purchases": [200.0],
        },
        {
            "id": 3,
            "name": "olena shevchenko",
            "age": 19,
            "city": "Delhi",
            "purchases": [80.0, 20.0],
        },
        {
            "id": 4,
            "name": "maksym bondar",
            "age": 16,
            "city": "Kyiv",
            "purchases": [1000.0],
        },
    ]


def test_only_adults():
    records = get_records()

    result = list(only_adults()(records))

    assert len(result) == 3
    assert all(record["age"] >= 18 for record in result)


def test_with_total():
    records = get_records()

    result = list(with_total()(records))

    assert result[0]["total"] == 150.0
    assert result[1]["total"] == 200.0


def test_normalize_names():
    records = get_records()

    result = list(normalize_names()(records))

    assert result[0]["name"] == "Anna Ivanova"


def test_top_n():
    records = get_records()

    pipeline = build_pipeline(top_n=2)
    result = list(pipeline(records))

    assert len(result) == 2
    assert result[0]["id"] == 2
    assert result[1]["id"] == 1


def test_no_mutation():
    records = get_records()
    original = deepcopy(records)

    pipeline = build_pipeline(top_n=3)
    list(pipeline(records))

    assert records == original


def test_reduce_stats():
    records = get_records()

    pipeline = build_pipeline(top_n=3)
    result = list(pipeline(records))

    stats = reduce_stats(result)

    assert stats["count"] == 3.0
    assert stats["sum_total"] == 475.0
    assert stats["avg_total"] == 475.0 / 3


def test_compose():
    records = get_records()

    pipeline = compose(
        with_total(),
        only_adults(),
    )

    result = list(pipeline(records))

    assert len(result) == 3
    assert all("total" in record for record in result)
