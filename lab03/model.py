from collections.abc import Mapping
from dataclasses import dataclass, replace
from types import MappingProxyType


@dataclass(frozen=True, slots=True)
class Item:
    sku: str
    price: float
    qty: int


@dataclass(frozen=True, slots=True)
class Order:
    id: int
    paid: bool
    items: tuple[Item, ...]
    tags: frozenset[str]
    meta: Mapping[str, str]

    def subtotal(self) -> float:
        return sum(item.price * item.qty for item in self.items)

    def add_tag(self, tag: str) -> "Order":
        return replace(self, tags=self.tags | frozenset({tag}))

    def with_item(self, item: Item) -> "Order":
        return replace(self, items=self.items + (item,))

    def change_paid(self, paid: bool) -> "Order":
        return replace(self, paid=paid)

    def __hash__(self) -> int:
        return hash((self.id, self.paid, self.items, self.tags))


def make_meta(**kwargs: str) -> Mapping[str, str]:
    return MappingProxyType(dict(kwargs))


def create_order() -> Order:
    items = (
        Item("A1", 50.0, 2),
        Item("B2", 20.0, 1),
    )

    return Order(
        id=10,
        paid=True,
        items=items,
        tags=frozenset({"delhi", "priority"}),
        meta=make_meta(source="fb_ads", campaign="summer"),
    )
