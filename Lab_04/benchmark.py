from statistics import median
from timeit import repeat
from algorithms import tribonacci, tribonacci_iter

def measure_memoized(n: int) -> float:
    """Вимірює час мемоізованої рекурсивної версії."""
    def calculate() -> int:
        tribonacci.cache_clear()
        return tribonacci(n)

    measurements = repeat(calculate, repeat=5, number=1000)
    return median(measurements) / 1000

def measure_iterative(n: int) -> float:
    """Вимірює час ітеративної версії."""
    measurements = repeat(
        lambda: tribonacci_iter(n),
        repeat=5,
        number=1000,
    )
    return median(measurements) / 1000

def main() -> None:
    print("=" * 75)
    print("ПОРІВНЯННЯ ЧАСУ ОБЧИСЛЕННЯ ЧИСЕЛ ТРІБОНАЧЧІ")
    print("=" * 75)
    print(
        f"{'n':<10}"
        f"{'Рекурсивна версія (мс)':<30}"
        f"{'Ітеративна версія (мс)':<25}"
    )

    for n in (20, 30, 35):
        recursive_time = measure_memoized(n) * 1000
        iterative_time = measure_iterative(n) * 1000

        tribonacci.cache_clear()
        recursive_result = tribonacci(n)
        iterative_result = tribonacci_iter(n)

        assert recursive_result == iterative_result

        print(
            f"{n:<10}"
            f"{recursive_time:<30.6f}"
            f"{iterative_time:<25.6f}"
        )

    print("\nІнформація про кеш:")
    tribonacci.cache_clear()
    tribonacci(35)
    print(tribonacci.cache_info())

    tribonacci.cache_clear()
    print("Кеш після очищення:")
    print(tribonacci.cache_info())

if __name__ == "__main__":
    main()
