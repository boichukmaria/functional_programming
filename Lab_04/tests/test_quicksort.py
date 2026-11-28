import random

from algorithms import quicksort


def test_quicksort_empty() -> None:
    assert quicksort([]) == []


def test_quicksort_single_element() -> None:
    assert quicksort([5]) == [5]


def test_quicksort_reversed() -> None:
    assert quicksort([3, 2, 1]) == [1, 2, 3]


def test_quicksort_duplicates() -> None:
    assert quicksort([2, 2, 1, 3, 2]) == [1, 2, 2, 2, 3]


def test_quicksort_random() -> None:
    random.seed(42)
    numbers = [random.randint(-1000, 1000) for _ in range(1000)]

    assert quicksort(numbers) == sorted(numbers)


def test_quicksort_does_not_change_input() -> None:
    numbers = [5, 3, 1, 4, 2]
    original = numbers[:]

    quicksort(numbers)

    assert numbers == original
