from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TState = TypeVar("TState")


class Agent(ABC, Generic[TState]):
    """
    Base contract for agents:
    - single responsibility
    - explicit input/output via passed state
    - no hidden global state
    """

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def run(self, state: TState) -> TState:
        """Run the agent and return updated state."""
        raise NotImplementedError
