from __future__ import annotations

from collections import deque
from collections.abc import Generator
from dataclasses import dataclass
from functools import lru_cache
from random import choice


def quicksort(xs: list[int]) -> list[int]:
    """Sort a list using recursive quicksort."""
    if len(xs) <= 1:
        return xs[:]

    pivot = choice(xs)

    left = [x for x in xs if x < pivot]
    middle = [x for x in xs if x == pivot]
    right = [x for x in xs if x > pivot]

    return quicksort(left) + middle + quicksort(right)


@dataclass(slots=True)
class Node:
    """A node of a binary tree."""

    key: int
    left: Node | None = None
    right: Node | None = None


def preorder(tree: Node | None) -> Generator[int, None, None]:
    """Return values in preorder."""
    if tree is None:
        return

    yield tree.key
    yield from preorder(tree.left)
    yield from preorder(tree.right)


def inorder(tree: Node | None) -> Generator[int, None, None]:
    """Return values in inorder."""
    if tree is None:
        return

    yield from inorder(tree.left)
    yield tree.key
    yield from inorder(tree.right)


def postorder(tree: Node | None) -> Generator[int, None, None]:
    """Return values in postorder."""
    if tree is None:
        return

    yield from postorder(tree.left)
    yield from postorder(tree.right)
    yield tree.key


def bfs_level_order(tree: Node | None) -> list[int]:
    """Traverse a binary tree using breadth-first search."""
    if tree is None:
        return []

    queue = deque([tree])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node.key)

        if node.left is not None:
            queue.append(node.left)

        if node.right is not None:
            queue.append(node.right)

    return result


def dfs_preorder_iter(tree: Node | None) -> list[int]:
    """Traverse a binary tree using iterative depth-first search."""
    if tree is None:
        return []

    stack = [tree]
    result = []

    while stack:
        node = stack.pop()
        result.append(node.key)

        if node.right is not None:
            stack.append(node.right)

        if node.left is not None:
            stack.append(node.left)

    return result


@lru_cache(maxsize=None)
def fib(n: int) -> int:
    """Calculate a Fibonacci number recursively with memoization."""
    if n < 0:
        raise ValueError("n must be non-negative")

    if n < 2:
        return n

    return fib(n - 1) + fib(n - 2)


def fib_iter(n: int) -> int:
    """Calculate a Fibonacci number iteratively."""
    if n < 0:
        raise ValueError("n must be non-negative")

    a, b = 0, 1

    for _ in range(n):
        a, b = b, a + b

    return a


@lru_cache(maxsize=None)
def tribonacci(n: int) -> int:
    """Calculate a Tribonacci number recursively with memoization."""
    if n < 0:
        raise ValueError("n must be non-negative")

    if n == 0:
        return 0

    if n == 1 or n == 2:
        return 1

    return tribonacci(n - 1) + tribonacci(n - 2) + tribonacci(n - 3)


def tribonacci_iter(n: int) -> int:
    """Calculate a Tribonacci number iteratively."""
    if n < 0:
        raise ValueError("n must be non-negative")

    if n == 0:
        return 0

    if n == 1 or n == 2:
        return 1

    a, b, c = 0, 1, 1

    for _ in range(3, n + 1):
        a, b, c = b, c, a + b + c

    return c
