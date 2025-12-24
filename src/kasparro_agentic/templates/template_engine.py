from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

TState = TypeVar("TState")


@dataclass(frozen=True, slots=True)
class TemplateField(Generic[TState]):
    """
    A template field is a structured definition:
    - key: output JSON key
    - resolver: function that extracts/builds the field from state
    """
    key: str
    resolver: Callable[[TState], object]


@dataclass(frozen=True, slots=True)
class Template(Generic[TState]):
    """
    A template is a structured definition of fields + resolvers.
    This intentionally avoids string templates to guarantee clean JSON output.
    """
    name: str
    fields: tuple[TemplateField[TState], ...]

    def render(self, state: TState) -> dict[str, object]:
        out: dict[str, object] = {}
        for field in self.fields:
            out[field.key] = field.resolver(state)
        return out
