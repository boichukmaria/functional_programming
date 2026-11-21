import argparse
import json
from pathlib import Path
from typing import cast
from lab2.lab2 import Record, build_pipeline, reduce_stats


def load_records(path: Path) -> list[Record]:
    data = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(data, list):
        raise ValueError("Файл повинен містити список записів")

    return cast(list[Record], data)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Аналіз покупок клієнтів інтернет-магазину"
    )

    parser.add_argument(
        "--data",
        type=Path,
        default=Path("lab2/sample_data.json"),
    )
    parser.add_argument("--top", type=int, default=3)
    parser.add_argument("--boost-city", type=str, default="Delhi")
    parser.add_argument("--factor", type=float, default=1.1)

    args = parser.parse_args()

    if args.top < 0:
        parser.error("--top не може бути від'ємним")

    records = load_records(args.data)

    pipeline = build_pipeline(
        top_n=args.top,
        city=args.boost_city,
        factor=args.factor,
    )

    result = list(pipeline(records))
    stats = reduce_stats(result)

    print("ТОП КЛІЄНТІВ:")
    print(json.dumps(result, ensure_ascii=False, indent=4))

    print("\nСТАТИСТИКА:")
    print(json.dumps(stats, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    main()
