from dataclasses import FrozenInstanceError
import pytest
from core import (
    add_item,
    add_tag,
    change_payment_status,
    get_subtotal,
)
from model import Item, create_order

def test_subtotal():
    order = create_order()
    assert get_subtotal(order) == 120.0

def test_add_item_without_mutation():
    order = create_order()
    new_order = add_item(order, "C3", 15.0, 2)

    assert len(order.items) == 2
    assert len(new_order.items) == 3
    assert new_order is not order
    assert get_subtotal(new_order) == 150.0

def test_add_tag_without_mutation():
    order = create_order()
    new_order = add_tag(order, "vip")

    assert "vip" not in order.tags
    assert "vip" in new_order.tags
    assert new_order is not order

def test_change_payment_status():
    order = create_order()
    new_order = change_payment_status(order, False)

    assert order.paid is True
    assert new_order.paid is False
    assert new_order is not order

def test_order_is_immutable():
    order = create_order()

    with pytest.raises(FrozenInstanceError):
        order.paid = False

def test_mapping_is_read_only():
    order = create_order()

    with pytest.raises(TypeError):
        order.meta["source"] = "changed"

def test_hashability():
    order = create_order()
    new_order = add_tag(order, "vip")

    orders = {order, new_order}

    assert len(orders) == 2
    assert isinstance(hash(order), int)

def test_item_is_immutable():
    item = Item("A1", 50.0, 2)

    with pytest.raises(FrozenInstanceError):
        item.price = 100.0
