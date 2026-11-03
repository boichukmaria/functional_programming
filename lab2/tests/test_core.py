from copy import deepcopy

from core import build_pipeline, compose, reduce_stats


def sample_records():
    return [
        {"id": 1, "name": "anna", "age": 20, "city": "Delhi", "purchases": [100, 200]},
        {"id": 2, "name": "ivan", "age": 17, "city": "Lviv", "purchases": [500]},
        {"id": 3, "name": "olena", "age": 25, "city": "Lviv", "purchases": [400, 200]},
    ]


def test_top_n():
    result = build_pipeline(top_n=1)(sample_records())
    assert len(result) == 1
    assert result[0]["id"] == 3


def test_no_mutation():
    records = sample_records()
    original = deepcopy(records)

    build_pipeline()(records)

    assert records == original


def test_reduce_stats():
    records = build_pipeline()(sample_records())
    stats = reduce_stats(records)

    assert stats["count"] == 2
    assert stats["sum_total"] == 930.0
    assert stats["avg_total"] == 465.0


def test_compose():
    function = compose(lambda x: x + 2, lambda x: x * 2)

    assert function(3) == 8
