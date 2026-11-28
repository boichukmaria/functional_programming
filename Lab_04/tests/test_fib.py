import pytest

from algorithms import fib, fib_iter


def test_fib_small() -> None:
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    assert [fib(n) for n in range(10)] == expected


def test_fib_iter_matches() -> None:
    for n in range(50):
        assert fib(n) == fib_iter(n)


def test_fib_zero() -> None:
    assert fib(0) == 0


def test_fib_negative() -> None:
    with pytest.raises(ValueError):
        fib(-1)

    with pytest.raises(ValueError):
        fib_iter(-1)


def test_fib_cache() -> None:
    fib.cache_clear()

    fib(10)

    assert fib.cache_info().currsize > 0
