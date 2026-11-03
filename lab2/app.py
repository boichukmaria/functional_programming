from core import Record, build_pipeline, reduce_stats

records: list[Record] = [
    {"id": 1, "name": "anna", "age": 20, "city": "Delhi", "purchases": [100, 200, 150]},
    {"id": 2, "name": "ivan", "age": 17, "city": "Lviv", "purchases": [300, 100]},
    {"id": 3, "name": "olena", "age": 25, "city": "Lviv", "purchases": [400, 200]},
    {"id": 4, "name": "maksym", "age": 30, "city": "Delhi", "purchases": [500, 300]},
]

processor = build_pipeline(top_n=2, city="Delhi", factor=1.1)

result = processor(records)

print("Top clients:")
for record in result:
    print(record)

print("\nStatistics:")
print(reduce_stats(result))
