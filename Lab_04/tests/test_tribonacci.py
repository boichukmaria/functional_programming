import pytest

from algorithms import tribonacci, tribonacci_iter


def test_tribonacci_first_values() -> None:
    expected = [0, 1, 1, 2, 4, 7, 13, 24, 44, 81]

    assert [tribonacci(n) for n in range(10)] == expected


def test_tribonacci_iter_matches() -> None:
    for n in range(50):
        assert tribonacci(n) == tribonacci_iter(n)


def test_tribonacci_zero() -> None:
    assert tribonacci(0) == 0


def test_tribonacci_negative() -> None:
    with pytest.raises(ValueError):
        tribonacci(-1)

    with pytest.raises(ValueError):
        tribonacci_iter(-1)


def test_tribonacci_cache() -> None:
    tribonacci.cache_clear()

    tribonacci(10)

    assert tribonacci.cache_info().currsize > 0


def test_tribonacci_cache_clear() -> None:
    tribonacci(10)
    tribonacci.cache_clear()

    assert tribonacci.cache_info().currsize == 0
