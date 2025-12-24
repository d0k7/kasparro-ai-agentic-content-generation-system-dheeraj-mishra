from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

from ..core.logging import get_logger

TState = TypeVar("TState")


@dataclass(frozen=True, slots=True)
class Node(Generic[TState]):
    name: str
    depends_on: tuple[str, ...]
    run: Callable[[TState], TState]


class DAGRunner(Generic[TState]):
    """Minimal DAG runner with timing + failure visibility + introspection."""

    def __init__(self, nodes: list[Node[TState]]) -> None:
        self._logger = get_logger("kasparro.dag")
        self._nodes: dict[str, Node[TState]] = {n.name: n for n in nodes}
        if len(self._nodes) != len(nodes):
            raise ValueError("Duplicate node name detected in DAG.")

    def describe(self) -> dict[str, object]:
        order = self._toposort()
        return {
            "nodes": [{"name": n.name, "depends_on": list(n.depends_on)} for n in self._nodes.values()],
            "execution_order": order,
        }

    def run(self, initial_state: TState) -> TState:
        ordered = self._toposort()
        state: TState = initial_state

        self._logger.info("DAG start | nodes=%d | order=%s", len(ordered), ordered)

        for name in ordered:
            node = self._nodes[name]
            start = time.perf_counter()
            self._logger.info("Node start | name=%s | depends_on=%s", node.name, node.depends_on)

            try:
                state = node.run(state)
            except Exception as e:
                duration_ms = (time.perf_counter() - start) * 1000.0
                self._logger.error(
                    "Node failed | name=%s | duration_ms=%.2f | error=%s",
                    node.name,
                    duration_ms,
                    repr(e),
                )
                raise

            duration_ms = (time.perf_counter() - start) * 1000.0
            self._logger.info("Node done | name=%s | duration_ms=%.2f", node.name, duration_ms)

        self._logger.info("DAG complete")
        return state

    def _toposort(self) -> list[str]:
        visited: set[str] = set()
        temp: set[str] = set()
        order: list[str] = []

        def visit(n: str) -> None:
            if n in visited:
                return
            if n in temp:
                raise ValueError(f"DAG has a cycle at: {n}")

            temp.add(n)
            node = self._nodes.get(n)
            if node is None:
                raise KeyError(f"Unknown node dependency: {n}")

            for dep in node.depends_on:
                visit(dep)

            temp.remove(n)
            visited.add(n)
            order.append(n)

        for name in self._nodes:
            visit(name)

        return order
