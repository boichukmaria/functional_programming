from collections.abc import Callable
from time import perf_counter

from algorithms import tribonacci, tribonacci_iter


def measure_time(function: Callable[[int], int], n: int) -> float:
    start = perf_counter()
    function(n)
    end = perf_counter()

    return end - start


def main() -> None:
    values = [20, 30, 35]

    print("ПОРІВНЯННЯ ЧАСУ ОБЧИСЛЕННЯ ЧИСЕЛ ТРІБОНАЧЧІ")
    print("-" * 65)
    print(f"{'n':<10}" f"{'Рекурсивна версія':<25}" f"{'Ітеративна версія':<25}")

    for n in values:
        tribonacci.cache_clear()

        recursive_time = measure_time(tribonacci, n)
        iterative_time = measure_time(tribonacci_iter, n)

        print(f"{n:<10}" f"{recursive_time:<25.8f}" f"{iterative_time:<25.8f}")

    print("\nІнформація про кеш:")
    print(tribonacci.cache_info())


if __name__ == "__main__":
    main()
